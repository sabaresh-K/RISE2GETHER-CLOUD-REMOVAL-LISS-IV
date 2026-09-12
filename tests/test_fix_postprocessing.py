import os
import torch
from PIL import Image
import numpy as np
from src.models import CloudRemovalGenerator, SARCycleGANGenerator

def color_matched_reconstruction(in_np, out_np):
    """
    Color-matches the model output to the input satellite scene's valid radiometric profile,
    and cleanly zero-masks black nodata margins.
    """
    valid_mask = (in_np.sum(axis=-1) > 15) # Identify actual satellite swathe
    rec = np.clip((out_np + 1.0) * 127.5, 0, 255).astype(np.float32)
    
    if np.any(valid_mask):
        for c in range(3):
            in_c = in_np[:, :, c][valid_mask]
            rec_c = rec[:, :, c][valid_mask]
            if len(in_c) > 0 and len(rec_c) > 0:
                in_m, in_s = in_c.mean(), in_c.std() + 1e-6
                rec_m, rec_s = rec_c.mean(), rec_c.std() + 1e-6
                # Align mean and variance to input optical spectrum
                matched = (rec_c - rec_m) / rec_s * in_s + in_m
                rec[:, :, c][valid_mask] = np.clip(matched, 0, 255)

    # Re-apply black margin mask
    rec[~valid_mask] = 0
    return rec.astype(np.uint8)

def test_fix():
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
        rec_fixed = color_matched_reconstruction(in_np, out1)

    os.makedirs("outputs/test_visuals", exist_ok=True)
    Image.fromarray(rec_fixed).save("outputs/test_visuals/fixed_color_matched_output.png")
    print(f"Fixed Output Shape: {rec_fixed.shape} | Min: {rec_fixed.min()} | Max: {rec_fixed.max()}")
    print("Saved outputs/test_visuals/fixed_color_matched_output.png")

if __name__ == "__main__":
    test_fix()
