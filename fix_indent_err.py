import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('st.markdown("### ⚙️ System Architecture Pipeline")') or \
       line.startswith("st.markdown('''") and i > 800 and i < 860:
        lines[i] = "    " + line
    elif line.startswith("''', unsafe_allow_html=True)") and i > 800 and i < 860:
        lines[i] = "    " + line

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)
