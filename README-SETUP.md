# Maison Thoroughbred — 2-minute setup

## 1. Put the files online

Keep all files in the same folder and upload them to your web host. Open `index.html` to check the site. No build step or database is needed. The three pages share their visual system through `styles.css`.

## 2. Change your inbox

Open `site-content.js` in any text editor. Find:

```js
email: "hello@maisonthoroughbred.com"
```

Replace the address with your inbox. The contact links and enquiry form will update automatically. FormSubmit may send a one-time confirmation email the first time you use a new address.

## 3. Swap images

In the same file, replace the URLs after `hero`, `story`, and inside `horses`. You can use image URLs from your own website or a service such as Cloudinary. For local images, upload them beside these files and use paths such as `images/hero.jpg`.

Use wide, high-quality images. The recommended ratio is 3:2 for the hero and story images, and 4:5 for horse cards.

## 4. Edit wording and horses

All visible wording is grouped in `site-content.js`: `home`, `about`, and `horses`. Change the text between quotation marks, keeping the commas and quotation marks in place. Add or remove horse objects by copying the existing format.

## 5. Preview on mobile

Open the site in a browser and resize the window, or use your browser’s device toolbar. The layout automatically adapts for phones and tablets.

## 6. Rebuild the presentation screenshots

The supplied `generate_showcase.py` uses Playwright and a headless Chromium browser to capture real rendered pages. To run it on a new computer:

```text
python -m pip install playwright Pillow
python -m playwright install chromium
python generate_showcase.py
```

It creates `1_Landing_Page.png`, `2_About_Upcoming_Horses.png`, `3_Contact_Page.png`, `Mobile_Responsive_View.png`, and the 1920×1400 `Syndicate_Website_Showcase.png`.

### Form fallback

The form first uses FormSubmit and gives instant validation feedback. If a browser blocks the request or the service is unavailable, it opens a pre-filled `mailto:` message instead.
