import os, json, yaml, hashlib, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(ROOT/"site"/"config.yaml", "r", encoding="utf-8"))
PAGES_PATH = ROOT/"generator"/"pages.json"

# Load existing pages
PAGES = json.load(open(PAGES_PATH, "r", encoding="utf-8")) if PAGES_PATH.exists() else []

MAX = int(CFG.get("build",{}).get("max_pages", 10000))
DAILY = int(CFG.get("build",{}).get("daily_new_pages", 30))

# Simple topic fabricators mapped to existing calculators
fabricators = [
    {
        "category":"Home DIY Calculators",
        "patterns":[
            ("{x} to {y} Converter", "unit-converter", "unit-converter.js", "Convert units", 
             [("feet","meters"),("meters","feet"),("inches","centimeters"),("centimeters","inches")])
        ],
        "tips":["Round to practical precision.","Double-check units before cutting."],
        "recs":[
            {"name":"Dual-scale tape","blurb":"Imperial/metric tape.","url":"https://www.amazon.com/s?k=dual+scale+measuring+tape"}
        ]
    },
    {
        "category":"Shop & Woodworking",
        "patterns":[
            ("Board Feet Calculator ({t}in x {w}in x {l}ft)", "boardfeet-calc","boardfeet-calc.js","Calculate board feet",
             [("1","4","8"),("2","6","8"),("1","6","10"),("1","8","6")])
        ],
        "tips":["Buy 10–15% extra for waste.","Confirm seller’s rounding rules."],
        "recs":[{"name":"Moisture meter","blurb":"Check before finishing.","url":"https://www.amazon.com/s?k=wood+moisture+meter"}]
    },
    {
        "category":"3D Printing & Maker",
        "patterns":[
            ("Filament Length from Spool Weight ({d}mm, {mat})", "filament-estimator","filament-estimator.js","Estimate length",
             [("1.75","PLA"),("1.75","PETG"),("2.85","PLA")])
        ],
        "tips":["Density varies by material and brand.","Weigh an empty spool for accuracy."],
        "recs":[{"name":"Digital scale","blurb":"Weigh spools precisely.","url":"https://www.amazon.com/s?k=0.1g+digital+scale"}]
    },
    {
        "category":"Travel & Shipping",
        "patterns":[
            ("Dimensional Weight Calculator ({mode})","dim-weight","dim-weight.js","Compute DIM weight",
             [("Air (139 divisor)","139"),("Ground (166 divisor)","166")])
        ],
        "tips":["Carriers round up to the next pound.","Use the smallest protective box."],
        "recs":[{"name":"Shipping scale","blurb":"Accurate to 0.1 lb.","url":"https://www.amazon.com/s?k=shipping+scale"}]
    },
    {
        "category":"Photography & Video",
        "patterns":[
            ("Percent Calculator for Discounts & Markups","percent-calc","percent-calc.js","Percent tools",[("x","y")])
        ],
        "tips":["For exposure math, keep a notebook of your common scenes.","Double-check before committing settings."],
        "recs":[{"name":"Notebook","blurb":"Jot settings & scenes.","url":"https://www.amazon.com/s?k=pocket+notebook"}]
    }
]

def slugify(s):
    s = s.lower()
    s = s.replace("(", "").replace(")", "").replace("&","and").replace("/","-")
    s = "-".join(re.findall(r"[a-z0-9]+", s))
    s = re.sub(r"-+","-",s).strip("-")
    return s

import re
def mk_page(title, h1, lede, calc_tag, calc_js, category, tips, recs):
    return {
        "slug": slugify(title),
        "title": title,
        "description": lede,
        "h1": h1,
        "lede": lede,
        "steps": ["Enter your values.","Click calculate.","Use the tips to improve accuracy."],
        "calculator_component": calc_tag,
        "calculator_js": calc_js,
        "calc_title": "Calculator",
        "category": category,
        "tips": tips,
        "recommendations": recs
    }

# Build a set of existing slugs
existing = {p["slug"] for p in PAGES}
added = 0

random.seed()  # nondeterministic

for fab in fabricators:
    if len(PAGES) + added >= MAX: break
    pats = fab["patterns"]
    random.shuffle(pats)
    for pat in pats:
        if len(PAGES) + added >= MAX: break
        title_tpl, tag, js, calc_title, variants = pat
        random.shuffle(variants)
        for var in variants:
            if len(PAGES) + added >= MAX or added >= DAILY: break
            # Build title/h1/lede from variant tuple
            if "{x}" in title_tpl and "{y}" in title_tpl:
                x,y = var
                title = title_tpl.format(x=x, y=y)
            elif "{t}" in title_tpl:
                t,w,l = var
                title = title_tpl.format(t=t, w=w, l=l)
            elif "{d}" in title_tpl and "{mat}" in title_tpl:
                d,mat = var
                title = title_tpl.format(d=d, mat=mat)
            elif "{mode}" in title_tpl:
                m,label = var
                title = title_tpl.format(mode=m)
            else:
                title = title_tpl
            h1 = title
            lede = f"Quick utility for {title.lower()}."
            slug = slugify(title)
            if slug in existing:
                continue
            page = mk_page(title, h1, lede, tag, js, fab["category"], fab["tips"], fab["recs"])
            PAGES.append(page)
            existing.add(slug)
            added += 1

# Save back
json.dump(PAGES, open(PAGES_PATH, "w", encoding="utf-8"), indent=2)
print(f"Added {added} new pages (total {len(PAGES)}).")
