import os
import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

pattern = r'# 5\. DOWNSTREAM IMPACT & TECH STACK\n\s+c1, c2 = st\.columns\(\[1\.5, 1\]\)\n\s+with c1:\n.*?\'\'\', unsafe_allow_html=True\)\n\s+with c2:\n.*?\'\'\', unsafe_allow_html=True\)'

replacement = r"""# 5. DOWNSTREAM IMPACT & TECH STACK
    st.markdown('''<div style="margin-bottom: 3rem;">
<span style="background:rgba(139,92,246,0.15); border:1px solid #8B5CF6; color:#8B5CF6; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Impact</span>
<h2 style="color:#ffffff; margin-top:0.8rem;">Downstream Domain Applications</h2>
<div class="pitch-card" style="padding:2rem; margin-top:1.5rem; display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:2rem;">
<div>
<h4 style="color:#8B5CF6; margin-top:0; font-size:1.2rem;">🌾 Precision Agriculture</h4>
<p style="color:#94A3B8; font-size:1rem; line-height:1.6;">Track crop health (NDVI) throughout monsoon seasons without missing growth stages.</p>
</div>
<div>
<h4 style="color:#8B5CF6; margin-top:0; font-size:1.2rem;">🌪️ Disaster Response</h4>
<p style="color:#94A3B8; font-size:1rem; line-height:1.6;">Provide situational awareness updates to rescue teams immediately after storms or landslides.</p>
</div>
<div>
<h4 style="color:#8B5CF6; margin-top:0; font-size:1.2rem;">🌲 Urban & Forest Planning</h4>
<p style="color:#94A3B8; font-size:1rem; line-height:1.6;">Monitor illegal deforestation, infrastructure growth, and reservoir levels year-round.</p>
</div>
</div>
</div>''', unsafe_allow_html=True)

    st.markdown('''<div style="margin-bottom: 3rem;">
<span style="background:rgba(16,185,129,0.15); border:1px solid #10B981; color:#10B981; padding:0.3rem 0.8rem; border-radius:20px; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Tech Stack</span>
<h2 style="color:#ffffff; margin-top:0.8rem;">Engineering Stack</h2>
<div class="pitch-card" style="padding:2rem; margin-top:1.5rem; display:flex; justify-content:space-around; align-items:center; flex-wrap:wrap; gap:2rem;">
<div style="text-align:center;">
<p style="color:#E2E8F0; font-size:1.1rem; font-weight:700; margin-bottom:0.4rem;">Deep Learning (AI/ML)</p>
<p style="color:#10B981; font-size:1rem; margin-bottom:0;">PyTorch, TorchVision, TensorBoard</p>
</div>
<div style="text-align:center;">
<p style="color:#E2E8F0; font-size:1.1rem; font-weight:700; margin-bottom:0.4rem;">Geospatial Processing</p>
<p style="color:#10B981; font-size:1rem; margin-bottom:0;">OpenCV, NumPy, Rasterio, GDAL, QGIS</p>
</div>
<div style="text-align:center;">
<p style="color:#E2E8F0; font-size:1.1rem; font-weight:700; margin-bottom:0.4rem;">Backend & Deployment</p>
<p style="color:#10B981; font-size:1rem; margin-bottom:0;">Python, FastAPI, Docker</p>
</div>
</div>
</div>''', unsafe_allow_html=True)"""

if re.search(pattern, text, flags=re.DOTALL):
    text = re.sub(pattern, replacement, text, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Stacked Downstream Impact and Tech Stack successfully.")
else:
    print("Pattern not found.")
