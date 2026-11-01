"""Render the site in Chromium and build a presentation board.

Install once with:
    python -m pip install playwright Pillow
    python -m playwright install chromium
Then run:
    python generate_showcase.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
W, H = 1920, 1400
BOARD = ROOT / "Syndicate_Website_Showcase.png"
PAGES = [
    ("index.html", "1_Landing_Page.png", "01 / LANDING"),
    ("about.html", "2_About_Upcoming_Horses.png", "02 / THE MAISON + HORSES"),
    ("contact.html", "3_Contact_Page.png", "03 / ENQUIRE"),
]
BG, CHARCOAL, GOLD, WHITE, MUTED = "#F2F0EB", "#111111", "#C5A059", "#FFFFFF", "#817D75"


def font(size, serif=False):
    candidates = [
        r"C:\Windows\Fonts\georgiab.ttf" if serif else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\georgia.ttf" if serif else r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def label(draw, xy, value, size, fill=CHARCOAL, serif=False, anchor=None):
    draw.text(xy, value, font=font(size, serif), fill=fill, anchor=anchor)


def render_pages():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        desktop = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        for filename, screenshot, _ in PAGES:
            desktop.goto((ROOT / filename).as_uri(), wait_until="domcontentloaded")
            desktop.wait_for_timeout(2500)
            desktop.screenshot(path=str(ROOT / screenshot), full_page=True)
        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        mobile.goto((ROOT / "index.html").as_uri(), wait_until="domcontentloaded")
        mobile.wait_for_timeout(2500)
        mobile.screenshot(path=str(ROOT / "Mobile_Responsive_View.png"), full_page=True)
        browser.close()


def fit_image(image, size):
    image = image.convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, WHITE)
    canvas.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return canvas


def compose_board():
    board = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(board)
    label(draw, (96, 75), "MAISON THOROUGHBRED", 17)
    label(draw, (96, 116), "A modern ownership experience.", 34, serif=True)
    label(draw, (1824, 88), "REAL BROWSER RENDERS  /  2026", 11, MUTED, anchor="ra")
    draw.line((96, 172, 1824, 172), fill="#D6D1C8", width=2)

    boxes = [(96, 240, 560, 710), (680, 240, 560, 710), (1264, 240, 560, 710)]
    for (filename, screenshot, title), (x, y, width, height) in zip(PAGES, boxes):
        draw.rounded_rectangle((x, y, x + width, y + height), 14, fill=WHITE, outline="#DEDAD1", width=2)
        draw.rectangle((x, y, x + width, y + 44), fill=CHARCOAL)
        label(draw, (x + 24, y + 22), title, 13, WHITE)
        browser_image = Image.open(ROOT / screenshot)
        preview = fit_image(browser_image, (width - 34, height - 70))
        board.paste(preview, (x + 17, y + 58))

    label(draw, (96, 1040), "OWNERSHIP, ELEVATED.", 12, GOLD)
    label(draw, (96, 1085), "Desktop clarity. Mobile intimacy.", 31, serif=True)
    mobile = fit_image(Image.open(ROOT / "Mobile_Responsive_View.png"), (270, 300))
    x, y = 1320, 1000
    draw.rounded_rectangle((x, y, x + 270, y + 300), 18, fill=CHARCOAL)
    board.paste(mobile, (x + 10, y + 10))
    label(draw, (1620, 1070), "Responsive by design", 18, serif=True)
    label(draw, (1620, 1105), "Real Playwright screenshots", 11, MUTED)
    label(draw, (1620, 1130), "Clean HTML5 / CSS3 / vanilla JS", 11, MUTED)
    draw.line((96, 1285, 1824, 1285), fill="#D6D1C8", width=2)
    label(draw, (96, 1320), "*  CURATED HORSES  /  CONSIDERED OWNERSHIP  /  RACE DAY, ELEVATED", 10, MUTED)
    board.save(BOARD, "PNG", optimize=True)


def main():
    render_pages()
    compose_board()
    print(f"Generated real page screenshots and {BOARD} ({W}x{H})")


if __name__ == "__main__":
    main()
