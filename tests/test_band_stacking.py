import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..")) if "src" in CURRENT_DIR else CURRENT_DIR
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.app import read_single_raster_band, generate_multiband_geotiff_bytes

def test_band_stacking_folder():
    target_dir = "C:\\Users\\sabar\\Downloads\\R2F02OCT2024069820011000053SSANSTUC00GTDB\\R2F02OCT2024069820011000053SSANSTUC00GTDB"
    b2_path = os.path.join(target_dir, "BAND2.tif")
    b3_path = os.path.join(target_dir, "BAND3.tif")
    b4_path = os.path.join(target_dir, "BAND4.tif")
    
    print("=== Testing Real LISS-IV 595MB Band Stacking Engine ===")
    print(f"Target Directory: {target_dir}")
    print(f"BAND2.tif exists: {os.path.exists(b2_path)} ({os.path.getsize(b2_path) / 1e6:.1f} MB)")
    print(f"BAND3.tif exists: {os.path.exists(b3_path)} ({os.path.getsize(b3_path) / 1e6:.1f} MB)")
    print(f"BAND4.tif exists: {os.path.exists(b4_path)} ({os.path.getsize(b4_path) / 1e6:.1f} MB)")

    class SimpleFileObj:
        def __init__(self, filepath):
            self.name = os.path.basename(filepath)
            self.filepath = filepath
        def read(self):
            with open(self.filepath, "rb") as f: return f.read()
        def getbuffer(self):
            with open(self.filepath, "rb") as f: return f.read()

    t0 = time.time()
    print("Reading Band 2 (Green)...")
    b2_data, meta2 = read_single_raster_band(SimpleFileObj(b2_path))
    print(f"Band 2 Shape: {b2_data.shape} | Meta: {meta2['width']}x{meta2['height']}")

    print("Reading Band 3 (Red)...")
    b3_data, meta3 = read_single_raster_band(SimpleFileObj(b3_path))
    print(f"Band 3 Shape: {b3_data.shape} | Meta: {meta3['width']}x{meta3['height']}")

    print("Reading Band 4 (NIR)...")
    b4_data, meta4 = read_single_raster_band(SimpleFileObj(b4_path))
    print(f"Band 4 Shape: {b4_data.shape} | Meta: {meta4['width']}x{meta4['height']}")

    print("Generating Stacking GeoTIFF bytes...")
    gtiff_bytes = generate_multiband_geotiff_bytes(b2_data, b3_data, b4_data, meta2)
    elapsed = time.time() - t0
    
    out_path = os.path.join(PROJECT_ROOT, "outputs", "stacked_liss4_user_dataset.tif")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(gtiff_bytes)
        
    print(f"SUCCESS! Multi-band GeoTIFF generated in {elapsed:.2f} seconds ({len(gtiff_bytes)/1e6:.2f} MB saved to {out_path})")

if __name__ == "__main__":
    test_band_stacking_folder()
