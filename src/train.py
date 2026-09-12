import os
import sys
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..")) if "src" in CURRENT_DIR else CURRENT_DIR
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.dataset_loader import LISS4CloudDataset
from src.models import CloudRemovalGenerator

def train_unet_rice2(epochs=15, batch_size=8, lr=0.0002):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== Training UNet Engine 1 on RICE2 Dataset | Device: {device} ===")
    
    dataset_dir = "C:\\Users\\sabar\\Downloads\\RICE_DATASET"
    if not os.path.exists(os.path.join(dataset_dir, "RICE2")):
        dataset_dir = os.path.join(PROJECT_ROOT, "data")
        dataset_type = "RICE1"
    else:
        dataset_type = "RICE2"

    dataset = LISS4CloudDataset(base_dir=dataset_dir, dataset_type=dataset_type)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=True)
    print(f"[Dataset] Total RICE2 samples: {len(dataset)} | Batches per epoch: {len(loader)}")

    model = CloudRemovalGenerator(in_channels=3, out_channels=3).to(device)
    criterion = nn.L1Loss()
    optimizer = optim.Adam(model.parameters(), lr=lr, betas=(0.5, 0.999))

    t_start = time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        
        for step, batch in enumerate(loader):
            if isinstance(batch, (list, tuple)):
                cloudy = batch[0].to(device)
                clear = batch[1].to(device)
            else:
                cloudy = batch["cloudy"].to(device)
                clear = batch["clear"].to(device)

            optimizer.zero_grad()
            output = model(cloudy)
            loss = criterion(output, clear)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        avg_loss = running_loss / len(loader)
        print(f"Epoch [{epoch:02d}/{epochs:02d}] | Loss L1: {avg_loss:.4f}")

    total_time = time.time() - t_start
    print(f"[Completed] UNet Training finished in {total_time / 60.0:.2f} minutes.")

    # Save to both data/ generator_checkpoint.pth and checkpoints/ rice1_generator.pth
    p1 = os.path.join(PROJECT_ROOT, "data", "generator_checkpoint.pth")
    p2 = os.path.join(PROJECT_ROOT, "checkpoints", "rice1_generator.pth")
    os.makedirs(os.path.dirname(p1), exist_ok=True)
    os.makedirs(os.path.dirname(p2), exist_ok=True)

    torch.save(model.state_dict(), p1)
    torch.save(model.state_dict(), p2)
    print(f"[Saved] UNet RICE2 Checkpoints saved to:\n  - {p1}\n  - {p2}")
    return model

if __name__ == "__main__":
    train_unet_rice2(epochs=15, batch_size=8)
