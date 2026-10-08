import os
import sys
import numpy as np
import torch
from pathlib import Path

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

print("=" * 60)
print("LISS-IV Inference")
print("=" * 60)
print("Device:", DEVICE)

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------

model = UNetGenerator(input_nc=3, output_nc=3).to(DEVICE)

model.load_state_dict(
    torch.load(
        "checkpoints/best_model.pth",
        map_location=DEVICE
    )
)

model.eval()

print("Best model loaded.")

# ---------------------------------------------------
# Dataset
# ---------------------------------------------------

dataset = LISS4CloudDataset(dataset_type="LISS4")

output_dir = "outputs/predictions"

os.makedirs(output_dir, exist_ok=True)

psnr_scores = []
ssim_scores = []
rmse_scores = []
sam_scores = []

with torch.no_grad():

    for idx in range(len(dataset)):

        cloudy, clean = dataset[idx]

        input_tensor = cloudy.unsqueeze(0).to(DEVICE)

        prediction = model(input_tensor)

        pred = prediction.squeeze().cpu().numpy()
        gt = clean.numpy()

        pred_img = ((pred + 1.0) * 127.5).clip(0,255)
        gt_img = ((gt + 1.0) * 127.5).clip(0,255)

        np.save(
            os.path.join(
                output_dir,
                f"prediction_{idx:04d}.npy"
            ),
            pred
        )

        psnr_scores.append(
            calculate_psnr(gt_img, pred_img)
        )

        ssim_scores.append(
            calculate_ssim(gt_img, pred_img)
        )

        rmse_scores.append(
            calculate_rmse(gt_img, pred_img)
        )

        sam_scores.append(
            calculate_sam(gt_img, pred_img)
        )

        print(
            f"{idx+1}/{len(dataset)} "
            f"PSNR={psnr_scores[-1]:.2f}"
        )

print("\n=============================")
print("Inference Complete")
print("=============================")

print("Average PSNR :", np.mean(psnr_scores))
print("Average SSIM :", np.mean(ssim_scores))
print("Average RMSE :", np.mean(rmse_scores))
print("Average SAM  :", np.mean(sam_scores))

print("\nPredictions saved to:")
print(output_dir)
