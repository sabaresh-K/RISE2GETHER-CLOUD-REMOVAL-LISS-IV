import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

scene = Path("data/raw_samples/247109911")

with rasterio.open(scene / "BAND2.tif") as src:
    green = src.read(1).astype(np.float32)

with rasterio.open(scene / "BAND3.tif") as src:
    red = src.read(1).astype(np.float32)

with rasterio.open(scene / "BAND4.tif") as src:
    nir = src.read(1).astype(np.float32)

# Normalize each band independently
red /= red.max()
green /= green.max()
nir /= nir.max()

rgb = np.dstack((red, green, nir))

plt.figure(figsize=(10,10))
plt.imshow(rgb)
plt.title("LISS-IV RGB Composite")
plt.axis("off")

plt.savefig("outputs/liss_rgb.png", dpi=300)

print("Saved RGB image to outputs/liss_rgb.png")
plt.show()
