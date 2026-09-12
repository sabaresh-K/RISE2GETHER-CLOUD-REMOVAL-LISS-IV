import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    """
    Residual Block with Reflection Padding and Instance Normalization.
    Ideal for CycleGAN texture and structure preservation.
    """
    def __init__(self, channels):
        super(ResidualBlock, self).__init__()
        self.block = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(channels, channels, kernel_size=3, padding=0, bias=False),
            nn.InstanceNorm2d(channels),
            nn.ReLU(inplace=True),
            nn.ReflectionPad2d(1),
            nn.Conv2d(channels, channels, kernel_size=3, padding=0, bias=False),
            nn.InstanceNorm2d(channels)
        )

    def forward(self, x):
        return x + self.block(x)


class CloudRemovalGenerator(nn.Module):
    """
    Engine 1: Optical U-Net Generator.
    Accepts 3-channel optical image (RGB) for fast single-scene cloud removal.
    """
    def __init__(self, in_channels=3, out_channels=3):
        super(CloudRemovalGenerator, self).__init__()
        
        # Encoder: Using sequential blocks
        self.down1 = nn.Sequential(nn.Conv2d(in_channels, 64, 4, 2, 1, bias=False), nn.BatchNorm2d(64), nn.LeakyReLU(0.2, True))
        self.down2 = nn.Sequential(nn.Conv2d(64, 128, 4, 2, 1, bias=False), nn.BatchNorm2d(128), nn.LeakyReLU(0.2, True))
        self.down3 = nn.Sequential(nn.Conv2d(128, 256, 4, 2, 1, bias=False), nn.BatchNorm2d(256), nn.LeakyReLU(0.2, True))
        self.down4 = nn.Sequential(nn.Conv2d(256, 512, 4, 2, 1, bias=False), nn.BatchNorm2d(512), nn.LeakyReLU(0.2, True))
        
        # Decoder
        self.up1 = nn.Sequential(nn.ConvTranspose2d(512, 256, 4, 2, 1, bias=False), nn.BatchNorm2d(256), nn.ReLU(True))
        self.up2 = nn.Sequential(nn.ConvTranspose2d(512, 128, 4, 2, 1, bias=False), nn.BatchNorm2d(128), nn.ReLU(True))
        self.up3 = nn.Sequential(nn.ConvTranspose2d(256, 64, 4, 2, 1, bias=False), nn.BatchNorm2d(64), nn.ReLU(True))
        
        # Final output layer
        self.final = nn.Sequential(nn.ConvTranspose2d(128, out_channels, 4, 2, 1), nn.Tanh())

    def forward(self, x):
        d1 = self.down1(x)
        d2 = self.down2(d1)
        d3 = self.down3(d2)
        d4 = self.down4(d3)
        u1 = self.up1(d4)
        u2 = self.up2(torch.cat([u1, d3], 1))
        u3 = self.up3(torch.cat([u2, d2], 1))
        return self.final(torch.cat([u3, d1], 1))


class SARCycleGANGenerator(nn.Module):
    """
    Engine 2: High-Fidelity SAR-Guided CycleGAN U-ResNet Generator.
    Fuses paired 5-channel input (3-channel Optical RGB + 2-channel Sentinel-1 SAR)
    with U-Net skip connections and bilinear upsampling to eliminate blurriness & grid artifacts.
    """
    def __init__(self, in_channels=5, out_channels=3, num_residual_blocks=6):
        super(SARCycleGANGenerator, self).__init__()
        self.in_channels = in_channels

        # Encoder Stage 1
        self.down1 = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(in_channels, 64, kernel_size=7, bias=False),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True)
        )
        # Encoder Stage 2
        self.down2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1, bias=False),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True)
        )
        # Encoder Stage 3
        self.down3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1, bias=False),
            nn.InstanceNorm2d(256),
            nn.ReLU(inplace=True)
        )

        # Bottleneck Residual Blocks
        res_blocks = [ResidualBlock(256) for _ in range(num_residual_blocks)]
        self.res_blocks = nn.Sequential(*res_blocks)

        # Upsampling Stage 1 (Bilinear + Skip Connection)
        self.up1 = nn.Sequential(
            nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False),
            nn.ReflectionPad2d(1),
            nn.Conv2d(256, 128, kernel_size=3, stride=1, padding=0, bias=False),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True)
        )
        # Upsampling Stage 2 (Bilinear + Skip Connection)
        self.up2 = nn.Sequential(
            nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False),
            nn.ReflectionPad2d(1),
            nn.Conv2d(256, 64, kernel_size=3, stride=1, padding=0, bias=False),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True)
        )

        # Final Output Layer
        self.final = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(128, out_channels, kernel_size=7),
            nn.Tanh()
        )

    def forward(self, x):
        """
        Input x: Tensor of shape (Batch, 5, Height, Width) or (Batch, 3, Height, Width).
        If 3-channel input is passed, 2 synthetic SAR edge/backscatter channels are automatically concatenated.
        """
        if x.size(1) == 3 and self.in_channels == 5:
            sobel_x = torch.tensor([[-1., 0., 1.], [-2., 0., 2.], [-1., 0., 1.]], device=x.device).view(1, 1, 3, 3)
            sobel_y = torch.tensor([[-1., -2., -1.], [0., 0., 0.], [1., 2., 1.]], device=x.device).view(1, 1, 3, 3)
            
            gray = 0.2989 * x[:, 0:1, :, :] + 0.5870 * x[:, 1:2, :, :] + 0.1140 * x[:, 2:3, :, :]
            grad_x = nn.functional.conv2d(gray, sobel_x, padding=1)
            grad_y = nn.functional.conv2d(gray, sobel_y, padding=1)
            sar_vv = torch.clamp(torch.sqrt(grad_x ** 2 + grad_y ** 2 + 1e-6) / 2.0 - 1.0, -1.0, 1.0)
            sar_vh = torch.clamp(torch.abs(grad_x - grad_y) / 2.0 - 1.0, -1.0, 1.0)
            
            x = torch.cat([x, sar_vv, sar_vh], dim=1)

        d1 = self.down1(x)
        d2 = self.down2(d1)
        d3 = self.down3(d2)
        
        r = self.res_blocks(d3)
        
        u1 = self.up1(r)
        u2 = self.up2(torch.cat([u1, d2], dim=1))
        
        out = self.final(torch.cat([u2, d1], dim=1))
        return out


class SARCycleGANDiscriminator(nn.Module):
    """
    PatchGAN Discriminator for SAR-Guided CycleGAN.
    Evaluates 70x70 local image patches for optical texture authenticity.
    """
    def __init__(self, in_channels=3):
        super(SARCycleGANDiscriminator, self).__init__()

        def discriminator_block(in_filters, out_filters, normalize=True):
            layers = [nn.Conv2d(in_filters, out_filters, kernel_size=4, stride=2, padding=1)]
            if normalize:
                layers.append(nn.InstanceNorm2d(out_filters))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            return layers

        self.model = nn.Sequential(
            *discriminator_block(in_channels, 64, normalize=False),
            *discriminator_block(64, 128),
            *discriminator_block(128, 256),
            *discriminator_block(256, 512),
            nn.ZeroPad2d((1, 0, 1, 0)),
            nn.Conv2d(512, 1, kernel_size=4, padding=1)
        )

    def forward(self, x):
        return self.model(x)
