import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace c1
old_c1 = '''    with c1:
        st.markdown(\'\'\'
    <div class="pitch-card">'''

new_c1 = '''    with c1:
        st.markdown(\'\'\'
    <div class="pitch-card" style="height: 380px; display:flex; flex-direction:column; justify-content:center;">'''

# Replace c2
old_c2 = '''    with c2:
        st.markdown(\'\'\'
    <div class="pitch-card" style="text-align:center; height:100%; display:flex; flex-direction:column; justify-content:center;">
        <div style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; color:#EF4444; padding:0.8rem 1.2rem; border-radius:8px; font-weight:800; font-size:1.2rem; margin-bottom:1rem;">
                Up to 60% Cloud Obscuration
</div>
    <p style="font-size:1rem; color:#94A3B8; margin-bottom:0;">Recovering critical spatial intelligence lost to tropical cloud cover during monsoon seasons.</p>
    </div>
        \'\'\', unsafe_allow_html=True)'''

new_c2 = '''    with c2:
        st.markdown(\'\'\'
    <div class="pitch-card" style="text-align:center; height:380px; display:flex; flex-direction:column; justify-content:center;">
        <div style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; color:#EF4444; padding:0.8rem 1.2rem; border-radius:8px; font-weight:800; font-size:1.2rem; margin-bottom:1.5rem;">
                Up to 60% Cloud Obscuration
        </div>
        <p style="font-size:1rem; color:#94A3B8; margin-bottom:0.8rem; line-height:1.6;">
            Recovering critical spatial intelligence lost to tropical cloud cover during monsoon seasons.
        </p>
        <p style="font-size:0.95rem; color:#E2E8F0; margin-bottom:0; line-height:1.6;">
            By leveraging Sentinel-1 SAR radar wavelengths, we penetrate heavy rain clouds and fog, ensuring continuous 24/7 visibility for agricultural tracking and disaster management.
        </p>
    </div>
        \'\'\', unsafe_allow_html=True)'''

text = text.replace(old_c1, new_c1)
text = text.replace(old_c2, new_c2)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated System Overview heights and content")
