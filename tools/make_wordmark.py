#!/usr/bin/env python3
"""生成 Lwo 字标 SVG（light / dark 双主题）。
做法：把文字转成矢量路径，输出精确贴合字形包围盒的 viewBox。
"""
import os
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

LIGHT_FILL = "#14181C"
DARK_FILL = "#E6EDF3"


def face(path, index):
    return TTCollection(path).fonts[index]


def build(font_path, index, text, tracking_em, target_height, pad, fill, out_name,
          svg_attrs=''):
    f = face(font_path, index)
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hmtx = f["hmtx"]
    upem = f["head"].unitsPerEm

    tracking = tracking_em * upem
    x = 0.0
    glyphs = []          # (glyph_name, x_offset)
    for ch in text:
        gname = cmap[ord(ch)]
        glyphs.append((gname, x))
        x += hmtx[gname][0] + tracking
    total_w = x - tracking  # 去掉末尾字距

    # 包围盒
    minx, miny, maxx, maxy = 1e9, 1e9, -1e9, -1e9
    for gname, off in glyphs:
        bp = BoundsPen(gs)
        gs[gname].draw(bp)
        if bp.bounds is None:
            continue
        x0, y0, x1, y1 = bp.bounds
        minx = min(minx, x0 + off); maxx = max(maxx, x1 + off)
        miny = min(miny, y0);       maxy = max(maxy, y1)

    bbox_w = maxx - minx
    bbox_h = maxy - miny
    s = target_height / bbox_h
    vw = round(bbox_w * s + pad * 2, 2)
    vh = round(target_height + pad * 2, 2)

    tx = pad - minx * s
    ty = pad + maxy * s

    paths = []
    for gname, off in glyphs:
        pen = SVGPathPen(gs)
        from fontTools.pens.transformPen import TransformPen
        from fontTools.misc.transform import Transform
        tp = TransformPen(pen, Transform(1, 0, 0, 1, off, 0))
        gs[gname].draw(tp)
        d = pen.getCommands()
        if d:
            paths.append(d)

    body = "".join(f'<path d="{d}"/>' for d in paths)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{vw}" height="{vh}" '
        f'viewBox="0 0 {vw} {vh}" role="img" aria-label="{text}"{svg_attrs}>'
        f'<g transform="translate({round(tx,3)} {round(ty,3)}) '
        f'scale({round(s,6)} {round(-s,6)})" fill="{fill}">{body}</g></svg>'
    )
    p = os.path.join(OUT, out_name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"  -> {out_name}  {vw}x{vh}  ({len(svg)} bytes)")
    return p


def main():
    os.makedirs(OUT, exist_ok=True)
    AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
    print("[main] Avenir Next Heavy")

    # 主推：Avenir Next Heavy, "Lwo"
    for fill, name in ((LIGHT_FILL, "wordmark-light.svg"), (DARK_FILL, "wordmark-dark.svg")):
        build(AVENIR, 8, "Lwo", 0.04, 100.0, 10.0, fill, name)

    # 备选 A：Futura Bold 全大写
    print("[alt-a] Futura Bold")
    for fill, name in ((LIGHT_FILL, "wordmark-alt-a-light.svg"), (DARK_FILL, "wordmark-alt-a-dark.svg")):
        build("/System/Library/Fonts/Supplemental/Futura.ttc", 2, "LWO", 0.10, 100.0, 10.0, fill, name)

    # 备选 B：Gill Sans UltraBold
    print("[alt-b] Gill Sans UltraBold")
    for fill, name in ((LIGHT_FILL, "wordmark-alt-b-light.svg"), (DARK_FILL, "wordmark-alt-b-dark.svg")):
        build("/System/Library/Fonts/Supplemental/GillSans.ttc", 6, "Lwo", 0.05, 100.0, 10.0, fill, name)


if __name__ == "__main__":
    main()
