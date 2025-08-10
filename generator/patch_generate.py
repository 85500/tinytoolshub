
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
gp = ROOT/"generator"/"generate.py"
txt = gp.read_text(encoding="utf-8")

# Ensure base_ctx includes cf_analytics_token and popular/featured contexts later
if 'cf_analytics_token' not in txt:
    txt = txt.replace('"year":', '"cf_analytics_token": cfg.get("cf_analytics_token",""),\n    "year":')

# Render discover if missing
if 'render_to("discover.html"' not in txt:
    m = re.search(r'render_to\(\s*"about\.html".*?\)\s*', txt, flags=re.S)
    if m:
        ins = m.end()
        txt = txt[:ins] + '\n# Discover page\ncats = sorted({p["category"] for p in pages_meta})\nrender_to("discover.html","discover.html", pages=pages_meta, categories=cats, **base_ctx)\n' + txt[ins:]

# Inject featured/popular contexts and use template names we provided
if 'render_to("index.html", "index.html",' in txt:
    txt = re.sub(r'render_to\("index\.html", "index\.html",(.*?)\)', 'render_to("index.html", "index.html", pages=pages_meta, featured=[p for p in pages_meta if p.get("category")== "Signature Apps"][:6], popular=pages_meta[:6], categories=sorted({p["category"] for p in pages_meta}), **base_ctx)', txt, flags=re.S)
if 'render_to("all.html", "all.html",' in txt:
    txt = re.sub(r'render_to\("all\.html", "all\.html",(.*?)\)', 'render_to("all.html", "all.html", pages=pages_meta, popular=pages_meta[:6], categories=sorted({p["category"] for p in pages_meta}), **base_ctx)', txt, flags=re.S)
if 'render_to("about.html", "about.html",' in txt:
    txt = re.sub(r'render_to\("about\.html", "about\.html",(.*?)\)', 'render_to("about.html", "about.html", popular=pages_meta[:6], categories=sorted({p["category"] for p in pages_meta}), **base_ctx)', txt, flags=re.S)

# Emit _redirects from generator/redirects.json if present
if "redirects.json" not in txt:
    txt += '\n# Write redirects to dist/_redirects if available\nimport json, os\nrj = os.path.join(ROOT, "generator", "redirects.json")\nif os.path.exists(rj):\n    try:\n        r = json.load(open(rj, "r", encoding="utf-8"))\n        with open(os.path.join(DIST, "_redirects"), "w", encoding="utf-8") as f:\n            for k,v in r.items():\n                f.write(f"{k} {v} 301\\n")\n    except Exception as e:\n        print("Redirects write failed:", e)\n'

gp.write_text(txt, encoding="utf-8")
print("Patched generate.py")
