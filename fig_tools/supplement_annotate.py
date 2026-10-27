"""Draw teaching overlays on FAA testing-supplement crops made by supplement_crops.py.

Usage (from the repository root):
    python fig_tools/supplement_annotate.py [--src docs/part_107_license/images] [--out review]

Writes:
    w05_supp_fig02_load_factor_30deg.png
        The Figure 2 load factor chart with the 30 degree row boxed (1.154) and the same point
        marked on the curve, plus the worked answer to FAA UAG sample question 7
        (33 lb x 1.154 = 38 lb).
    w05_supp_fig26_cooperstown_pattern.jpg
        The Figure 26 Cooperstown crop with the standard left-hand traffic pattern for runway 13
        drawn on it: landing direction toward 130 degrees, the five legs, and an aircraft at
        midfield left downwind (heading 310), which sits north-east of the runway. Answer to FAA
        UAG sample question 18. The chart is public domain (FAA-CT-8080-2H); the overlay is ours
        and is labelled "pattern drawn for teaching".

The airport position in the crop and the runway heading are constants below; the pattern is
built from them, so the geometry always matches the runway number. Pattern size is exaggerated
for legibility (a real pattern is about 1/2 to 1 NM from the runway).
"""
from __future__ import annotations

import argparse
import math
import os

from PIL import Image, ImageDraw, ImageFont

# Cooperstown (S32) airport symbol centre in w05_supp_fig26_cooperstown.jpg, crop pixels.
AIRPORT = (231.0, 184.0)
RUNWAY_HEADING = 130.0          # landing on runway 13
SCALE = 3                       # draw on a 3x upscale so lines stay smooth
RUNWAY_HALF = 22.0              # crop pixels, exaggerated
EXTEND = 26.0                   # upwind and final extensions beyond the runway ends
OFFSET = 62.0                   # downwind distance from the runway, exaggerated
ZOOM = (40, 45, 426, 300)       # crop box (crop pixels) kept around the pattern
CREDIT_H = 34                   # height of the credit strip at the bottom of the source crop

