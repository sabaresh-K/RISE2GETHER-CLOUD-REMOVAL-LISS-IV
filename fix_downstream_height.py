import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_str1 = '<div class="pitch-card" style="height: 100%; min-height: 150px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Precision Agriculture</h4>'
new_str1 = '<div class="pitch-card" style="height: 220px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Precision Agriculture</h4>'

old_str2 = '<div class="pitch-card" style="height: 100%; min-height: 150px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Emergency Flood Response</h4>'
new_str2 = '<div class="pitch-card" style="height: 220px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Emergency Flood Response</h4>'

old_str3 = '<div class="pitch-card" style="height: 100%; min-height: 150px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Forestry & Urban Sprawl</h4>'
new_str3 = '<div class="pitch-card" style="height: 220px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Forestry & Urban Sprawl</h4>'

text = text.replace(old_str1, new_str1)
text = text.replace(old_str2, new_str2)
text = text.replace(old_str3, new_str3)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Box heights synced")
