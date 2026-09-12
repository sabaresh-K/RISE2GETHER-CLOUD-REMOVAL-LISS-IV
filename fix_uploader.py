
import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

fix = """
    /* Make SURE the file uploader pill is dark */
    [data-testid="stFileUploader"] section, 
    div[data-testid="stUploadedFile"],
    .stUploadedFile,
    ul[data-testid="stUploadedFileList"] > li {
        background-color: #031D15 !important;
        background: #031D15 !important;
    }
    
    [data-testid="stFileUploader"] section *,
    div[data-testid="stUploadedFile"] * {
        color: #10B981 !important;
    }
    
    #MainMenu {visibility: hidden;}
"""
text = text.replace("#MainMenu {visibility: hidden;}", fix)
with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("Done!")

