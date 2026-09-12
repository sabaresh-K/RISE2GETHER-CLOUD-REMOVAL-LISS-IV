import os
import sys
import time
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..")) if "src" in CURRENT_DIR else CURRENT_DIR
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.dataset_loader import LISS4CloudDataset
from src.cyclegan_model import CycleGANModel

def train_cyclegan(
    dataset_dir="C:\\Users\\sabar\\Downloads\\RICE_DATASET",
    dataset_type="RICE2",
    epochs=10,
    batch_size=2,
    lr=0.0002,
    device="cuda",
    target_size=(256, 256)
):
    print("=== Launching Accelerated SAR-Guided CycleGAN GPU Pipeline ===", flush=True)
    
    # 1. Device Selection & CUDNN Optimization
    device_obj = torch.device("cuda" if torch.cuda.is_available() and device == "cuda" else "cpu")
    print(f"[Device] Using compute device: {device_obj}", flush=True)
    if device_obj.type == "cuda":
        print(f"[GPU Hardware] {torch.cuda.get_device_name(0)} (CUDA Enabled)", flush=True)
        torch.cuda.empty_cache()
        torch.backends.cudnn.benchmark = True

    # 2. Dataset Loader
    if not os.path.exists(dataset_dir):
        print(f"[Warning] Path {dataset_dir} not found. Attempting relative dataset lookup.", flush=True)
        dataset_dir = os.path.join(PROJECT_ROOT, "data")
        dataset_type = "RICE1"

    dataset = LISS4CloudDataset(base_dir=dataset_dir, dataset_type=dataset_type)
    loader = DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=0, 
        pin_memory=(device_obj.type == "cuda"), 
        drop_last=True
    )
    print(f"[Dataset] Total training samples: {len(dataset)} | Batches per epoch: {len(loader)} | Batch size: {batch_size}", flush=True)

    # 3. Model Initialization (Upgraded U-ResNet CycleGAN Generator)
    model = CycleGANModel(in_channels_a=5, out_channels_b=3, lr=lr, device=device_obj.type)
    print("[Architecture] Upgraded U-ResNet CycleGAN Generator with Skip Connections & Bilinear Upsampling", flush=True)
    
    # 4. Training Loop
    t_start = time.time()
    for epoch in range(1, epochs + 1):
        epoch_g_loss = 0.0
        epoch_d_loss = 0.0
        epoch_cyc_loss = 0.0
        
        for i, batch in enumerate(loader):
            if isinstance(batch, (list, tuple)):
                cloudy_opt = batch[0]
                clear_opt = batch[1]
            else:
                cloudy_opt = batch["cloudy"]
                clear_opt = batch["clear"]

            # Move tensors to GPU
            cloudy_opt = cloudy_opt.to(device_obj, non_blocking=True)
            clear_opt = clear_opt.to(device_obj, non_blocking=True)

            # Resize to 256x256 for optimal VRAM usage
            if cloudy_opt.shape[-2:] != target_size:
                cloudy_opt = F.interpolate(cloudy_opt, size=target_size, mode="bilinear", align_corners=False)
            if clear_opt.shape[-2:] != target_size:
                clear_opt = F.interpolate(clear_opt, size=target_size, mode="bilinear", align_corners=False)

            model.set_input(cloudy_opt, clear_opt)
            losses = model.optimize_parameters()
            
            epoch_g_loss += losses["loss_G"]
            epoch_d_loss += (losses["loss_D_A"] + losses["loss_D_B"])
            epoch_cyc_loss += losses["loss_cycle"]

            if (i + 1) % 50 == 0:
                print(f"  [GPU Epoch {epoch:02d}/{epochs:02d}] Batch [{i+1}/{len(loader)}] | G_Loss: {losses['loss_G']:.4f} | D_Loss: {(losses['loss_D_A']+losses['loss_D_B']):.4f} | L1_Loss: {losses.get('loss_L1', 0.0):.4f}", flush=True)

        avg_g = epoch_g_loss / len(loader)
        avg_d = epoch_d_loss / len(loader)
        avg_cyc = epoch_cyc_loss / len(loader)
        
        print(f"==> Epoch [{epoch:02d}/{epochs:02d}] Complete | Avg G Loss: {avg_g:.4f} | Avg D Loss: {avg_d:.4f} | Avg Cycle Loss: {avg_cyc:.4f}", flush=True)

    total_time = time.time() - t_start
    print(f"[Completed] CycleGAN Training finished in {total_time / 60.0:.2f} minutes.")

    # 5. Save Checkpoints
    out_dir1 = os.path.join(PROJECT_ROOT, "data")
    out_dir2 = os.path.join(PROJECT_ROOT, "checkpoints")
    
    p1 = model.save_checkpoint(out_dir1, filename="cyclegan_generator.pth")
    p2 = model.save_checkpoint(out_dir2, filename="sar_cyclegan.pth")
    
    # Save PyTorch state dict for Generator A2B compatible with Streamlit model loader
    gen_path = os.path.join(out_dir1, "cyclegan_a2b.pth")
    torch.save(model.netG_A2B.state_dict(), gen_path)

    print(f"[Saved] CycleGAN Checkpoints saved to:\n  - {p1}\n  - {p2}\n  - {gen_path}")
    return model

if __name__ == "__main__":
    train_cyclegan(epochs=5, batch_size=1)
