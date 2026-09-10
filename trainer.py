# training/trainer.py
import os
import torch
import torch.optim as optim
from models import UNetGenerator, NLayerDiscriminator, init_weights
from training import HybridReconstructionLoss


class Pix2PixTrainer:
    """
    Orchestration training engine managing hardware acceleration,
    optimization steps, loss tracking, checkpoint saving and loading.
    """

    def __init__(self, config, device='cuda'):
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.config = config

        # -------------------------
        # Generator
        # -------------------------
        self.netG = UNetGenerator(
            input_nc=config['model']['input_nc'],
            output_nc=config['model']['output_nc'],
            ngf=config['model']['ngf']
        ).to(self.device)

        # -------------------------
        # Discriminator
        # -------------------------
        disc_input_nc = (
            config['model']['input_nc']
            + config['model']['output_nc']
        )

        self.netD = NLayerDiscriminator(
            input_nc=disc_input_nc,
            ndf=config['model']['ndf']
        ).to(self.device)

        # -------------------------
        # Weight Initialization
        # -------------------------
        init_weights(self.netG, init_type='normal')
        init_weights(self.netD, init_type='normal')

        # -------------------------
        # Loss
        # -------------------------
        self.loss_engine = HybridReconstructionLoss(
            lambda_L1=config['training']['lambda_L1']
        )

        # -------------------------
        # Optimizers
        # -------------------------
        self.optimizer_G = optim.Adam(
            self.netG.parameters(),
            lr=config['training']['lr_g'],
            betas=(
                config['training']['beta1'],
                config['training']['beta2']
            )
        )

        self.optimizer_D = optim.Adam(
            self.netD.parameters(),
            lr=config['training']['lr_d'],
            betas=(
                config['training']['beta1'],
                config['training']['beta2']
            )
        )

    # -------------------------------------------------------
    # Train One Batch
    # -------------------------------------------------------

    def optimize_batch(self, real_cloudy, real_clear):

        real_cloudy = real_cloudy.to(self.device)
        real_clear = real_clear.to(self.device)

        # -------------------------
        # Train Discriminator
        # -------------------------

        self.optimizer_D.zero_grad()

        fake_clear = self.netG(real_cloudy)

        real_pair = torch.cat(
            (real_cloudy, real_clear),
            dim=1
        )

        pred_real = self.netD(real_pair)

        fake_pair_D = torch.cat(
            (real_cloudy, fake_clear.detach()),
            dim=1
        )

        pred_fake_D = self.netD(fake_pair_D)

        loss_D = self.loss_engine.calculate_discriminator_loss(
            pred_real,
            pred_fake_D
        )

        loss_D.backward()
        self.optimizer_D.step()

        # -------------------------
        # Train Generator
        # -------------------------

        self.optimizer_G.zero_grad()

        fake_pair_G = torch.cat(
            (real_cloudy, fake_clear),
            dim=1
        )

        pred_fake_G = self.netD(fake_pair_G)

        loss_G, loss_G_GAN, loss_G_L1 = \
            self.loss_engine.calculate_generator_loss(
                pred_fake_G,
                fake_clear,
                real_clear
            )

        loss_G.backward()
        self.optimizer_G.step()

        return {
            'loss_D': loss_D.item(),
            'loss_G': loss_G.item(),
            'loss_G_GAN': loss_G_GAN.item(),
            'loss_G_L1': loss_G_L1.item()
        }

    # -------------------------------------------------------
    # Save Checkpoint
    # -------------------------------------------------------

    def save_checkpoint(
        self,
        epoch,
        directory="outputs/checkpoints"
    ):

        os.makedirs(directory, exist_ok=True)

        checkpoint_path = os.path.join(
            directory,
            f"checkpoint_epoch_{epoch}.pth"
        )

        torch.save({
            "epoch": epoch,
            "netG_state_dict": self.netG.state_dict(),
            "netD_state_dict": self.netD.state_dict(),
            "optimizer_G_state_dict": self.optimizer_G.state_dict(),
            "optimizer_D_state_dict": self.optimizer_D.state_dict(),
        }, checkpoint_path)

        print(f"[✓] Checkpoint successfully persisted: {checkpoint_path}")

    # -------------------------------------------------------
    # Load Checkpoint
    # -------------------------------------------------------

    def load_checkpoint(self, checkpoint_path):

        checkpoint = torch.load(
            checkpoint_path,
            map_location=self.device
        )

        self.netG.load_state_dict(
            checkpoint["netG_state_dict"]
        )

        if "netD_state_dict" in checkpoint:
            self.netD.load_state_dict(
                checkpoint["netD_state_dict"]
            )

        if "optimizer_G_state_dict" in checkpoint:
            self.optimizer_G.load_state_dict(
                checkpoint["optimizer_G_state_dict"]
            )

        if "optimizer_D_state_dict" in checkpoint:
            self.optimizer_D.load_state_dict(
                checkpoint["optimizer_D_state_dict"]
            )

        epoch = checkpoint.get("epoch", 0)

        print("========================================")
        print("Pretrained Checkpoint Loaded Successfully")
        print("========================================")
        print(f"Epoch : {epoch}")
        print(f"File  : {checkpoint_path}")

        return epoch
