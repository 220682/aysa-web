"""Descarga logos corregidos y universidades de Arequipa."""
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

UNI = Path(__file__).resolve().parents[1] / "images" / "universidades"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def wiki(title: str, dest: str) -> bool:
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
        print("wiki", dest, len(blob))
        return True
    return False


def scrape(site: str, dest: str) -> bool:
    html = urllib.request.urlopen(urllib.request.Request(site, headers=UA), timeout=30).read().decode(
        "utf-8", "ignore"
    )
    for img in re.findall(
        r'(?:src|href)=["\']([^"\']*(?:logo|Logo|escudo|brand|isotipo)[^"\']*\.(?:png|svg|jpg|webp))["\']',
        html,
        flags=re.I,
    ):
        if img.startswith("//"):
            img = "https:" + img
        elif img.startswith("/"):
            img = site.rstrip("/") + img
        if "thumb" in img and "brando" in img.lower():
            continue
        if "868-hm" in img or "person" in img.lower() or "foto" in img.lower():
            continue
        try:
            data = urllib.request.urlopen(
                urllib.request.Request(img, headers={**UA, "Referer": site}), timeout=30
            ).read()
            if len(data) < 500:
                continue
            ext = ".svg" if img.endswith(".svg") or b"<svg" in data[:300] else ".png"
            out = UNI / (Path(dest).stem + ext)
            out.write_bytes(data)
            print("scrape", out.name, img[:70], len(data))
            return True
        except Exception as exc:
            print("try", img[:60], exc)
    return False


# UTP: logo oficial (no foto del campus)
wiki("UTP-logo.svg", "utp.svg") or wiki("Universidad Tecnológica del Perú.png", "utp.png")

# URP: logo institucional
for t in (
    "Universidad Ricardo Palma logo.png",
    "Logo Universidad Ricardo Palma.png",
    "Escudo Universidad Ricardo Palma.png",
):
    if wiki(t, "urp.png"):
        break
else:
    scrape("https://www.urp.edu.pe/", "urp.png")

# USS: San Sebastián (no confundir con USMP)
for t in ("Universidad San Sebastián logo.png", "Logo USS Peru.png", "Universidad Señor de Sipán logo.png"):
    if wiki(t, "uss.png"):
        break
else:
    scrape("https://www.uss.edu.pe/", "uss.png")

# Arequipa
for dest, titles, site in (
    (
        "ucsm.png",
        ("Universidad Católica de Santa María logo.png", "Logo UCSM.png", "Escudo UCSM.png"),
        "https://www.ucsm.edu.pe/",
    ),
    (
        "ucsp.png",
        ("Universidad Católica San Pablo logo.png", "Logo UCSP Arequipa.png"),
        "https://www.ucsp.edu.pe/",
    ),
    (
        "unsa.png",
        ("Universidad Nacional de San Agustín logo.png", "Logo UNSA.png", "Escudo UNSA.png"),
        "https://www.unsa.edu.pe/",
    ),
):
    ok = False
    for t in titles:
        try:
            if wiki(t, dest):
                ok = True
                break
        except Exception as exc:
            print("wiki err", t, exc)
    if not ok:
        scrape(site, dest)

# USS San Sebastián
for t in ("Universidad San Sebastián logo.png", "Logo USS Peru.png"):
    try:
        if wiki(t, "uss.png"):
            break
    except Exception:
        pass
else:
    scrape("https://www.uss.edu.pe/", "uss.png")
