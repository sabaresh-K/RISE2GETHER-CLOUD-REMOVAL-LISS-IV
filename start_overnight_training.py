import os
import sys
import glob
import numpy as np
import subprocess
from pathlib import Path

print("=========================================================")
print("INIT: OVERNIGHT SAR-GUIDED CYCLEGAN TRAINING PIPELINE")
print("=========================================================")

LISS4_SOURCE_DIR = r"E:\RISE2GETHER\LISS-IV"
PROJECT_ROOT = r"c:\Users\sabar\Downloads\CLOUD REMOVAL"

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

try:
    import torch
    if torch.cuda.is_available():
        print(f"GPU DETECTED: {torch.cuda.get_device_name(0)}")
        print("BEAST MODE: ENABLED")
    else:
        print("No GPU detected! Training will be slow.")
except ImportError:
    pass

folders = [f.path for f in os.scandir(LISS4_SOURCE_DIR) if f.is_dir()]
print(f"Found {len(folders)} spatial regions for training:")
for f in folders:
    print(f"  - {os.path.basename(f)}")

print("\n[PIPELINE] Launching multi-stage preprocessing & training...")
train_script_path = os.path.join(PROJECT_ROOT, "src", "train_cyclegan.py")

cmd = [sys.executable, train_script_path]

print(f"\n>> Executing: {' '.join(cmd)}")
print(">> Training has been sent to the background overnight queue.")
print(">> Logs will be saved to training_overnight.log")
print("=========================================================")

with open("training_overnight.log", "w", encoding="utf-8") as log_file:
    process = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT)

print(f"Pipeline running with PID: {process.pid}")
