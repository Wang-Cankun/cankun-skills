#!/usr/bin/env python3
"""strip check：渲染 PDF 每页底部 20% 拼成检查条，人眼查页脚碰撞（travel-dossier）。

Usage:  python check_overflow.py <dossier.pdf> <outdir> [页码 页码 ...]
省略页码 = 全书。产出 <outdir>/bottoms-N.png（每张 <=10 页），用 Read 工具逐张目检：
页脚横线与页码必须完整可见、其上有空隙；内容压线/穿线即溢出。
修法优先级：删一行内容 > 缩图高 > 收 margin；禁止缩正文字号。
依赖：pdftoppm (poppler)、PIL。
"""
import sys, os, glob, subprocess
from PIL import Image

def main():
    pdf, outdir = sys.argv[1], sys.argv[2]
    pages = [int(x) for x in sys.argv[3:]] or None
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, "pg-*.png")) + glob.glob(os.path.join(outdir, "bottoms-*.png")):
        os.remove(f)
    if pages:
        for p in pages:
            subprocess.run(["pdftoppm", "-png", "-r", "55", "-f", str(p), "-l", str(p),
                            pdf, os.path.join(outdir, f"pg-{p:02d}")], check=True)
    else:
        subprocess.run(["pdftoppm", "-png", "-r", "55", pdf, os.path.join(outdir, "pg")], check=True)
    files = sorted(glob.glob(os.path.join(outdir, "pg*.png")))
    crops = []
    for f in files:
        im = Image.open(f)
        w, h = im.size
        crops.append((os.path.basename(f), im.crop((0, int(h * 0.80), w, h))))
    per = 10
    for i in range(0, len(crops), per):
        batch = crops[i:i + per]
        W = batch[0][1].size[0]
        H = sum(c.size[1] + 12 for _, c in batch)
        sheet = Image.new("RGB", (W, H), "#333")
        y = 0
        for name, c in batch:
            sheet.paste(c, (0, y)); y += c.size[1] + 12
        out = os.path.join(outdir, f"bottoms-{i//per+1}.png")
        sheet.save(out)
        print(out, "<-", [n for n, _ in batch])

if __name__ == "__main__":
    main()
