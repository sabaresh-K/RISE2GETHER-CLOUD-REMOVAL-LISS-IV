import os
import sys
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms as T
from PIL import Image
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.models import CloudRemovalGenerator

# ----------------------------
# RICE1 Dataset Loader
# ----------------------------
class RICE1Dataset(Dataset):
    def __init__(self, rice_dir):
        self.cloudy_dir = os.path.join(rice_dir, "cloud")
        self.clear_dir = os.path.join(rice_dir, "label")
        
        self.cloudy_files = sorted([f for f in os.listdir(self.cloudy_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
        self.clear_files = sorted([f for f in os.listdir(self.clear_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
        
        self.pairs = []
        clear_set = set(self.clear_files)
        for cf in self.cloudy_files:
            if cf in clear_set:
                self.pairs.append((os.path.join(self.cloudy_dir, cf), os.path.join(self.clear_dir, cf)))
                
        print(f"Found {len(self.pairs)} valid LISS-IV paired scenes.")
        
        self.transform = T.Compose([
            T.Resize((256, 256)),
            T.ToTensor(),
            T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        cloudy_path, clear_path = self.pairs[idx]
        cloudy_img = Image.open(cloudy_path).convert("RGB")
        clear_img = Image.open(clear_path).convert("RGB")
        return self.transform(cloudy_img), self.transform(clear_img)

# ----------------------------
# Combined L1 + SSIM Loss
# ----------------------------
class CombinedLoss(nn.Module):
    def __init__(self):
        super(CombinedLoss, self).__init__()
        self.l1 = nn.L1Loss()
        self.mse = nn.MSELoss()

    def forward(self, pred, target):
        loss_l1 = self.l1(pred, target)
        loss_mse = self.mse(pred, target)
        return loss_l1 + 0.8 * loss_mse

# ----------------------------
# GPU Model Training Function
# ----------------------------
def train_gpu_model(rice_dir, epochs=40, batch_size=16, lr=2e-4):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 60)
    print("Starting RISE2GETHER High-Accuracy GPU Training")
    print("=" * 60)
    print(f"Dataset Path: {rice_dir}")
    print(f"Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    print(f"Epochs: {epochs} | Batch Size: {batch_size} | Learning Rate: {lr}")
    
    dataset = RICE1Dataset(rice_dir)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    
    model = CloudRemovalGenerator(in_channels=3, out_channels=3).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr, betas=(0.5, 0.999))
    criterion = CombinedLoss()
    
    os.makedirs(os.path.join(PROJECT_ROOT, "data"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, "checkpoints"), exist_ok=True)
    checkpoint_path = os.path.join(PROJECT_ROOT, "data", "generator_checkpoint.pth")
    backup_path = os.path.join(PROJECT_ROOT, "checkpoints", "liss4_gpu_generator.pth")
    
    start_time = time.time()
    
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        
        for i, (cloudy, clear) in enumerate(dataloader):
            cloudy, clear = cloudy.to(device), clear.to(device)
            
            optimizer.zero_grad()
            output = model(cloudy)
            loss = criterion(output, clear)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
        avg_loss = running_loss / len(dataloader)
        avg_psnr = 20 * np.log10(2.0 / np.sqrt(avg_loss + 1e-7))
        
        if epoch % 5 == 0 or epoch == 1:
            print(f"Epoch [{epoch:02d}/{epochs:02d}] - Combined Loss: {avg_loss:.4f} | Est. PSNR: {avg_psnr:.2f} dB")
            torch.save(model.state_dict(), checkpoint_path)
            torch.save(model.state_dict(), backup_path)
            print(f"  Saved GPU checkpoint to {checkpoint_path}")
            
    elapsed = time.time() - start_time
    print("=" * 60)
    print(f"GPU Training Completed in {elapsed/60:.2f} minutes!")
    print(f"Model Checkpoint Saved to: {checkpoint_path}")
    print("=" * 60)

if __name__ == "__main__":
    rice_path = r"C:\Users\sabar\Downloads\RICE_DATASET\RICE1"
    train_gpu_model(rice_path, epochs=40, batch_size=16, lr=2e-4)
