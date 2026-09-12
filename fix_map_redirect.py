import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_href = 'href="https://www.google.com/maps/place/Sri+Eshwar+College+of+Engineering,+Coimbatore/"'
new_href = 'href="https://www.google.com/maps/search/?api=1&query=Sri+Eshwar+College+of+Engineering"'

text = text.replace(old_href, new_href)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated href to precise search API")
