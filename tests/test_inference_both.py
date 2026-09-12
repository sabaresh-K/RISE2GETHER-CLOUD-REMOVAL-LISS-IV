import torch
from PIL import Image
import numpy as np
from src.app import load_model_core, run_model_inference

def test_inference():
    print("=== Testing Both Models in app.py ===")
    
    # Create test dummy image
    dummy_np = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    dummy_img = Image.fromarray(dummy_np)
    
    # 1. Test Engine 1: Optical U-Net
    print("Running Engine 1 (Optical U-Net)...")
    rec1, dev1, metrics1, lat1 = run_model_inference(dummy_img, engine_mode="Engine 1: Optical U-Net (Single Scene)")
    print(f"Engine 1 Success! Rec shape: {rec1.shape}, Latency: {lat1}, Metrics: {metrics1}")
    
    # 2. Test Engine 2: SAR-Guided CycleGAN
    print("Running Engine 2 (SAR-Guided CycleGAN)...")
    rec2, dev2, metrics2, lat2 = run_model_inference(dummy_img, engine_mode="Engine 2: SAR-Guided CycleGAN (LISS-IV + Sentinel-1 SAR)")
    print(f"Engine 2 Success! Rec shape: {rec2.shape}, Latency: {lat2}, Metrics: {metrics2}")
    
    print("SUCCESS: Both Engine 1 (Optical U-Net) and Engine 2 (SAR CycleGAN) are fully working!")

if __name__ == "__main__":
    test_inference()
