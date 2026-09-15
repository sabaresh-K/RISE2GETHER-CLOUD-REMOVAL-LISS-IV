with open(r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "elif selected_page ==" in line and "About" in line:
        print("".join(lines[i:i+30]))
        break
