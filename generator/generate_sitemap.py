# generator/generate_sitemap.py
import os, argparse, time, html

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--base", required=True)
    args = ap.parse_args()

    urls=[]
    for root,_,files in os.walk(args.root):
        for f in files:
            if not f.endswith(".html"): continue
            if f.startswith("_"): continue
            path=os.path.join(root,f)
            rel=os.path.relpath(path,args.root).replace("\\","/")
            if rel.endswith("index.html"): rel=rel[:-len("index.html")]
            url=f"{args.base.rstrip('/')}/{rel}"
            m=int(os.path.getmtime(path))
            urls.append((url,m))
    urls.sort(key=lambda x:x[0])

    sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u,m in urls:
        sm.append("  <url>")
        sm.append(f"    <loc>{html.escape(u)}</loc>")
        sm.append(f"    <lastmod>{time.strftime('%Y-%m-%d', time.gmtime(m))}</lastmod>")
        sm.append("  </url>")
    sm.append("</urlset>\n")

    with open(os.path.join(args.root,"sitemap.xml"),"w",encoding="utf-8") as f:
        f.write("\n".join(sm))
    with open(os.path.join(args.root,"robots.txt"),"w",encoding="utf-8") as f:
        f.write(f"Sitemap: {args.base.rstrip('/')}/sitemap.xml\nUser-agent: *\nAllow: /\n")

if __name__ == "__main__":
    main()
