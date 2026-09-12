import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('st.markdown("### ⚙️ System Architecture Pipeline")')
end = text.find('st.markdown("### Downstream High-Value Impact")')

new_pipeline = """st.markdown("### ⚙️ System Architecture Pipeline")
st.markdown('''
<div style="display:flex; flex-direction:column; align-items:center; gap: 1rem; margin-bottom:2rem; width:100%;">

<div class="pitch-card" style="width:100%; max-width:800px; margin-bottom:0; border-left: 4px solid #10B981; padding:1.5rem;">
<h4 style="color:#10B981; margin-top:0; font-size:1.2rem;">01. Data Ingestion</h4>
<p style="font-size:1rem; color:#94A3B8; margin-bottom:0;"><strong>Optical Input:</strong> LISS-IV 3-Band GeoTIFF (B2: Green, B3: Red, B4: NIR) at 5.8 m.<br><br><strong>Microwave Input:</strong> Sentinel-1 SAR (Dual Polarization: VV & VH backscatter channels).</p>
</div>

<div style="color:#10B981; font-size:2.5rem; font-weight:900;">⬇</div>

<div class="pitch-card" style="width:100%; max-width:800px; margin-bottom:0; border-left: 4px solid #F97316; padding:1.5rem;">
<h4 style="color:#F97316; margin-top:0; font-size:1.2rem;">02. Sub-Pixel Preprocessing & Mask Generation</h4>
<p style="font-size:1rem; color:#94A3B8; margin-bottom:0;">Precise geospatial co-registration, radiometric calibration, and dynamic cloud/shadow boundary detection.</p>
</div>

<div style="color:#F97316; font-size:2.5rem; font-weight:900;">⬇</div>

<div class="pitch-card" style="width:100%; max-width:800px; margin-bottom:0; border-left: 4px solid #F59E0B; padding:1.5rem;">
<h4 style="color:#F59E0B; margin-top:0; font-size:1.2rem;">03. Dual-Branch Feature Extraction & Fusion</h4>
<p style="font-size:1rem; color:#94A3B8; margin-bottom:0;">Dedicated Optical Encoder captures spectral context. Dedicated SAR Encoder extracts ground geometry and structural edges. Multimodal intermediate fusion bridges radar backscatter with optical reflectance.</p>
</div>

<div style="color:#F59E0B; font-size:2.5rem; font-weight:900;">⬇</div>

<div class="pitch-card" style="width:100%; max-width:800px; margin-bottom:0; border-left: 4px solid #3B82F6; padding:1.5rem;">
<h4 style="color:#3B82F6; margin-top:0; font-size:1.2rem;">04. Generative Neural Surface Reconstruction</h4>
<p style="font-size:1rem; color:#94A3B8; margin-bottom:0;">U-Net-based reconstruction core restores occluded surface patches while strictly preserving authentic clear-sky pixels.</p>
</div>

<div style="color:#3B82F6; font-size:2.5rem; font-weight:900;">⬇</div>

<div class="pitch-card" style="width:100%; max-width:800px; margin-bottom:0; border-left: 4px solid #8B5CF6; padding:1.5rem;">
<h4 style="color:#8B5CF6; margin-top:0; font-size:1.2rem;">05. GIS-Ready Export & Validation</h4>
<p style="font-size:1rem; color:#94A3B8; margin-bottom:0;">Produces full-precision, georeferenced .tif GeoTIFF rasters and True/False Color .png previews with computed PSNR, SSIM, SAM, and RMSE evaluation scores.</p>
</div>

</div>
''', unsafe_allow_html=True)

"""

text = text[:start] + new_pipeline + text[end:]
with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed Markdown Code block issue and switched to vertical layout")
