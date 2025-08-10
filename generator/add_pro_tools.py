
import json, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = ROOT/"generator"/"pages.json"

new_pages = [
  {
    "slug":"cut-list-optimizer",
    "title":"Cut‑List Optimizer (1D)",
    "description":"Best‑fit cut plan for lumber with kerf and waste.",
    "h1":"Cut‑List Optimizer",
    "lede":"Enter stock length, kerf, and required cuts to minimize waste.",
    "steps":["Enter stock length and kerf.","Paste your required cuts, one per line.","Click Optimize to get boards and waste."],
    "calculator_component":"cutlist-optimizer",
    "calculator_js":"cutlist-optimizer.js",
    "calc_title":"Optimize cut list",
    "category":"Pro Tools",
    "tips":["Add 5–10% contingency for defects.","Group similar cuts to reduce setup time."],
    "recommendations":[
      {"name":"Rip‑cut blade","blurb":"Thin‑kerf for less waste.","url":"https://www.amazon.com/s?k=thin+kerf+saw+blade"},
      {"name":"Stop block","blurb":"Repeatable lengths.","url":"https://www.amazon.com/s?k=table+saw+stop+block"}
    ]
  },
  {
    "slug":"box-fit-rotation-planner",
    "title":"Box‑Fit & Rotation Planner",
    "description":"Find which boxes fit and compute DIM weight.",
    "h1":"Box‑Fit & Rotation Planner",
    "lede":"Try all rotations, see fit, empty volume, and dimensional weight.",
    "steps":["Enter item size.","Paste box sizes.","Pick carrier mode and compute."],
    "calculator_component":"boxfit-planner",
    "calculator_js":"boxfit-planner.js",
    "calc_title":"Find best box",
    "category":"Pro Tools",
    "tips":["Smaller boxes reduce DIM charges.","Add padding clearance when choosing a box."],
    "recommendations":[
      {"name":"Variety box pack","blurb":"Right size, lower DIM.","url":"https://www.amazon.com/s?k=shipping+box+assortment"}
    ]
  },
  {
    "slug":"tile-flooring-planner",
    "title":"Tile & Flooring Planner",
    "description":"Coverage, cuts, and suggested boxes with waste.",
    "h1":"Tile & Flooring Planner",
    "lede":"Estimate tile count, stagger, and edge cuts.",
    "steps":["Enter room size.","Enter tile size and grout width.","Choose waste and stagger pattern."],
    "calculator_component":"tile-planner",
    "calculator_js":"tile-planner.js",
    "calc_title":"Plan layout",
    "category":"Pro Tools",
    "tips":["Order extra for breakage and pattern matching.","Dry‑lay a small area to verify offsets."],
    "recommendations":[
      {"name":"Tile spacers","blurb":"Consistent grout lines.","url":"https://www.amazon.com/s?k=tile+spacers"}
    ]
  },
  {
    "slug":"batch-unit-converter",
    "title":"Batch Unit Converter",
    "description":"Convert dozens of values in one go.",
    "h1":"Batch Unit Converter",
    "lede":"Paste a list and get bulk conversions to the unit you need.",
    "steps":["Paste values with units.","Choose the target unit.","Convert and copy the result."],
    "calculator_component":"batch-converter",
    "calculator_js":"batch-converter.js",
    "calc_title":"Batch convert",
    "category":"Pro Tools",
    "tips":["Use short units like ft, in, cm, m.","Export results into spreadsheets."],
    "recommendations":[]
  },
  {
    "slug":"3d-print-spool-manager",
    "title":"3D Print Spool Manager",
    "description":"Track remaining grams and length per spool (local only).",
    "h1":"3D Print Spool Manager",
    "lede":"Estimate remaining meters and log usage—saved in your browser.",
    "steps":["Add or update a spool with weight and material.","Log grams used per print.","Watch remaining meters update."],
    "calculator_component":"spool-manager",
    "calculator_js":"spool-manager.js",
    "calc_title":"Manage spools",
    "category":"Pro Tools",
    "tips":["Weigh empty spools for accuracy.","Material density varies by brand."],
    "recommendations":[]
  },
  {
    "slug":"pc-airflow-psu-estimator",
    "title":"PC Airflow & PSU Estimator",
    "description":"Quick airflow sufficiency check and PSU headroom.",
    "h1":"PC Airflow & PSU Estimator",
    "lede":"Estimate intake CFM and recommended PSU wattage.",
    "steps":["Enter component power draw.","Enter fan count and CFM.","Review airflow verdict and PSU size."],
    "calculator_component":"pc-planner",
    "calculator_js":"pc-planner.js",
    "calc_title":"Estimate build",
    "category":"Pro Tools",
    "tips":["Aim for 20–30% PSU headroom.","High‑density filters reduce CFM."],
    "recommendations":[
      {"name":"PSU calculator","blurb":"Cross‑check vendor specs.","url":"https://www.amazon.com/s?k=psu+power+supply"}
    ]
  }
]

data = json.loads(PAGES.read_text(encoding='utf-8'))
slugs = {p['slug'] for p in data}
added = 0
for p in new_pages:
  if p['slug'] not in slugs:
    data.append(p); slugs.add(p['slug']); added += 1
PAGES.write_text(json.dumps(data, indent=2), encoding='utf-8')
print(f"Added {added} pro tools. Total pages: {len(data)}")
