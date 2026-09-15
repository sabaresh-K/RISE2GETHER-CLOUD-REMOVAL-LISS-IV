import os
import re

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# We need to find all st.markdown(''' ... ''', unsafe_allow_html=True) blocks
# and remove all leading spaces from the lines inside them.
def remove_indent(match):
    content = match.group(1)
    # remove leading spaces from each line
    fixed_content = '\n'.join([line.lstrip() for line in content.split('\n')])
    return f"st.markdown('''{fixed_content}''', unsafe_allow_html=True)"

# Find st.markdown(''' content ''', unsafe_allow_html=True)
pattern = r"st\.markdown\(\'\'\'(.*?)\'\'\', unsafe_allow_html=True\)"
fixed_text = re.sub(pattern, remove_indent, text, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(fixed_text)

print("Fixed indentation for all st.markdown blocks!")
