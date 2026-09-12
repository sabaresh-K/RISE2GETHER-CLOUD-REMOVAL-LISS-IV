import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace indented HTML tags with unindented ones to prevent Markdown code-block interpretation
text = text.replace("    <div", "<div")
text = text.replace("        <h1", "<h1")
text = text.replace("        <h3", "<h3")
text = text.replace("        <h4", "<h4")
text = text.replace("        <p", "<p")
text = text.replace("    </div>", "</div>")
text = text.replace("        </div>", "</div>")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("Removed markdown 4-space indentations")
