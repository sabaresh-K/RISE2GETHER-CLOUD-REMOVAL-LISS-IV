import os
import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Enhance CycleGAN in Home Page
# Find "03. AI Core (CycleGAN & U-Net)" and make CycleGAN huge
text = text.replace(
    '<h4 style="color:#10B981; margin-top:0; font-size:1.1rem;">03. AI Core (CycleGAN & U-Net)</h4>',
    '<h4 style="color:#10B981; margin-top:0; font-size:1.4rem; font-weight:900;">03. SAR-Guided CycleGAN & U-Net Core</h4>'
)

# Enhance CycleGAN in About Page
# Find "AI-Powered Cloud Reconstruction" and add CycleGAN
text = text.replace(
    '<h2 style="color:#ffffff; margin-top:0.8rem;">AI-Powered Cloud Reconstruction</h2>',
    '<h2 style="color:#ffffff; margin-top:0.8rem;">CycleGAN-Powered Cloud Reconstruction</h2>'
)

text = text.replace(
    '<h4 style="color:#34D399; margin-top:0; font-size:1.1rem;">SAR-Guided U-Net Reconstruction</h4>',
    '<h4 style="color:#34D399; margin-top:0; font-size:1.4rem; font-weight:900;">SAR-Guided CycleGAN Reconstruction</h4>'
)

text = text.replace(
    '<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Fuses Sentinel-1 microwave radar backscatter (C-band) to reconstruct structural layouts under dense clouds. A generative U-Net core with dense skip connections directly routes high-frequency spatial details to ensure the native 5.8m resolution is flawlessly preserved.</p>',
    '<p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;"><strong>Our core innovation relies on a custom CycleGAN architecture.</strong> It fuses Sentinel-1 microwave radar backscatter (C-band) to reconstruct structural layouts under dense clouds. The generative CycleGAN core, built on a U-Net backbone with dense skip connections, directly routes high-frequency spatial details to ensure the native 5.8m resolution is flawlessly preserved through unpaired image-to-image translation.</p>'
)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Enhanced CycleGAN mentions successfully.")
