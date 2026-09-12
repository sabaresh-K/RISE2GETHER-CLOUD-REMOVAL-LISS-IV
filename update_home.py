import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("# PAGE 1: HOME")
end = text.find("# PAGE 2: ABOUT")

new_home_page = """# PAGE 1: HOME
# --------------------------------------------------------------------------
if selected_page == "Home":
    st.markdown('''
    <div class="pitch-card" style="text-align:center; padding:3.5rem 2rem; border-top: 4px solid #10B981;">
        <h1 style="color:#10B981; font-size:3.2rem; font-weight:900; margin:0 0 0.5rem 0; line-height:1.2;">
            🛰️ CloudClear-LISS
        </h1>
        <h3 style="color:#FFFFFF; font-size:1.8rem; font-weight:700; margin:0 0 1.5rem 0;">
            Revealing the Earth Beneath the Clouds
        </h3>
        <p style="font-size:1.2rem; color:#E2E8F0; max-width:850px; margin:0 auto 1rem auto; line-height:1.6;">
            <strong>AI-Powered Multimodal Cloud Removal & Ground Surface Reconstruction for ISRO LISS-IV Satellite Imagery</strong>
        </p>
        <p style="font-size:1rem; color:#94A3B8; margin:0;">
            <em>Developed by Team Rise2Gether | Sri Eshwar College of Engineering and Technology</em>
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### 🌐 System Overview")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown('''
        <div class="pitch-card">
            <h4 style="color:#10B981; margin-top:0;">The Obscuration Challenge</h4>
            <p style="font-size:1.05rem; color:#E2E8F0; line-height:1.6;">
                Persistent cloud cover and atmospheric shadows obscure up to <strong>30%–60% of optical satellite scenes</strong> over the Indian subcontinent, rendering high-resolution Earth observation data unusable during critical agricultural and monsoon seasons.
            </p>
            <p style="font-size:1.05rem; color:#94A3B8; line-height:1.6; margin-bottom:0;">
                <strong>CloudClear-LISS</strong> integrates high-resolution <strong>5.8 m LISS-IV optical data</strong> with all-weather, cloud-penetrating <strong>Sentinel-1 C-Band Synthetic Aperture Radar (SAR)</strong> imagery. Using a dual-encoder generative reconstruction pipeline, our system penetrates cloud obstructions to restore true surface reflectance and spatial details without geographic distortion or spectral loss.
            </p>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown('''
        <div class="pitch-card" style="text-align:center; height:100%; display:flex; flex-direction:column; justify-content:center;">
            <div style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; color:#EF4444; padding:0.8rem 1.2rem; border-radius:8px; font-weight:800; font-size:1.2rem; margin-bottom:1rem;">
                Up to 60% Cloud Obscuration
            </div>
            <p style="font-size:1rem; color:#94A3B8; margin-bottom:0;">Recovering critical spatial intelligence lost to tropical cloud cover during monsoon seasons.</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("### ⚙️ System Architecture Pipeline")
    st.markdown('''
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem; margin-bottom:2rem;">
        <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #10B981;">
            <h4 style="color:#10B981; margin-top:0;">01. Multi-Source Data Ingestion</h4>
            <p style="font-size:0.95rem; color:#94A3B8; margin-bottom:0;"><strong>Optical Input:</strong> LISS-IV 3-Band GeoTIFF (B2: Green, B3: Red, B4: NIR) at 5.8 m.<br><br><strong>Microwave Input:</strong> Sentinel-1 SAR (Dual Polarization: VV & VH backscatter channels).</p>
        </div>
        <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #F97316;">
            <h4 style="color:#F97316; margin-top:0;">02. Sub-Pixel Preprocessing & Mask Generation</h4>
            <p style="font-size:0.95rem; color:#94A3B8; margin-bottom:0;">Precise geospatial co-registration, radiometric calibration, and dynamic cloud/shadow boundary detection.</p>
        </div>
        <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #F59E0B;">
            <h4 style="color:#F59E0B; margin-top:0;">03. Dual-Branch Feature Extraction & Fusion</h4>
            <p style="font-size:0.95rem; color:#94A3B8; margin-bottom:0;">Dedicated Optical Encoder captures spectral context. Dedicated SAR Encoder extracts ground geometry and structural edges. Multimodal intermediate fusion bridges radar backscatter with optical reflectance.</p>
        </div>
        <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #3B82F6;">
            <h4 style="color:#3B82F6; margin-top:0;">04. Generative Neural Surface Reconstruction</h4>
            <p style="font-size:0.95rem; color:#94A3B8; margin-bottom:0;">U-Net-based reconstruction core restores occluded surface patches while strictly preserving authentic clear-sky pixels.</p>
        </div>
        <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #8B5CF6; grid-column: 1 / -1;">
            <h4 style="color:#8B5CF6; margin-top:0;">05. GIS-Ready Export & Validation</h4>
            <p style="font-size:0.95rem; color:#94A3B8; margin-bottom:0;">Produces full-precision, georeferenced .tif GeoTIFF rasters and True/False Color .png previews with computed PSNR, SSIM, SAM, and RMSE evaluation scores.</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("### Downstream High-Value Impact")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown('<div class="pitch-card"><h4 style="color:#10B981; margin-top:0;">Precision Agriculture</h4><p style="color:#94A3B8; margin-bottom:0;">Continuous NDVI monitoring throughout monsoon seasons without waiting gaps.</p></div>', unsafe_allow_html=True)
    with d2:
        st.markdown('<div class="pitch-card"><h4 style="color:#10B981; margin-top:0;">Emergency Flood Response</h4><p style="color:#94A3B8; margin-bottom:0;">Active radar penetrates storm clouds to delineate standing water boundaries in real time.</p></div>', unsafe_allow_html=True)
    with d3:
        st.markdown('<div class="pitch-card"><h4 style="color:#10B981; margin-top:0;">Forestry & Urban Sprawl</h4><p style="color:#94A3B8; margin-bottom:0;">Track canopy density and urban growth metrics with high spatial confidence.</p></div>', unsafe_allow_html=True)

"""

text = text[:start] + new_home_page + text[end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("Done updating Home page!")
