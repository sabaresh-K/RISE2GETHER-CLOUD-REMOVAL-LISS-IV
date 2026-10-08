import os
import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

home_pattern = r'if selected_page == "Home":.*?elif selected_page == "About":'
home_replacement = """if selected_page == "Home":
    
    # 1. THE CHALLENGE SECTION
    st.markdown('''
    <div style="margin-bottom: 3rem;">
        <span style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; color:#EF4444; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">The Challenge</span>
        <h2 style="color:#ffffff; margin-top:0.8rem;">High-Resolution Cloud Obscuration</h2>
        <p style="color:#94A3B8; font-size:1.1rem; margin-top:0;">Why traditional optical remote sensing struggles to capture persistent ground realities.</p>
        
        <div style="display:flex; gap:1.5rem; margin-top:1.5rem;">
            <div class="pitch-card" style="flex:1; border-top: 2px solid #EF4444 !important; padding:1.5rem;">
                <h4 style="color:#EF4444; margin-top:0;">LISS-IV High Resolution</h4>
                <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">ISRO's LISS-IV sensor aboard Resourcesat provides exceptional high-resolution optical imagery at 5.8 meters, essential for monitoring micro-level changes in agriculture and land use.</p>
            </div>
            <div class="pitch-card" style="flex:1; border-top: 2px solid #F97316 !important; padding:1.5rem;">
                <h4 style="color:#F97316; margin-top:0;">Tropical Cloud Obscuration</h4>
                <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">Persistent cloud cover obscures critical scenes, rendering up to 64% of optical data unusable in tropical regions and leaving massive temporal gaps in GIS analysis.</p>
            </div>
            <div class="pitch-card" style="flex:1; border-top: 2px solid #F59E0B !important; padding:1.5rem;">
                <h4 style="color:#F59E0B; margin-top:0;">Limitations of Existing Methods</h4>
                <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">Spatial interpolation blurs ground textures, while optical temporal averages fail during rapid land events (e.g. floods). A physical deep learning model is required.</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 2. TECHNICAL PIPELINE & SYSTEM ARCHITECTURE
    st.markdown('''
    <div style="margin-bottom: 3rem;">
        <span style="background:rgba(59,130,246,0.15); border:1px solid #3B82F6; color:#3B82F6; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Technical Pipeline</span>
        <h2 style="color:#ffffff; margin-top:0.8rem;">System Architecture</h2>
        
        <div style="display:flex; flex-direction:column; gap:1rem; margin-top:1.5rem;">
            <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #3B82F6; padding:1.5rem;">
                <h4 style="color:#3B82F6; margin-top:0; font-size:1.1rem;">01. Data Acquisition</h4>
                <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;"><strong>LISS-IV Input:</strong> 5.8m spatial resolution optical bands (G, R, NIR). Crucial for land analysis but obscured by clouds.<br>
                <strong>Sentinel-1 SAR Input:</strong> C-band microwave radar (VV/VH dual-pol) data penetrating clouds to record surface roughness and physical layouts.</p>
            </div>
            <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #06B6D4; padding:1.5rem;">
                <h4 style="color:#06B6D4; margin-top:0; font-size:1.1rem;">02. Preprocessing</h4>
                <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Geo-alignment, co-registration, radiometric normalization, and cloud/shadow mask extraction.</p>
            </div>
            <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #10B981; padding:1.5rem;">
                <h4 style="color:#10B981; margin-top:0; font-size:1.1rem;">03. AI Core (CycleGAN & U-Net)</h4>
                <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Dual generators utilizing U-Net skip connections reconstruct hidden optical reflectance from SAR structural features with high fidelity.</p>
            </div>
            <div class="pitch-card" style="margin-bottom:0; border-left: 4px solid #8B5CF6; padding:1.5rem;">
                <h4 style="color:#8B5CF6; margin-top:0; font-size:1.1rem;">04. Output Layer</h4>
                <p style="color:#94A3B8; font-size:0.95rem; margin-bottom:0;">Assembles clean patches back into WGS84 coordinates. Runs validation metrics (PSNR, SSIM, SAM, RMSE) for GIS mapping.</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 3. KEY FEATURES
    st.markdown('''
    <div style="margin-bottom: 3rem;">
        <span style="background:rgba(16,185,129,0.15); border:1px solid #10B981; color:#10B981; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Engineered for Geospatial Rigor</span>
        
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:1.5rem; margin-top:1.5rem;">
            <div class="model-feature-card">
                <h4 style="color:#10B981; margin-top:0;">LISS-IV Resolution</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Maintains native 5.8m pixel spacing without introducing synthetic artifacts.</p>
            </div>
            <div class="model-feature-card">
                <h4 style="color:#10B981; margin-top:0;">Multi-Sensor Fusion</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Blends optical reflection with C-band radar backscatter for structural fidelity.</p>
            </div>
            <div class="model-feature-card">
                <h4 style="color:#10B981; margin-top:0;">CycleGAN Architecture</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Unpaired image-to-image translation guarantees structural consistency across domains.</p>
            </div>
            <div class="model-feature-card">
                <h4 style="color:#10B981; margin-top:0;">Georeferenced Output</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Retains all coordinate system metadata (UTM / WGS84) for GIS software integration.</p>
            </div>
            <div class="model-feature-card">
                <h4 style="color:#10B981; margin-top:0;">Quality Validated</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Verified via PSNR, SSIM, SAM, and RMSE relative to ground truth.</p>
            </div>
            <div class="model-feature-card">
                <h4 style="color:#10B981; margin-top:0;">GPU Accelerated</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Optimized PyTorch inference allows rapid patch-wise scene recovery in seconds.</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 4. WORKFLOW ("HOW IT WORKS")
    st.markdown('''
    <div style="margin-bottom: 3rem;">
        <span style="background:rgba(245,158,11,0.15); border:1px solid #F59E0B; color:#F59E0B; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Workflow</span>
        <h2 style="color:#ffffff; margin-top:0.8rem;">How It Works</h2>
        
        <div style="display:flex; justify-content:space-between; gap:1rem; margin-top:1.5rem; text-align:center;">
            <div class="metric-card-box" style="flex:1; height:auto; padding:1.5rem;">
                <h3 style="color:#F59E0B; margin:0;">01. Upload</h3>
                <p style="color:#94A3B8; font-size:0.9rem; margin-top:0.5rem;">Cloudy LISS-IV (optical) and Sentinel-1 (SAR) scenes.</p>
            </div>
            <div class="metric-card-box" style="flex:1; height:auto; padding:1.5rem;">
                <h3 style="color:#F59E0B; margin:0;">02. Align</h3>
                <p style="color:#94A3B8; font-size:0.9rem; margin-top:0.5rem;">Co-registration, normalization, and patch extraction (256x256 grids).</p>
            </div>
            <div class="metric-card-box" style="flex:1; height:auto; padding:1.5rem;">
                <h3 style="color:#F59E0B; margin:0;">03. Detect</h3>
                <p style="color:#94A3B8; font-size:0.9rem; margin-top:0.5rem;">Generates cloud & shadow masks using spectral signature thresholds.</p>
            </div>
            <div class="metric-card-box" style="flex:1; height:auto; padding:1.5rem;">
                <h3 style="color:#F59E0B; margin:0;">04. Reconstruct</h3>
                <p style="color:#94A3B8; font-size:0.9rem; margin-top:0.5rem;">CycleGAN core infuses SAR edge details and structural layouts into masks.</p>
            </div>
            <div class="metric-card-box" style="flex:1; height:auto; padding:1.5rem;">
                <h3 style="color:#F59E0B; margin:0;">05. Export</h3>
                <p style="color:#94A3B8; font-size:0.9rem; margin-top:0.5rem;">Assembles patches back into a georeferenced, cloud-free GeoTIFF raster.</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 5. DOWNSTREAM IMPACT & TECH STACK
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown('''
        <div style="margin-bottom: 2rem;">
            <span style="background:rgba(139,92,246,0.15); border:1px solid #8B5CF6; color:#8B5CF6; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Impact</span>
            <h2 style="color:#ffffff; margin-top:0.8rem;">Downstream Domain Applications</h2>
            
            <div class="pitch-card" style="padding:1.5rem; margin-top:1.5rem;">
                <h4 style="color:#8B5CF6; margin-top:0;">Precision Agriculture</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Track crop health (NDVI) throughout monsoon seasons without missing growth stages.</p>
                <h4 style="color:#8B5CF6; margin-top:1rem;">Disaster Response</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Provide situational awareness updates to rescue teams immediately after storms or landslides.</p>
                <h4 style="color:#8B5CF6; margin-top:1rem;">Urban & Forest Planning</h4>
                <p style="color:#94A3B8; font-size:0.95rem;">Monitor illegal deforestation, infrastructure growth, and reservoir levels year-round.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown('''
        <div style="margin-bottom: 2rem;">
            <span style="background:rgba(16,185,129,0.15); border:1px solid #10B981; color:#10B981; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Tech Stack</span>
            <h2 style="color:#ffffff; margin-top:0.8rem;">Engineering Stack</h2>
            
            <div class="pitch-card" style="padding:1.5rem; margin-top:1.5rem; text-align:center;">
                <p style="color:#E2E8F0; font-size:1rem; font-weight:700; margin-bottom:0.2rem;">Deep Learning (AI/ML)</p>
                <p style="color:#10B981; font-size:0.95rem; margin-bottom:1.5rem;">PyTorch, TorchVision, TensorBoard</p>
                
                <p style="color:#E2E8F0; font-size:1rem; font-weight:700; margin-bottom:0.2rem;">Geospatial Processing</p>
                <p style="color:#10B981; font-size:0.95rem; margin-bottom:1.5rem;">OpenCV, NumPy, Rasterio, GDAL, QGIS</p>
                
                <p style="color:#E2E8F0; font-size:1rem; font-weight:700; margin-bottom:0.2rem;">Backend & Deployment</p>
                <p style="color:#10B981; font-size:0.95rem; margin-bottom:0;">Python, FastAPI, Docker</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

elif selected_page == "About":"""
text = re.sub(home_pattern, home_replacement, text, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated Home Page with new structured content")
