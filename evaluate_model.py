import os
import sys
import numpy as np
import torch
from torch.utils.data import DataLoader

# -------------------------------------------------
# Project Imports
# -------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from src.dataset_loader import LISS4CloudDataset
from src.metrics import (
    calculate_psnr,
    calculate_ssim,
    calculate_rmse,
    calculate_sam,
)

from models.networks import UNetGenerator

# -------------------------------------------------
# Device
# -------------------------------------------------

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=" * 60)
print("LISS-IV Cloud Removal Evaluation")
print("=" * 60)
print("Device:", DEVICE)

# -------------------------------------------------
# Dataset
# -------------------------------------------------

dataset = LISS4CloudDataset(
    base_dir="datasets/liss4_dataset",
    dataset_type="LISS4"
)

loader = DataLoader(
    dataset,
    batch_size=1,
    shuffle=False
)

print("Dataset Size:", len(dataset))

# -------------------------------------------------
# Model
# -------------------------------------------------

model = UNetGenerator(
    input_nc=3,
    output_nc=3,
    num_downs=8
).to(DEVICE)

checkpoint = torch.load(
    "checkpoints/best_model.pth",
    map_location=DEVICE
)

model.load_state_dict(checkpoint)
model.eval()

print("Best model loaded successfully.\n")

# -------------------------------------------------
# Evaluation
# -------------------------------------------------

psnr_total = 0.0
ssim_total = 0.0
rmse_total = 0.0
sam_total = 0.0

with torch.no_grad():

    for i, (cloudy, clean) in enumerate(loader):

        cloudy = cloudy.to(DEVICE)

        prediction = model(cloudy)

        pred = prediction.squeeze(0).cpu().numpy()
        gt = clean.squeeze(0).numpy()

        # Convert from [-1,1] to [0,255]
        pred = ((pred + 1.0) / 2.0) * 255.0
        gt = ((gt + 1.0) / 2.0) * 255.0

        pred = np.clip(pred, 0, 255)
        gt = np.clip(gt, 0, 255)

        psnr_total += calculate_psnr(gt, pred)
        ssim_total += calculate_ssim(gt, pred)
        rmse_total += calculate_rmse(gt, pred)
        sam_total += calculate_sam(gt, pred)

        if (i + 1) % 25 == 0:
            print(f"{i+1}/{len(loader)} evaluated")

# -------------------------------------------------
# Final Results
# -------------------------------------------------

n = len(loader)

avg_psnr = psnr_total / n
avg_ssim = ssim_total / n
avg_rmse = rmse_total / n
avg_sam = sam_total / n

print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(f"Average PSNR : {avg_psnr:.4f}")
print(f"Average SSIM : {avg_ssim:.4f}")
print(f"Average RMSE : {avg_rmse:.4f}")
print(f"Average SAM  : {avg_sam:.4f}")

# -------------------------------------------------
# Save Results
# -------------------------------------------------

os.makedirs("outputs", exist_ok=True)

with open("outputs/results.txt", "w") as f:

    f.write("LISS-IV Cloud Removal Evaluation\n")
    f.write("=" * 40 + "\n\n")
    f.write(f"Dataset Size : {n}\n\n")
    f.write(f"Average PSNR : {avg_psnr:.4f}\n")
    f.write(f"Average SSIM : {avg_ssim:.4f}\n")
    f.write(f"Average RMSE : {avg_rmse:.4f}\n")
    f.write(f"Average SAM  : {avg_sam:.4f}\n")

print("\nResults saved to:")
print("outputs/results.txt")
