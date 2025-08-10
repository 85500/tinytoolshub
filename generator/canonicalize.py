# generator/canonicalize.py
import re, argparse, sys
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

def normalize_title(t: str) -> str:
    t = re.sub(r"\(.*?\)", "", t)
    t = re.sub(r"\b(converter|calculator)\b", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="outp", required=True)
    args = ap.parse_args()

    html = open(args.inp, "r", encoding="utf-8").read()
    soup = BeautifulSoup(html, "lxml")

    anchors = soup.select("a")
    seen = {}
    to_remove = []

    for a in anchors:
        text = a.get_text(" ", strip=True)
        if not text:
            continue
        key = normalize_title(text)
        if key in seen:
            prev = seen[key].get_text(" ", strip=True)
            if fuzz.token_set_ratio(text, prev) >= 85:
                to_remove.append(a)
        else:
            seen[key] = a
            clean = re.sub(r"\(.*?\)", "", text).strip()
            clean = re.sub(r"\s+-\s+", " – ", clean)
            if clean:
                a.string = clean

    for a in to_remove:
        parent = a
        for _ in range(3):
            if parent and parent.name in ("li", "div", "p"):
                parent.decompose(); break
            parent = parent.parent

    with open(args.outp, "w", encoding="utf-8") as f:
        f.write(str(soup))

if __name__ == "__main__":
    sys.exit(main())
