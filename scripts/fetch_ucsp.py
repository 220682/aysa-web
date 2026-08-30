import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

UNI = Path(__file__).resolve().parents[1] / "images" / "universidades"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def wiki_search_and_download(dest: str, search: str) -> bool:
    q = (
        "https://commons.wikimedia.org/w/api.php?action=query&list=search"
        f"&srsearch={urllib.parse.quote(search)}&srnamespace=6&format=json"
    )
    data = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=60))
    for hit in data.get("query", {}).get("search", [])[:5]:
        title = hit["title"].replace("File:", "")
        q2 = (
            "https://commons.wikimedia.org/w/api.php?action=query&titles=File:"
            + urllib.parse.quote(title)
            + "&prop=imageinfo&iiprop=url&format=json"
        )
        page = json.load(urllib.request.urlopen(urllib.request.Request(q2, headers=UA), timeout=60))
        for p in page["query"]["pages"].values():
            if "imageinfo" not in p:
                continue
            url = p["imageinfo"][0]["url"]
            blob = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
            if len(blob) > 800:
                (UNI / dest).write_bytes(blob)
                print("wiki OK", dest, title, len(blob))
                return True
    return False


def scrape_ucsp() -> bool:
    site = "https://www.ucsp.edu.pe/"
    html = urllib.request.urlopen(urllib.request.Request(site, headers=UA), timeout=30).read().decode(
        "utf-8", "ignore"
    )
    imgs = re.findall(r'(?:src|data-src|content)=["\']([^"\']+)["\']', html, flags=re.I)
    for img in imgs:
        low = img.lower()
        if not any(k in low for k in ("logo", "escudo", "brand", "ucsp")):
            continue
        if not any(low.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".svg")):
            continue
        if img.startswith("//"):
            img = "https:" + img
        elif img.startswith("/"):
            img = "https://www.ucsp.edu.pe" + img
        try:
            req = urllib.request.Request(img, headers={**UA, "Referer": site})
            data = urllib.request.urlopen(req, timeout=30).read()
            if len(data) < 500:
                continue
            ext = ".svg" if b"<svg" in data[:400] else ".png"
            (UNI / f"ucsp{ext}").write_bytes(data)
            print("scrape OK", img, len(data))
            return True
        except Exception as exc:
            print("try", img, exc)
    return False


if not (UNI / "ucsp.png").exists():
    for term in (
        "Universidad Católica San Pablo logo",
        "UCSP Arequipa escudo",
        "Universidad Católica San Pablo escudo",
    ):
        if wiki_search_and_download("ucsp.png", term):
            break
    else:
        scrape_ucsp()
