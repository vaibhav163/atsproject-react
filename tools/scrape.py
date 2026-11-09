#!/usr/bin/env python3
"""Full scrape of atsproject.in project pages -> src/data/projects-data.json + images."""
import json, os, re, ssl, sys, time, urllib.request, urllib.error
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
from PIL import Image
import io

ssl._create_default_https_context = ssl._create_unverified_context
ROOT = os.path.expanduser("~/workspace/atsproject-react")
PUB = os.path.join(ROOT, "public")
INV = json.load(open(os.path.expanduser("~/workspace/research_notes/ats-group/inventory.json")))
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

CITY_NAMES = {"noida":"Noida","greater-noida":"Greater Noida","gurugram":"Gurugram","delhi":"Delhi",
 "faridabad":"Faridabad","sohna":"Sohna","mumbai":"Mumbai","ghaziabad":"Ghaziabad","gujarat":"Gujarat",
 "shimla":"Shimla","panchkula":"Panchkula","panipat":"Panipat"}

def fetch(url, binary=False, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            data = urllib.request.urlopen(req, timeout=25).read()
            return data if binary else data.decode("utf-8", "ignore")
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(1.5)

def clean(t):
    return re.sub(r"\s+", " ", (t or "")).strip()

def save_webp(raw, dest_base, max_w=1600):
    """Save image as WebP (dest_base without ext). Returns relative path or None."""
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
        else:
            im = im.convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
        dest = dest_base + ".webp"
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im.save(dest, "WEBP", quality=78, method=4)
        return dest
    except Exception:
        return None

def save_original(raw, dest_path):
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(raw)
        return dest_path
    except Exception:
        return None

failures = []
projects = []

for item in INV:
    city, slug, page_url = item["city"], item["slug"], item["url"]
    print(f"\n=== {city}/{slug} ===", flush=True)
    try:
        html = fetch(page_url)
    except Exception as e:
        print("  PAGE FAIL", e); failures.append({"slug": slug, "what": "page", "err": str(e)})
        projects.append({"slug": slug, "city": city, "cityName": CITY_NAMES[city], "name": item["title"],
                         "partial": True, "overview": item["desc"], "images": [], "gallery": [], "plans": []})
        continue
    soup = BeautifulSoup(html, "html.parser")
    full_text = clean(soup.get_text(" "))
    about = soup.find(id="about")

    # --- name + location from h1 in #about ---
    name, location = "", ""
    h1 = about.find("h1") if about else soup.find("h1")
    if h1:
        spans = h1.find_all("span")
        if spans:
            name = clean(spans[0].get_text())
            if len(spans) > 1:
                location = clean(spans[1].get_text())
        if not name:
            name = clean(h1.get_text()).split("at ")[0].strip()
    location = re.sub(r"^at\s+", "", location)
    if not name:
        name = clean(item["title"].split("-")[0].split("|")[0])

    # --- configuration + starting price + RERA (from the 'Presents' block) ---
    config, starting_price, rera = "", "", ""
    if about:
        pres = about.find("p")
        if pres:
            strongs = [clean(s.get_text()) for s in pres.find_all(["strong", "b"])]
            ptxt = clean(pres.get_text(" "))
            m = re.search(r"Presents\s+(.+?)\s+(?:Starting from|This project|☛)", ptxt)
            if m:
                config = m.group(1).strip()
            m = re.search(r"Starting from\s*(₹[\d.,]+\s*(?:Cr|Lakh|Lacs?|L)?\*?)", ptxt)
            if m:
                starting_price = m.group(1).strip()
    m = re.search(r"Project RERA Number\s*[-–:]\s*([A-Z]{2,}RERA[A-Z0-9/]+)", full_text)
    if m:
        rera = m.group(1).strip()
    else:
        m = re.search(r"\b((?:UP|HR|PB|MH|GJ|HP)RERA[A-Z]*[A-Z0-9/]{3,})\b", full_text)
        if m:
            rera = m.group(1).strip()
    if not config:
        m = re.search(r"(\d\s*BHK(?:\s*&\s*\d\s*BHK)?(?:\s*\+\s*\w+)?)", item["title"] + " " + item["desc"])
        if m:
            config = m.group(1).strip()

    # --- USP highlights + location advantages (✔ tables) ---
    highlights, loc_adv = [], []
    for table in soup.find_all("table"):
        ttxt = clean(table.get_text(" "))
        cells = [clean(td.get_text(" ")).lstrip("✔ ").strip() for td in table.find_all("td")]
        cells = [c for c in cells if c and "✔" in clean(table.get_text(" "))]
        items = []
        for td in table.find_all("td"):
            t = clean(td.get_text(" "))
            if t.startswith("✔"):
                items.append(t.lstrip("✔ ").strip())
        if not items:
            continue
        if "Location Advantage" in ttxt:
            loc_adv.extend(items)
        elif "USP" in ttxt:
            highlights.extend(items)
    highlights = list(dict.fromkeys([h for h in highlights if len(h) > 2]))[:12]
    loc_adv = list(dict.fromkeys([h for h in loc_adv if len(h) > 2]))[:12]

    # --- overview paragraphs from #about (skip presents + tables) ---
    paras = []
    if about:
        for p in about.find_all("p"):
            t = clean(p.get_text(" "))
            if not t or "Presents" in t or "RERA Number" in t:
                continue
            if len(t) > 60:
                paras.append(t)
    overview = " ".join(paras)[:3500]
    if len(overview) < 80:
        overview = item["desc"]

    # --- amenities (ul.first li span) ---
    amenities = []
    for htag in soup.find_all(["h2", "h3"]):
        if "Amenit" in htag.get_text():
            ul = htag.find_next("ul")
            if ul:
                for li in ul.find_all("li"):
                    sp = li.find("span")
                    t = clean(sp.get_text()) if sp else clean(li.get_text())
                    if t and len(t) < 60:
                        amenities.append(t)
            break
    amenities = list(dict.fromkeys(amenities))[:24]

    # --- price table ---
    price_rows = []
    pl = soup.find(id="pricelist")
    if pl:
        tbl = pl.find("table")
        if tbl:
            for tr in tbl.find_all("tr"):
                cells = [clean(td.get_text(" ")) for td in tr.find_all(["td", "th"])]
                cells = [re.sub(r"View Unit Price", "On Request", c) for c in cells]
                if cells and any(cells):
                    price_rows.append(cells)
    price_header = price_rows[0] if price_rows else []
    price_rows = price_rows[1:] if len(price_rows) > 1 else []
    price_rows = [r for r in price_rows if any(re.search(r"\d", c) or "BHK" in c or "₹" in c for c in r)][:14]

    # --- type + status ---
    blob = (item["title"] + " " + item["desc"] + " " + config).lower()
    if "commercial" in blob or "retail shop" in blob or "office space" in blob:
        ptype = "Commercial"
    elif "plot" in blob:
        ptype = "Plots"
    else:
        ptype = "Residential"
    status = ""
    low = (item["desc"] + " " + overview).lower()
    if "ready to move" in low or "ready-to-move" in low:
        status = "Ready to Move"
    elif "upcoming" in low:
        status = "Upcoming"
    elif "new launch" in low:
        status = "New Launch"
    elif "under construction" in low:
        status = "Under Construction"

    # --- images: categorize by URL ---
    img_urls = []
    for im in soup.find_all("img"):
        src = im.get("src") or im.get("data-src") or ""
        if src:
            img_urls.append(urljoin(page_url, src))
    hero_c, gallery_c, plans_c, loc_c = [], [], [], []
    seen = set()
    for u in img_urls:
        lu = u.lower()
        if u in seen or "refresh.png" in lu or "phone" in lu or "whatsapp" in lu:
            continue
        seen.add(u)
        if "/images/projects/" in lu or "favicon" in lu:
            continue
        if "-logo" in lu or "/logo" in lu:
            continue
        if "-banner" in lu:
            hero_c.append(u)
        elif "/gallery/" in lu:
            gallery_c.append(u)
        elif "/floor-plans/" in lu or "/floorplan" in lu:
            plans_c.append(u)
        elif "location-map" in lu or "location_map" in lu:
            loc_c.append(u)
        elif re.search(r"/images/\d+\.(jpg|png|jpeg)$", lu):
            gallery_c.append(u)
    # fallback hero from city thumbnail naming: ../../images/projects/ats-....jpg handled at city level later

    dest_dir = os.path.join(PUB, "images", "projects", slug)
    downloaded = {"hero": "", "gallery": [], "plans": [], "locationMap": ""}
    def dl(url, name, max_w=1600):
        try:
            raw = fetch(url, binary=True)
            if len(raw) < 3000:
                return ""
            out = save_webp(raw, os.path.join(dest_dir, name), max_w)
            if out:
                return "/images/projects/" + slug + "/" + os.path.basename(out)
            ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
            out2 = save_original(raw, os.path.join(dest_dir, name + ext))
            return "/images/projects/" + slug + "/" + os.path.basename(out2) if out2 else ""
        except Exception as e:
            failures.append({"slug": slug, "what": "image", "url": url, "err": str(e)[:100]})
            return ""

    if hero_c:
        downloaded["hero"] = dl(hero_c[0], "hero")
    for i, u in enumerate(gallery_c[:6]):
        r = dl(u, f"gallery-{i+1}")
        if r:
            downloaded["gallery"].append(r)
    for i, u in enumerate(plans_c[:3]):
        r = dl(u, f"plan-{i+1}")
        if r:
            downloaded["plans"].append(r)
    if loc_c:
        downloaded["locationMap"] = dl(loc_c[0], "location-map")
    if not downloaded["hero"] and downloaded["gallery"]:
        downloaded["hero"] = downloaded["gallery"][0]

    partial = not (overview and (downloaded["hero"] or downloaded["gallery"]))
    projects.append({
        "slug": slug, "city": city, "cityName": CITY_NAMES[city], "name": name,
        "location": location, "type": ptype, "status": status, "config": config,
        "startingPrice": starting_price, "rera": rera, "overview": overview,
        "highlights": highlights, "amenities": amenities, "locationAdvantages": loc_adv,
        "priceHeader": price_header, "priceRows": price_rows,
        "hero": downloaded["hero"], "gallery": downloaded["gallery"], "plans": downloaded["plans"],
        "locationMap": downloaded["locationMap"],
        "metaTitle": item["title"].replace("&amp;", "&"), "metaDesc": item["desc"].replace("&amp;", "&"),
        "sourceUrl": page_url, "partial": partial,
    })
    print(f"  name={name} | rera={rera or '-'} | price={starting_price or '-'} | rows={len(price_rows)} "
          f"| hl={len(highlights)} am={len(amenities)} loc={len(loc_adv)} | hero={'Y' if downloaded['hero'] else 'N'} "
          f"gal={len(downloaded['gallery'])} plans={len(downloaded['plans'])}", flush=True)

# --- homepage sliders + city images + logo ---
print("\n=== homepage assets ===", flush=True)
home_html = fetch("https://www.atsproject.in/")
hs = BeautifulSoup(home_html, "html.parser")
home_imgs = []
for im in hs.find_all("img"):
    src = im.get("src") or ""
    if src:
        home_imgs.append(urljoin("https://www.atsproject.in/", src))
sliders = [u for u in home_imgs if "slider" in u.lower() and "mobile" not in u.lower()]
for i, u in enumerate(sorted(set(sliders))[:2]):
    try:
        raw = fetch(u, binary=True)
        out = save_webp(raw, os.path.join(PUB, "images", "home", f"slider-{i+1}"), 1920)
        print("  slider:", out, flush=True)
    except Exception as e:
        failures.append({"slug": "home", "what": "slider", "url": u, "err": str(e)[:100]})
city_imgs = [u for u in home_imgs if "/city/" in u.lower()]
for u in sorted(set(city_imgs)):
    cname = os.path.splitext(os.path.basename(urlparse(u).path))[0]  # projects-in-noida
    try:
        raw = fetch(u, binary=True)
        out = save_webp(raw, os.path.join(PUB, "images", "city", cname), 1200)
        print("  city:", out, flush=True)
    except Exception as e:
        failures.append({"slug": "home", "what": "city", "url": u, "err": str(e)[:100]})

# logo: scan home + one project page for logo-ish imgs, prefer ats.ind.in schema logo
logo_candidates = []
for u in home_imgs:
    if "logo" in u.lower():
        logo_candidates.append(u)
# ats.ind.in's ats-infra-logo.png is a fully transparent placeholder and
# its favicon is only 32px, so use the full-colour logo published in the
# footer of the official ATS Greens site (atsgreens.com).
logo_candidates += ["https://www.atsgreens.com/wp-content/uploads/2022/01/ats-logo-footer.png"]
logo_saved = ""
for u in logo_candidates:
    try:
        raw = fetch(u, binary=True)
        if len(raw) < 1500:
            continue
        ext = os.path.splitext(urlparse(u).path)[1].lower() or ".png"
        dest = os.path.join(PUB, "assets", "ats-logo" + ext)
        if save_original(raw, dest):
            logo_saved = "/assets/ats-logo" + ext
            print("  logo:", u, "->", logo_saved, flush=True)
            break
    except Exception:
        continue

out = {"projects": projects, "failures": failures, "logo": logo_saved}
with open(os.path.join(ROOT, "projects-data.json"), "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print(f"\nDONE: {len(projects)} projects, {len(failures)} failures, logo={logo_saved}")
