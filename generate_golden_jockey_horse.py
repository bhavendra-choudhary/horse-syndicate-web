"""Download and render a transparent metallic Muybridge gallop sequence."""
from io import BytesIO
from pathlib import Path

import numpy as np
import requests
from PIL import Image, ImageFilter, ImageSequence

ROOT = Path(__file__).parent
OUTPUT = ROOT / "images" / "golden-jockey-horse.webp"
PREVIEW = ROOT / "images" / "golden-jockey-horse.png"
SOURCE = (
    "https://upload.wikimedia.org/wikipedia/commons/7/7b/"
    "Muybridge_race_horse_~_big_transp.gif?download=1"
)
CACHE = ROOT / "images" / "muybridge-source.gif"


def gold_frame(frame: Image.Image) -> Image.Image:
    rgba = frame.convert("RGBA").resize((1200, 800), Image.Resampling.LANCZOS)
    pixels = np.asarray(rgba).copy()
    rgb = pixels[:, :, :3].astype(np.float32)
    alpha = pixels[:, :, 3]
    luminance = (rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114) / 255
    gold = np.zeros_like(rgb)
    gold[:, :, 0] = 138 + luminance * 117
    gold[:, :, 1] = 91 + luminance * 150
    gold[:, :, 2] = 20 + luminance * 156
    pixels[:, :, :3] = np.clip(gold, 0, 255).astype(np.uint8)
    pixels[:, :, 3] = alpha
    return Image.fromarray(pixels, "RGBA").filter(ImageFilter.UnsharpMask(radius=1.2, percent=135, threshold=3))


def main() -> None:
    if CACHE.exists():
        source_bytes = CACHE.read_bytes()
    else:
        response = requests.get(
            SOURCE,
            headers={"User-Agent": "Mozilla/5.0 VanguardThoroughbreds/1.0"},
            timeout=60,
        )
        response.raise_for_status()
        source_bytes = response.content
        CACHE.write_bytes(source_bytes)
    source = Image.open(BytesIO(source_bytes))
    frames = [gold_frame(frame) for frame in ImageSequence.Iterator(source)]
    if not frames:
        raise RuntimeError("The Wikimedia source did not contain any animation frames.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=110,
        loop=0,
        lossless=True,
        method=6,
    )
    frames[0].save(PREVIEW, "PNG", optimize=True)
    print(f"Saved {len(frames)} gold gallop frames to {OUTPUT}")
    print(f"Saved preview frame to {PREVIEW} ({frames[0].width}x{frames[0].height})")


if __name__ == "__main__":
    main()
