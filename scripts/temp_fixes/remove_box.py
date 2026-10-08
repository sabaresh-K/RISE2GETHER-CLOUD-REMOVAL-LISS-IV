import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

target_line = '        st.info("Engine 1 operates on optical only. Engine 2 fuses Optical + SAR if provided, or generates radar proxies automatically.")\n'

text = text.replace(target_line, "")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Box removed successfully")
