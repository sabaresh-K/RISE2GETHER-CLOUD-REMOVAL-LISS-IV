import os
import glob
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset


class RemoteSensingDataset(Dataset):
    """
    Generic dataset loader supporting:

    - RICE1 / RICE2 (PNG/JPG)
    - LISS-IV (.npy patches)

    Output:
        {
            "cloudy": Tensor(3,H,W),
            "clear": Tensor(3,H,W)
        }

    Tensor range:
        [-1, 1]
    """

    def __init__(self, root_dir, patch_size=256):

        self.root_dir = root_dir
        self.patch_size = patch_size

        self.cloudy_images = sorted(
            glob.glob(os.path.join(root_dir, "cloud", "*"))
        )

        self.clear_images = sorted(
            glob.glob(os.path.join(root_dir, "label", "*"))
        )

        if len(self.cloudy_images) == 0:
            raise ValueError(
                f"No images found inside:\n{root_dir}/cloud"
            )

        if len(self.cloudy_images) != len(self.clear_images):
            raise ValueError(
                f"Dataset mismatch.\n"
                f"Cloud images : {len(self.cloudy_images)}\n"
                f"Clear images : {len(self.clear_images)}"
            )

        print(f"Loaded {len(self.cloudy_images)} image pairs.")

    def __len__(self):
        return len(self.cloudy_images)

    def _load_file(self, path):

        ext = os.path.splitext(path)[1].lower()

        # ----------------------------
        # LISS-IV patches (.npy)
        # ----------------------------
        if ext == ".npy":

            img = np.load(path).astype(np.float32)

            if img.max() > 1.0:
                img = img / 255.0

            return img

        # ----------------------------
        # PNG / JPG
        # ----------------------------
        img = cv2.imread(path, cv2.IMREAD_COLOR)

        if img is None:
            raise RuntimeError(f"Unable to read image:\n{path}")

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = img.astype(np.float32) / 255.0

        return img

    def __getitem__(self, idx):

        cloudy = self._load_file(self.cloudy_images[idx])
        clear = self._load_file(self.clear_images[idx])

        # -------------------------------------------------------
        # Case 1 : PNG/JPG (H,W,3)
        # -------------------------------------------------------

        if cloudy.ndim == 3 and cloudy.shape[-1] == 3:

            if cloudy.shape[:2] != (
                self.patch_size,
                self.patch_size,
            ):

                cloudy = cv2.resize(
                    cloudy,
                    (self.patch_size, self.patch_size)
                )

                clear = cv2.resize(
                    clear,
                    (self.patch_size, self.patch_size)
                )

            cloudy = np.transpose(cloudy, (2, 0, 1))
            clear = np.transpose(clear, (2, 0, 1))

        # -------------------------------------------------------
        # Case 2 : .npy already CHW
        # -------------------------------------------------------

        elif cloudy.ndim == 3 and cloudy.shape[0] == 3:

            if cloudy.shape[1:] != (
                self.patch_size,
                self.patch_size,
            ):

                cloudy = np.stack([
                    cv2.resize(
                        channel,
                        (self.patch_size, self.patch_size)
                    )
                    for channel in cloudy
                ])

                clear = np.stack([
                    cv2.resize(
                        channel,
                        (self.patch_size, self.patch_size)
                    )
                    for channel in clear
                ])

        else:

            raise RuntimeError(
                f"Unsupported image shape: {cloudy.shape}"
            )

        # Normalize to [-1,1]
        cloudy = (cloudy * 2.0) - 1.0
        clear = (clear * 2.0) - 1.0

        cloudy = torch.from_numpy(
            cloudy.astype(np.float32)
        )

        clear = torch.from_numpy(
            clear.astype(np.float32)
        )

        return {
            "cloudy": cloudy,
            "clear": clear,
        }


if __name__ == "__main__":

    dataset = RemoteSensingDataset(
        root_dir="datasets/liss4_dataset"
    )

    print("Dataset size:", len(dataset))

    sample = dataset[0]

    print("Cloudy :", sample["cloudy"].shape)
    print("Clear  :", sample["clear"].shape)
    print("Range  :", sample["cloudy"].min().item(),
          sample["cloudy"].max().item())
