"""Topic 4 Figures 3 and 3b: the reconstruction pipeline and its outputs.

Both draw one recognizable building rather than an abstract scatter, because
the point of Figure 3 is that every stage is the *same scene* at a different
density. The figure these replaced used unrelated dots at each stage, so nothing
carried that.

Four stages, not three: sparse cloud, dense cloud, mesh, textured model. A grid
layout and a version carrying processing cost were also drawn and set aside;
they are in the history if the page layout ever changes.

Usage:
    python fig_tools/fig_pipeline.py --png
    python fig_tools/fig_pipeline.py --out docs/week_04/images
"""
from __future__ import annotations

import argparse
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    polygon, rect, render_png, text, translate)

CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)
K = 0.87


def iso(x, y, z):
    """Standard isometric projection, so every stage draws the same building."""
    return (K * (x - y), 0.5 * (x + y) - z)


W, D, H, RIDGE = 60, 40, 45, 66
# the faces a viewer on this side actually sees, roof first for draw order
FACES = (
    ("roof", (iso(0, D, H), iso(W, D, H), iso(W, D / 2, RIDGE), iso(0, D / 2, RIDGE)), "#b06a5a"),
    ("wall_front", (iso(0, D, 0), iso(W, D, 0), iso(W, D, H), iso(0, D, H)), "#cbd3da"),
    ("wall_side", (iso(W, 0, 0), iso(W, D, 0), iso(W, D, H), iso(W, 0, H)), "#aab4bd"),
    ("gable", (iso(W, D, H), iso(W, 0, H), iso(W, D / 2, RIDGE)), "#b8c1c9"),
)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def face_points(pts, nu, nv, rng=None, jitter=0.0):
    """Sample a grid of points across a quad or triangle."""
    out = []
    for i in range(nu + 1):
        u = i / nu
        for j in range(nv + 1):
            v = j / nv
            if len(pts) == 4:
                p = lerp(lerp(pts[0], pts[1], u), lerp(pts[3], pts[2], u), v)
            else:
                if u + v > 1:
                    continue
                p = (pts[0][0] + (pts[1][0] - pts[0][0]) * u + (pts[2][0] - pts[0][0]) * v,
                     pts[0][1] + (pts[1][1] - pts[0][1]) * u + (pts[2][1] - pts[0][1]) * v)
            if rng and jitter:
                p = (p[0] + rng.uniform(-jitter, jitter),
                     p[1] + rng.uniform(-jitter, jitter))
            out.append(p)
    return out


def edge_points(pts, per_edge):
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        for k in range(per_edge):
            out.append(lerp(a, b, k / per_edge))
    return out


def building(stage, scale=1.0):
    """The same building at one of four reconstruction stages."""
    grp = g()
    rng = random.Random(11)

    if stage == "sparse":
        # tie points cluster on corners and edges, which is where features are
        seen = []
        for _, pts, _ in FACES:
            seen += edge_points(pts, 4)
        for p in seen:
            grp.add(circle(p[0], p[1], 2.4, fill=P["ink"]))
        for _, pts, _ in FACES:
            for p in pts:
                grp.add(circle(p[0], p[1], 3.4, fill=P["accent"]))

    elif stage == "dense":
        for _, pts, col in FACES:
            for p in face_points(pts, 16, 16, rng, 0.9):
                grp.add(circle(p[0], p[1], 1.15, fill=col))

    elif stage == "mesh":
        for _, pts, _ in FACES:
            grp.add(polygon(pts, fill="#f2f5f8", stroke="#9aa7b2",
                            stroke_width=1))
        for _, pts, _ in FACES:
            n = 4
            for i in range(n + 1):
                t = i / n
                if len(pts) == 4:
                    a, b = lerp(pts[0], pts[1], t), lerp(pts[3], pts[2], t)
                    c, d_ = lerp(pts[0], pts[3], t), lerp(pts[1], pts[2], t)
                    grp.add(line(*a, *b, stroke="#8fa3b5", stroke_width=0.8))
                    grp.add(line(*c, *d_, stroke="#8fa3b5", stroke_width=0.8))
                    grp.add(line(*a, *d_, stroke="#c5cdd5", stroke_width=0.6))
                else:
                    a = lerp(pts[0], pts[1], t)
                    b = lerp(pts[0], pts[2], t)
                    grp.add(line(*a, *b, stroke="#8fa3b5", stroke_width=0.8))
            grp.add(polygon(pts, fill="none", stroke=P["line"],
                            stroke_width=1.2))

    else:  # textured
        for _, pts, col in FACES:
            grp.add(polygon(pts, fill=col, stroke=P["line"], stroke_width=1.2))
        # a couple of details, so it reads as photographed rather than shaded
        w = FACES[1][1]
        for u in (0.22, 0.62):
            win = [lerp(lerp(w[0], w[1], u), lerp(w[3], w[2], u), 0.34),
                   lerp(lerp(w[0], w[1], u + 0.16), lerp(w[3], w[2], u + 0.16), 0.34),
                   lerp(lerp(w[0], w[1], u + 0.16), lerp(w[3], w[2], u + 0.16), 0.68),
                   lerp(lerp(w[0], w[1], u), lerp(w[3], w[2], u), 0.68)]
            grp.add(polygon(win, fill="#7d93a8", stroke=P["line"],
                            stroke_width=0.8))

    return g(grp, transform=f"scale({scale})") if scale != 1 else grp


