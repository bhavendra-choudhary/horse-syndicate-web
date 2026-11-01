"""Download five real racehorse images from Wikimedia Commons.

Usage:
    python download_racehorse_images.py
"""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import re
from PIL import Image
from io import BytesIO

ROOT = Path(__file__).parent
IMAGE_DIR = ROOT / "images"
API = "https://commons.wikimedia.org/w/api.php"
JPG_NAMES = ["hero-racehorse.jpg", "horse-1.jpg", "horse-2.jpg", "horse-3.jpg", "story-horse.jpg"]
SEARCH_TERMS = ["Thoroughbred horse racing", "Racehorse galloping", "Thoroughbred paddock"]


def api(params):
    query = urlencode({"action": "query", "format": "json", "origin": "*", **params})
    request = Request(f"{API}?{query}", headers={"User-Agent": "MaisonThoroughbred/1.0 image downloader"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def search_images():
    pages = []
    seen = set()
    for term in SEARCH_TERMS:
        data = api({
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {term}",
            "gsrnamespace": 6,
            "gsrlimit": 20,
            "prop": "imageinfo",
            "iiprop": "url|size|mime",
            "iiurlwidth": 2200,
        })
        for page in data.get("query", {}).get("pages", {}).values():
            info = page.get("imageinfo", [{}])[0]
            url = info.get("thumburl") or info.get("url")
            if not url or url in seen or info.get("mime") not in {"image/jpeg", "image/png"}:
                continue
            seen.add(url)
            pages.append((page.get("title", "Wikimedia image"), url))
    if len(pages) < len(JPG_NAMES):
        raise RuntimeError(f"Only found {len(pages)} usable Wikimedia images")
    return pages[:len(JPG_NAMES)]


def safe_filename(name):
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")


def download():
    IMAGE_DIR.mkdir(exist_ok=True)
    selected = search_images()
    for filename, (title, url) in zip(JPG_NAMES, selected):
        request = Request(url, headers={"User-Agent": "MaisonThoroughbred/1.0 image downloader"})
        with urlopen(request, timeout=60) as response:
            data = response.read()
        image = Image.open(BytesIO(data)).convert("RGB")
        image.save(IMAGE_DIR / filename, "JPEG", quality=94, optimize=True)
        print(f"{filename}: {image.width}x{image.height} | {title} | {safe_filename(url)[:70]}")


def verify():
    for filename in JPG_NAMES:
        path = IMAGE_DIR / filename
        if not path.exists():
            raise RuntimeError(f"Missing {path}")
        with Image.open(path) as image:
            image.verify()
            if image.format != "JPEG":
                raise RuntimeError(f"{filename} is {image.format}, not JPEG")
        print(f"Verified JPEG: {path}")


if __name__ == "__main__":
    download()
    verify()
