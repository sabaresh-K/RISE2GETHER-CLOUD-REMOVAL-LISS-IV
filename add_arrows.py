import os
import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the System Architecture section to include arrows
arch_pattern = r'(<h2 style="color:#ffffff; margin-top:0\.8rem;">System Architecture</h2>\n<div style="display:flex; flex-direction:column; gap:1rem; margin-top:1\.5rem;">\n<div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #3B82F6; padding:1\.5rem;">\n<h4 style="color:#3B82F6; margin-top:0; font-size:1\.1rem;">01\. Data Acquisition</h4>\n<p style="color:#94A3B8; font-size:0\.95rem; margin-bottom:0;"><strong>LISS-IV Input:</strong> 5\.8m spatial resolution optical bands \(G, R, NIR\)\. Crucial for land analysis but obscured by clouds\.<br>\n<strong>Sentinel-1 SAR Input:</strong> C-band microwave radar \(VV/VH dual-pol\) data penetrating clouds to record surface roughness and physical layouts\.</p>\n</div>\n)<div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #06B6D4; padding:1\.5rem;">\n<h4 style="color:#06B6D4; margin-top:0; font-size:1\.1rem;">02\. Preprocessing</h4>\n<p style="color:#94A3B8; font-size:0\.95rem; margin-bottom:0;">Geo-alignment, co-registration, radiometric normalization, and cloud/shadow mask extraction\.</p>\n</div>\n<div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #10B981; padding:1\.5rem;">\n<h4 style="color:#10B981; margin-top:0; font-size:1\.4rem; font-weight:900;">03\. SAR-Guided CycleGAN & U-Net Core</h4>\n<p style="color:#94A3B8; font-size:0\.95rem; margin-bottom:0;">Dual generators utilizing U-Net skip connections reconstruct hidden optical reflectance from SAR structural features with high fidelity\.</p>\n</div>\n<div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #8B5CF6; padding:1\.5rem;">\n<h4 style="color:#8B5CF6; margin-top:0; font-size:1\.1rem;">04\. Output Layer</h4>\n<p style="color:#94A3B8; font-size:0\.95rem; margin-bottom:0;">Assembles clean patches back into WGS84 coordinates\. Runs validation metrics \(PSNR, SSIM, SAM, RMSE\) for GIS mapping\.</p>\n</div>'

arch_replacement = r"""\1<div style="color:#06B6D4; font-size:2rem; font-weight:900; text-align:center;">⬇</div>
<div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #06B6D4; padding:1.5rem;">
<h4 style="color:#06B6D4; margin-top:0; font-size:1.1rem;">02. Preprocessing</h4>
<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Geo-alignment, co-registration, radiometric normalization, and cloud/shadow mask extraction.</p>
</div>
<div style="color:#10B981; font-size:2rem; font-weight:900; text-align:center;">⬇</div>
<div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #10B981; padding:1.5rem;">
<h4 style="color:#10B981; margin-top:0; font-size:1.4rem; font-weight:900;">03. SAR-Guided CycleGAN & U-Net Core</h4>
<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Dual generators utilizing U-Net skip connections reconstruct hidden optical reflectance from SAR structural features with high fidelity.</p>
</div>
<div style="color:#8B5CF6; font-size:2rem; font-weight:900; text-align:center;">⬇</div>
<div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #8B5CF6; padding:1.5rem;">
<h4 style="color:#8B5CF6; margin-top:0; font-size:1.1rem;">04. Output Layer</h4>
<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Assembles clean patches back into WGS84 coordinates. Runs validation metrics (PSNR, SSIM, SAM, RMSE) for GIS mapping.</p>
</div>"""

if re.search(arch_pattern, text):
    text = re.sub(arch_pattern, arch_replacement, text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Arrows added to System Architecture.")
else:
    print("Pattern not found. Checking current text.")
