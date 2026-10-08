import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from pathlib import Path
from tqdm import tqdm
from torch.utils.data import DataLoader, random_split

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.networks import UNetGenerator
from src.dataset_loader import LISS4CloudDataset
from src.metrics import (
    calculate_psnr,
    calculate_ssim,
    calculate_rmse,
    calculate_sam,
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BATCH_SIZE = 4
EPOCHS = 30
LEARNING_RATE = 2e-4

CHECKPOINT_DIR = "checkpoints"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

print("=" * 60)
print("LISS-IV Cloud Removal Training")
print("=" * 60)
print("Device:", DEVICE)

# ----------------------------
# Dataset
# ----------------------------

dataset = LISS4CloudDataset(dataset_type="LISS4")

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = random_split(
    dataset,
    [train_size, val_size]
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

print(f"Training Samples : {len(train_dataset)}")
print(f"Validation Samples : {len(val_dataset)}")

# ----------------------------
# Model
# ----------------------------

model = UNetGenerator(
    input_nc=3,
    output_nc=3
).to(DEVICE)

criterion = nn.L1Loss()

optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE,
    betas=(0.5, 0.999)
)

print("Model created successfully.")
# ----------------------------
# Training
# ----------------------------

best_psnr = -1.0

for epoch in range(EPOCHS):

    print(f"\nEpoch [{epoch+1}/{EPOCHS}]")

    model.train()

    train_loss = 0.0

    progress = tqdm(train_loader)

    for cloudy, clean in progress:

        cloudy = cloudy.to(DEVICE)
        clean = clean.to(DEVICE)

        optimizer.zero_grad()

        prediction = model(cloudy)

        loss = criterion(prediction, clean)

        loss.backward()

        optimizer.step()

        train_loss += loss.item()

        progress.set_description(
            f"Loss: {loss.item():.4f}"
        )

    train_loss /= len(train_loader)

    print(f"Training Loss : {train_loss:.6f}")

    # ----------------------------
    # Validation
    # ----------------------------

    model.eval()

    psnr_list = []
    ssim_list = []
    rmse_list = []
    sam_list = []

    with torch.no_grad():

        for cloudy, clean in val_loader:

            cloudy = cloudy.to(DEVICE)
            clean = clean.to(DEVICE)

            prediction = model(cloudy)

            pred = prediction.squeeze().cpu().numpy()
            gt = clean.squeeze().cpu().numpy()

            pred = ((pred + 1.0) * 127.5).clip(0, 255)
            gt = ((gt + 1.0) * 127.5).clip(0, 255)

            psnr_list.append(calculate_psnr(gt, pred))
            ssim_list.append(calculate_ssim(gt, pred))
            rmse_list.append(calculate_rmse(gt, pred))
            sam_list.append(calculate_sam(gt, pred))

    avg_psnr = np.mean(psnr_list)
    avg_ssim = np.mean(ssim_list)
    avg_rmse = np.mean(rmse_list)
    avg_sam = np.mean(sam_list)

    print(f"PSNR : {avg_psnr:.3f}")
    print(f"SSIM : {avg_ssim:.4f}")
    print(f"RMSE : {avg_rmse:.4f}")
    print(f"SAM  : {avg_sam:.4f}")

    checkpoint = os.path.join(
        CHECKPOINT_DIR,
        f"epoch_{epoch+1}.pth"
    )

    torch.save(
        model.state_dict(),
        checkpoint
    )

    print("Checkpoint Saved:", checkpoint)

    if avg_psnr > best_psnr:

        best_psnr = avg_psnr

        torch.save(
            model.state_dict(),
            os.path.join(
                CHECKPOINT_DIR,
                "best_model.pth"
            )
        )

        print("Best model updated.")

print("\nTraining Finished Successfully.")
