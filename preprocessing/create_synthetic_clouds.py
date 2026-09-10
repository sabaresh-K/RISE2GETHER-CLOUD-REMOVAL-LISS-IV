import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import gaussian_filter

# -----------------------------
# Paths
# -----------------------------
input_dir = Path("datasets/liss4/patches")
output_dir = Path("datasets/liss4/cloudy")
output_dir.mkdir(parents=True, exist_ok=True)

patches = sorted(input_dir.glob("*.npy"))

print(f"Found {len(patches)} patches.")

# -----------------------------
# Parameters
# -----------------------------
CLOUD_PROBABILITY = 0.75
SIGMA = 18
THRESHOLD = 0.62
ALPHA = 0.75

saved = 0

# -----------------------------
# Generate Clouds
# -----------------------------
for patch_file in patches:

    patch = np.load(patch_file).astype(np.float32)
    cloudy = patch.copy()

    if np.random.rand() < CLOUD_PROBABILITY:

        H, W = patch.shape[1], patch.shape[2]

        noise = np.random.rand(H, W)

        cloud = gaussian_filter(noise, sigma=SIGMA)

        cloud = (cloud - cloud.min()) / (cloud.max() - cloud.min())

        cloud = (cloud > THRESHOLD).astype(np.float32)

        cloud = gaussian_filter(cloud, sigma=8)

        cloud = np.clip(cloud, 0, 1)

        cloud = cloud[np.newaxis, :, :]

        cloudy = cloudy * (1 - ALPHA * cloud) + ALPHA * cloud

    np.save(output_dir / patch_file.name, cloudy.astype(np.float32))

    saved += 1

print("----------------------------------")
print("Synthetic Cloud Generation Complete")
print("----------------------------------")
print("Saved:", saved)

# -----------------------------
# Preview first 3 patches
# -----------------------------
sample_files = sorted(output_dir.glob("*.npy"))[:3]

fig, axes = plt.subplots(3, 2, figsize=(8, 12))

for i, file in enumerate(sample_files):

    clean = np.load(input_dir / file.name)
    cloudy = np.load(file)

    clean = np.transpose(clean, (1, 2, 0))
    cloudy = np.transpose(cloudy, (1, 2, 0))

    axes[i, 0].imshow(clean)
    axes[i, 0].set_title("Clean")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(cloudy)
    axes[i, 1].set_title("Cloudy")
    axes[i, 1].axis("off")

plt.tight_layout()

Path("outputs/liss4").mkdir(parents=True, exist_ok=True)

plt.savefig("outputs/liss4/cloud_preview.png", dpi=300)

plt.close()

print("✓ Preview saved to outputs/liss4/cloud_preview.png")
