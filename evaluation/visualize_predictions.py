import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.dataset_loader import LISS4CloudDataset

OUTPUT_DIR = "outputs/comparisons"
os.makedirs(OUTPUT_DIR, exist_ok=True)

dataset = LISS4CloudDataset(dataset_type="LISS4")

print(f"Loaded {len(dataset)} samples")


def tensor_to_image(x):
    x = x.numpy()
    x = np.transpose(x, (1, 2, 0))
    x = ((x + 1) / 2).clip(0, 1)
    return x


for i in range(len(dataset)):

    cloudy, clean = dataset[i]

    pred = np.load(
        f"outputs/predictions/prediction_{i:04d}.npy"
    )

    pred = np.transpose(pred, (1, 2, 0))
    pred = ((pred + 1) / 2).clip(0, 1)

    cloudy = tensor_to_image(cloudy)
    clean = tensor_to_image(clean)

    fig = plt.figure(figsize=(12,4))

    plt.subplot(1,3,1)
    plt.imshow(cloudy)
    plt.title("Cloudy")
    plt.axis("off")

    plt.subplot(1,3,2)
    plt.imshow(pred)
    plt.title("Prediction")
    plt.axis("off")

    plt.subplot(1,3,3)
    plt.imshow(clean)
    plt.title("Ground Truth")
    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            f"comparison_{i:04d}.png"
        ),
        dpi=200
    )

    plt.close(fig)

    if (i + 1) % 25 == 0:
        print(f"{i+1}/{len(dataset)} completed")

print("\nVisualization completed.")
print("Saved to:", OUTPUT_DIR)
