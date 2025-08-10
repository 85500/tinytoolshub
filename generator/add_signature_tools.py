
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = ROOT/"generator"/"pages.json"
data = json.loads(PAGES.read_text(encoding='utf-8'))

new_pages = [
  {
    "slug":"sheet-optimizer-2d",
    "title":"Sheet Optimizer (2D)",
    "description":"Kerf-aware cut planner for sheet goods with visual layout.",
    "h1":"Sheet Optimizer (2D)",
    "lede":"Paste part sizes and get a visual cut plan across sheets.",
    "steps":["Enter sheet size and kerf.","Paste parts as `WxH x Qty`.","Optimize and review the layout."],
    "calculator_component":"sheet-optimizer-2d",
    "calculator_js":"sheet-optimizer-2d.js",
    "calc_title":"Optimize layout",
    "category":"Signature Apps",
    "tips":["Group similar parts to simplify cuts.","Add margin if your saw kerf varies."],
    "recommendations":[
      {"name":"Track saw","blurb":"Long, straight cuts.","url":"https://www.amazon.com/s?k=track+saw"},
      {"name":"Plywood blade","blurb":"Clean edges, less tearout.","url":"https://www.amazon.com/s?k=plywood+blade"}
    ]
  },
  {
    "slug":"project-quote-builder",
    "title":"Project Quote & BOM Builder",
    "description":"Paste items, taxes, markup—get a clean quote & CSV export.",
    "h1":"Project Quote & BOM Builder",
    "lede":"Build estimates fast and export a ready-to-send CSV.",
    "steps":["Paste items as `name, qty, unit`.","Set tax/markup/discount.","Export CSV or copy totals."],
    "calculator_component":"quote-builder",
    "calculator_js":"quote-builder.js",
    "calc_title":"Build quote",
    "category":"Signature Apps",
    "tips":["Use separate labor line-items.","Save your common parts list in a note for reuse."],
    "recommendations":[
      {"name":"Label printer","blurb":"Organize BOM picks.","url":"https://www.amazon.com/s?k=label+printer"}
    ]
  }
]

slugs={p['slug'] for p in data}
added=0
for p in new_pages:
  if p['slug'] not in slugs:
    data.append(p); slugs.add(p['slug']); added+=1

PAGES.write_text(json.dumps(data, indent=2), encoding='utf-8')
print(f"Added {added} signature tools. Total: {len(data)}")
