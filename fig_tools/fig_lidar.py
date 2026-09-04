"""Topic 6 Figure 1: how LiDAR separates ground from vegetation.

The figure this replaced asserted that the last return is ground, but draws two
unrelated scatters of dots with no pulse, no returns, and nothing connecting
them, so the mechanism was invisible and the claim had to be taken on trust.

This shows it twice: one pulse producing several returns on the left, then
what a whole flight's worth of those looks like as a classified cross-section on
the right, with the two surfaces drawn through the points they come from.

Usage:
    python fig_tools/fig_lidar.py --png
    python fig_tools/fig_lidar.py --out docs/week_06/images
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_side  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line, path,  # noqa: E402
                    rect, render_png, text, translate)

CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)
GROUND = "#8a6a45"
VEG = "#4a8a4a"
BEAM = "#4a90d9"


CROWN = ((0.88, 0.11), (0.72, 0.15), (0.56, 0.13))   # height, radius, of h
CROWN_R = 0.20                                        # overall half-width, of h


def tree(cx, base, h, spread=1.0):
    """A layered crown with gaps in it, so a pulse can find a way through."""
    grp = g(line(cx, base, cx, base - h * 0.62, stroke="#7a5a3a",
                 stroke_width=4, stroke_linecap="round"))
    for i, (dy, r) in enumerate(CROWN):
        grp.add(circle(cx + (h * 0.06 if i == 1 else -h * 0.05) * spread,
                       base - h * dy, h * r * spread, fill=VEG,
                       opacity="0.42"))
    return grp


def canopy_top(x, cx, base, h):
    """A dome over the crown, so the DSM curves instead of stepping."""
    r = h * CROWN_R
    if abs(x - cx) >= r:
        return None
    return base - h * 0.94 * math.sqrt(1 - ((x - cx) / r) ** 2)


# ---------------------------------------------------------------------------
# Left: one pulse, several returns
# ---------------------------------------------------------------------------
def one_pulse(fig):
    fig.add(rect(30, 84, 330, 452, **CARD))
    fig.add(text(195, 114, "One pulse, several returns", text_anchor="middle",
                 font_size=15, font_weight="bold", fill=P["ink"]))

    bx, gy, top = 132, 470, 156
    fig.add(line(60, gy, 330, gy, stroke=GROUND, stroke_width=3,
                 stroke_linecap="round"))
    fig.add(translate(bx, top - 22, aircraft_mini_side(0.5, nose=False)))
    fig.add(tree(bx + 4, gy, 236, 1.0))
    fig.add(circle(bx + 14, gy - 46, 23, fill=VEG, opacity="0.42"))

    # the pulse on its way down
    fig.add(line(bx, top - 6, bx, gy, stroke=BEAM, stroke_width=2,
                 stroke_dasharray="5 5"))

    returns = ((258, "1", "first return", "top of the canopy"),
               (322, "2", "", "a branch further down"),
               (418, "3", "", "low scrub"),
               (gy, "4", "last return", "the ground"))
    for y, n, tag, what in returns:
        last = n == "4"
        fig.add(circle(bx, y, 6.5, fill=BEAM if not last else GROUND,
                       stroke=P["line"], stroke_width=1.5))
        fig.add(text(bx + 66, y - 4, n + (" — " + tag if tag else ""),
                     font_size=11.5, font_weight="bold",
                     fill=GROUND if last else P["ink"]))
        fig.add(text(bx + 66, y + 10, what, font_size=10.5, fill=P["muted"]))

    # the same four, as the sensor actually records them
    tx = 76
    fig.add(line(tx, 250, tx, gy, stroke="#c5cdd5", stroke_width=1.5))
    for y, n, _, _ in returns:
        fig.add(line(tx - 7, y, tx + 7, y, stroke=P["ink"], stroke_width=2.5))
    fig.add(g(text(0, 0, "time after the pulse leaves", text_anchor="middle",
                   font_size=10.5, fill=P["muted"]),
              transform=f"translate({tx - 16},{(250 + gy) / 2}) rotate(-90)"))

    fig.add(text(195, 512, "The last one back came the furthest, so it is the",
                 text_anchor="middle", font_size=11.5, fill=P["muted"]))
    fig.add(text(195, 528, "lowest thing the pulse reached.",
                 text_anchor="middle", font_size=11.5, fill=P["muted"]))


# ---------------------------------------------------------------------------
# Right: a whole flight, classified
# ---------------------------------------------------------------------------
def ground_at(x):
    return 430 + 16 * math.sin((x - 400) / 58)


BUILDING = (686, 752, 122)    # x0, x1, height


def whole_flight(fig):
    fig.add(rect(380, 84, 490, 452, **CARD))
    fig.add(text(625, 114, "Many pulses, sorted into two surfaces",
                 text_anchor="middle", font_size=15, font_weight="bold",
                 fill=P["ink"]))

    x0, x1 = 404, 846
    trees = ((470, 170), (556, 135), (628, 155))
    bx0, bx1, bh = BUILDING

    for cx, h in trees:
        fig.add(tree(cx, ground_at(cx), h, 0.9))
    fig.add(rect(bx0, ground_at((bx0 + bx1) / 2) - bh, bx1 - bx0, bh,
                 fill="#c2cad2", stroke=P["line"], stroke_width=1.5))

    # ground returns, except where a solid roof stops the pulse
    for i in range(60):
        x = x0 + i * (x1 - x0) / 59
        if bx0 - 4 < x < bx1 + 4:
            continue
        fig.add(circle(x, ground_at(x), 2.6, fill=GROUND))
    # roof returns are last returns too, and they are not the ground
    roof_y = ground_at((bx0 + bx1) / 2) - bh
    for i in range(9):
        fig.add(circle(bx0 + 4 + i * (bx1 - bx0 - 8) / 8, roof_y, 2.6,
                       fill=GROUND))
    # canopy returns
    for cx, h in trees:
        base = ground_at(cx)
        for dy, spread in ((0.92, 0.22), (0.78, 0.34), (0.62, 0.30),
                           (0.46, 0.18)):
            for k in range(6):
                x = cx - h * spread / 2 + k * h * spread / 5
                fig.add(circle(x, base - h * dy + (k % 3) * 2.5, 2.4,
                               fill="#2f6b2f"))

    # the two surfaces, drawn through the points they are made of
    dsm = []
    for i in range(90):
        x = x0 + i * (x1 - x0) / 89
        y = ground_at(x)
        for cx, h in trees:
            t = canopy_top(x, cx, ground_at(cx), h)
            if t is not None:
                y = min(y, t)
        if bx0 <= x <= bx1:
            y = min(y, roof_y)
        dsm.append((x, y))
    fig.add(path("M" + " L".join(f"{x0 + i * (x1 - x0) / 89:.0f},"
                                 f"{ground_at(x0 + i * (x1 - x0) / 89):.0f}"
                                 for i in range(90)),
                 fill="none", stroke=BEAM, stroke_width=4.5))
    fig.add(path("M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in dsm),
                 fill="none", stroke=P["bad"], stroke_width=2.2,
                 stroke_dasharray="7 5"))

    lx, ly = x0 + 4, 152
    fig.add(line(lx, ly, lx + 34, ly, stroke=P["bad"], stroke_width=2.2,
                 stroke_dasharray="7 5"))
    fig.add(text(lx + 42, ly + 4, "DSM, red dashed — the top of whatever the",
                 font_size=11, fill=P["ink"]))
    fig.add(text(lx + 42, ly + 19, "pulse hit first: canopy, roof, or ground",
                 font_size=11, fill=P["muted"]))
    fig.add(line(lx, ly + 40, lx + 34, ly + 40, stroke=BEAM, stroke_width=4.5))
    fig.add(text(lx + 42, ly + 44, "DTM, blue solid — ground returns only,",
                 font_size=11, fill=P["ink"]))
    fig.add(text(lx + 42, ly + 59, "with the vegetation classified out",
                 font_size=11, fill=P["muted"]))

    # canopy height is the gap between them
    chx = 556
    fig.add(g(line(chx + 40, ground_at(chx) - 135 * 0.94, chx + 40,
                   ground_at(chx)),
              line(chx + 34, ground_at(chx) - 135 * 0.94, chx + 46,
                   ground_at(chx) - 135 * 0.94),
              line(chx + 34, ground_at(chx), chx + 46, ground_at(chx)),
              stroke=P["ink"], stroke_width=1.8))
    fig.add(text(chx + 52, ground_at(chx) - 58, "canopy", font_size=11,
                 font_weight="bold", fill=P["ink"]))
    fig.add(text(chx + 52, ground_at(chx) - 44, "height", font_size=11,
                 font_weight="bold", fill=P["ink"]))

    ox, lx2 = 796, 754
    fig.add(arrow(ox, ground_at(ox) + 44, ox, ground_at(ox) + 10,
                  color=P["muted"], width=1.8, head=7))
    for i, ln in enumerate(("open ground: nothing above it,",
                            "so both surfaces are identical",
                            "and the dashes ride on the blue")):
        fig.add(text(lx2, ground_at(ox) + 60 + i * 14, ln, text_anchor="middle",
                     font_size=10.5, fill=P["muted"]))

    bcx = (bx0 + bx1) / 2
    fig.add(text(bcx, roof_y - 44, "no ground return here:", text_anchor="middle",
                 font_size=10.5, fill=P["bad"]))
    fig.add(text(bcx, roof_y - 30, "the roof stops the pulse", text_anchor="middle",
                 font_size=10.5, fill=P["bad"]))
    fig.add(arrow(bcx, roof_y - 22, bcx, roof_y - 8, color=P["bad"], width=2,
                  head=7))


def build() -> Figure:
    fig = Figure(900, 610,
                 "How LiDAR separates the ground from what grows on it",
                 "A pulse that finds a gap keeps going. The deepest thing it "
                 "reaches is what you want for a terrain model.")
    one_pulse(fig)
    whole_flight(fig)
    fig.add(text(450, 588,
                 "Under a building there is no ground return at all, so the "
                 "terrain model is interpolated across the footprint.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()
    fname = os.path.join(args.out, figure_name(6, 1, "lidar_returns"))
    build().save(fname)
    print("wrote", fname)
    if args.png:
        png = render_png(fname)
        if png:
            print("wrote", png)


if __name__ == "__main__":
    main()
