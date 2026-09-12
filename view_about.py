import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('st.markdown("### Downstream High-Value Impact")')
end = text.find('# PAGE 3: FEATURES')
print(text[start:end])
