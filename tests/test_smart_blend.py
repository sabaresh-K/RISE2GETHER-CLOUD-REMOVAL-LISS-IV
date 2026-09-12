import os
import torch
from PIL import Image
import numpy as np
from src.models import CloudRemovalGenerator, SARCycleGANGenerator

def smart_cloud_reconstruction(in_np, out_np):
    """
    Smart Cloud Removal Reconstruction:
    - Identifies valid swathe area vs black nodata padding.
    - Extracts cloud/shadow regions from the input.
    - Blends model predictions smoothly in cloudy regions while preserving 100% sharp ground details in clear regions!
    """
    valid_mask = (in_np.sum(axis=-1) > 15)
    rec_raw = np.clip((out_np + 1.0) * 127.5, 0, 255).astype(np.float32)
    
    # 1. Cloud & Brightness Masking (Identify cloudy regions in input)
    gray_in = 0.2989 * in_np[:, :, 0] + 0.5870 * in_np[:, :, 1] + 0.1140 * in_np[:, :, 2]
    cloud_intensity = np.clip((gray_in - 140.0) / 115.0, 0.0, 1.0) # Soft cloud weight (0 = clear, 1 = heavy cloud)
    cloud_weight = np.expand_dims(cloud_intensity, axis=-1)
    
    # 2. Smoothly blend original clear terrain with neural prediction in cloudy zones
    blended = (1.0 - cloud_weight) * in_np + cloud_weight * rec_raw
    blended = np.clip(blended, 0, 255)
    
    # 3. Re-apply solid black margins
    blended[~valid_mask] = 0
    return blended.astype(np.uint8), valid_mask

def test_smart_blend():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    unet = CloudRemovalGenerator(3, 3).to(device)
    unet.load_state_dict(torch.load("data/generator_checkpoint.pth", map_location=device))
    unet.eval()

    sample_path = "outputs/liss4/cloud_preview.png"
    if not os.path.exists(sample_path):
        sample_path = "outputs/liss_rgb.png"

    img = Image.open(sample_path).convert("RGB").resize((512, 512))
    in_np = np.array(img).astype(np.float32)
    norm_in = (in_np / 127.5) - 1.0
    tensor_in = torch.from_numpy(norm_in).permute(2, 0, 1).unsqueeze(0).to(device)

    with torch.inference_mode():
        out1 = unet(tensor_in).squeeze(0).cpu().permute(1, 2, 0).numpy()
        rec_fixed, mask = smart_cloud_reconstruction(in_np, out1)

    os.makedirs("outputs/test_visuals", exist_ok=True)
    Image.fromarray(rec_fixed).save("outputs/test_visuals/smart_blended_output.png")
    print(f"Smart Blended Output Shape: {rec_fixed.shape} | Min: {rec_fixed.min()} | Max: {rec_fixed.max()}")
    print("Saved outputs/test_visuals/smart_blended_output.png")

if __name__ == "__main__":
    test_smart_blend()
