import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('st.markdown("### ⚙️ System Architecture Pipeline")'):
        lines[i] = "    " + line
    elif line.startswith("st.markdown('''") and 810 < i < 865:
        lines[i] = "    " + line
    elif line.startswith("''', unsafe_allow_html=True)") and 810 < i < 865:
        lines[i] = "    " + line
    elif line.startswith('st.markdown("### Downstream High-Value Impact")'):
        lines[i] = "    " + line

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)
