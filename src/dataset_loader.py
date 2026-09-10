import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image


class LISS4CloudDataset(Dataset):
    def __init__(
        self,
        base_dir=None,
        dataset_type="RICE1",
        transform=None,
    ):
        self.dataset_type = dataset_type
        self.transform = transform

        # ----------------------------
        # Dataset Paths
        # ----------------------------

        if dataset_type == "RICE1":

            if base_dir is None:
                base_dir = "/home/jeffrin/isro_hackathon/data/datasets/RICE"

            self.cloudy_dir = os.path.join(base_dir, "RICE1", "cloud")
            self.clear_dir = os.path.join(base_dir, "RICE1", "label")
            self.use_masks = False

        elif dataset_type == "RICE2":

            if base_dir is None:
                base_dir = "/home/jeffrin/isro_hackathon/data/datasets/RICE"

            self.cloudy_dir = os.path.join(base_dir, "RICE2", "cloud")
            self.clear_dir = os.path.join(base_dir, "RICE2", "label")
            self.mask_dir = os.path.join(base_dir, "RICE2", "mask")
            self.use_masks = True

        elif dataset_type == "LISS4":

            if base_dir is None:
                base_dir = "/home/jeffrin/isro_hackathon/datasets/liss4_dataset"

            self.cloudy_dir = os.path.join(base_dir, "cloud")
            self.clear_dir = os.path.join(base_dir, "label")
            self.use_masks = False

        else:
            raise ValueError(
                "dataset_type must be one of: RICE1, RICE2, LISS4"
            )

        # ----------------------------
        # Check directories
        # ----------------------------

        if not os.path.isdir(self.cloudy_dir):
            raise FileNotFoundError(self.cloudy_dir)

        if not os.path.isdir(self.clear_dir):
            raise FileNotFoundError(self.clear_dir)

        # ----------------------------
        # File list
        # ----------------------------

        if self.dataset_type == "LISS4":

            self.filenames = sorted(
                [
                    f
                    for f in os.listdir(self.cloudy_dir)
                    if f.endswith(".npy")
                ]
            )

        else:

            self.filenames = sorted(
                [
                    f
                    for f in os.listdir(self.cloudy_dir)
                    if f.lower().endswith(
                        (".png", ".jpg", ".jpeg")
                    )
                ]
            )

        print(
            f"Loaded {len(self.filenames)} samples from {dataset_type}"
        )

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):

        filename = self.filenames[idx]

        # ====================================================
        # LISS-IV (.npy patches)
        # ====================================================

        if self.dataset_type == "LISS4":

            cloudy = np.load(
                os.path.join(self.cloudy_dir, filename)
            ).astype(np.float32)

            clear = np.load(
                os.path.join(self.clear_dir, filename)
            ).astype(np.float32)

            cloudy_tensor = torch.from_numpy(cloudy)
            clear_tensor = torch.from_numpy(clear)

            return cloudy_tensor, clear_tensor

        # ====================================================
        # RICE (.png images)
        # ====================================================

        cloudy_img = Image.open(
            os.path.join(self.cloudy_dir, filename)
        ).convert("RGB")

        clear_img = Image.open(
            os.path.join(self.clear_dir, filename)
        ).convert("RGB")

        mask_tensor = torch.tensor(0.0)

        if self.use_masks:

            mask_img = Image.open(
                os.path.join(self.mask_dir, filename)
            ).convert("L")

            mask_np = (
                np.array(mask_img, dtype=np.float32) / 255.0
            )

            mask_tensor = (
                torch.from_numpy(mask_np).unsqueeze(0)
            )

        if self.transform:

            cloudy_tensor = self.transform(cloudy_img)
            clear_tensor = self.transform(clear_img)

        else:

            cloudy_np = np.array(
                cloudy_img,
                dtype=np.float32,
            )

            clear_np = np.array(
                clear_img,
                dtype=np.float32,
            )

            cloudy_tensor = (
                torch.from_numpy(cloudy_np)
                .permute(2, 0, 1)
                .float()
            )

            clear_tensor = (
                torch.from_numpy(clear_np)
                .permute(2, 0, 1)
                .float()
            )

            cloudy_tensor = (cloudy_tensor / 127.5) - 1.0
            clear_tensor = (clear_tensor / 127.5) - 1.0

        if self.use_masks:
            return cloudy_tensor, clear_tensor, mask_tensor

        return cloudy_tensor, clear_tensor


if __name__ == "__main__":

    print("Testing RICE1...")
    rice = LISS4CloudDataset(dataset_type="RICE1")
    print(len(rice))

    print("Testing LISS4...")
    liss = LISS4CloudDataset(dataset_type="LISS4")
    print(len(liss))
