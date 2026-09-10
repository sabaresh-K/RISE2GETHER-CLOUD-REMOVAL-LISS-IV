import os
import numpy as np
import rasterio
from rasterio.windows import Window
from pathlib import Path

# -------------------------------
# CONFIGURATION
# -------------------------------

scene = Path("data/raw_samples/247109911")

PATCH_SIZE = 256
STRIDE = 256

OUTPUT = Path("datasets/liss4/patches")
OUTPUT.mkdir(parents=True, exist_ok=True)

# -------------------------------
# READ BANDS
# -------------------------------

band2 = rasterio.open(scene / "BAND2.tif")
band3 = rasterio.open(scene / "BAND3.tif")
band4 = rasterio.open(scene / "BAND4.tif")

width = band2.width
height = band2.height

print(f"Image size : {width} x {height}")

count = 0
discarded = 0

# -------------------------------
# PATCH EXTRACTION
# -------------------------------

for row in range(0, height - PATCH_SIZE + 1, STRIDE):

    for col in range(0, width - PATCH_SIZE + 1, STRIDE):

        window = Window(col, row, PATCH_SIZE, PATCH_SIZE)

        g = band2.read(1, window=window)
        r = band3.read(1, window=window)
        n = band4.read(1, window=window)

        patch = np.stack([g, r, n], axis=0)

        # Remove mostly empty patches
        if np.mean(patch == 0) > 0.80:
            discarded += 1
            continue

        patch = patch.astype(np.float32)

        patch[0] /= 655.0
        patch[1] /= 593.0
        patch[2] /= 574.0

        np.save(
            OUTPUT / f"patch_{count:06d}.npy",
            patch
        )

        count += 1

print("\nExtraction Complete")
print("----------------------------")
print("Saved patches :", count)
print("Discarded     :", discarded)
