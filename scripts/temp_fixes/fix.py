
import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

fix = """
    [data-testid="stUploadedFile"] { background-color: #031D15 !important; border: 1px solid #10B981 !important; }
    [data-testid="stUploadedFile"] * { color: #10B981 !important; font-weight: 800 !important; }
    [data-testid="stUploadedFile"] button { background: transparent !important; box-shadow: none !important; border: none !important; color: #EF4444 !important; }
    #MainMenu {visibility: hidden;}
"""
text = text.replace("#MainMenu {visibility: hidden;}", fix)
with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("Done!")

