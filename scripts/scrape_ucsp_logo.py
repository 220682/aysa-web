import re
import urllib.request
from pathlib import Path

UNI = Path(__file__).resolve().parents[1] / "images" / "universidades"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
SITE = "https://www.ucsp.edu.pe/"

html = urllib.request.urlopen(urllib.request.Request(SITE, headers=UA), timeout=30).read().decode(
    "utf-8", "ignore"
)

candidates = []
for match in re.findall(r'(?:src|data-src|content|href)=["\']([^"\']+)["\']', html, flags=re.I):
    low = match.lower()
    if not any(ext in low for ext in (".png", ".jpg", ".jpeg", ".webp", ".svg")):
        continue
    if not any(k in low for k in ("logo", "escudo", "brand", "ucsp", "header", "site-logo", "custom-logo")):
        continue
    if match.startswith("//"):
        match = "https:" + match
    elif match.startswith("/"):
        match = "https://www.ucsp.edu.pe" + match
    candidates.append(match)

print("candidates", len(candidates))
for url in dict.fromkeys(candidates):
    print(url)
    try:
        data = urllib.request.urlopen(
            urllib.request.Request(url, headers={**UA, "Referer": SITE}), timeout=30
        ).read()
        if len(data) < 500:
            continue
        ext = ".svg" if b"<svg" in data[:400] else ".png"
        out = UNI / f"ucsp{ext}"
        out.write_bytes(data)
        print("saved", out.name, len(data))
        break
    except Exception as exc:
        print("fail", exc)
