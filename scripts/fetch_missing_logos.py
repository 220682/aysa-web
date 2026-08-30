import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

UNI = Path(__file__).resolve().parents[1] / "images" / "universidades"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def wiki_download(dest: str, title: str) -> bool:
    q = (
        "https://commons.wikimedia.org/w/api.php?action=query&titles=File:"
        + urllib.parse.quote(title)
        + "&prop=imageinfo&iiprop=url&format=json"
    )
    data = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=60))
    for page in data["query"]["pages"].values():
        if "imageinfo" not in page:
            continue
        url = page["imageinfo"][0]["url"]
        blob = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
        (UNI / dest).write_bytes(blob)
        print("wiki OK", dest, len(blob))
        return True
    return False


def scrape_logo(site: str, name: str) -> bool:
    html = urllib.request.urlopen(urllib.request.Request(site, headers=UA), timeout=30).read().decode(
        "utf-8", "ignore"
    )
    pattern = r'(?:src|href)=["\']([^"\']*(?:logo|Logo|escudo|brand)[^"\']*\.(?:png|svg|jpg|webp))["\']'
    for img in re.findall(pattern, html, flags=re.I):
        if img.startswith("//"):
            img = "https:" + img
        elif img.startswith("/"):
            img = site.rstrip("/") + img
        try:
            req = urllib.request.Request(img, headers={**UA, "Referer": site})
            data = urllib.request.urlopen(req, timeout=30).read()
            if len(data) < 400:
                continue
            ext = ".svg" if img.endswith(".svg") or b"<svg" in data[:300] else ".png"
            (UNI / f"{name}{ext}").write_bytes(data)
            print("scrape OK", name, img, len(data))
            return True
        except Exception as exc:
            print("scrape try", img, exc)
    return False


if not (UNI / "urp.png").exists():
    for title in (
        "Universidad Ricardo Palma logo.png",
        "Logo Universidad Ricardo Palma.png",
        "Escudo Universidad Ricardo Palma.png",
    ):
        if wiki_download("urp.png", title):
            break
    else:
        scrape_logo("https://www.urp.edu.pe/", "urp")

if not (UNI / "esan.png").exists():
    scrape_logo("https://www.esan.edu.pe/", "esan")
