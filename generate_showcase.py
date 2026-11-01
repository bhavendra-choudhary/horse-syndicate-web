"""Render the site in Chromium and build a presentation board.

Install once with:
    python -m pip install playwright Pillow
    python -m playwright install chromium
Then run:
    python generate_showcase.py
"""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
W, H = 1920, 1400
BOARD = ROOT / "Syndicate_Website_Showcase.png"
GIF = ROOT / "Syndicate_Live_Preview.gif"
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
            desktop.goto((ROOT / filename).as_uri(), wait_until="commit")
            try:
                desktop.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            desktop.wait_for_timeout(3000 if filename == "index.html" else 1500)
            height = desktop.evaluate("document.body.scrollHeight")
            for position in range(0, height, 900):
                desktop.evaluate("(y) => window.scrollTo(0, y)", position)
                desktop.wait_for_timeout(180)
            desktop.evaluate("window.scrollTo(0, 0)")
            desktop.wait_for_timeout(400)
            desktop.screenshot(path=str(ROOT / screenshot), full_page=True)
            if filename == "about.html":
                desktop.locator(".horses").screenshot(path=str(ROOT / "About_Upcoming_Horses_Grid.png"))
        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        mobile.goto((ROOT / "index.html").as_uri(), wait_until="commit")
        try:
            mobile.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        mobile.wait_for_timeout(3000)
        height = mobile.evaluate("document.body.scrollHeight")
        for position in range(0, height, 700):
            mobile.evaluate("(y) => window.scrollTo(0, y)", position)
            mobile.wait_for_timeout(160)
        mobile.evaluate("window.scrollTo(0, 0)")
        mobile.wait_for_timeout(300)
        mobile.screenshot(path=str(ROOT / "Mobile_Responsive_View.png"), full_page=True)
        capture_live_preview(browser)
        browser.close()


def viewport_frame(page):
    return Image.open(BytesIO(page.screenshot(type="png"))).convert("RGB")


def capture_live_preview(browser):
    """Capture a compact, real-browser sequence for the contest preview GIF."""
    page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
    page.goto((ROOT / "index.html").as_uri(), wait_until="commit")
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    frames = []
    for delay in (250, 750, 1250):
        page.wait_for_timeout(delay if not frames else delay - (250 if len(frames) == 1 else 750))
        frames.append(viewport_frame(page))
    page.wait_for_timeout(1500)
    page.evaluate("window.scrollTo(0, 0)")
    frames.append(viewport_frame(page))
    page.evaluate("window.scrollTo(0, document.querySelector('#command-dashboard')?.offsetTop || 900)")
    page.wait_for_timeout(500)
    frames.append(viewport_frame(page))
    page.evaluate("window.scrollTo(0, document.querySelector('#command-dashboard')?.offsetTop || 900)")
    page.wait_for_timeout(900)
    frames.append(viewport_frame(page))

    for filename, selector in (("about.html", ".horses"), ("about.html", "[data-horse-grid]"), ("about.html", "[data-horse-grid]")):
        page.goto((ROOT / filename).as_uri(), wait_until="commit")
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        if selector != ".horses":
            page.evaluate("(selector) => window.scrollTo(0, document.querySelector(selector)?.offsetTop || 700)", selector)
            page.wait_for_timeout(400)
        frames.append(viewport_frame(page))

    page.goto((ROOT / "contact.html").as_uri(), wait_until="commit")
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(1500)
    frames.append(viewport_frame(page))
    page.evaluate("window.scrollTo(0, document.querySelector('.contact-layout')?.offsetTop || 600)")
    page.wait_for_timeout(450)
    frames.append(viewport_frame(page))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(450)
    frames.append(viewport_frame(page))
    page.close()

    prepared = []
    for index, frame in enumerate(frames[:12]):
        frame.thumbnail((1280, 800), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (1280, 800), "#0A0B0E")
        canvas.paste(frame, ((1280 - frame.width) // 2, (800 - frame.height) // 2))
        ImageDraw.Draw(canvas).point((index, 0), fill="#D4AF37")
        prepared.append(canvas.quantize(colors=128, method=Image.Quantize.MEDIANCUT))
    prepared[0].save(
        GIF,
        save_all=True,
        append_images=prepared[1:],
        duration=850,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"Generated {GIF} ({GIF.stat().st_size / 1024 / 1024:.2f} MB)")


def fit_image(image, size):
    image = image.convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, WHITE)
    canvas.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return canvas


def compose_board():
    board = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(board)
    label(draw, (96, 75), "VANGUARD THOROUGHBREDS", 17)
    label(draw, (96, 116), "Direct access to classic glory.", 34, serif=True)
    label(draw, (1824, 88), "REAL BROWSER RENDERS  /  2026", 11, MUTED, anchor="ra")
    draw.line((96, 172, 1824, 172), fill="#D6D1C8", width=2)

    boxes = [(96, 220, 560, 650), (680, 220, 560, 650), (1264, 220, 560, 650)]
    showcase_images = [
        ROOT / "1_Landing_Page.png",
        ROOT / "About_Upcoming_Horses_Grid.png",
        ROOT / "3_Contact_Page.png",
    ]
    for (filename, screenshot, title), showcase_image, (x, y, width, height) in zip(PAGES, showcase_images, boxes):
        draw.rounded_rectangle((x, y, x + width, y + height), 14, fill=WHITE, outline="#DEDAD1", width=2)
        draw.rectangle((x, y, x + width, y + 44), fill=CHARCOAL)
        label(draw, (x + 24, y + 22), title, 13, WHITE)
        browser_image = Image.open(showcase_image)
        if showcase_image.name == "1_Landing_Page.png":
            browser_image = browser_image.crop((0, 0, min(browser_image.width, 1440), min(browser_image.height, 1100)))
        elif showcase_image.name == "3_Contact_Page.png":
            browser_image = browser_image.crop((0, 0, min(browser_image.width, 1440), min(browser_image.height, 1100)))
        preview = fit_image(browser_image, (width - 34, height - 70))
        board.paste(preview, (x + 17, y + 58))

    label(draw, (96, 1010), "OWNERSHIP, ELEVATED.", 12, GOLD)
    label(draw, (96, 1055), "Desktop clarity. Mobile intimacy.", 31, serif=True)
    mobile = fit_image(Image.open(ROOT / "Mobile_Responsive_View.png").crop((0, 0, 390, min(1800, Image.open(ROOT / "Mobile_Responsive_View.png").height))), (300, 330))
    x, y = 1250, 990
    draw.rounded_rectangle((x, y, x + 300, y + 350), 18, fill=CHARCOAL)
    board.paste(mobile, (x + 10, y + 10))
    label(draw, (1600, 1060), "Responsive by design", 18, serif=True)
    label(draw, (1600, 1095), "Large editorial crops", 11, MUTED)
    label(draw, (1600, 1120), "Real Playwright renders", 11, MUTED)
    draw.line((96, 1285, 1824, 1285), fill="#D6D1C8", width=2)
    label(draw, (96, 1320), "*  CURATED BLOODSTOCK  /  CLEAR ECONOMICS  /  CLASSIC GLORY", 10, MUTED)
    board.save(BOARD, "PNG", optimize=True)


def main():
    render_pages()
    compose_board()
    print(f"Generated real page screenshots and {BOARD} ({W}x{H})")


if __name__ == "__main__":
    main()
