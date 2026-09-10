import rasterio
from pathlib import Path

scene = Path("data/raw_samples/247109911")

for band in ["BAND2.tif", "BAND3.tif", "BAND4.tif"]:

    path = scene / band

    with rasterio.open(path) as src:
        print("=" * 50)
        print(f"{band}")
        print("=" * 50)
        print("Width      :", src.width)
        print("Height     :", src.height)
        print("Bands      :", src.count)
        print("CRS        :", src.crs)
        print("Transform  :", src.transform)
        print("Data type  :", src.dtypes[0])

        img = src.read(1)

        print("Min value  :", img.min())
        print("Max value  :", img.max())
