#!/usr/bin/env python3
"""Enrichment pass: broader RERA / starting-price / USP / location extraction
for pages whose markup differs from the standard template. Only fills
fields that are empty; never overwrites scraped values, never invents."""
import json, os, re, ssl, time, urllib.request
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
ROOT = os.path.expanduser("~/workspace/atsproject-react")
DATA = os.path.join(ROOT, "projects-data.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(1.5)

def clean(t):
    return re.sub(r"\s+", " ", (t or "")).strip()

RERA_PATTERNS = [
    r"\b(UPRERA[A-Z]*[A-Z0-9/]{3,})\b",
    r"\b(HRERA[- ]?GGM[/\d][A-Z0-9/\-]{3,})\b",
    r"\b(GGM[/\d][A-Z0-9/\-]{5,})\b",
    r"\b(PBRERA[A-Z0-9/\-]{5,})\b",
    r"\b(MahaRERA[A-Z0-9/\-]{5,})\b",
    r"\b(GUJRERA[A-Z0-9/\-]{5,})\b",
    r"Registration\s*(?:No\.?|Number)\s*[-–:]\s*([A-Z0-9/\-]{8,30})",
    r"RERA\s*(?:Reg\.?\s*)?(?:No\.?|Number)\s*[-–:]\s*([A-Z0-9/\-]{8,30})",
]

d = json.load(open(DATA))
changed = {"rera": 0, "price": 0, "highlights": 0, "loc": 0}
for p in d["projects"]:
    need = (not p["rera"]) or (not p["startingPrice"]) or (not p["highlights"]) or (not p["locationAdvantages"])
    if not need:
        continue
    try:
        html = fetch(p["sourceUrl"])
    except Exception as e:
        print(p["slug"], "FETCH FAIL", str(e)[:60])
        continue
    soup = BeautifulSoup(html, "html.parser")
    full = clean(soup.get_text(" "))

    if not p["rera"]:
        for pat in RERA_PATTERNS:
            m = re.search(pat, full)
            if m:
                tok = (m.group(1) if m.lastindex else m.group(0)).strip(" .,-")
                if re.search(r"\d", tok) and len(tok) >= 8:
                    p["rera"] = tok
                    changed["rera"] += 1
                    break

    if not p["startingPrice"]:
        m = re.search(r"Starting from\s*(₹[\d.,]+\s*(?:Cr|Lakh|Lacs?|L)?\*?)", full)
        if m:
            p["startingPrice"] = m.group(1).strip()
            changed["price"] += 1

    # ✔ items in document order, classified by the nearest preceding marker
    if not p["highlights"] or not p["locationAdvantages"]:
        mode = None
        hl, loc = [], []
        for el in soup.find_all(["td", "li", "p", "div", "span"]):
            # only leaf-ish elements to avoid duplicates from parents
            if el.find(["td", "li", "p"]):
                continue
            t = clean(el.get_text(" "))
            low = t.lower()
            if "usp of the project" in low or low.startswith("usp"):
                mode = "hl"
                continue
            if "location advantage" in low:
                mode = "loc"
                continue
            if low.startswith("master plan") or low.startswith("floor plan") or low.startswith("price list"):
                mode = None
            if t.startswith("✔"):
                item = t.lstrip("✔ ").strip()
                if len(item) > 2 and len(item) < 160:
                    (hl if mode == "hl" else loc if mode == "loc" else hl).append(item)
        hl = list(dict.fromkeys(hl))[:12]
        loc = list(dict.fromkeys(loc))[:12]
        if hl and not p["highlights"]:
            p["highlights"] = hl
            changed["highlights"] += 1
        if loc and not p["locationAdvantages"]:
            p["locationAdvantages"] = loc
            changed["loc"] += 1
    print(f"{p['slug']}: rera={p['rera'] or '-'} price={p['startingPrice'] or '-'} hl={len(p['highlights'])} loc={len(p['locationAdvantages'])}", flush=True)

json.dump(d, open(DATA, "w"), indent=1, ensure_ascii=False)
ps = d["projects"]
print("\nPATCH DONE", changed)
print("totals: rera", sum(1 for p in ps if p["rera"]), "| price", sum(1 for p in ps if p["startingPrice"]),
      "| hl", sum(1 for p in ps if p["highlights"]), "| loc", sum(1 for p in ps if p["locationAdvantages"]))
