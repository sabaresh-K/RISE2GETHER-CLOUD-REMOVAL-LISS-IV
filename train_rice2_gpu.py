import os
import sys
import time
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
sys.path.insert(0, CURRENT_DIR)

from src.models import CloudRemovalGenerator

class RICE2Dataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.cloud_dir = os.path.join(data_dir, 'cloud')
        self.label_dir = os.path.join(data_dir, 'label')
        
        self.filenames = sorted([f for f in os.listdir(self.cloud_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif'))])
        self.transform = transform or transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        fname = self.filenames[idx]
        cloud_path = os.path.join(self.cloud_dir, fname)
        label_path = os.path.join(self.label_dir, fname)

        cloud_img = Image.open(cloud_path).convert('RGB')
        label_img = Image.open(label_path).convert('RGB') if os.path.exists(label_path) else cloud_img

        return self.transform(cloud_img), self.transform(label_img)

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('==================================================')
    print('   STARTING GPU MODEL TRAINING ON RICE2 DATASET')
    print(f'   Device Target: {device}')
    if torch.cuda.is_available():
        print(f'   GPU Hardware: {torch.cuda.get_device_name(0)}')
    print('==================================================')

    data_dir = r'C:\Users\sabar\Downloads\RICE_DATASET\RICE2'
    dataset = RICE2Dataset(data_dir)
    train_loader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=0, pin_memory=True)
    print(f'Dataset Loaded: {len(dataset)} paired images | Batches per Epoch: {len(train_loader)}')

    model = CloudRemovalGenerator(in_channels=3, out_channels=3).to(device)
    
    checkpoint_path = os.path.join(CURRENT_DIR, 'data', 'generator_checkpoint.pth')
    backup_path = os.path.join(CURRENT_DIR, 'checkpoints', 'rice1_generator.pth')
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)

    if os.path.exists(checkpoint_path):
        try:
            model.load_state_dict(torch.load(checkpoint_path, map_location=device), strict=False)
            print('Loaded existing checkpoint weights for fine-tuning.')
        except Exception as e:
            print(f'Starting clean training: {e}')

    criterion_l1 = nn.L1Loss()
    criterion_mse = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0002, betas=(0.5, 0.999))

    epochs = 40
    start_time = time.time()

    for epoch in range(1, epochs + 1):
        model.train()
        running_l1 = 0.0
        running_mse = 0.0

        for cloud_batch, label_batch in train_loader:
            cloud_batch = cloud_batch.to(device)
            label_batch = label_batch.to(device)

            optimizer.zero_grad()
            output = model(cloud_batch)

            loss_l1 = criterion_l1(output, label_batch)
            loss_mse = criterion_mse(output, label_batch)
            total_loss = loss_l1 + 0.5 * loss_mse

            total_loss.backward()
            optimizer.step()

            running_l1 += loss_l1.item() * cloud_batch.size(0)
            running_mse += loss_mse.item() * cloud_batch.size(0)

        epoch_l1 = running_l1 / len(dataset)
        epoch_mse = running_mse / len(dataset)
        psnr_est = 20 * np.log10(2.0 / (np.sqrt(epoch_mse) + 1e-8))

        if epoch % 5 == 0 or epoch == epochs or epoch == 1:
            print(f'Epoch [{epoch:02d}/{epochs:02d}] | L1 Loss: {epoch_l1:.4f} | MSE Loss: {epoch_mse:.4f} | Est PSNR: {psnr_est:.2f} dB', flush=True)

    # Save final trained model weights
    torch.save(model.state_dict(), checkpoint_path)
    torch.save(model.state_dict(), backup_path)
    elapsed = time.time() - start_time
    print('==================================================')
    print(f'   TRAINING COMPLETE IN {elapsed:.2f} SECONDS!')
    print(f'   Checkpoint saved to: {checkpoint_path}')
    print(f'   Backup checkpoint saved to: {backup_path}')
    print('==================================================')

if __name__ == '__main__':
    train()
