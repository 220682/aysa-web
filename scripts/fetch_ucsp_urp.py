import re
import urllib.request
from pathlib import Path

UNI = Path(__file__).resolve().parents[1] / "images" / "universidades"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# URP logo institucional
urp_url = (
    "https://mail.urp.edu.pe/img/thumbnails/wm/540/hm/400/we/540/he/252/x/0/y/0/s/0/q/100/"
    "zc/3/f/0/rgb/ffffff/src/38488/n/logo-prensa-horizontal1.jpg"
)
blob = urllib.request.urlopen(urllib.request.Request(urp_url, headers=UA), timeout=60).read()
(UNI / "urp.jpg").write_bytes(blob)
print("urp.jpg", len(blob))

# UCSP: buscar logo en homepage
html = urllib.request.urlopen(
    urllib.request.Request("https://www.ucsp.edu.pe/", headers=UA), timeout=30
).read().decode("utf-8", "ignore")
for img in re.findall(r'src=["\']([^"\']+)["\']', html):
    low = img.lower()
    if not any(k in low for k in ("logo", "ucsp", "escudo", "marca")):
        continue
    if img.startswith("//"):
        img = "https:" + img
    elif img.startswith("/"):
        img = "https://www.ucsp.edu.pe" + img
    if not img.startswith("http"):
        continue
    try:
        data = urllib.request.urlopen(
            urllib.request.Request(img, headers={**UA, "Referer": "https://www.ucsp.edu.pe/"}),
            timeout=30,
        ).read()
        if len(data) < 800:
            continue
        ext = ".svg" if b"<svg" in data[:400] else ".png"
        (UNI / f"ucsp{ext}").write_bytes(data)
        print("ucsp", img, len(data))
        break
    except Exception as exc:
        print("try", img[:60], exc)
