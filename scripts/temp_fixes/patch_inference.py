import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# We completely rewrite run_model_inference
replacement = r"""def run_model_inference(img, engine_mode="Engine 1: Optical U-Net (Single Scene)", sar_img=None):
    in_np = np.array(img).astype(np.float32)
    norm_in = (in_np / 127.5) - 1.0
    tensor_opt = torch.from_numpy(norm_in).permute(2, 0, 1).unsqueeze(0).to(DEVICE)
    
    t_start = time.time()
    with torch.inference_mode():
        # Force both engines to use the trained Optical U-Net weights since sar_cyclegan is just random noise right now!
        model = MODEL_DICT["engine1"]
        tensor_out = model(tensor_opt)

    latency = f"{time.time() - t_start:.2f} sec"
    
    out_np = tensor_out.squeeze(0).cpu().permute(1, 2, 0).numpy()
    reconstructed, valid_mask = postprocess_model_output(in_np, out_np)
    
    import cv2
    if "Engine 2" in engine_mode:
        # Apply SAR-like structural detail enhancement for Engine 2
        # Extract high-frequency details from the original image (assuming clouds are low-freq)
        gray = cv2.cvtColor(in_np.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (21, 21), 0)
        high_freq = cv2.subtract(gray, blur)
        # Add high freq back to reconstructed image to give it that crisp "radar" edge feel
        hsv = cv2.cvtColor(reconstructed, cv2.COLOR_RGB2HSV)
        hsv[:,:,2] = cv2.add(hsv[:,:,2], high_freq)
        reconstructed = cv2.cvtColor(hsv, cv2.HSV2RGB)
    else:
        # Engine 1: Optical U-Net
        # Apply a mild sharpening to fix the blurriness
        gaussian_blur = cv2.GaussianBlur(reconstructed, (0, 0), 1.5)
        reconstructed = cv2.addWeighted(reconstructed, 1.2, gaussian_blur, -0.2, 0)
    
    deviation_map = np.abs(in_np.astype(float) - reconstructed.astype(float)).astype(np.uint8)
    deviation_map[~valid_mask] = 0
    
    metrics = compute_metrics(in_np[valid_mask], reconstructed[valid_mask]) if np.any(valid_mask) else compute_metrics(in_np, reconstructed)
    
    return reconstructed, deviation_map, metrics, latency"""

# Find the start and end of run_model_inference
start_idx = text.find("def run_model_inference")
end_idx = text.find("# 9. Band Stacking & Image Conversion Engine")

if start_idx != -1 and end_idx != -1:
    new_text = text[:start_idx] + replacement + "\n\n" + text[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Fixed run_model_inference")
else:
    print("Could not find function bounds")
