# generator/elevate_site.py
import argparse, re, os, html
from bs4 import BeautifulSoup

KEYWORDS = {
    "home-diy": ["tile","grout","mortar","paint","drywall","deck","roof","concrete","rebar","stud","joist","beam","shingle","primer","roller","sprayer","fence"],
    "pc-tech": ["gpu","psu","cpu","monitor","dpi","ppi","case","pcie","nvme","nas","raid","wifi","router","mesh","hdmi","displayport"],
    "travel": ["carry-on","carry on","luggage","airline","tsa","bag","suitcase","packing","adapter","voltage","plug"],
    "shipping": ["dim","freight","usps","ups","fedex","pallet","box","carton","cubic","weight"],
    "3d-print": ["filament","resin","nozzle","gcode","extrusion","fep","sla","fdm","prus","bambu","ender"],
    "photo-video": ["aperture","nd","filter","focal","lens","gimbal","payload","exposure","shutter","iso","depth of field","dof"],
    "math-finance": ["loan","interest","mortgage","apr","roi","markup","discount","percent","percentage","ratio"],
    "converters": ["feet","meters","inch","mm","btu","psi","bar","celsius","fahrenheit","kelvin","area","volume","mass","density"],
}

def slugify(t):
    t = re.sub(r"[^a-z0-9]+","-", t.lower())
    return re.sub(r"-+","-", t).strip("-")

