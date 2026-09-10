import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------
# Folder containing patches
# --------------------------
patch_dir = Path("datasets/liss4/patches")

files = sorted(patch_dir.glob("*.npy"))

print(f"Total patches: {len(files)}")

# --------------------------
# Create one figure with 6 images
# --------------------------
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

for ax, file in zip(axes.ravel(), files[:6]):

    patch = np.load(file)

    # Convert (C,H,W) -> (H,W,C)
    img = np.transpose(patch, (1, 2, 0))

    ax.imshow(img)
    ax.set_title(file.name)
    ax.axis("off")

plt.tight_layout()

# --------------------------
# Save figure
# --------------------------
Path("outputs/liss4").mkdir(parents=True, exist_ok=True)

plt.savefig("outputs/liss4/first_6_patches.png", dpi=300)

plt.close()

print("✓ Saved figure to outputs/liss4/first_6_patches.png")
