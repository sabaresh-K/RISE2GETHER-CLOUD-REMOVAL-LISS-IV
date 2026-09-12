import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_loc = """    with loc_col:
        st.markdown('''
    <div class="pitch-card">
    <h4 style="color:#10B981; margin-top:0;">Our Institution</h4>
    <h3 style="color:#FFFFFF; margin:0.5rem 0 0.2rem 0; font-size:1.3rem;">Sri Eshwar College of Engineering and Technology</h3>
    <p style="color:#94A3B8; font-size:0.95rem;">Coimbatore, Tamil Nadu, India</p>
            <hr style="border-color:rgba(0,212,255,0.2); margin:1rem 0;">
    <p style="font-size:0.9rem; color:#CBD5E1;"><strong>Coordinates:</strong> 10.871° N, 77.019° E</p>
    </div>
        ''', unsafe_allow_html=True)"""

new_loc = """    with loc_col:
        st.markdown('''
    <div class="pitch-card">
        <h4 style="color:#10B981; margin-top:0;">Our Institution</h4>
        <h3 style="color:#FFFFFF; margin:0.5rem 0 0.2rem 0; font-size:1.3rem;">Sri Eshwar College of Engineering and Technology</h3>
        <p style="color:#94A3B8; font-size:0.95rem;">Coimbatore, Tamil Nadu, India</p>
        
        <div style="margin-top:1rem; border-radius:8px; overflow:hidden; border:1px solid rgba(16,185,129,0.3);">
            <iframe src="https://maps.google.com/maps?q=Sri+Eshwar+College+of+Engineering+and+Technology&t=&z=14&ie=UTF8&iwloc=&output=embed" width="100%" height="280" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>
        </div>
        
        <div style="margin-top:1.2rem; text-align:center;">
            <a href="https://www.google.com/maps/search/Sri+Eshwar+College+of+Engineering+and+Technology" target="_blank" style="display:inline-block; padding:0.6rem 1.2rem; background:rgba(16,185,129,0.1); border:1px solid #10B981; color:#10B981; text-decoration:none; font-weight:bold; border-radius:5px; transition:0.3s; width:100%; box-sizing:border-box;">
                📍 Open in Google Maps
            </a>
        </div>
    </div>
        ''', unsafe_allow_html=True)"""

# In case encoding issues prevent exact string matching, we use find and replace
start_idx = text.find('with loc_col:')
end_idx = text.find('# Shared Global Footer')
if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + new_loc + '\n\n' + text[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Replaced location block successfully.")
else:
    print("Could not find the bounds.")
