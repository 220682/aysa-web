import json
import urllib.parse
import urllib.request
from pathlib import Path

UNI = Path(__file__).resolve().parents[1] / "images" / "universidades"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

WIKI = {
    "ucsp.png": "Escudo de la Universidad Católica San Pablo.png",
    "unsa.png": "Escudo de la Universidad Nacional de San Agustín.png",
    "urp.png": "Logo Universidad Ricardo Palma.png",
}

for dest, title in WIKI.items():
    q = (
        "https://commons.wikimedia.org/w/api.php?action=query&titles=File:"
        + urllib.parse.quote(title)
        + "&prop=imageinfo&iiprop=url&format=json"
    )
    data = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=60))
    for page in data["query"]["pages"].values():
        if "imageinfo" not in page:
            print("missing", title)
            continue
        url = page["imageinfo"][0]["url"]
        blob = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
        (UNI / dest).write_bytes(blob)
        print("ok", dest, len(blob))

# URP fallback from institutional mail portal asset
urp_alt = "https://mail.urp.edu.pe/img/thumbnails/wm/540/hm/400/we/540/he/252/x/0/y/79/s/0/q/100/zc/3/f/0/rgb/ffffff/src/38488/n/logo-prensa-horizontal1.jpg"
if not (UNI / "urp.png").exists() or (UNI / "urp.png").stat().st_size < 2000:
    blob = urllib.request.urlopen(urllib.request.Request(urp_alt, headers=UA), timeout=60).read()
    (UNI / "urp.jpg").write_bytes(blob)
    print("ok urp.jpg", len(blob))
