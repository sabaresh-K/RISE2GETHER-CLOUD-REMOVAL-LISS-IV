import os
import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

def remove_blank_lines(match):
    content = match.group(1)
    # remove completely empty lines or lines with just whitespace
    fixed_content = '\n'.join([line for line in content.split('\n') if line.strip() != ''])
    return f"st.markdown('''{fixed_content}''', unsafe_allow_html=True)"

pattern = r"st\.markdown\(\'\'\'(.*?)\'\'\', unsafe_allow_html=True\)"
fixed_text = re.sub(pattern, remove_blank_lines, text, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(fixed_text)

print("Removed blank lines from all st.markdown blocks!")
