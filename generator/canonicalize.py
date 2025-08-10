# generator/canonicalize.py
import re, argparse, sys
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

def normalize_title(t: str) -> str:
    # Drop all parentheticals (variants and versions), normalize
    t = re.sub(r"\(.*?\)", "", t)
    t = re.sub(r"\b(converter|calculator)\b", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

def looks_versioned(t: str) -> bool:
    return bool(re.search(r"\(v\d+\)", t, re.I))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="outp", required=True)
    args = ap.parse_args()

    html = open(args.inp, "r", encoding="utf-8").read()
    soup = BeautifulSoup(html, "lxml")

    # Find all section containers under Discover
    # structure: headings (h2/##) followed by link lists
    # We dedupe *per section* to preserve your collections.
    sections = soup.find_all(string=re.compile(r"^\s*##\s+"))
    # Fallback: look for h2 tags if markdown was already rendered
    if not sections:
        sections = soup.select("h2")

    # In practice your Discover page is already rendered HTML with anchors inside grids
    # so we just sweep all links within the Discover content block.
    root = soup
    # Gather all links in discover
    anchors = root.select("a")

    seen_keys = {}
    to_remove = []

    for a in anchors:
        text = a.get_text(" ", strip=True)
        if not text:
            continue

        key = normalize_title(text)
        # Prefer the first non-versioned hit; otherwise keep first encountered
        if key in seen_keys:
            # Duplicate candidate; compare aggressively to catch near-dupes
            prev_text = seen_keys[key].get_text(" ", strip=True)
            score = fuzz.token_set_ratio(text, prev_text)
            if score >= 85:
                to_remove.append(a)
        else:
            seen_keys[key] = a
            # Also scrub display text: drop variants like "(1.75mm, PLA)" and "(v6)"
            clean = re.sub(r"\(.*?\)", "", text).strip()
            # Normalize spaces around hyphens
            clean = re.sub(r"\s+-\s+", " – ", clean)
            if clean:
                a.string = clean

    for a in to_remove:
        # remove the entire list item/card if possible
        parent = a
        for _ in range(3):
            if parent.name in ("li", "div", "p"):
                parent.decompose(); break
            parent = parent.parent

    with open(args.outp, "w", encoding="utf-8") as f:
        f.write(str(soup))

if __name__ == "__main__":
    sys.exit(main())
