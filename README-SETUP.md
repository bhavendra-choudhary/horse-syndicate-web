# Vanguard Thoroughbreds — 2-minute setup

## 1. Put the files online

Keep all files in the same folder and upload them to your web host, including the `images` folder. Open `index.html` to check the site. No build step or database is needed. The three pages share their visual system through `styles.css`.

## 2. Change your inbox

Open `site-content.js` in any text editor. Find:

```js
email: "concierge@vanguardthoroughbreds.com"
```

Replace the address with your inbox. The contact links and enquiry form will update automatically. FormSubmit may send a one-time confirmation email the first time you use a new address.

## 3. Refresh the local racehorse images

The site uses five real JPEG photographs downloaded from Wikimedia Commons. To refresh them, run:

```text
python download_racehorse_images.py
```

The script searches “Thoroughbred horse racing”, “Racehorse galloping”, and “Thoroughbred paddock”, saves five files into `images`, and verifies each one as a valid JPEG.

## 4. Swap images

In `site-content.js`, replace the paths after `hero`, `story`, and inside `horses`. Keep images in the `images` folder and use paths such as `images/hero.jpg`.

Use wide, high-quality images. The recommended ratio is 3:2 for the hero and story images, and 4:5 for horse cards.

## 5. Edit wording and horses

All visible wording is grouped in `site-content.js`: `home`, `about`, and `horses`. Change the text between quotation marks, keeping the commas and quotation marks in place. Add or remove horse objects by copying the existing format.

## 6. Preview on mobile

Open the site in a browser and resize the window, or use your browser’s device toolbar. The layout automatically adapts for phones and tablets.

## 7. Rebuild the presentation screenshots

The supplied `generate_showcase.py` uses Playwright and a headless Chromium browser to capture real rendered pages. To run it on a new computer:

```text
python -m pip install playwright Pillow
python -m playwright install chromium
python generate_showcase.py
```

It creates `1_Landing_Page.png`, `2_About_Upcoming_Horses.png`, `3_Contact_Page.png`, `Mobile_Responsive_View.png`, the 1920×1400 `Syndicate_Website_Showcase.png`, and a 12-frame `Syndicate_Live_Preview.gif`. The intro plays once per browser session; use the bottom-left replay pill to preview it again.

### Form fallback

The form first uses FormSubmit and gives instant validation feedback. If a browser blocks the request or the service is unavailable, it opens a pre-filled `mailto:` message instead.
