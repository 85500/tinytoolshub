
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
pages_path = ROOT/"generator"/"pages.json"
redirects_path = ROOT/"generator"/"redirects.json"

data = json.loads(pages_path.read_text(encoding="utf-8"))

def base_title(t):
  t0 = re.sub(r'\b[vV]\s?(\d+)\b', '', t).strip()
  t0 = re.sub(r'\s*[-–—]\s*v\d+\b', '', t0).strip()
  t0 = re.sub(r'\s*\(v\d+\)\s*', '', t0).strip()
  t0 = re.sub(r'\s+', ' ', t0)
  return t0

groups = {}
for p in data:
  key = (base_title(p["title"]).lower(), p.get("category","").lower())
  groups.setdefault(key, []).append(p)

keep = []
redirects = {}
for key, items in groups.items():
  if len(items)==1:
    keep.append(items[0]); continue
  # choose the one with calculator_component, else longest description, else first
  items_sorted = sorted(items, key=lambda x: (1 if x.get("calculator_component") else 0, len(x.get("description",""))), reverse=True)
  primary = items_sorted[0]
  keep.append(primary)
  for dup in items_sorted[1:]:
    redirects[f"/{dup['slug']}.html"] = f"/{primary['slug']}.html"

# de-dup by slug collisions too
seen = set(); final = []
for p in keep:
  if p["slug"] in seen: continue
  seen.add(p["slug"]); final.append(p)

pages_path.write_text(json.dumps(final, indent=2), encoding="utf-8")
redirects_path.write_text(json.dumps(redirects, indent=2), encoding="utf-8")
print(f"Kept {len(final)} pages. Redirects: {len(redirects)}")
