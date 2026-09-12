import os
from PIL import Image
import numpy as np
import torch
from src.models import CloudRemovalGenerator, SARCycleGANGenerator

def inspect():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    
    # 1. Load UNet Engine 1
    unet = CloudRemovalGenerator(3, 3).to(device)
    unet_ckpt = "data/generator_checkpoint.pth"
    if os.path.exists(unet_ckpt):
        unet.load_state_dict(torch.load(unet_ckpt, map_location=device))
        print("Loaded UNet checkpoint!")
    unet.eval()

    # 2. Load CycleGAN Engine 2
    gan = SARCycleGANGenerator(5, 3).to(device)
    gan_ckpt = "data/cyclegan_a2b.pth"
    if os.path.exists(gan_ckpt):
        gan.load_state_dict(torch.load(gan_ckpt, map_location=device))
        print("Loaded CycleGAN checkpoint!")
    gan.eval()

    # Test images
    test_paths = [
        "C:\\Users\\sabar\\Downloads\\0.png",
        "C:\\Users\\sabar\\Downloads\\89.png"
    ]
    
    os.makedirs("outputs/test_visuals", exist_ok=True)
    
    for path in test_paths:
        if not os.path.exists(path):
            continue
        fname = os.path.basename(path)
        img = Image.open(path).convert("RGB").resize((512, 512))
        in_np = np.array(img).astype(np.float32)
        norm_in = (in_np / 127.5) - 1.0
        tensor_in = torch.from_numpy(norm_in).permute(2, 0, 1).unsqueeze(0).to(device)
        
        with torch.inference_mode():
            # UNet
            out_unet = unet(tensor_in)
            np_unet = out_unet.squeeze(0).cpu().permute(1, 2, 0).numpy()
            img_unet = np.clip((np_unet + 1.0) * 127.5, 0, 255).astype(np.uint8)
            Image.fromarray(img_unet).save(f"outputs/test_visuals/{fname}_UNET_out.png")
            print(f"{fname} UNet Output Min: {img_unet.min()}, Max: {img_unet.max()}, Mean: {img_unet.mean():.2f}")

            # CycleGAN
            out_gan = gan(tensor_in)
            np_gan = out_gan.squeeze(0).cpu().permute(1, 2, 0).numpy()
            img_gan = np.clip((np_gan + 1.0) * 127.5, 0, 255).astype(np.uint8)
            Image.fromarray(img_gan).save(f"outputs/test_visuals/{fname}_CYCLEGAN_out.png")
            print(f"{fname} CycleGAN Output Min: {img_gan.min()}, Max: {img_gan.max()}, Mean: {img_gan.mean():.2f}")

if __name__ == "__main__":
    inspect()
