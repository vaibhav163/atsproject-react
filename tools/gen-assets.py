#!/usr/bin/env python3
"""Generate favicons/app icons + OG image from the downloaded ATS logo,
and a webmanifest. Normalizes the logo to /assets/ats-logo.png."""
import io, json, os
from PIL import Image

ROOT = os.path.expanduser("~/workspace/atsproject-react")
ASSETS = os.path.join(ROOT, "public", "assets")
os.makedirs(ASSETS, exist_ok=True)

# find downloaded logo (any ext)
logo_src = None
for f in sorted(os.listdir(ASSETS)):
    if f.startswith("ats-logo."):
        logo_src = os.path.join(ASSETS, f)
        break
if not logo_src:
    raise SystemExit("logo not found in public/assets — scrape must run first")

logo = Image.open(logo_src)
logo.load()
print("logo source:", logo_src, logo.size, logo.mode)
logo_rgba = logo.convert("RGBA")
logo_rgba.save(os.path.join(ASSETS, "ats-logo.png"))
if logo_src != os.path.join(ASSETS, "ats-logo.png"):
    os.remove(logo_src)

# --- icons: logo mark padded on white rounded square ---
def icon(size, name):
    bg = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    mark = logo_rgba.copy()
    mark.thumbnail((int(size * 0.86), int(size * 0.86)), Image.LANCZOS)
    bg.alpha_composite(mark, ((size - mark.width) // 2, (size - mark.height) // 2))
    bg.convert("RGB").save(os.path.join(ASSETS, name))
    return name

icon(16, "favicon-16.png")
icon(32, "favicon-32.png")
icon(180, "apple-touch-icon.png")
icon(192, "icon-192.png")
icon(512, "icon-512.png")
# favicon.ico (multi-size)
ico_base = Image.new("RGBA", (256, 256), (255, 255, 255, 255))
mark = logo_rgba.copy()
mark.thumbnail((220, 220), Image.LANCZOS)
ico_base.alpha_composite(mark, ((256 - mark.width) // 2, (256 - mark.height) // 2))
ico_base.save(os.path.join(ASSETS, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

# --- OG image 1200x630: homepage slider (fallback: first project hero) ---
og_src = os.path.join(ROOT, "public", "images", "home", "slider-1.webp")
if not os.path.exists(og_src):
    proj_dir = os.path.join(ROOT, "public", "images", "projects")
    for slug in sorted(os.listdir(proj_dir)):
        cand = os.path.join(proj_dir, slug, "hero.webp")
        if os.path.exists(cand):
            og_src = cand
            break
im = Image.open(og_src).convert("RGB")
w, h = im.size
target = 1200 / 630
if w / h > target:
    nw = int(h * target)
    im = im.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
else:
    nh = int(w / target)
    im = im.crop((0, (h - nh) // 2, w, (h + nh) // 2))
im = im.resize((1200, 630), Image.LANCZOS)
# dark green band at bottom for legibility as a share card
band = Image.new("RGB", (1200, 110), (13, 32, 22))
im.paste(band, (0, 520))
im.save(os.path.join(ASSETS, "og-image.jpg"), quality=85)
print("og-image.jpg from", og_src)

manifest = {
    "name": "ATS Projects — Authorized Channel Partner",
    "short_name": "ATS Projects",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0d2016",
    "theme_color": "#0d2016",
    "icons": [
        {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
    ],
}
with open(os.path.join(ASSETS, "site.webmanifest"), "w") as f:
    json.dump(manifest, f, indent=2)
print("icons + manifest done:", sorted(os.listdir(ASSETS)))
