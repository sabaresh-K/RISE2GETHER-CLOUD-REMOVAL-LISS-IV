import os
import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Home Page Updates
text = text.replace(
    '<h4 style="color:#10B981; margin-top:0; font-size:1.4rem; font-weight:900;">03. SAR-Guided CycleGAN & U-Net Core</h4>',
    '<h4 style="color:#10B981; margin-top:0; font-size:1.3rem; font-weight:900;">03. AI Core (SAR-Guided CycleGAN)</h4>'
)

text = text.replace(
    '<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Dual generators utilizing U-Net skip connections reconstruct hidden optical reflectance from SAR structural features with high fidelity.</p>',
    '<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Our generative CycleGAN leverages Sentinel-1 SAR structural guidance to reconstruct terrain beneath thick clouds. An independent Optical U-Net is utilized purely for single-scene optical mapping.</p>'
)

# About Page Updates
text = text.replace(
    '<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;"><strong>Our core innovation relies on a custom CycleGAN architecture.</strong> It fuses Sentinel-1 microwave radar backscatter (C-band) to reconstruct structural layouts under dense clouds. The generative CycleGAN core, built on a U-Net backbone with dense skip connections, directly routes high-frequency spatial details to ensure the native 5.8m resolution is flawlessly preserved through unpaired image-to-image translation.</p>',
    '<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;"><strong>Our core innovation relies on a custom CycleGAN architecture.</strong> It strictly uses Sentinel-1 microwave radar backscatter (C-band) as structural guidance to reconstruct layouts under dense clouds. Conversely, our secondary U-Net functions purely as an optical network without SAR input. The CycleGAN core ensures the native 5.8m resolution is flawlessly preserved through unpaired image-to-image translation.</p>'
)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated SAR-Guided CycleGAN separation logic across pages.")
