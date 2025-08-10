# generator/make_og_images.py
import argparse, os, re
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

def slugify(t):
    t = re.sub(r"[^a-z0-9]+", "-", t.lower())
    return re.sub(r"-+","-", t).strip("-")

def draw(path, title):
    W,H=1200,630
    img = Image.new("RGB",(W,H),(11,16,32))
    d = ImageDraw.Draw(img)
    for i in range(0,W,36):
        shade = 20 + (i//36)%20
        d.rectangle([(i,0),(i+18,H)], fill=(10,14,28+shade//2))
    try: font = ImageFont.truetype("arial.ttf", 68)
    except: font = ImageFont.load_default()
    bbox = d.textbbox((0,0), title, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.text(((W-tw)//2,(H-th)//2), title, fill=(220,235,255), font=font)
    try: bf = ImageFont.truetype("arial.ttf", 30)
    except: bf = ImageFont.load_default()
    d.rounded_rectangle([(40,H-80),(260,H-40)], 16, fill=(96,165,250))
    d.text((60,H-78), "TinyToolsHub", fill=(5,10,20), font=bf)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path,"PNG", optimize=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--discover", required=True)
    ap.add_argument("--out", required=True)
    args=ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    soup = BeautifulSoup(open(args.discover,"r",encoding="utf-8").read(),"lxml")
    seen=set()
    for a in soup.select("a"):
        t=a.get_text(" ", strip=True)
        if not t: continue
        t=re.sub(r"\(.*?\)","",t).strip()
        if t in seen: continue
        seen.add(t)
        slug=slugify(t)
        draw(os.path.join(args.out, f"{slug}.png"), t)

if __name__ == "__main__":
    main()
