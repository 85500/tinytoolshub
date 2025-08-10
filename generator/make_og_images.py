# generator/make_og_images.py
import argparse, os, re
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

def slugify(t):
    t = re.sub(r"[^a-z0-9]+", "-", t.lower())
    return re.sub(r"-+", "-", t).strip("-")

def draw_card(path, title):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (248, 250, 252))
    d = ImageDraw.Draw(img)

    # gradient-ish diagonal stripes
    for i in range(0, W, 40):
        shade = 245 - (i // 40) % 12
        d.rectangle([(i, 0), (i+20, H)], fill=(shade, shade, shade))

    # Title text
    try:
        # System fonts vary; fall back to default if not found.
        font = ImageFont.truetype("arial.ttf", 68)
    except:
        font = ImageFont.load_default()

    bbox = d.textbbox((0,0), title, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.text(((W - tw)//2, (H - th)//2), title, fill=(18, 28, 45), font=font)

    # Badge
    badge = "TinyToolsHub"
    try:
        bf = ImageFont.truetype("arial.ttf", 30)
    except:
        bf = ImageFont.load_default()
    d.rounded_rectangle([(40, H-80), (260, H-40)], 16, fill=(18,28,45))
    d.text((60, H-78), badge, fill=(248,250,252), font=bf)

    img.save(path, "PNG", optimize=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--discover", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    soup = BeautifulSoup(open(args.discover, "r", encoding="utf-8").read(), "lxml")
    titles = []
    for a in soup.select("a"):
        t = a.get_text(" ", strip=True)
        if not t: continue
        t = re.sub(r"\(.*?\)", "", t).strip()
        titles.append(t)

    # unique
    seen = set()
    for t in titles:
        if t in seen: continue
        seen.add(t)
        slug = slugify(t)
        out = os.path.join(args.out, f"{slug}.png")
        draw_card(out, t)

if __name__ == "__main__":
    main()
