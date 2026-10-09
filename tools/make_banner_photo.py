#!/usr/bin/env python3
"""横版照片裁成通栏横幅（3.56:1）。
源图：tools/src-photo.jpeg（1621x1080，室内老家具场景）
输出：assets/banner.jpg
"""
import os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src-photo.jpeg")
OUT = os.path.join(BASE, "..", "assets", "banner.jpg")

RATIO = 3.56   # 横幅宽高比
CY = 0.54      # 裁切窗口纵向中心（占原图高度的比例，>0.5 = 偏下）


def main():
    src = Image.open(SRC).convert("RGB")
    w, h = src.size
    ch = min(round(w / RATIO), h)
    cy = round(h * CY)
    y0 = max(0, min(h - ch, cy - ch // 2))
    band = src.crop((0, y0, w, y0 + ch))
    band.save(OUT, "JPEG", quality=88, optimize=True)
    print(f"  -> banner.jpg  {band.width}x{band.height} "
          f"(crop y {y0}-{y0 + ch})  {os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
