import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

start_str = '    # Feature Capabilities & Real-Time Telemetry Grid'
end_str = '        with t_row2_c2:\n            st.markdown(f\'<div class="metric-card-box"><div class="metric-card-val">{sam}</div><div class="metric-card-lbl">SAM Spectral Angle</div></div>\', unsafe_allow_html=True)'

start_idx = text.find(start_str)
end_idx = text.find(end_str) + len(end_str)

new_code = """    # Real-Time Telemetry Grid
    st.markdown('<h4 style="color:#10B981; margin-bottom:1rem; text-align:center;">REAL-TIME TELEMETRY & EVALUATION METRICS</h4>', unsafe_allow_html=True)
    
    if 'metrics' in st.session_state and st.session_state['metrics'] is not None:
        psnr, ssim, rmse, sam = st.session_state['metrics']
    else:
        psnr, ssim, rmse, sam = "READY", "READY", "READY", "READY"

    m1, m2, m3, m4 = st.columns(4)
    
    card_style = 'height:100%; min-height:130px; display:flex; flex-direction:column; justify-content:center; align-items:center;'
    
    with m1:
        st.markdown(f'<div class="metric-card-box" style="{card_style}"><div class="metric-card-val">{psnr}</div><div class="metric-card-lbl">PSNR (Peak Signal)</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card-box" style="{card_style}"><div class="metric-card-val">{ssim}</div><div class="metric-card-lbl">SSIM Index</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card-box" style="{card_style}"><div class="metric-card-val">{rmse}</div><div class="metric-card-lbl">RMSE Error</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card-box" style="{card_style}"><div class="metric-card-val">{sam}</div><div class="metric-card-lbl">SAM Spectral Angle</div></div>', unsafe_allow_html=True)"""

text = text[:start_idx] + new_code + text[end_idx:]

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Removed system capabilities and aligned metrics perfectly.")