BLUE = (0, 98, 184)
ORANGE = (230, 126, 34)
WHITE = (255, 255, 255)
INK = (26, 26, 26)


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "DejaVuSans-Bold.ttf"] if bold else ["arial.ttf", "DejaVuSans.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def heading_vec(deg: float) -> tuple[float, float]:
    """Unit vector for a compass heading in image coordinates (x east, y down)."""
    r = math.radians(deg)
    return math.sin(r), -math.cos(r)


def arrow(d: ImageDraw.ImageDraw, a, b, colour, width, head=16):
    d.line([a, b], fill=colour, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (+1, -1):
        t = ang + math.pi - s * math.radians(28)
        d.line([b, (b[0] + head * math.cos(t), b[1] + head * math.sin(t))], fill=colour, width=width)


def label(d, xy, text, f, fill=INK, anchor="la"):
    x, y = xy
    box = d.textbbox((x, y), text, font=f, anchor=anchor)
    pad = 5
    d.rounded_rectangle((box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad), radius=6,
                        fill=WHITE, outline=fill, width=2)
    d.text((x, y), text, font=f, fill=fill, anchor=anchor)


def cooperstown(src: str, out: str) -> str:
    base = Image.open(os.path.join(src, "w05_supp_fig26_cooperstown.jpg")).convert("RGB")
    w, h = base.size
    im = base.resize((w * SCALE, h * SCALE), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    S = lambda p: (p[0] * SCALE, p[1] * SCALE)  # noqa: E731

    dx, dy = heading_vec(RUNWAY_HEADING)            # landing direction
    lx, ly = heading_vec(RUNWAY_HEADING - 90.0)     # pilot's left = the pattern side
    assert lx > 0 and ly < 0, "left of 130 degrees must point north-east"
    cx, cy = AIRPORT

    def P(along: float, side: float):
        return (cx + dx * along + lx * side, cy + dy * along + ly * side)

    r1 = P(-RUNWAY_HALF, 0)              # threshold of runway 13 (north-west end)
    r2 = P(+RUNWAY_HALF, 0)              # far end
    up_end = P(RUNWAY_HALF + EXTEND, 0)
    cross_end = P(RUNWAY_HALF + EXTEND, OFFSET)
    down_end = P(-RUNWAY_HALF - EXTEND, OFFSET)
    final_start = P(-RUNWAY_HALF - EXTEND, 0)
    mid_down = P(0, OFFSET)

    lw = 7
    legs = [(r2, up_end, "upwind"), (up_end, cross_end, "crosswind"),
            (cross_end, down_end, "downwind"), (down_end, final_start, "base"),
            (final_start, r1, "final")]
    for a, b, _ in legs:
        arrow(d, S(a), S(b), BLUE, lw)
    d.line([S(r1), S(r2)], fill=INK, width=9)                       # runway, emphasised
    arrow(d, S(P(-RUNWAY_HALF + 4, 0)), S(P(RUNWAY_HALF - 2, 0)), WHITE, 3, head=10)

    f = font(36, bold=True)
    fs = font(30)
    off = 34
    label(d, (S(P(RUNWAY_HALF + EXTEND / 2, 0))[0] + 18, S(P(RUNWAY_HALF + EXTEND / 2, 0))[1] + 10),
          "upwind", fs, BLUE)
    label(d, (S(P(-RUNWAY_HALF - EXTEND / 2, 0))[0] - 18, S(P(-RUNWAY_HALF - EXTEND / 2, 0))[1] - 6),
          "final", fs, BLUE, anchor="ra")
    label(d, (S(P(-RUNWAY_HALF - EXTEND, OFFSET / 2))[0] - 14, S(P(-RUNWAY_HALF - EXTEND, OFFSET / 2))[1]),
          "base", fs, BLUE, anchor="rm")
    label(d, (S(P(RUNWAY_HALF + EXTEND, OFFSET / 2))[0] + 14, S(P(RUNWAY_HALF + EXTEND, OFFSET / 2))[1]),
          "crosswind", fs, BLUE, anchor="lm")

    # aircraft at midfield left downwind, heading 310
    mx, my = S(mid_down)
    d.ellipse((mx - 22, my - 22, mx + 22, my + 22), fill=ORANGE, outline=WHITE, width=4)
    hx, hy = heading_vec(310.0)
    arrow(d, (mx - hx * 12, my - hy * 12), (mx + hx * 30, my + hy * 30), WHITE, 5, head=12)
    label(d, (mx + 30, my - off - 20), "midfield left downwind", f, ORANGE)
    label(d, (mx + 30, my - off + 18), "north-east of the runway", fs, ORANGE)
    label(d, (S(r1)[0] - 30, S(r1)[1] - 34), "RWY 13: land toward 130°", fs, INK, anchor="rb")
    dl = S(P(-RUNWAY_HALF - EXTEND * 0.4, OFFSET))
    label(d, (dl[0] - 12, dl[1] - 14), "downwind, 310°", fs, BLUE, anchor="rb")

    # north arrow
    nx, ny = (ZOOM[2] - 14) * SCALE, (ZOOM[1] + 22) * SCALE
    arrow(d, (nx, ny + 60), (nx, ny), INK, 5, head=14)
    d.text((nx, ny - 8), "N", font=f, fill=INK, anchor="mb")

    # teaching note above the existing credit strip
    note = "Pattern drawn for teaching, not to scale"
    label(d, ((ZOOM[0] + 6) * SCALE, (ZOOM[3] - 6) * SCALE), note, fs, INK, anchor="lb")

    # zoom on the pattern, then re-attach the chart's credit strip from the bottom of the crop
    x0, y0, x1, y1 = ZOOM
    zoomed = im.crop((x0 * SCALE, y0 * SCALE, x1 * SCALE, y1 * SCALE))
    strip_h = CREDIT_H * SCALE
    im = Image.new('RGB', (zoomed.width, zoomed.height + strip_h), WHITE)
    im.paste(zoomed, (0, 0))
    ImageDraw.Draw(im).text((18, zoomed.height + strip_h // 2),
                            'FAA-CT-8080-2H, Figure 26. Public domain. Not for navigation.',
                            font=font(40), fill=INK, anchor='lm')
    im = im.resize((int(im.width / SCALE * 2.4), int(im.height / SCALE * 2.4)), Image.LANCZOS)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "w05_supp_fig26_cooperstown_pattern.jpg")
    im.save(path, quality=88, optimize=True)
    return path


# Figure 2 crop (w05_supp_fig02_load_factor.png, 1030 x 805): table row and graph axes, crop pixels.
LF_ROW_30 = (28, 273, 382, 337)           # the 30 degree row of the table
LF_X0, LF_X90 = 485.0, 990.0              # graph x pixel at 0 and 90 degrees of bank
LF_Y1, LF_Y9 = 580.0, 136.0               # graph y pixel at load factor 1 and 9
LF_AXIS_Y = 636.0                         # bottom of the plotting area


def load_factor(src: str, out: str) -> str:
    im = Image.open(os.path.join(src, 'w05_supp_fig02_load_factor.png')).convert('RGB')
    d = ImageDraw.Draw(im)
    bank = 30.0
    n = 1.0 / math.cos(math.radians(bank))
    assert abs(n - 1.1547) < 1e-3
    x = LF_X0 + (LF_X90 - LF_X0) * bank / 90.0
    y = LF_Y1 - (LF_Y1 - LF_Y9) * (n - 1.0) / 8.0
    d.rounded_rectangle(LF_ROW_30, radius=8, outline=ORANGE, width=6)
    for i in range(int(LF_AXIS_Y), int(y), -14):                      # dashed up from 30 degrees
        d.line([(x, i), (x, max(i - 7, y))], fill=ORANGE, width=4)
    for i in range(int(x), int(LF_X0), -14):                          # dashed across to the axis
        d.line([(i, y), (max(i - 7, LF_X0), y)], fill=ORANGE, width=4)
    d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=ORANGE, outline=WHITE, width=3)
    label(d, (x + 18, y - 70), '30° bank → 1.154', font(30, bold=True), ORANGE)
    label(d, (x + 18, y - 120), '33 lb × 1.154 ≈ 38 lb', font(30, bold=True), INK)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, 'w05_supp_fig02_load_factor_30deg.png')
    im.save(path, optimize=True)
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--src", default="docs/part_107_license/images")
    ap.add_argument("--out", default="review")
    a = ap.parse_args()
    for p in (cooperstown(a.src, a.out), load_factor(a.src, a.out)):
        print("wrote", p, f"{os.path.getsize(p) // 1024} KB")


if __name__ == "__main__":
    main()
