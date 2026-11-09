#!/usr/bin/env python3
"""Second enrichment: segment-based ✔ extraction (USP/Key Features and
Location Advantage text blocks) + RERA notes like 'OC Applied'.
Only fills empty fields; values are verbatim from the source pages."""
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

def segment(text, starts, ends):
    low = text.lower()
    si, sl = -1, 0
    for s in starts:
        i = low.find(s.lower())
        if i >= 0 and (si < 0 or i < si):
            si, sl = i, len(s)
    if si < 0:
        return ""
    rest = text[si + sl:]
    rlow = rest.lower()
    ei = len(rest)
    for e in ends:
        j = rlow.find(e.lower())
        if 0 <= j < ei:
            ei = j
    return rest[:ei]

def items_from(seg):
    parts = [clean(x).lstrip(":- ").strip() for x in seg.split("✔")]
    out = [x for x in parts if 3 <= len(x) <= 160 and not x.lower().startswith(("usp", "key features", "location advantage"))]
    return list(dict.fromkeys(out))[:12]

d = json.load(open(DATA))
gains = {"hl": 0, "loc": 0, "note": 0}
for p in d["projects"]:
    if p["highlights"] and p["locationAdvantages"] and p.get("reraNote"):
        continue
    if p["highlights"] and p["locationAdvantages"] and p["rera"]:
        continue
    try:
        html = fetch(p["sourceUrl"])
    except Exception as e:
        print(p["slug"], "FAIL", str(e)[:50])
        continue
    soup = BeautifulSoup(html, "html.parser")
    full = clean(soup.get_text(" "))
    if not p.get("reraNote") and not p["rera"]:
        m = re.search(r"RERA Number\s*[-–:]\s*([A-Za-z][A-Za-z ]{2,28})", full)
        if m and not re.search(r"\d{4}", m.group(1)):
            p["reraNote"] = clean(m.group(1))
            gains["note"] += 1
    if not p["highlights"]:
        seg = segment(full, ["USP of the Project", "Key Features of the Project", "Key Features"],
                      ["Location Advantage", "Master Plan", "Floor Plans", "Price List", "Amenities", "Downloads"])
        it = items_from(seg)
        if it:
            p["highlights"] = it
            gains["hl"] += 1
    if not p["locationAdvantages"]:
        seg = segment(full, ["Location Advantage", "Location Advantages"],
                      ["Master Plan", "Floor Plans", "Price List", "Amenities", "Downloads", "Gallery"])
        it = items_from(seg)
        if it:
            p["locationAdvantages"] = it
            gains["loc"] += 1
    print(f"{p['slug']}: hl={len(p['highlights'])} loc={len(p['locationAdvantages'])} note={p.get('reraNote','')}", flush=True)

json.dump(d, open(DATA, "w"), indent=1, ensure_ascii=False)
ps = d["projects"]
print("\nPATCH2 DONE", gains)
print("totals: hl", sum(1 for p in ps if p["highlights"]), "| loc", sum(1 for p in ps if p["locationAdvantages"]),
      "| rera", sum(1 for p in ps if p["rera"]))
print("still thin:", [p["slug"] for p in ps if not p["highlights"] and not p["locationAdvantages"]])
