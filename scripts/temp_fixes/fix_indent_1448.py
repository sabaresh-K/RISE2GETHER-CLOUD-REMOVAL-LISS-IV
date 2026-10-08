import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'with loc_col:' in line:
        # Find where loc_col starts and what its indent is
        lines[i] = "    with loc_col:\n"
        # Indent the next line which is st.markdown('''
        if "st.markdown('''" in lines[i+1]:
            lines[i+1] = "        st.markdown('''\n"

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)
