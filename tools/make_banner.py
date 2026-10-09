#!/usr/bin/env python3
"""生成 profile 横幅（设计款，无照片依赖）。
1600x400，深墨渐变 + 细网格 + 光晕 + 水波纹线。
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
W, H = 1600, 400


def wave(y_base, amp, period, phase, x0=0, x1=W, step=16):
    pts = []
    x = x0
    while x <= x1:
        y = y_base + amp * math.sin((x / period) * 2 * math.pi + phase)
        pts.append((round(x, 1), round(y, 1)))
        x += step
    d = f"M{pts[0][0]} {pts[0][1]}" + "".join(f"L{x} {y}" for x, y in pts[1:])
    return d


def main():
    os.makedirs(OUT, exist_ok=True)

    waves = []
    # 底部水波纹：越靠下越密、越淡
    for i in range(11):
        t = i / 10.0
        y = 268 + t * 132
        amp = 3.0 * (1 - t) + 0.8
        period = 520 - i * 18
        phase = i * 0.42
        op = 0.095 * (1 - t) ** 1.6 + 0.014
        lw = 1.1 - 0.45 * t
        waves.append(
            f'<path d="{wave(y, amp, period, phase)}" fill="none" '
            f'stroke="#7FC4D8" stroke-opacity="{round(op,3)}" stroke-width="{round(lw,2)}"/>'
        )

    # 上方飘逸弧线
    arcs = []
    for i, (y0, amp, per, ph, op) in enumerate([
        (70, 26, 900, 0.6, 0.30),
        (108, 18, 1150, 2.1, 0.20),
        (150, 12, 1400, 4.0, 0.12),
    ]):
        arcs.append(
            f'<path d="{wave(y0, amp, per, ph)}" fill="none" stroke="#8FD3E8" '
            f'stroke-opacity="{op}" stroke-width="1.1"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Lwo">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#0B1115"/>
    <stop offset="46%" stop-color="#16212A"/>
    <stop offset="100%" stop-color="#22323C"/>
  </linearGradient>
  <radialGradient id="glow1" cx="0.74" cy="0.16" r="0.62">
    <stop offset="0%" stop-color="#5FB0C9" stop-opacity="0.40"/>
    <stop offset="55%" stop-color="#3C7E93" stop-opacity="0.10"/>
    <stop offset="100%" stop-color="#3C7E93" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow2" cx="0.12" cy="0.92" r="0.55">
    <stop offset="0%" stop-color="#2F6B80" stop-opacity="0.26"/>
    <stop offset="100%" stop-color="#2F6B80" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
    <path d="M34 0H0V34" fill="none" stroke="#9DB4C0" stroke-opacity="0.055" stroke-width="1"/>
  </pattern>
  <linearGradient id="fadeTop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#000" stop-opacity="0.22"/>
    <stop offset="35%" stop-color="#000" stop-opacity="0"/>
  </linearGradient>
</defs>

<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect width="{W}" height="{H}" fill="url(#glow1)"/>
<rect width="{W}" height="{H}" fill="url(#glow2)"/>

<g>
{chr(10).join(arcs)}
</g>

<g>
{chr(10).join(waves)}
</g>

<rect width="{W}" height="{H}" fill="url(#fadeTop)"/>
<path d="M0 0.5H{W}" stroke="#B9D6E2" stroke-opacity="0.16" stroke-width="1"/>
<path d="M0 {H-0.5}H{W}" stroke="#B9D6E2" stroke-opacity="0.10" stroke-width="1"/>
</svg>'''

    p = os.path.join(OUT, "banner.svg")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"  -> banner.svg  {len(svg)} bytes")


if __name__ == "__main__":
    main()
