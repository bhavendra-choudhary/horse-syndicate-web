"""Build a clean, shaded 24K-gold horse from the existing alpha silhouette."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import distance_transform_edt, gaussian_filter

ROOT = Path(__file__).parent
SOURCE = ROOT / "images" / "golden-jockey-horse.png"
OUTPUT = ROOT / "images" / "golden-jockey-horse.png"


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    scale = 4
    width, height = source.size
    alpha = np.asarray(source.getchannel("A").resize((width * scale, height * scale), Image.Resampling.LANCZOS), dtype=np.float32) / 255
    alpha = gaussian_filter(alpha, sigma=0.8)
    alpha = np.clip(alpha, 0, 1)

    interior = distance_transform_edt(alpha > 0.08)
    interior = gaussian_filter(interior, sigma=2.2)
    light = gaussian_filter(interior, sigma=9)
    light = (light - light.min()) / max(light.max() - light.min(), 1)
    dx = gaussian_filter(interior, sigma=3, order=(0, 1))
    dy = gaussian_filter(interior, sigma=3, order=(1, 0))
    normal_z = np.sqrt(np.clip(1 - (dx * 0.045) ** 2 - (dy * 0.045) ** 2, 0, 1))
    diffuse = np.clip(dx * -0.035 + dy * -0.025 + normal_z * 0.92, 0, 1)
    specular = np.clip((diffuse ** 18) * 1.2 + (light ** 10) * 0.75, 0, 1)

    shadow = np.array([92, 62, 9], dtype=np.float32)
    mid = np.array([212, 175, 55], dtype=np.float32)
    highlight = np.array([255, 246, 204], dtype=np.float32)
    t = np.clip(0.18 + diffuse[..., None] * 0.76, 0, 1)
    rgb = shadow + (mid - shadow) * t
    rgb += (highlight - rgb) * specular[..., None]

    rim = np.clip(1 - distance_transform_edt(alpha > 0.2) / 18, 0, 1) * alpha
    rgb += np.array([70, 50, 16], dtype=np.float32) * rim[..., None]
    pixels = np.dstack((np.clip(rgb, 0, 255).astype(np.uint8), (alpha * 255).astype(np.uint8)))
    result = Image.fromarray(pixels, "RGBA").resize((width, height), Image.Resampling.LANCZOS)
    result = result.filter(ImageFilter.UnsharpMask(radius=1.1, percent=115, threshold=2))
    result.save(OUTPUT, "PNG", optimize=True)
    print(f"Saved clean shaded gold silhouette: {OUTPUT} ({width}x{height})")


if __name__ == "__main__":
    main()
