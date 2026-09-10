from pathlib import Path
import shutil

clean_dir = Path("datasets/liss4/patches")
cloudy_dir = Path("datasets/liss4/cloudy")

dataset_root = Path("datasets/liss4_dataset")

clean_out = dataset_root / "label"
cloudy_out = dataset_root / "cloud"

clean_out.mkdir(parents=True, exist_ok=True)
cloudy_out.mkdir(parents=True, exist_ok=True)

clean_files = sorted(clean_dir.glob("*.npy"))
cloudy_files = sorted(cloudy_dir.glob("*.npy"))

assert len(clean_files) == len(cloudy_files)

for c, cl in zip(clean_files, cloudy_files):

    shutil.copy(c, clean_out / c.name)
    shutil.copy(cl, cloudy_out / cl.name)

print("--------------------------------")
print("Dataset Build Complete")
print("--------------------------------")
print("Clean :", len(clean_files))
print("Cloud :", len(cloudy_files))
print("Saved :", dataset_root)
