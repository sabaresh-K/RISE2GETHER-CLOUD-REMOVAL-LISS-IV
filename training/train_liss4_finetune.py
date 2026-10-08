import os
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.dataset_loader import LISS4CloudDataset
from src.models import UNetGenerator
from src.metrics import calculate_psnr, calculate_ssim, calculate_rmse, calculate_sam


# ======================================
# Configuration
# ======================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 60)
print("LISS-IV Cloud Removal Fine Tuning")
print("=" * 60)
print("Device:", DEVICE)


BATCH_SIZE = 4
START_EPOCH = 100
FINETUNE_EPOCHS = 30


CHECKPOINT = (
    "outputs/checkpoints/checkpoint_epoch_100.pth"
)


SAVE_DIR = (
    "outputs/liss4_finetune"
)

os.makedirs(
    SAVE_DIR,
    exist_ok=True
)



# ======================================
# Dataset
# ======================================

train_dataset = LISS4CloudDataset(
    dataset_type="LISS4"
)


val_dataset = LISS4CloudDataset(
    dataset_type="LISS4"
)



train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)


val_loader = DataLoader(
    val_dataset,
    batch_size=1,
    shuffle=False
)


print(
    "Train samples:",
    len(train_dataset)
)

print(
    "Validation samples:",
    len(val_dataset)
)



# ======================================
# Model
# ======================================

generator = UNetGenerator().to(DEVICE)



# ======================================
# Load pretrained RICE model
# ======================================

if os.path.exists(CHECKPOINT):

    print("Loading checkpoint...")

    checkpoint = torch.load(
        CHECKPOINT,
        map_location=DEVICE
    )


    if "generator" in checkpoint:

        generator.load_state_dict(
            checkpoint["generator"]
        )

    else:

        generator.load_state_dict(
            checkpoint
        )


    print(
        "Loaded:",
        CHECKPOINT
    )


else:

    print(
        "Checkpoint not found!"
    )



# ======================================
# Optimizer
# ======================================

optimizer = torch.optim.Adam(
    generator.parameters(),
    lr=1e-5
)



criterion = torch.nn.L1Loss()



# ======================================
# Fine tuning
# ======================================

for epoch in range(
    START_EPOCH,
    START_EPOCH + FINETUNE_EPOCHS
):

    generator.train()

    total_loss = 0


    loop = tqdm(
        train_loader,
        desc=f"Epoch {epoch+1}"
    )


    for cloudy, clean in loop:


        cloudy = cloudy.to(DEVICE)
        clean = clean.to(DEVICE)


        optimizer.zero_grad()


        output = generator(
            cloudy
        )


        loss = criterion(
            output,
            clean
        )


        loss.backward()


        optimizer.step()


        total_loss += loss.item()


        loop.set_postfix(
            loss=loss.item()
        )


    avg_loss = (
        total_loss /
        len(train_loader)
    )


    print(
        "Training Loss:",
        avg_loss
    )



    # ==================================
    # Validation
    # ==================================

    generator.eval()


    psnr = 0
    ssim = 0
    rmse = 0
    sam = 0


    with torch.no_grad():

        for cloudy, clean in val_loader:

            cloudy = cloudy.to(DEVICE)
            clean = clean.to(DEVICE)


            pred = generator(
                cloudy
            )


            psnr += calculate_psnr(
                pred,
                clean
            )

            ssim += calculate_ssim(
                pred,
                clean
            )

            rmse += calculate_rmse(
                pred,
                clean
            )

            sam += calculate_sam(
                pred,
                clean
            )


    n = len(val_loader)


    print("-----------------------")
    print("PSNR:", psnr/n)
    print("SSIM:", ssim/n)
    print("RMSE:", rmse/n)
    print("SAM :", sam/n)



    # ==================================
    # Save
    # ==================================

    save_path = os.path.join(
        SAVE_DIR,
        f"checkpoint_epoch_{epoch+1}.pth"
    )


    torch.save(
        {
            "epoch":epoch+1,
            "generator":
                generator.state_dict(),
            "optimizer":
                optimizer.state_dict()
        },
        save_path
    )


    print(
        "Saved:",
        save_path
    )


print(
    "LISS-IV Fine tuning completed"
)
