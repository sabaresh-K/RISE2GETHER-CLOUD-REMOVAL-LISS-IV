import urllib.request
import json
import os
import time

BASE_URL = "http://localhost:8000"

def test_frontend_get():
    print("[1/4] Testing Frontend SPA Root GET (/) ...")
    try:
        resp = urllib.request.urlopen(f"{BASE_URL}/")
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        content = resp.read().decode('utf-8')
        assert "<div id=\"root\">" in content, "Root div missing from index.html"
        print("  --> PASS: React SPA served successfully (Status 200).")
        return True
    except Exception as e:
        print(f"  --> FAIL: {e}")
        return False

def test_model_inference():
    print("[2/4] Testing PyTorch Model Inference (/api/process-raster) ...")
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/process-raster", method="POST")
        resp = urllib.request.urlopen(req)
        assert resp.status == 200
        data = json.loads(resp.read().decode('utf-8'))
        assert data.get("success") is True, "Inference returned failure"
        assert "reconstructed_image" in data, "Missing reconstructed image"
        metrics = data.get("metrics", {})
        print(f"  --> PASS: Model Online ({data.get('status')})")
        print(f"      Latency : {data.get('latency')}")
        print(f"      Metrics : PSNR={metrics.get('psnr')}, SSIM={metrics.get('ssim')}, RMSE={metrics.get('rmse')}, SAM={metrics.get('sam')}")
        return True
    except Exception as e:
        print(f"  --> FAIL: {e}")
        return False

def test_band_conversion():
    print("[3/4] Testing LISS-IV Multi-Band Stacking Engine (/api/convert-bands) ...")
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/convert-bands", method="POST")
        resp = urllib.request.urlopen(req)
        assert resp.status == 200
        data = json.loads(resp.read().decode('utf-8'))
        assert data.get("status") == "success", "Band conversion returned failure"
        print(f"  --> PASS: Stacking Engine Success.")
        print(f"      FCC Preview URL : {data.get('png_download_url')}")
        print(f"      GeoTIFF URL     : {data.get('tif_download_url')}")
        print(f"      Metadata        : {data.get('metadata')}")
        return True
    except Exception as e:
        print(f"  --> FAIL: {e}")
        return False

def test_contact_submission():
    print("[4/4] Testing Contact Transmission (/submit-contact) ...")
    try:
        payload = json.dumps({"name": "System Audit Test", "email": "test@rise2gether.org", "message": "Testing endpoint"}).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/submit-contact", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        resp = urllib.request.urlopen(req)
        assert resp.status == 200
        data = json.loads(resp.read().decode('utf-8'))
        assert data.get("success") is True
        print("  --> PASS: Inquiry logged successfully.")
        return True
    except Exception as e:
        print(f"  --> FAIL: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("      CLOUDCLEAR-LISS SYSTEM DIAGNOSTIC AUDIT")
    print("=" * 60)
    r1 = test_frontend_get()
    r2 = test_model_inference()
    r3 = test_band_conversion()
    r4 = test_contact_submission()
    print("=" * 60)
    if all([r1, r2, r3, r4]):
        print("RESULT: ALL 4 SYSTEM MODULES VERIFIED 100% OPERATIONAL.")
    else:
        print("RESULT: SOME CHECKS FAILED.")
    print("=" * 60)
