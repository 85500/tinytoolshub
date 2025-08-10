
import io, sys, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
gp = ROOT / "generator" / "generate.py"
txt = gp.read_text(encoding="utf-8")
if "render_to(\"discover.html\"" not in txt:
    m = re.search(r"render_to\(\s*\"about\.html\".*?\)\s*", txt)
    if m:
        insert_at = m.end()
        addition = '\n# Discover page\ncats = sorted({p["category"] for p in pages_meta})\nrender_to("discover.html","discover.html", pages=pages_meta, categories=cats, **base_ctx)\n'
        txt = txt[:insert_at] + addition + txt[insert_at:]
        gp.write_text(txt, encoding="utf-8")
        print("Patched generate.py to render discover.html")
    else:
        print("Could not find insertion point; no changes made.")
else:
    print("generate.py already renders discover.html")
