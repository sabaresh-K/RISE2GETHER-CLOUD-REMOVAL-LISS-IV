import os
import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the content in About page before Multi-Objective Adversarial Optimization
about_pattern = r'(elif selected_page == "About":\n).*?(    st\.markdown\("### Multi-Objective Adversarial Optimization"\))'

new_about_content = r"""\1    # 1. THE CHALLENGE SECTION
    st.markdown('''
    <div style="margin-bottom: 3rem;">
        <span style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; color:#EF4444; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">The Challenge</span>
        <h2 style="color:#ffffff; margin-top:0.8rem;">Clouds Obscuring Earth's Surface</h2>
        
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:1.5rem; margin-top:1.5rem;">
            <div class="pitch-card" style="border-top: 2px solid #EF4444 !important; padding:1.5rem;">
                <h4 style="color:#EF4444; margin-top:0;">LISS-IV Spatial Resolution</h4>
                <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">LISS-IV provides ultra-high resolution (5.8m) optical imagery essential for detailed GIS analysis.</p>
            </div>
            <div class="pitch-card" style="border-top: 2px solid #F97316 !important; padding:1.5rem;">
                <h4 style="color:#F97316; margin-top:0;">Persistent Cloud Cover</h4>
                <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">Clouds frequently obscure 30% to 60% of optical images in tropical areas, rendering them unusable.</p>
            </div>
            <div class="pitch-card" style="border-top: 2px solid #F59E0B !important; padding:1.5rem;">
                <h4 style="color:#F59E0B; margin-top:0;">Information Loss</h4>
                <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">Traditional interpolation and temporal averaging lose critical spatial boundaries and spectral characteristics.</p>
            </div>
            <div class="pitch-card" style="border-top: 2px solid #EAB308 !important; padding:1.5rem;">
                <h4 style="color:#EAB308; margin-top:0;">Need for Custom Solution</h4>
                <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">A critical gap exists for an ISRO-specific pipeline tailored to LISS-IV resolutions and spectral bands.</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 2. OUR INNOVATION SECTION
    st.markdown('''
    <div style="margin-bottom: 3rem;">
        <span style="background:rgba(16,185,129,0.15); border:1px solid #10B981; color:#10B981; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Our Innovation</span>
        <h2 style="color:#ffffff; margin-top:0.8rem;">AI-Powered Cloud Reconstruction</h2>
        
        <div style="display:flex; flex-direction:column; gap:1rem; margin-top:1.5rem;">
            <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #10B981; padding:1.5rem;">
                <h4 style="color:#10B981; margin-top:0; font-size:1.1rem;">AI Cloud Detection</h4>
                <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Deep segmentation networks accurately flag clouds, shadows, and clear ground margins.</p>
            </div>
            <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #34D399; padding:1.5rem;">
                <h4 style="color:#34D399; margin-top:0; font-size:1.1rem;">SAR-Guided U-Net Reconstruction</h4>
                <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Fuses Sentinel-1 microwave radar backscatter (C-band) to reconstruct structural layouts under dense clouds. A generative U-Net core with dense skip connections directly routes high-frequency spatial details to ensure the native 5.8m resolution is flawlessly preserved.</p>
            </div>
            <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #059669; padding:1.5rem;">
                <h4 style="color:#059669; margin-top:0; font-size:1.1rem;">LISS-IV Optimization</h4>
                <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Model explicitly trained to match LISS-IV's unique Green, Red, and Near-Infrared (NIR) band parameters.</p>
            </div>
            <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #047857; padding:1.5rem;">
                <h4 style="color:#047857; margin-top:0; font-size:1.1rem;">Production GeoTIFFs</h4>
                <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Exports standard georeferenced rasters, preserving coordinate reference systems (CRS) for QGIS and ArcGIS.</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

\2"""

text = re.sub(about_pattern, new_about_content, text, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated About Page content successfully.")
