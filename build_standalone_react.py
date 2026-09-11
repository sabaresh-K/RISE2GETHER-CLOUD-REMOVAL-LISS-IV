import os
import re

dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend", "dist"))
index_path = os.path.join(dist_dir, "index.html")
out_path = os.path.join(dist_dir, "index_standalone.html")

if not os.path.exists(index_path):
    print("index.html not found in frontend/dist")
    exit(1)

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace CSS link with inline <style>
def replace_css(match):
    href = match.group(1).lstrip("/")
    css_file = os.path.join(dist_dir, href)
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as cf:
            css_content = cf.read()
        return f"<style>{css_content}</style>"
    return match.group(0)

html = re.sub(r'<link\s+rel="stylesheet"[^>]*href="([^"]+)"[^>]*>', replace_css, html)

# Replace JS script tag with inline <script type="module">
def replace_js(match):
    src = match.group(1).lstrip("/")
    js_file = os.path.join(dist_dir, src)
    if os.path.exists(js_file):
        with open(js_file, "r", encoding="utf-8") as jf:
            js_content = jf.read()
        return f"<script type=\"module\">{js_content}</script>"
    return match.group(0)

html = re.sub(r'<script\s+type="module"[^>]*src="([^"]+)"[^>]*></script>', replace_js, html)

with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated standalone React HTML: {out_path} ({os.path.getsize(out_path)} bytes)")
