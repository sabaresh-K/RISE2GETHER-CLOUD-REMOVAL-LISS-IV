import os
import torch
import torch.nn as nn
from src.models import SARCycleGANGenerator, SARCycleGANDiscriminator

class ImageBuffer:
    """
    Image buffer to store previously generated images for discriminator training.
    Reduces model oscillation according to Shrivastava et al. & Zhu et al.
    """
    def __init__(self, buffer_size=50):
        self.buffer_size = buffer_size
        self.num_imgs = 0
        self.images = []

    def push_and_pop(self, images):
        if self.buffer_size == 0:
            return images
        return_images = []
        for image in images:
            image = torch.unsqueeze(image.data, 0)
            if self.num_imgs < self.buffer_size:
                self.num_imgs += 1
                self.images.append(image)
                return_images.append(image)
            else:
                if torch.rand(1).item() > 0.5:
                    idx = torch.randint(0, self.buffer_size, (1,)).item()
                    tmp = self.images[idx].clone()
                    self.images[idx] = image
                    return_images.append(tmp)
                else:
                    return_images.append(image)
        return torch.cat(return_images, 0)


class CycleGANModel(nn.Module):
    """
    Full SAR-Guided CycleGAN System.
    Handles Domain A (Cloudy Optical + Sentinel-1 SAR) <-> Domain B (Cloud-Free Optical).
    
    Includes:
    - Generator A2B: Cloudy+SAR -> Cloud-Free Optical
    - Generator B2A: Cloud-Free Optical -> Synthetic Cloudy+SAR
    - Discriminator A: Discriminates real vs fake Domain A
    - Discriminator B: Discriminates real vs fake Domain B
    - Cycle-Consistency & Identity Losses
    """
    def __init__(self, in_channels_a=5, out_channels_b=3, lr=0.0002, lambda_cyc=10.0, lambda_idt=5.0, device="cuda"):
        super(CycleGANModel, self).__init__()
        
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.lambda_cyc = lambda_cyc
        self.lambda_idt = lambda_idt
        
        # 1. Generators
        self.netG_A2B = SARCycleGANGenerator(in_channels=in_channels_a, out_channels=out_channels_b).to(self.device)
        self.netG_B2A = SARCycleGANGenerator(in_channels=out_channels_b, out_channels=out_channels_b).to(self.device)
        
        # 2. Discriminators
        self.netD_A = SARCycleGANDiscriminator(in_channels=3).to(self.device)
        self.netD_B = SARCycleGANDiscriminator(in_channels=out_channels_b).to(self.device)
        
        # 3. Buffers
        self.fake_A_buffer = ImageBuffer(buffer_size=50)
        self.fake_B_buffer = ImageBuffer(buffer_size=50)
        
        # 4. Loss Criteria
        self.criterionGAN = nn.MSELoss().to(self.device)
        self.criterionCycle = nn.L1Loss().to(self.device)
        self.criterionIdt = nn.L1Loss().to(self.device)
        
        # 5. Optimizers
        self.optimizer_G = torch.optim.Adam(
            list(self.netG_A2B.parameters()) + list(self.netG_B2A.parameters()),
            lr=lr, betas=(0.5, 0.999)
        )
        self.optimizer_D = torch.optim.Adam(
            list(self.netD_A.parameters()) + list(self.netD_B.parameters()),
            lr=lr, betas=(0.5, 0.999)
        )

        # Placeholders
        self.real_A = None
        self.real_B = None
        self.fake_B = None
        self.fake_A = None
        self.rec_A = None
        self.rec_B = None

    def set_input(self, real_A, real_B):
        """
        real_A: Domain A (Cloudy Optical + SAR) tensor (B, 5, H, W) or (B, 3, H, W)
        real_B: Domain B (Cloud-Free Optical) tensor (B, 3, H, W)
        """
        self.real_A = real_A.to(self.device)
        self.real_B = real_B.to(self.device)

    def forward(self):
        """Runs forward passes for both generators."""
        self.fake_B = self.netG_A2B(self.real_A) # Cloudy+SAR -> Cloud-Free Optical
        self.rec_A = self.netG_B2A(self.fake_B)  # Cloud-Free -> Reconstructed Cloudy
        
        self.fake_A = self.netG_B2A(self.real_B) # Cloud-Free -> Synthetic Cloudy
        self.rec_B = self.netG_A2B(self.fake_A)  # Synthetic Cloudy -> Reconstructed Cloud-Free

    def backward_G(self):
        """Calculates combined Generator Loss (Adversarial + Cycle + Identity)."""
        # Identity loss
        idt_A = self.netG_B2A(self.real_A[:, :3, :, :] if self.real_A.size(1) >= 3 else self.real_A)
        loss_idt_A = self.criterionIdt(idt_A[:, :3, :, :], self.real_A[:, :3, :, :]) * self.lambda_idt
        
        idt_B = self.netG_A2B(self.real_B)
        loss_idt_B = self.criterionIdt(idt_B, self.real_B) * self.lambda_idt

        # GAN loss: G_A2B(A) should fool D_B
        pred_fake_B = self.netD_B(self.fake_B)
        target_real_B = torch.ones_like(pred_fake_B, device=self.device)
        loss_GAN_A2B = self.criterionGAN(pred_fake_B, target_real_B)

        # GAN loss: G_B2A(B) should fool D_A
        pred_fake_A = self.netD_A(self.fake_A)
        target_real_A = torch.ones_like(pred_fake_A, device=self.device)
        loss_GAN_B2A = self.criterionGAN(pred_fake_A, target_real_A)

        # Cycle consistency loss
        real_A_opt = self.real_A[:, :3, :, :] if self.real_A.size(1) >= 3 else self.real_A
        rec_A_opt = self.rec_A[:, :3, :, :] if self.rec_A.size(1) >= 3 else self.rec_A
        loss_cycle_A = self.criterionCycle(rec_A_opt, real_A_opt) * self.lambda_cyc
        loss_cycle_B = self.criterionCycle(self.rec_B, self.real_B) * self.lambda_cyc

        # Paired L1 Reconstruction Loss (Direct Supervised Ground Truth Alignment)
        loss_L1_A2B = self.criterionCycle(self.fake_B, self.real_B) * 10.0

        # Total Generator Loss
        loss_G = loss_GAN_A2B + loss_GAN_B2A + loss_cycle_A + loss_cycle_B + loss_idt_A + loss_idt_B + loss_L1_A2B
        loss_G.backward()
        
        return {
            "loss_G": loss_G.item(),
            "loss_G_A2B": loss_GAN_A2B.item(),
            "loss_G_B2A": loss_GAN_B2A.item(),
            "loss_cycle": (loss_cycle_A + loss_cycle_B).item(),
            "loss_idt": (loss_idt_A + loss_idt_B).item(),
            "loss_L1": loss_L1_A2B.item()
        }

    def backward_D_A(self):
        """Calculates Discriminator A Loss."""
        real_A_input = self.real_A[:, :3, :, :] if self.real_A.size(1) >= 3 else self.real_A
        fake_A_buffered = self.fake_A_buffer.push_and_pop(self.fake_A[:, :3, :, :] if self.fake_A.size(1) >= 3 else self.fake_A)
        
        pred_real = self.netD_A(real_A_input)
        loss_D_real = self.criterionGAN(pred_real, torch.ones_like(pred_real, device=self.device))
        
        pred_fake = self.netD_A(fake_A_buffered.detach())
        loss_D_fake = self.criterionGAN(pred_fake, torch.zeros_like(pred_fake, device=self.device))
        
        loss_D_A = (loss_D_real + loss_D_fake) * 0.5
        loss_D_A.backward()
        return loss_D_A.item()

    def backward_D_B(self):
        """Calculates Discriminator B Loss."""
        fake_B_buffered = self.fake_B_buffer.push_and_pop(self.fake_B)
        
        pred_real = self.netD_B(self.real_B)
        loss_D_real = self.criterionGAN(pred_real, torch.ones_like(pred_real, device=self.device))
        
        pred_fake = self.netD_B(fake_B_buffered.detach())
        loss_D_fake = self.criterionGAN(pred_fake, torch.zeros_like(pred_fake, device=self.device))
        
        loss_D_B = (loss_D_real + loss_D_fake) * 0.5
        loss_D_B.backward()
        return loss_D_B.item()

    def optimize_parameters(self):
        """Single training optimization step."""
        self.forward()
        
        # 1. Generators
        self.optimizer_G.zero_grad()
        g_losses = self.backward_G()
        self.optimizer_G.step()
        
        # 2. Discriminators
        self.optimizer_D.zero_grad()
        loss_D_A = self.backward_D_A()
        loss_D_B = self.backward_D_B()
        self.optimizer_D.step()
        
        g_losses["loss_D_A"] = loss_D_A
        g_losses["loss_D_B"] = loss_D_B
        return g_losses

    def save_checkpoint(self, save_dir, filename="sar_cyclegan.pth"):
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, filename)
        torch.save({
            "G_A2B": self.netG_A2B.state_dict(),
            "G_B2A": self.netG_B2A.state_dict(),
            "D_A": self.netD_A.state_dict(),
            "D_B": self.netD_B.state_dict()
        }, path)
        return path

    def load_checkpoint(self, checkpoint_path):
        if os.path.exists(checkpoint_path):
            ckpt = torch.load(checkpoint_path, map_location=self.device)
            if "G_A2B" in ckpt:
                self.netG_A2B.load_state_dict(ckpt["G_A2B"])
                if "G_B2A" in ckpt: self.netG_B2A.load_state_dict(ckpt["G_B2A"])
                if "D_A" in ckpt: self.netD_A.load_state_dict(ckpt["D_A"])
                if "D_B" in ckpt: self.netD_B.load_state_dict(ckpt["D_B"])
            else:
                self.netG_A2B.load_state_dict(ckpt)
            return True
        return False
