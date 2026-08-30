"""Download university logos and stock photos for AYSA landing."""
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "images"
UNI = ROOT / "universidades"
STOCK = ROOT / "stock"
UNI.mkdir(parents=True, exist_ok=True)
STOCK.mkdir(parents=True, exist_ok=True)

UA = "AYSA-landing-asset-fetch/1.0 (local dev; contact: aysa)"


def fetch(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())
        print("OK", dest.name, dest.stat().st_size)
        return True
    except Exception as exc:
        print("FAIL", dest.name, exc)
        return False


# Direct Wikimedia upload URLs (no API)
WIKI = {
    "utp.png": "https://upload.wikimedia.org/wikipedia/commons/2/29/Universidad_Tecnol%C3%B3gica_del_Per%C3%BA.png",
    "upn.png": "https://upload.wikimedia.org/wikipedia/commons/2/22/UPN_-_Universidad_Privada_del_Norte.png",
    "ucv.png": "https://upload.wikimedia.org/wikipedia/commons/8/8b/Isotipo_ucv.png",
    "upc.png": "https://upload.wikimedia.org/wikipedia/commons/7/7a/UPC_logo_transparente.png",
    "usil.jpg": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Usil.jpg",
    "ulima.png": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Universidad_de_Lima_logo.png",
    "usmp.png": "https://upload.wikimedia.org/wikipedia/commons/4/4e/USMP-2020.png",
    "unmsm.png": "https://upload.wikimedia.org/wikipedia/commons/3/3a/UNMSM_logo2_png.png",
    "continental.png": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Ucontinental-logotipo.png",
    "pucp.png": "https://upload.wikimedia.org/wikipedia/commons/d/dd/PUCP_logo.png",
    "cientifica.png": "https://upload.wikimedia.org/wikipedia/commons/4/4a/UCSUR.png",
    "utec.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/0f/UTEC.jpg",
    "uss.png": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Logov2sss12.png",
    "uni.png": "https://upload.wikimedia.org/wikipedia/commons/6/6a/Escudo_UNI.png",
}

# Clearbit / official domains fallback
CLEARBIT = {
    "esan.png": "https://logo.clearbit.com/esan.edu.pe",
    "urp.png": "https://logo.clearbit.com/urp.edu.pe",
}

PHOTOS = {
    "hero-1.jpg": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1920&q=85&auto=format&fit=crop",
    "hero-2.jpg": "https://images.unsplash.com/photo-1565793298595-6a879b1d9492?w=1920&q=85&auto=format&fit=crop",
    "hero-3.jpg": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=85&auto=format&fit=crop",
    "split-main.jpg": "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=1200&q=85&auto=format&fit=crop",
    "split-a.jpg": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=85&auto=format&fit=crop",
    "split-b.jpg": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&q=85&auto=format&fit=crop",
    "cta-bg.jpg": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=1920&q=85&auto=format&fit=crop",
}

for name, url in {**WIKI, **CLEARBIT}.items():
    fetch(url, UNI / name)
    time.sleep(2.5)

for name, url in PHOTOS.items():
    fetch(url, STOCK / name)
    time.sleep(1)
