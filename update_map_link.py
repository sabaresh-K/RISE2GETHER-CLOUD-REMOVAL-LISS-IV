import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_iframe = 'src="https://maps.google.com/maps?q=Sri+Eshwar+College+of+Engineering+and+Technology&t=&z=14&ie=UTF8&iwloc=&output=embed"'
new_iframe = 'src="https://maps.google.com/maps?q=Sri+Eshwar+College+of+Engineering,+Coimbatore&t=&z=15&ie=UTF8&iwloc=&output=embed"'

old_href = 'href="https://www.google.com/maps/search/Sri+Eshwar+College+of+Engineering+and+Technology"'
new_href = 'href="https://www.google.com/maps/place/Sri+Eshwar+College+of+Engineering,+Coimbatore/"'

text = text.replace(old_iframe, new_iframe)
text = text.replace(old_href, new_href)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Map updated successfully")
