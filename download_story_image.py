"""Download and validate a sharp, full-colour 4K Wikimedia story image."""
from io import BytesIO
from pathlib import Path
import time

import numpy as np
import requests
from PIL import Image, ImageFilter

ROOT = Path(__file__).parent
OUTPUT = ROOT / "images" / "story-horse.jpg"
API = "https://commons.wikimedia.org/w/api.php"


def sharpness(image: Image.Image) -> float:
    gray = np.asarray(image.convert("L"), dtype=np.float32)
    laplacian = (
        -4 * gray
        + np.roll(gray, 1, 0)
        + np.roll(gray, -1, 0)
        + np.roll(gray, 1, 1)
        + np.roll(gray, -1, 1)
    )
    return float(laplacian.var())


def main() -> None:
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 VanguardThoroughbreds/1.0"
    response = session.get(
        API,
        params={
            "action": "query",
            "generator": "search",
            "gsrsearch": "thoroughbred horse racing paddock galloping",
            "gsrnamespace": 6,
            "gsrlimit": 30,
            "prop": "imageinfo",
            "iiprop": "url|size|mime",
            "iiurlwidth": 3200,
            "format": "json",
        },
        timeout=60,
    )
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {}).values()
    candidates = []
    for page in pages:
        info = page.get("imageinfo", [{}])[0]
        if info.get("mime") in {"image/jpeg", "image/jpg"} and info.get("width", 0) >= 2400:
            candidates.append(info.get("thumburl") or info.get("url"))
    candidates.extend([
        "https://upload.wikimedia.org/wikipedia/commons/8/8a/2014_Preakness_Stakes_start.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/7b/Horseracing_Churchill_Downs.jpg",
        "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c8/Horse_Racing_%283432412110%29.jpg/3840px-Horse_Racing_%283432412110%29.jpg",
    ])
    if not candidates:
        raise RuntimeError("No Wikimedia JPEG candidate at least 2400px wide was found.")

    for url in candidates:
        try:
            image_response = session.get(url, timeout=90)
            image_response.raise_for_status()
            image = Image.open(BytesIO(image_response.content)).convert("RGB")
            if image.width < 2400 or sharpness(image) < 35:
                continue
            image.save(OUTPUT, "JPEG", quality=96, subsampling=0, optimize=True, progressive=True)
            print(f"Saved {OUTPUT}: {image.size}, sharpness={sharpness(image):.1f}")
            return
        except Exception as exc:
            print(f"Skipping candidate: {exc}")
            time.sleep(1)
    raise RuntimeError("All Wikimedia candidates failed RGB, size, or sharpness validation.")


if __name__ == "__main__":
    main()
