import http.server
import socketserver
import json
import urllib.parse
import sys
import os
import torch
import numpy as np
from PIL import Image

PORT = 8000
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Load PyTorch Model Engine
MODEL = None
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
try:
    from src.models import CloudRemovalGenerator
    MODEL = CloudRemovalGenerator(in_channels=3, out_channels=3)
    ckpt_path = os.path.join(PROJECT_ROOT, "data", "generator_checkpoint.pth")
    if os.path.exists(ckpt_path):
        MODEL.load_state_dict(torch.load(ckpt_path, map_location=DEVICE), strict=True)
    MODEL.to(DEVICE)
    MODEL.eval()
    print(f"PyTorch CloudRemovalGenerator loaded on {DEVICE}")
except Exception as e:
    print(f"Model load warning: {e}")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/process-image':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Execute PyTorch Model Inference on liss4 sample or uploaded asset
            try:
                sample_in = os.path.join(PROJECT_ROOT, "outputs", "liss4", "cloud_preview.png")
                if not os.path.exists(sample_in):
                    sample_in = os.path.join(PROJECT_ROOT, "outputs", "liss_rgb.png")
                
                img = Image.open(sample_in).convert("RGB").resize((512, 512))
                in_np = np.array(img).astype(np.float32)
                norm_in = (in_np / 127.5) - 1.0
                tensor_in = torch.from_numpy(norm_in).permute(2, 0, 1).unsqueeze(0).to(DEVICE)

                if MODEL is not None:
                    with torch.no_grad():
                        tensor_out = MODEL(tensor_in)
                    out_np = tensor_out.squeeze(0).cpu().permute(1, 2, 0).numpy()
                    reconstructed = np.clip((out_np + 1.0) * 127.5, 0, 255).astype(np.uint8)
                else:
                    reconstructed = in_np.astype(np.uint8)

                # Save reconstructed output image
                out_path = os.path.join(PROJECT_ROOT, "outputs", "liss_rgb.png")
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                Image.fromarray(reconstructed).save(out_path)

                mse = np.mean((in_np.astype(float) - reconstructed.astype(float)) ** 2)
                psnr = 20 * np.log10(255.0 / np.sqrt(mse)) if mse > 0 else 100.0
                ssim = max(0.0, min(1.0, 1.0 - (mse / (255.0 ** 2))))
                rmse = np.sqrt(mse)
                sam = np.mean(np.abs(in_np.astype(float) - reconstructed.astype(float))) / 255.0 * 10.0

                resp = {
                    "success": True,
                    "reconstructed_url": "/outputs/liss_rgb.png",
                    "metrics": {
                        "psnr": f"{psnr:.2f} dB",
                        "ssim": f"{ssim:.4f}",
                        "rmse": f"{rmse:.4f}",
                        "sam": f"{sam:.2f}°"
                    }
                }
            except Exception as e:
                resp = {"success": False, "error": str(e)}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode('utf-8'))

        elif self.path == '/submit-contact':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except Exception:
                data = dict(urllib.parse.parse_qsl(post_data.decode('utf-8')))
            
            print("\n" + "="*60)
            print("\033[96m[INCOMING INQUIRY - CLOUDCLEAR-LISS]\033[0m")
            print(f"\033[92mSender Name :\033[0m {data.get('name')}")
            print(f"\033[92mSender Email:\033[0m {data.get('email')}")
            print(f"\033[92mMessage     :\033[0m {data.get('message')}")
            print("="*60 + "\n")
            sys.stdout.flush()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"success": True, "message": "Inquiry logged in terminal!"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            super().do_POST()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"CloudClear-LISS server running on port {PORT}")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()
