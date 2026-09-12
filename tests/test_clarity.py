import os
from PIL import Image
import numpy as np
import torch
from src.models import CloudRemovalGenerator, SARCycleGANGenerator

def auto_stretch_contrast(img_np):
    """Percentile contrast stretching (1% - 99%) to guarantee crisp 0-255 dynamic range."""
    img_out = np.zeros_like(img_np)
    for c in range(3):
        channel = img_np[:, :, c].astype(float)
        p1, p99 = np.percentile(channel, (1, 99))
        if p99 > p1:
            stretched = np.clip((channel - p1) / (p99 - p1) * 255.0, 0, 255)
            img_out[:, :, c] = stretched.astype(np.uint8)
        else:
            img_out[:, :, c] = img_np[:, :, c]
    return img_out

def test_clarity():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    unet = CloudRemovalGenerator(3, 3).to(device)
    unet.load_state_dict(torch.load("data/generator_checkpoint.pth", map_location=device))
    unet.eval()

    gan = SARCycleGANGenerator(5, 3).to(device)
    gan.load_state_dict(torch.load("data/cyclegan_a2b.pth", map_location=device))
    gan.eval()

    for fname in ["0.png", "89.png"]:
        path = f"C:\\Users\\sabar\\Downloads\\{fname}"
        if not os.path.exists(path):
            continue
        img = Image.open(path).convert("RGB").resize((512, 512))
        in_np = np.array(img).astype(np.float32)
        norm_in = (in_np / 127.5) - 1.0
        tensor_in = torch.from_numpy(norm_in).permute(2, 0, 1).unsqueeze(0).to(device)

        with torch.inference_mode():
            out1 = unet(tensor_in).squeeze(0).cpu().permute(1, 2, 0).numpy()
            out2 = gan(tensor_in).squeeze(0).cpu().permute(1, 2, 0).numpy()

            raw1 = np.clip((out1 + 1.0) * 127.5, 0, 255).astype(np.uint8)
            raw2 = np.clip((out2 + 1.0) * 127.5, 0, 255).astype(np.uint8)

            enhanced1 = auto_stretch_contrast(raw1)
            enhanced2 = auto_stretch_contrast(raw2)

            print(f"[{fname} UNet Raw] Min: {raw1.min()}, Max: {raw1.max()} -> [Enhanced] Min: {enhanced1.min()}, Max: {enhanced1.max()}")
            print(f"[{fname} CycleGAN Raw] Min: {raw2.min()}, Max: {raw2.max()} -> [Enhanced] Min: {enhanced2.min()}, Max: {enhanced2.max()}")

            Image.fromarray(enhanced1).save(f"outputs/test_visuals/{fname}_UNet_ENHANCED.png")
            Image.fromarray(enhanced2).save(f"outputs/test_visuals/{fname}_CycleGAN_ENHANCED.png")

if __name__ == "__main__":
    test_clarity()