def normalize_title(t: str) -> str:
    t = re.sub(r"\(v\d+\)", "", t, flags=re.I)
    t = re.sub(r"\(.*?\)", "", t)
    t = re.sub(r"\b(converter|calculator)\b", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

def guess_tags(title: str):
    low = title.lower()
    tags = set()
    for tag, words in KEYWORDS.items():
        if any(w in low for w in words):
            tags.add(tag)
    if not tags:
        tags.add("general")
    return sorted(tags)

def build_new_html(items):
    css = """
    :root{--bg:#0b1020;--card:#0f172a;--muted:#93a4c0;--text:#e6eefc;--chip:#1e293b;--glow:#60a5fa}
    *{box-sizing:border-box}
    html,body{margin:0;height:100%;background:linear-gradient(180deg,#0b1020 0%,#0b152e 100%);color:var(--text);font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial,sans-serif}
    a{color:inherit;text-decoration:none}
    .wrap{max-width:1100px;margin:0 auto;padding:24px}
    .hero{padding:30px 0 12px}
    .hero h1{font-size:34px;margin:0 0 10px}
    .muted{color:var(--muted)}
    .search{display:flex;gap:10px;margin:16px 0 8px}
    .search input{flex:1;padding:12px 14px;border-radius:12px;border:1px solid #1f2a44;background:#0c1530;color:var(--text);outline:none}
    .chips{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 20px}
    .chip{padding:6px 10px;border-radius:999px;background:var(--chip);color:#cfe0ff;font-size:12px;border:1px solid #2b3857;cursor:pointer}
    .chip.active{outline:2px solid var(--glow)}
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
    .card{position:relative;border:1px solid #1e2a49;background:linear-gradient(180deg,#0e1630,#0c142a);border-radius:16px;overflow:hidden;box-shadow:0 1px 0 #102042,inset 0 0 0 1px rgba(255,255,255,.02)}
    .thumb{height:140px;background:radial-gradient(60% 80% at 50% 10%,rgba(96,165,250,.25),transparent 60%),linear-gradient(180deg,#0f1b3a,#0a1330)}
    .thumb img{width:100%;height:100%;object-fit:cover;display:block;opacity:.92}
    .body{padding:12px 14px}
    .title{font-weight:600;margin:0 0 6px}
    .tags{display:flex;flex-wrap:wrap;gap:6px}
    .tag{font-size:11px;padding:4px 8px;border-radius:999px;background:#0b1a38;border:1px solid #1b2b50;color:#b9d1ff}
    .btns{display:flex;gap:8px;margin-top:10px}
    .btn{flex:1;text-align:center;padding:8px 10px;border-radius:10px;background:#0f1c3c;border:1px solid #1e2b55;color:#d9e8ff}
    .btn:hover{border-color:#365da8}
    .fade{opacity:0;transform:translateY(6px);animation:reveal .5s ease forwards}
    @keyframes reveal{to{opacity:1;transform:none}}
    .footer{opacity:.8;margin:40px 0 0;font-size:13px}
    """
    js = """
    (function(){
      const q = document.querySelector('#q');
      const chips = [...document.querySelectorAll('.chip[data-tag]')];
      const cards = [...document.querySelectorAll('[data-title]')];
      function norm(s){ return (s||'').toLowerCase().normalize('NFKD').replace(/[^a-z0-9\s-]/g,''); }
      let activeTag = null;
      function apply(){
        const text = norm(q.value);
        for(const el of cards){
          const title = el.dataset.titleNorm;
          const tags = (el.dataset.tags||'').split(',');
          const hitsText = !text || title.includes(text);
          const hitsTag = !activeTag || tags.includes(activeTag);
          el.style.display = (hitsText && hitsTag) ? '' : 'none';
        }
      }
      q?.addEventListener('input', apply);
      chips.forEach(c=>c.addEventListener('click', ()=>{
        const t = c.dataset.tag;
        if(activeTag===t){ activeTag=null; chips.forEach(x=>x.classList.remove('active')); }
        else { activeTag=t; chips.forEach(x=>x.classList.toggle('active', x===c)); }
        apply();
      }));
      const io = new IntersectionObserver(entries=>{
        entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('fade'); io.unobserve(e.target);} });
      }, {rootMargin:'0px 0px -10% 0px'});
      cards.forEach(c=>io.observe(c));
      apply();
    })();
    """

    tag_set = set()
    for it in items:
        for t in it['tags']: tag_set.add(t)
    tag_order = sorted(tag_set)

    def card(it):
        title = html.escape(it['title'])
        href = html.escape(it['href'])
        tags = ''.join(f'<span class="tag">{html.escape(t)}</span>' for t in it['tags'])
        tag_attr = ','.join(it['tags'])
        slug = it['slug']
        thumb = f'og/{slug}.png' if it.get('has_og') else ''
        thumb_html = f'<div class="thumb">{f"<img src=\"/{thumb}\" alt=\"\">" if thumb else ""}</div>'
        return f'''
        <a class="card" href="{href}" data-title="{html.escape(it['title_lower'])}" data-title-norm="{html.escape(it['title_norm'])}" data-tags="{html.escape(tag_attr)}">
          {thumb_html}
          <div class="body">
            <div class="title">{title}</div>
            <div class="tags">{tags}</div>
            <div class="btns">
              <div class="btn">Open tool</div>
            </div>
          </div>
        </a>'''

    cards_html = '\n'.join(card(it) for it in items)
    chips_html = ''.join(f'<button class="chip" data-tag="{html.escape(t)}">{html.escape(t)}</button>' for t in tag_order)

    html_out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Discover — TinyToolsHub</title>
<meta name="description" content="A curated set of genuinely useful, no-BS tools for builders, makers, and travelers.">
<link rel="icon" href="/favicon.ico">
<style>{css}</style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <h1>Discover useful tools</h1>
      <div class="muted">De-duplicated. Categorized. Fast.</div>
      <div class="search">
        <input id="q" type="search" placeholder="Search tools (e.g., tile, PSU, carry-on)">
      </div>
      <div class="chips">{chips_html}</div>
    </header>

    <main class="grid">
      {cards_html}
    </main>

    <footer class="footer muted">
      This page is auto-generated nightly. Product links may be affiliate links.
    </footer>
  </div>
<script>{js}</script>
</body>
</html>"""
    return html_out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="outp", required=True)
    ap.add_argument("--og", dest="ogdir", default="dist/og")
    args = ap.parse_args()

    raw = open(args.inp, "r", encoding="utf-8").read()
    soup = BeautifulSoup(raw, "lxml")
    anchors = soup.select("a[href]")

    seen = {}
    items = []
    for a in anchors:
      href = a.get("href","").strip()
      if not href or href.startswith("http"):
        continue
      title = a.get_text(" ", strip=True)
      if not title or len(title) < 3:
        continue
      title_clean = re.sub(r"\(v\d+\)", "", title, flags=re.I)
      title_clean = re.sub(r"\(.*?\)", "", title_clean).strip()
      key = normalize_title(title)
      if key in seen:
        continue
      seen[key] = True

      slug = slugify(title_clean)
      tags = guess_tags(title_clean)
      it = {
        "title": title_clean,
        "title_lower": title_clean.lower(),
        "title_norm": normalize_title(title_clean),
        "href": href,
        "tags": tags,
        "slug": slug,
        "has_og": os.path.exists(os.path.join(args.ogdir, f"{slug}.png"))
      }
      items.append(it)

    items.sort(key=lambda x: (x["tags"][0] if x["tags"] else "zzz", x["title_lower"]))
    new_html = build_new_html(items)
    with open(args.outp, "w", encoding="utf-8") as f:
      f.write(new_html)

if __name__ == "__main__":
    main()
