import os, json, datetime, yaml, urllib.parse, re
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.dirname(__file__))
DIST = os.path.join(ROOT, "dist")
TPL = os.path.join(ROOT, "generator", "templates")

os.makedirs(DIST, exist_ok=True)

with open(os.path.join(ROOT, "site", "config.yaml"), "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

with open(os.path.join(ROOT, "generator", "pages.json"), "r", encoding="utf-8") as f:
    PAGES = json.load(f)

env = Environment(loader=FileSystemLoader(TPL), autoescape=select_autoescape())

def render_to(tpl_name, out_name, **ctx):
    tpl = env.get_template(tpl_name)
    html = tpl.render(**ctx)
    with open(os.path.join(DIST, out_name), "w", encoding="utf-8") as f:
        f.write(html)

def add_affiliate_tag(url, tag):
    if not tag or "amazon." not in url.lower():
        return url
    parsed = urllib.parse.urlsplit(url)
    qs = urllib.parse.parse_qs(parsed.query)
    qs["tag"] = [tag]
    new_query = urllib.parse.urlencode(qs, doseq=True)
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc or "www.amazon.com"
    path = parsed.path or "/s"
    return urllib.parse.urlunsplit((scheme, netloc, path, new_query, parsed.fragment))

base_url = (cfg.get("base_url","") or "").rstrip("/")
gsc_verif = cfg.get("gsc_verification","")

base_ctx = {
    "site_name": cfg.get("site_name","TinyToolsHub"),
    "adsense_client_id": cfg.get("adsense_client_id",""),
    "sovrn_key": cfg.get("sovrn_key",""),
    "skimlinks_pub_id": cfg.get("skimlinks_pub_id",""),
    "gsc_verification": gsc_verif,
    "base_path": "",
    "cf_analytics_token": cfg.get("cf_analytics_token",""),
    "year": datetime.datetime.now().year
}

# Build page meta list
pages_meta = []
for p in PAGES:
    pages_meta.append({
        "slug": p["slug"],
        "title": p["title"],
        "description": p["description"],
        "category": p.get("category",""),
    })

# Related links: same category
by_cat = {}
for pm in pages_meta:
    by_cat.setdefault(pm["category"], []).append(pm)
for pm in pages_meta:
    siblings = [s for s in by_cat.get(pm["category"], []) if s["slug"] != pm["slug"]]
    pm["related"] = siblings[:5]

# Render each page
for pm in pages_meta:
    orig = next(x for x in PAGES if x["slug"] == pm["slug"])
    recs = []
    for r in orig.get("recommendations", []):
        r = dict(r)
        r["url"] = add_affiliate_tag(r.get("url",""), cfg.get("amazon_tag",""))
        recs.append(r)
    ctx = dict(base_ctx)
    canonical_url = (base_url + f"/{pm['slug']}.html") if base_url else ""
    ctx.update({
        "title": pm["title"],
        "description": pm["description"],
        "h1": orig.get("h1", pm["title"]),
        "lede": orig.get("lede",""),
        "steps": orig.get("steps", []),
        "calculator_component": orig.get("calculator_component"),
        "calculator_js": orig.get("calculator_js"),
        "calc_title": orig.get("calc_title", "Calculator"),
        "tips": orig.get("tips", []),
        "recommendations": recs,
        "canonical_url": canonical_url,
        "related": pm.get("related", [])
    })
    render_to("page.html", f"{pm['slug']}.html", **ctx)

# Index/all/about
home_canon = (base_url + "/index.html") if base_url else ""
render_to("index.html", "index.html", pages=pages_meta, featured=[p for p in pages_meta if p.get("category")== "Signature Apps"][:6], popular=pages_meta[:6], categories=sorted({p["category"] for p in pages_meta}), **base_ctx)
all_canon = (base_url + "/all.html") if base_url else ""
render_to("all.html", "all.html", pages=pages_meta, popular=pages_meta[:6], categories=sorted({p["category"] for p in pages_meta}), **base_ctx)
about_canon = (base_url + "/about.html") if base_url else ""
render_to("about.html", "about.html", popular=pages_meta[:6], categories=sorted({p["category"] for p in pages_meta}), **base_ctx)


# Discover page
cats = sorted({p["category"] for p in pages_meta})
render_to("discover.html","discover.html", pages=pages_meta, categories=cats, **base_ctx)
print(f"Built {len(PAGES)} pages → dist/")

# Sitemap/robots/feed
def write(path, txt):
    with open(os.path.join(DIST, path), "w", encoding="utf-8") as f:
        f.write(txt)

if base_url:
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    urls = [f"<url><loc>{base_url}/index.html</loc><lastmod>{now}</lastmod></url>"]
    for pm in pages_meta:
        urls.append(f"<url><loc>{base_url}/{pm['slug']}.html</loc><lastmod>{now}</lastmod></url>")
    sitemap = "<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>\n" + "\n".join(urls) + "\n</urlset>"
    write("sitemap.xml", sitemap)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n")

    items = []
    for pm in pages_meta[:50]:
        items.append(f"<item><title>{pm['title']}</title><link>{base_url}/{pm['slug']}.html</link></item>")
    rss = f"<?xml version='1.0' encoding='UTF-8'?>\n<rss version='2.0'><channel><title>{cfg.get('site_name','TinyToolsHub')}</title><link>{base_url}</link>{''.join(items)}</channel></rss>"
    write("feed.xml", rss)

# Auto-generate ads.txt from adsense_client_id
pub = cfg.get("adsense_client_id","")
m = re.search(r"pub-\d+", pub or "")
if m:
    write("ads.txt", f"google.com, {m.group(0)}, DIRECT, f08c47fec0942fa0\n")

# Write redirects to dist/_redirects if available
import json, os
rj = os.path.join(ROOT, "generator", "redirects.json")
if os.path.exists(rj):
    try:
        r = json.load(open(rj, "r", encoding="utf-8"))
        with open(os.path.join(DIST, "_redirects"), "w", encoding="utf-8") as f:
            for k,v in r.items():
                f.write(f"{k} {v} 301\n")
    except Exception as e:
        print("Redirects write failed:", e)
