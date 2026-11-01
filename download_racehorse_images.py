"""Download five real racehorse images from Wikimedia Commons.

Usage:
    python download_racehorse_images.py
"""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import re
import time
from urllib.error import HTTPError, URLError
from PIL import Image, ImageStat
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
            "gsrlimit": 50,
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
            if info.get("width", 0) < 1200 or info.get("height", 0) < 700:
                continue
            pages.append((page.get("title", "Wikimedia image"), url))
    if len(pages) < len(JPG_NAMES):
        raise RuntimeError(f"Only found {len(pages)} usable Wikimedia images")
    return pages[:len(JPG_NAMES)]


def safe_filename(name):
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")


def download():
    IMAGE_DIR.mkdir(exist_ok=True)
    selected = search_images()
    valid_existing = []
    for filename in JPG_NAMES:
        path = IMAGE_DIR / filename
        try:
            with Image.open(path) as existing:
                stat = ImageStat.Stat(existing.convert("RGB").resize((80, 80)))
                valid = existing.format == "JPEG" and existing.mode == "RGB" and path.stat().st_size > 30_000 and max(stat.mean) - min(stat.mean) >= 5
            valid_existing.append(valid)
        except (FileNotFoundError, OSError):
            valid_existing.append(False)
    downloaded = sum(valid_existing)
    if downloaded:
        print(f"Retaining {downloaded} existing validated color JPEG(s)")
    for title, url in selected:
        if downloaded == len(JPG_NAMES):
            break
        request = Request(url, headers={"User-Agent": "MaisonThoroughbred/1.0 image downloader"})
        data = None
        for attempt in range(4):
            try:
                with urlopen(request, timeout=60) as response:
                    data = response.read()
                break
            except (HTTPError, URLError):
                time.sleep(3 + attempt * 2)
        if data is None:
            continue
        image = Image.open(BytesIO(data)).convert("RGB")
        if len(data) < 30_000:
            continue
        stat = ImageStat.Stat(image.resize((80, 80)))
        channel_spread = max(stat.mean) - min(stat.mean)
        if channel_spread < 5:
            continue
        filename = next(filename for index, filename in enumerate(JPG_NAMES) if not valid_existing[index])
        image.save(IMAGE_DIR / filename, "JPEG", quality=94, optimize=True)
        print(f"{filename}: {image.width}x{image.height} | {title} | {safe_filename(url)[:70]}")
        downloaded += 1
        valid_existing[JPG_NAMES.index(filename)] = True
        time.sleep(1)
    if downloaded != len(JPG_NAMES):
        raise RuntimeError(f"Only downloaded {downloaded} vibrant JPEGs")


def verify():
    for filename in JPG_NAMES:
        path = IMAGE_DIR / filename
        if not path.exists():
            raise RuntimeError(f"Missing {path}")
        with Image.open(path) as image:
            image.verify()
            if image.format != "JPEG" or path.stat().st_size <= 30_000 or image.mode != "RGB":
                raise RuntimeError(f"{filename} is {image.format}, not JPEG")
        print(f"Verified JPEG: {path}")


if __name__ == "__main__":
    download()
    verify()
