import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find the loc_col markdown block and un-indent the HTML lines inside it
old_block = """        st.markdown('''
    <div class="pitch-card">
        <h4 style="color:#10B981; margin-top:0;">Our Institution</h4>
        <h3 style="color:#FFFFFF; margin:0.5rem 0 0.2rem 0; font-size:1.3rem;">Sri Eshwar College of Engineering and Technology</h3>
        <p style="color:#94A3B8; font-size:0.95rem;">Coimbatore, Tamil Nadu, India</p>
        
        <div style="margin-top:1rem; border-radius:8px; overflow:hidden; border:1px solid rgba(16,185,129,0.3);">
            <iframe src="https://maps.google.com/maps?q=Sri+Eshwar+College+of+Engineering,+Coimbatore&t=&z=15&ie=UTF8&iwloc=&output=embed" width="100%" height="280" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>
        </div>
        
        <div style="margin-top:1.2rem; text-align:center;">
            <a href="https://www.google.com/maps/place/Sri+Eshwar+College+of+Engineering,+Coimbatore/" target="_blank" style="display:inline-block; padding:0.6rem 1.2rem; background:rgba(16,185,129,0.1); border:1px solid #10B981; color:#10B981; text-decoration:none; font-weight:bold; border-radius:5px; transition:0.3s; width:100%; box-sizing:border-box;">
                📍 Open in Google Maps
            </a>
        </div>
    </div>
        ''', unsafe_allow_html=True)"""

new_block = """        st.markdown('''
<div class="pitch-card">
<h4 style="color:#10B981; margin-top:0;">Our Institution</h4>
<h3 style="color:#FFFFFF; margin:0.5rem 0 0.2rem 0; font-size:1.3rem;">Sri Eshwar College of Engineering and Technology</h3>
<p style="color:#94A3B8; font-size:0.95rem;">Coimbatore, Tamil Nadu, India</p>

<div style="margin-top:1rem; border-radius:8px; overflow:hidden; border:1px solid rgba(16,185,129,0.3);">
<iframe src="https://maps.google.com/maps?q=Sri+Eshwar+College+of+Engineering,+Coimbatore&t=&z=15&ie=UTF8&iwloc=&output=embed" width="100%" height="280" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>
</div>

<div style="margin-top:1.2rem; text-align:center;">
<a href="https://www.google.com/maps/place/Sri+Eshwar+College+of+Engineering,+Coimbatore/" target="_blank" style="display:inline-block; padding:0.6rem 1.2rem; background:rgba(16,185,129,0.1); border:1px solid #10B981; color:#10B981; text-decoration:none; font-weight:bold; border-radius:5px; transition:0.3s; width:100%; box-sizing:border-box;">
📍 Open in Google Maps
</a>
</div>
</div>
''', unsafe_allow_html=True)"""

text = text.replace(old_block, new_block)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed HTML indentation")
