import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update .metric-card-box CSS
old_metric_css = """    .metric-card-box {
        background: rgba(4, 30, 22, 0.94);
        border: 1px solid rgba(16, 185, 129, 0.45);
        border-top: 3px solid #34D399;
        border-radius: 14px;
        padding: 1.35rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }"""
new_metric_css = """    .metric-card-box {
        background: rgba(4, 30, 22, 0.94);
        border: 1px solid rgba(16, 185, 129, 0.45);
        border-top: 3px solid #34D399;
        border-radius: 14px;
        padding: 1.35rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }"""

text = text.replace(old_metric_css, new_metric_css)


# 2. Update Downstream cards
old_d1 = '<div class="pitch-card"><h4 style="color:#10B981; margin-top:0;">Precision Agriculture</h4><p style="color:#94A3B8; margin-bottom:0;">Continuous NDVI monitoring throughout monsoon seasons without waiting gaps.</p></div>'
old_d2 = '<div class="pitch-card"><h4 style="color:#10B981; margin-top:0;">Emergency Flood Response</h4><p style="color:#94A3B8; margin-bottom:0;">Active radar penetrates storm clouds to delineate standing water boundaries in real time.</p></div>'
old_d3 = '<div class="pitch-card"><h4 style="color:#10B981; margin-top:0;">Forestry & Urban Sprawl</h4><p style="color:#94A3B8; margin-bottom:0;">Track canopy density and urban growth metrics with high spatial confidence.</p></div>'

new_d1 = '<div class="pitch-card" style="height: 100%; min-height: 150px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Precision Agriculture</h4><p style="color:#94A3B8; margin-bottom:0;">Continuous NDVI monitoring throughout monsoon seasons without waiting gaps.</p></div>'
new_d2 = '<div class="pitch-card" style="height: 100%; min-height: 150px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Emergency Flood Response</h4><p style="color:#94A3B8; margin-bottom:0;">Active radar penetrates storm clouds to delineate standing water boundaries in real time.</p></div>'
new_d3 = '<div class="pitch-card" style="height: 100%; min-height: 150px; display: flex; flex-direction: column; justify-content: center;"><h4 style="color:#10B981; margin-top:0;">Forestry & Urban Sprawl</h4><p style="color:#94A3B8; margin-bottom:0;">Track canopy density and urban growth metrics with high spatial confidence.</p></div>'

text = text.replace(old_d1, new_d1)
text = text.replace(old_d2, new_d2)
text = text.replace(old_d3, new_d3)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Alignment fixed")
