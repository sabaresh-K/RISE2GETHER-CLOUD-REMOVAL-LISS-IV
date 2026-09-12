import os
import shutil
from PIL import Image
import numpy as np
from src.app import run_model_inference

def test_user_images():
    print("=== Testing Both Models on User Images 0.png and 89.png ===")
    
    # Image 1: 0.png
    p1 = "C:\\Users\\sabar\\Downloads\\0.png"
    if not os.path.exists(p1):
        p1_alt = "C:\\Users\\sabar\\Downloads\\RICE_DATASET\\RICE2\\cloud\\0.png"
        if os.path.exists(p1_alt):
            shutil.copy(p1_alt, p1)

    # Image 2: 89.png
    p2 = "C:\\Users\\sabar\\Downloads\\89.png"
    p2_src = "C:\\Users\\sabar\\Downloads\\RICE_DATASET\\RICE2\\cloud\\89.png"
    if os.path.exists(p2_src):
        shutil.copy(p2_src, p2)
        print(f"[Copied] {p2_src} -> {p2}")

    img0 = Image.open(p1).convert("RGB").resize((512, 512))
    img89 = Image.open(p2).convert("RGB").resize((512, 512))

    # --- Test Image 0.png ---
    print("\n--- Testing Image: 0.png ---")
    rec0_e1, dev0_e1, met0_e1, lat0_e1 = run_model_inference(img0, engine_mode="Engine 1: Optical U-Net (Single Scene)")
    print(f"0.png [Engine 1 U-Net]    -> Latency: {lat0_e1} | PSNR: {met0_e1[0]} | SSIM: {met0_e1[1]}")
    Image.fromarray(rec0_e1).save("c:\\Users\\sabar\\Downloads\\CLOUD REMOVAL\\outputs\\rec_0_engine1.png")

    rec0_e2, dev0_e2, met0_e2, lat0_e2 = run_model_inference(img0, engine_mode="Engine 2: SAR-Guided CycleGAN (LISS-IV + Sentinel-1 SAR)")
    print(f"0.png [Engine 2 CycleGAN] -> Latency: {lat0_e2} | PSNR: {met0_e2[0]} | SSIM: {met0_e2[1]}")
    Image.fromarray(rec0_e2).save("c:\\Users\\sabar\\Downloads\\CLOUD REMOVAL\\outputs\\rec_0_engine2.png")

    # --- Test Image 89.png ---
    print("\n--- Testing Image: 89.png ---")
    rec89_e1, dev89_e1, met89_e1, lat89_e1 = run_model_inference(img89, engine_mode="Engine 1: Optical U-Net (Single Scene)")
    print(f"89.png [Engine 1 U-Net]   -> Latency: {lat89_e1} | PSNR: {met89_e1[0]} | SSIM: {met89_e1[1]}")
    Image.fromarray(rec89_e1).save("c:\\Users\\sabar\\Downloads\\CLOUD REMOVAL\\outputs\\rec_89_engine1.png")

    rec89_e2, dev89_e2, met89_e2, lat89_e2 = run_model_inference(img89, engine_mode="Engine 2: SAR-Guided CycleGAN (LISS-IV + Sentinel-1 SAR)")
    print(f"89.png [Engine 2 CycleGAN]-> Latency: {lat89_e2} | PSNR: {met89_e2[0]} | SSIM: {met89_e2[1]}")
    Image.fromarray(rec89_e2).save("c:\\Users\\sabar\\Downloads\\CLOUD REMOVAL\\outputs\\rec_89_engine2.png")

    print("\nSUCCESS: All user image model tests completed cleanly!")

if __name__ == "__main__":
    test_user_images()
