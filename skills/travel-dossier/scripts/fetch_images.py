#!/usr/bin/env python3
"""Wikimedia Commons 抓图管线（travel-dossier）。

Usage:  python fetch_images.py <spec.json> <outdir>

spec.json:  { "语义文件名": ["查询词1", "查询词2"], ... }
每项按查询词顺序搜索，命中第一张 [jpeg, 宽>=1100, 标题不含 map/karte/plan/diagram] 即下载，
压缩至 <=155KB 存 <outdir>/<name>.jpg，授权写入 <outdir>/credits.json。
抓完必须拼 contact sheet 目检——搜索命中不等于主体正确。
"""
import json, sys, os, io, time, hashlib, urllib.request, urllib.parse
from PIL import Image

UA = {"User-Agent": "TravelDossier/1.0 (personal use)"}
BAN = ("map", "karte", "plan", "diagram", "logo")

def get(url, timeout=60, tries=5):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                time.sleep(8 * (i + 1)); continue
            raise

def search(query):
    api = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
           "&generator=search&gsrnamespace=6&gsrlimit=12"
           f"&gsrsearch={urllib.parse.quote(query)}"
           "&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiurlwidth=1100")
    data = json.loads(get(api, 30))
    for p in sorted((data.get("query", {}).get("pages", {}) or {}).values(),
                    key=lambda p: p.get("index", 99)):
        ii = p.get("imageinfo", [{}])[0]
        t = p["title"].lower()
        if ii.get("mime") == "image/jpeg" and ii.get("width", 0) >= 1100 \
           and not any(b in t for b in BAN):
            return p["title"], ii
    return None

def compress(raw):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width > 1000:
        im = im.resize((1000, int(im.height * 1000 / im.width)), Image.LANCZOS)
    q = 75
    while True:
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, progressive=True, optimize=True)
        if buf.tell() <= 155_000 or q <= 45:
            return buf.getvalue()
        q -= 8

def main():
    spec_path, outdir = sys.argv[1], sys.argv[2]
    spec = json.load(open(spec_path))
    os.makedirs(outdir, exist_ok=True)
    cpath = os.path.join(outdir, "credits.json")
    credits = json.load(open(cpath)) if os.path.exists(cpath) else {}
    for name, queries in spec.items():
        dest = os.path.join(outdir, f"{name}.jpg")
        if os.path.exists(dest):
            print("skip", name); continue
        picked = None
        for q in queries:
            picked = search(q)
            if picked: break
            time.sleep(2)
        if not picked:
            print("!! MISS", name); continue
        title, ii = picked
        time.sleep(3)
        data = compress(get(ii["thumburl"]))
        open(dest, "wb").write(data)
        lic = ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "?")
        credits[name] = f"{title} · {lic}"
        print(f"ok {name}: {len(data)//1024}KB <- {title} [{lic}]")
        time.sleep(3)
    json.dump(credits, open(cpath, "w"), ensure_ascii=False, indent=1)
    # 哈希去重提示
    seen = {}
    for f in os.listdir(outdir):
        if f.endswith(".jpg"):
            h = hashlib.md5(open(os.path.join(outdir, f), "rb").read(2048)).hexdigest()[:8]
            seen.setdefault(h, []).append(f)
    for h, fs in seen.items():
        if len(fs) > 1:
            print("!! DUPLICATE", fs)

if __name__ == "__main__":
    main()