STAGES = (
    ("sparse", "Sparse cloud", "the tie points themselves",
     "hundreds of points"),
    ("dense", "Dense cloud", "a point for almost every pixel",
     "millions of points"),
    ("mesh", "Mesh", "a surface stretched over the points",
     "triangles, not points"),
    ("textured", "Textured model", "the photos draped back on",
     "what you show a client"),
)
# ---------------------------------------------------------------------------
# Figure 3: one row of four stages
# ---------------------------------------------------------------------------
def build_pipeline() -> Figure:
    fig = Figure(900, 400, "From matched points to a model",
                 "The same building at each stage. Only the amount of detail "
                 "changes.")
    cols, w, h, top = (128, 340, 552, 764), 176, 252, 84
    for i, (cx, (stage, title, sub, count)) in enumerate(zip(cols, STAGES)):
        fig.add(rect(cx - w / 2, top, w, h, **CARD))
        fig.add(translate(cx, top + 96, building(stage, 0.86)))
        fig.add(text(cx, top + 176, title, text_anchor="middle", font_size=14,
                     font_weight="bold", fill=P["ink"]))
        fig.add(text(cx, top + 198, sub, text_anchor="middle", font_size=11,
                     fill=P["muted"]))
        fig.add(text(cx, top + 222, count, text_anchor="middle", font_size=11,
                     font_style="italic", fill=P["accent"]))
        if i < 3:
            fig.add(arrow(cx + w / 2 + 5, top + h / 2, cx + w / 2 + 22,
                          top + h / 2, color="#b6c2cc", width=3, head=9))
    fig.add(text(450, 376,
                 "Every stage after the first is derived. Get the tie points "
                 "wrong and nothing downstream can recover.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Companion: where the 2D deliverables come from
# ---------------------------------------------------------------------------
def build_products_branch() -> Figure:
    fig = Figure(900, 470, "From the surface to the deliverables",
                 "The orthophoto and the DSM are the same surface, read two "
                 "different ways.")

    # the surface itself
    fig.add(rect(40, 84, 292, 316, **CARD))
    fig.add(text(186, 114, "The surface", text_anchor="middle", font_size=15,
                 font_weight="bold", fill=P["ink"]))
    fig.add(translate(196, 236, building("textured", 1.5)))
    fig.add(text(186, 356, "meshed from the dense cloud,", text_anchor="middle",
                 font_size=11.5, fill=P["muted"]))
    fig.add(text(186, 374, "with the photos draped over it", text_anchor="middle",
                 font_size=11.5, fill=P["muted"]))

    for y0, label in ((160, "ortho"), (330, "dsm")):
        fig.add(arrow(340, 242, 384, y0 + 24, color="#b6c2cc", width=3,
                      head=10))

    # orthophoto: the same surface photographed straight down, at one scale
    fig.add(rect(400, 84, 460, 152, **CARD))
    fig.add(text(424, 114, "Orthophoto", font_size=15, font_weight="bold",
                 fill=P["ink"]))
    fig.add(text(424, 136, "every pixel put where it truly belongs,",
                 font_size=11.5, fill=P["muted"]))
    fig.add(text(424, 154, "at one constant scale across the whole image",
                 font_size=11.5, fill=P["muted"]))
    ox, oy = 742, 168
    fig.add(rect(ox - 76, oy - 46, 152, 92, fill="#e4ead9", stroke=P["line"],
                 stroke_width=1.2))
    fig.add(rect(ox - 40, oy - 28, 80, 56, fill="#b06a5a", stroke=P["line"],
                 stroke_width=1.2))
    fig.add(line(ox - 40, oy, ox + 40, oy, stroke="#8a4f42", stroke_width=1.5))
    for dx in (-52, 0, 52):
        fig.add(arrow(ox + dx, oy - 68, ox + dx, oy - 52, color=P["accent"],
                      width=2, head=7))
    fig.add(text(ox, oy - 76, "seen from straight above", text_anchor="middle",
                 font_size=10.5, fill=P["accent"]))

    # DSM: the same surface sampled onto a grid of heights
    fig.add(rect(400, 254, 460, 152, **CARD))
    fig.add(text(424, 284, "Surface model (DSM)", font_size=15,
                 font_weight="bold", fill=P["ink"]))
    fig.add(text(424, 306, "the height of that surface, sampled onto",
                 font_size=11.5, fill=P["muted"]))
    fig.add(text(424, 324, "a regular grid, one height per cell",
                 font_size=11.5, fill=P["muted"]))
    gx, gy2, cell = 666, 336, 11
    ramp = ("#e8eee4", "#cfdcc6", "#adc49f", "#8fae7f", "#6d9463")
    for r in range(6):
        for c in range(14):
            inside = 4 <= c <= 9 and 1 <= r <= 4
            lvl = (4 if (5 <= c <= 8 and 2 <= r <= 3) else 3) if inside else                 (1 if (c + r) % 3 else 0)
            fig.add(rect(gx + c * cell, gy2 + r * cell, cell - 1, cell - 1,
                         fill=ramp[lvl]))
    fig.add(text(gx + 7 * cell, gy2 - 8, "low to high", text_anchor="middle",
                 font_size=10.5, fill=P["muted"]))

    fig.add(text(450, 442,
                 "Strip the buildings and vegetation out of that grid and the "
                 "same surface becomes a DTM.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, number, slug, variant in (
        (build_pipeline, 3, "pipeline", ""),
        (build_products_branch, 3, "to_products", "b"),
    ):
        fname = os.path.join(args.out, figure_name(4, number, slug, variant))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
