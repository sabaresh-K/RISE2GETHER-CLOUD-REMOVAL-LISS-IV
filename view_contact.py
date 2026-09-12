import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

contact_started = False
for line in lines:
    if 'selected_page == "Contact"' in line:
        contact_started = True
    if contact_started:
        print(line, end="")
