"""Mechanism figures for How Photos Become 3D (Week 7).

The reading's original drawings show the *outcomes* of structure from motion:
parallax, overlap, the four stages of one building, the surface read as a
picture or a grid. These eleven show the *mechanisms* between them, one per
drawing, for the Week 7 lecture deck:

    w04_fig01_pipeline_overview.svg   six stages, four Bentley buttons
    w04_fig02b_triangle_math.svg      the triangle, with the numbers
    w04_fig03_camera_solve.svg        cameras and points solved together
    w04_fig05_features.svg            where the software finds points
    w04_fig06_matching.svg            fingerprints, matches, one rejected
    w04_fig06b_sift.svg               SIFT in four steps
    w04_fig06c_ransac.svg             RANSAC: the majority decides
    w04_fig08_dense_matching.svg      one pixel, one line, one depth
    w04_fig09_meshing.svg             points to triangles; the webbed pole
    w04_fig11_dem_grid.svg            the surface sampled on a grid
    w04_fig10_orthorectification.svg  relief displacement and its removal

Numbers 2, 4, 7 and 12 are the original figures (fig_week04.py and
fig_pipeline.py); 13 to 21 are Planning the Flight. The w04_ set is one
sequence in nav order across the two readings. 2b, 6b and 6c are lettered
variants that sit beside the figure they extend, so adding them moved no
number.

Usage:
    python fig_tools/fig_sfm.py --png
    python fig_tools/fig_sfm.py --out docs/gen_reading/images
"""
from __future__ import annotations

import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import car  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (El, Figure, arrow, circle, figure_name, g,  # noqa: E402
                    line, path, polygon, rect, render_png, text,
                    translate)

W = 900
CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)
GREEN = "#2f8f4e"
ORANGE = P["warn"]
BLUE = P["accent"]
RED = P["bad"]


def _t(fig, x, y, s, size=12, bold=False, fill=None, anchor="middle",
       italic=False):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 font_style="italic" if italic else None,
                 fill=fill or P["ink"]))


def camera(x, y, scale=1.0, tilt=0.0, colour=None):
    """A small camera glyph seen from the side, lens pointing down."""
    colour = colour or P["dark"]
    s = scale
    body = g(rect(-16 * s, -9 * s, 32 * s, 18 * s, rx=3 * s, fill=colour),
             rect(-6 * s, 9 * s, 12 * s, 7 * s, fill=colour),
             circle(0, 18 * s, 4 * s, fill=P["screen"], stroke=colour,
                    stroke_width=1.5),
             transform=f"rotate({tilt})")
    return translate(x, y, body)


# ---------------------------------------------------------------------------
# 1. Pipeline overview: six stages, four buttons
# ---------------------------------------------------------------------------
STAGES = [
    ("Photos", "with GPS tags"),
    ("Features", "and matches"),
    ("Cameras", "+ sparse cloud"),
    ("Dense cloud", "millions of points"),
    ("Mesh", "and texture"),
    ("Products", "ortho, DSM, 3D"),
]
BUTTONS = [("Import photos", 0, 0), ("Aerotriangulation", 1, 2),
           ("Reconstruction", 3, 4), ("Production", 5, 5)]


def build_pipeline_overview() -> Figure:
    fig = Figure(W, 400, "Six stages, four buttons",
                 "What structure from motion does, and what the software "
                 "calls each part of it.")
    n = len(STAGES)
    bw, bh, gap = 124, 78, 18
    x0 = (W - (n * bw + (n - 1) * gap)) / 2
    y = 120
    xs = []
    for i, (head, sub) in enumerate(STAGES):
        x = x0 + i * (bw + gap)
        xs.append(x)
        fig.add(rect(x, y, bw, bh, rx=10, fill=P["white"], stroke=BLUE,
                     stroke_width=1.8))
        _t(fig, x + bw / 2, y + 34, head, size=13.5, bold=True)
        _t(fig, x + bw / 2, y + 56, sub, size=11, fill=P["muted"])
        if i < n - 1:
            fig.add(arrow(x + bw + 2, y + bh / 2, x + bw + gap - 2,
                          y + bh / 2, color=BLUE, width=2, head=7))
    # small glyphs above the boxes
    gy = y - 26
    fig.add(rect(xs[0] + bw / 2 - 14, gy - 10, 28, 20, rx=3, fill=P["body"],
                 stroke=P["line"], stroke_width=1))
    for k in range(5):
        fig.add(circle(xs[1] + bw / 2 - 20 + k * 10, gy, 2.5, fill=BLUE))
    fig.add(camera(xs[2] + bw / 2, gy - 2, 0.55))
    rnd = random.Random(3)
    for _ in range(40):
        fig.add(circle(xs[3] + bw / 2 - 24 + rnd.random() * 48,
                       gy - 8 + rnd.random() * 16, 1.2, fill=P["dark"]))
    fig.add(path(f"M{xs[4] + bw / 2 - 22},{gy + 8} l14,-16 l14,16 l14,-16 "
                 f"l14,16 M{xs[4] + bw / 2 - 8},{gy + 8} l14,-16",
                 fill="none", stroke=P["dark"], stroke_width=1.2))
    fig.add(rect(xs[5] + bw / 2 - 16, gy - 9, 32, 18, fill=P["screen"],
                 stroke=P["line"], stroke_width=1))

    # Bentley's buttons as brackets under the stages
    by = y + bh + 40
    for label, i0, i1 in BUTTONS:
        xa, xb = xs[i0], xs[i1] + bw
        fig.add(path(f"M{xa},{by - 8} V{by} H{xb} V{by - 8}", fill="none",
                     stroke=ORANGE, stroke_width=2))
        fig.add(rect((xa + xb) / 2 - 62, by + 12, 124, 26, rx=13,
                     fill="#fdf3e6", stroke=ORANGE, stroke_width=1.5))
        _t(fig, (xa + xb) / 2, by + 29, label, size=11.5, bold=True)
    _t(fig, W / 2, by + 64, "Bentley iTwin Capture Modeler, the four steps "
       "you click", size=11.5, fill=P["muted"])
    _t(fig, W / 2, 372,
       "The software does the arithmetic. The photos decide whether the "
       "arithmetic has anything to work with.", size=12.5, fill=P["muted"],
       italic=True)
    return fig


# ---------------------------------------------------------------------------
# 2b. The triangle, with the numbers
# ---------------------------------------------------------------------------
def _arc(cx, cy, r, a0, a1):
    """SVG path for an arc about (cx, cy). Angles are in degrees from straight
    down, positive toward +x, so they read the way a nadir angle does."""
    def pt(a):
        return (cx + r * math.sin(math.radians(a)),
                cy + r * math.cos(math.radians(a)))
    (x0, y0), (x1, y1) = pt(a0), pt(a1)
    sweep = 0 if a1 > a0 else 1
    return f"M{x0:.1f},{y0:.1f} A{r},{r} 0 0 {sweep} {x1:.1f},{y1:.1f}"


def build_triangle_math() -> Figure:
    b, alpha, beta = 40.0, 32.0, 25.0
    ta = math.tan(math.radians(alpha))       # 0.6249
    tb = math.tan(math.radians(beta))        # 0.4663
    d = b / (ta + tb)                        # 36.66 m
    off_a = d * ta                           # 22.9 m
    fig = Figure(W, 520, "The triangle, with the numbers",
                 "Side view. The baseline b comes from the GPS tags; the angles "
                 "α and β come from where P sits in each photo.")
    fig.add(rect(30, 84, 520, 394, **CARD))
    k = 7.0                                  # pixels per metre
    ax, bx, ly = 150, 150 + b * k, 182       # ly: the lens line, where rays start
    fx, py = ax + off_a * k, ly + d * k

    # the baseline, measured from GPS
    mid, dim_y = (ax + bx) / 2, 138
    for end in (ax, bx):
        fig.add(arrow(mid, dim_y, end, dim_y, color=P["muted"], width=1.4,
                      head=7))
        fig.add(line(end, dim_y - 6, end, dim_y + 6, stroke=P["muted"],
                     stroke_width=1.4))
    _t(fig, mid, 110, f"baseline b = {b:.0f} m", size=13, bold=True)
    _t(fig, mid, 126, "measured from GPS", size=11, fill=P["muted"])

    # the camera line, split where the drop to P meets it
    fig.add(line(ax, ly, bx, ly, stroke="#9aa7b2", stroke_width=1.5))
    for x in (ax, fx, bx):
        fig.add(line(x, ly - 5, x, ly + 5, stroke=P["dark"], stroke_width=1.5))
    _t(fig, (ax + fx) / 2, ly + 22, "d·tan α", size=13, bold=True, fill=ORANGE)
    _t(fig, (fx + bx) / 2, ly + 22, "d·tan β", size=13, bold=True, fill=GREEN)

    # ground, the drop, the two rays
    fig.add(line(60, py, 520, py, stroke="#9aa7b2", stroke_width=3,
                 stroke_linecap="round"))
    fig.add(line(fx, ly, fx, py, stroke=BLUE, stroke_width=1.6,
                 stroke_dasharray="6 4"))
    _t(fig, fx - 10, ly + 122, "depth d", size=13, bold=True, fill=BLUE,
       anchor="end")
    fig.add(line(ax, ly, fx, py, stroke=ORANGE, stroke_width=2))
    fig.add(line(bx, ly, fx, py, stroke=GREEN, stroke_width=2))

    # each angle measured from straight down (nadir)
    for x in (ax, bx):
        fig.add(line(x, ly, x, ly + 62, stroke=P["muted"], stroke_width=1.2,
                     stroke_dasharray="4 3"))
    fig.add(path(_arc(ax, ly, 50, 0, alpha), fill="none", stroke=ORANGE,
                 stroke_width=2))
    fig.add(path(_arc(bx, ly, 50, 0, -beta), fill="none", stroke=GREEN,
                 stroke_width=2))
    # labels tucked under their arcs, the inner end kept 8 px off the ray
    lab_y = ly + 80
    _t(fig, ax + (lab_y - ly - 12) * ta - 8, lab_y, f"α = {alpha:.0f}°",
       size=13, bold=True, fill=ORANGE, anchor="end")
    _t(fig, bx - (lab_y - ly - 12) * tb + 8, lab_y, f"β = {beta:.0f}°",
       size=13, bold=True, fill=GREEN, anchor="start")

    fig.add(circle(fx, py, 7, fill=BLUE, stroke=P["white"], stroke_width=1.5))
    _t(fig, fx + 14, py + 20, "P", size=13, bold=True, fill=BLUE,
       anchor="start")
    for x, name, anchor, dx in ((ax, "A", "end", -26), (bx, "B", "start", 26)):
        fig.add(camera(x, ly - 18))
        _t(fig, x + dx, ly - 13, name, size=14, bold=True, anchor=anchor)

    # the derivation
    x0 = 570
    fig.add(rect(x0, 84, 300, 394, **CARD))
    _t(fig, x0 + 150, 112, "The arithmetic", size=13.5, bold=True)
    tx, y = x0 + 22, 150
    for note, eq in (
        ("the two offsets make up the baseline", "d·tan α + d·tan β = b"),
        ("take d out and divide both sides", "d = b / (tan α + tan β)"),
        (f"tan {alpha:.0f}° = {ta:.3f}, tan {beta:.0f}° = {tb:.3f}",
         f"d = {b:.0f} / ({ta:.3f} + {tb:.3f}) = {d:.1f} m"),
    ):
        _t(fig, tx, y, note, size=11.5, fill=P["muted"], anchor="start")
        _t(fig, tx, y + 24, eq, size=14, anchor="start")
        y += 74
    _t(fig, tx, y, f"offset from A: {d:.1f} × {ta:.3f} = {off_a:.1f} m",
       size=11.5, fill=P["muted"], anchor="start")
    fig.add(rect(x0 + 12, y + 12, 276, 62, rx=8, fill="#e8f1fb", stroke=BLUE,
                 stroke_width=1.2))
    _t(fig, tx, y + 38, f"the point is {d:.1f} m below the cameras", size=13,
       bold=True, anchor="start")
    _t(fig, tx, y + 60, f"and {off_a:.1f} m from A", size=13, bold=True,
       anchor="start")

    _t(fig, W / 2, 506,
       "Two known positions, two measured angles, one unknown: with GPS for b "
       "and the photos for α and β, every tie point is a triangle like this.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 3. Cameras and points solved together
# ---------------------------------------------------------------------------
def build_camera_solve() -> Figure:
    fig = Figure(W, 540, "Where was the camera? Where is the point? Solved together",
                 "Every matched point sends one ray from every photo that saw "
                 "it. Move cameras and points until the rays agree.")
    fig.add(rect(30, 84, 560, 420, **CARD))
    gy = 440
    fig.add(line(60, gy, 560, gy, stroke="#9aa7b2", stroke_width=3,
                 stroke_linecap="round"))
    cams = [(130, 150), (300, 130), (470, 150)]
    pts = [(170, 400, GREEN), (310, 380, BLUE), (440, 405, ORANGE)]
    for (px, py, col) in pts:
        for (cx, cy) in cams:
            fig.add(line(cx, cy + 16, px, py, stroke=col, stroke_width=1.3,
                         opacity="0.75"))
    for i, (cx, cy) in enumerate(cams):
        fig.add(camera(cx, cy, 0.9))
        _t(fig, cx, cy - 22, f"photo {'ABC'[i]}", size=12, bold=True)
    for (px, py, col) in pts:
        fig.add(circle(px, py, 7, fill=col, stroke=P["white"],
                       stroke_width=1.5))
    _t(fig, 170, 426, "P", size=12, bold=True, fill=GREEN)
    _t(fig, 310, 426, "Q", size=12, bold=True, fill=BLUE)
    _t(fig, 440, 426, "R", size=12, bold=True, fill=ORANGE)
    _t(fig, 310, 480, "three cameras, three points, nine rays: one solve",
       size=12, fill=P["muted"])

    # inset: a ray that misses
    fig.add(rect(610, 84, 260, 420, **CARD))
    _t(fig, 740, 112, "A ray that misses", size=13.5, bold=True)
    ix, iy = 740, 300
    fig.add(camera(700, 170, 0.8))
    fig.add(circle(ix, iy, 7, fill=BLUE, stroke=P["white"], stroke_width=1.5))
    fig.add(line(700, 186, ix + 26, iy + 14, stroke=RED, stroke_width=1.6,
                 stroke_dasharray="5 4"))
    fig.add(line(ix, iy, ix + 26, iy + 14, stroke=RED, stroke_width=2))
    _t(fig, 790, 322, "error", size=11, bold=True, fill=RED)
    fig.add(arrow(700, 150, 726, 150, color=GREEN, width=2, head=7))
    fig.add(arrow(ix - 2, iy - 12, ix - 2, iy - 30, color=GREEN, width=2,
                  head=7))
    _t(fig, 740, 372, "nudge the camera and the point", size=11.5,
       fill=P["muted"])
    _t(fig, 740, 390, "until the miss is as small as it", size=11.5,
       fill=P["muted"])
    _t(fig, 740, 408, "can be for every ray at once", size=11.5,
       fill=P["muted"])
    _t(fig, 740, 446, "This is bundle adjustment.", size=12, bold=True)
    _t(fig, 740, 466, "Bentley: aerotriangulation.", size=12,
       fill=P["muted"])

    _t(fig, W / 2, 526,
       "The GPS tag on each photo is the first guess and sets the scale. "
       "The photos themselves do the rest.", size=12.5, fill=P["muted"],
       italic=True)
    return fig


# ---------------------------------------------------------------------------
# 5. Where the software finds points
# ---------------------------------------------------------------------------
def _scene(fig, ox, oy, scale=1.0, shift=0.0):
    """A simple site scene inside a photo frame at (ox, oy): building corner,
    manhole, parked car, stripes, a tree, blank asphalt. `shift` slides the
    content sideways to fake a second viewpoint."""
    s = scale
    dx = shift
    # asphalt
    fig.add(rect(ox, oy, 380 * s, 260 * s, fill="#e6e8ea"))
    # building (top-left), with a roof edge
    fig.add(polygon([(ox + (20 + dx) * s, oy + 20 * s), (ox + (150 + dx) * s, oy + 20 * s),
                     (ox + (150 + dx) * s, oy + 120 * s), (ox + (90 + dx) * s, oy + 120 * s),
                     (ox + (90 + dx) * s, oy + 80 * s), (ox + (20 + dx) * s, oy + 80 * s)],
                    fill="#c2cad2", stroke=P["line"], stroke_width=1.2))
    # stripes (bottom-left)
    for k in range(6):
        x = ox + (30 + dx + k * 22) * s
        fig.add(line(x, oy + 180 * s, x, oy + 240 * s, stroke=P["white"],
                     stroke_width=3 * s))
    # manhole
    fig.add(circle(ox + (250 + dx) * s, oy + 90 * s, 9 * s, fill="#8a8f94",
                   stroke=P["line"], stroke_width=1))
    # car
    fig.add(car(ox + (300 + dx) * s, oy + 200 * s, 0.7 * s))
    # tree
    fig.add(circle(ox + (330 + dx) * s, oy + 60 * s, 24 * s, fill="#8cb87a",
                   stroke="#5f8a4d", stroke_width=1.2))
    fig.add(circle(ox + (345 + dx) * s, oy + 48 * s, 14 * s, fill="#9cc48a",
                   stroke="none"))


def build_features() -> Figure:
    fig = Figure(W, 520, "Where the software finds its points",
                 "A tie point has to be findable again in the next photo. "
                 "Corners and texture are; blank and repeating surfaces are not.")
    ox, oy = 60, 100
    fig.add(rect(ox - 8, oy - 8, 396, 276, rx=6, fill=P["white"],
                 stroke=P["line"], stroke_width=1.5))
    _scene(fig, ox, oy)
    good = [(20, 20), (150, 20), (150, 120), (90, 120), (90, 80), (20, 80),
            (250, 90), (300, 200), (330, 60), (318, 42), (345, 76)]
    for (x, y) in good:
        fig.add(circle(ox + x, oy + y, 6, fill="none", stroke=GREEN,
                       stroke_width=2))
    # the two "no" regions
    fig.add(rect(ox + 200, oy + 140, 80, 60, rx=6, fill="none", stroke=RED,
                 stroke_width=1.8, stroke_dasharray="6 4"))
    fig.add(rect(ox + 22, oy + 174, 130, 72, rx=6, fill="none", stroke=RED,
                 stroke_width=1.8, stroke_dasharray="6 4"))

    # legend and notes
    fig.add(rect(480, 92, 390, 390, **CARD))
    fig.add(circle(506, 124, 6, fill="none", stroke=GREEN, stroke_width=2))
    _t(fig, 522, 128, "Keypoints: corners, edges that end, texture",
       size=12.5, bold=True, anchor="start")
    _t(fig, 522, 148, "A building corner, a manhole lid, the edge of a",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 522, 164, "car, the texture of a tree canopy. Each one",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 522, 180, "looks like itself and like nothing nearby.",
       size=11.5, fill=P["muted"], anchor="start")

    fig.add(rect(500, 206, 12, 12, rx=2, fill="none", stroke=RED,
                 stroke_width=1.8, stroke_dasharray="3 2"))
    _t(fig, 522, 217, "Blank asphalt: nothing to grab", size=12.5, bold=True,
       anchor="start")
    _t(fig, 522, 237, "Every pixel looks like every other pixel. The",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 522, 253, "software finds no point here, and the model",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 522, 269, "will be smooth and vague across it.",
       size=11.5, fill=P["muted"], anchor="start")

    fig.add(rect(500, 295, 12, 12, rx=2, fill="none", stroke=RED,
                 stroke_width=1.8, stroke_dasharray="3 2"))
    _t(fig, 522, 306, "Identical stripes: the wrong thing to grab",
       size=12.5, bold=True, anchor="start")
    _t(fig, 522, 326, "Every stripe looks like every other stripe, so a",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 522, 342, "point found here is matched to the wrong stripe",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 522, 358, "in the next photo. Worse than blank.",
       size=11.5, fill=P["muted"], anchor="start")

    _t(fig, 675, 404, "Thousands of these per photo, found automatically.",
       size=11.5, fill=P["muted"])
    _t(fig, 675, 422, "You never pick them. You fly so that they exist.",
       size=11.5, fill=P["muted"])
    _t(fig, 675, 458, "Overcast light helps: no hard shadows that move",
       size=11, fill=P["muted"], italic=True)
    _t(fig, 675, 474, "between photos and look like features.",
       size=11, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 6. Fingerprints and matches
# ---------------------------------------------------------------------------
def _fingerprint(fig, x, y, seed, size=4):
    rnd = random.Random(seed)
    for r in range(3):
        for c in range(3):
            v = rnd.random()
            shade = "#1a1a1a" if v > 0.66 else ("#8a8f94" if v > 0.33
                                                 else "#e6e8ea")
            fig.add(rect(x + c * size, y + r * size, size, size, fill=shade,
                         stroke="#ffffff", stroke_width=0.4))


def build_matching() -> Figure:
    fig = Figure(W, 540, "Matching: a fingerprint for every point",
                 "The pixels around a keypoint are summarised into a small "
                 "pattern. Patterns that agree across two photos are a match.")
    axo, ayo = 40, 100
    bxo, byo = 490, 100
    sc = 0.95
    for (ox, oy, lab, sh) in ((axo, ayo, "photo A", 0), (bxo, byo, "photo B", -18)):
        fig.add(rect(ox - 8, oy - 8, 380 * sc + 16, 260 * sc + 16, rx=6,
                     fill=P["white"], stroke=P["line"], stroke_width=1.5))
        _scene(fig, ox, oy, sc, shift=sh)
        _t(fig, ox + 190 * sc, oy - 16, lab, size=12.5, bold=True)

    pairs = [((150, 20), 11), ((150, 120), 12), ((250, 90), 13),
             ((330, 60), 14), ((300, 200), 15)]
    for (pt, seed) in pairs:
        ax, ay = axo + pt[0] * sc, ayo + pt[1] * sc
        bx, by = bxo + (pt[0] - 18) * sc, byo + pt[1] * sc
        for (x, y) in ((ax, ay), (bx, by)):
            fig.add(circle(x, y, 6, fill="none", stroke=GREEN, stroke_width=2))
        fig.add(line(ax + 6, ay, bx - 6, by, stroke=GREEN, stroke_width=1.3,
                     opacity="0.8"))
        _fingerprint(fig, ax + 9, ay - 20, seed)
        _fingerprint(fig, bx + 9, by - 20, seed)
    # one wrong match: a stripe in A to a different stripe in B
    ax, ay = axo + 74 * sc, ayo + 232 * sc
    bx, by = bxo + (118 - 18) * sc, byo + 232 * sc
    for (x, y) in ((ax, ay), (bx, by)):
        fig.add(circle(x, y, 6, fill="none", stroke=RED, stroke_width=2))
    fig.add(line(ax + 6, ay, bx - 6, by, stroke=RED, stroke_width=1.6,
                 stroke_dasharray="6 4"))
    _fingerprint(fig, ax + 9, ay - 20, 21)
    _fingerprint(fig, bx + 9, by - 20, 21)
    mx, my = (ax + bx) / 2, ay
    fig.add(line(mx - 7, my - 7, mx + 7, my + 7, stroke=RED, stroke_width=2.5))
    fig.add(line(mx - 7, my + 7, mx + 7, my - 7, stroke=RED, stroke_width=2.5))

    fig.add(rect(40, 380, 400, 110, **CARD))
    _t(fig, 60, 406, "Green: fingerprints agree, geometry agrees",
       size=12.5, bold=True, anchor="start")
    _t(fig, 60, 428, "The same corner, the same manhole, the same car,",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 60, 444, "shifted the way everything else shifted between",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 60, 460, "the two photos. Kept as tie points.",
       size=11.5, fill=P["muted"], anchor="start")

    fig.add(rect(460, 380, 410, 110, rx=10, fill="#fdf3e6", stroke=ORANGE,
                 stroke_width=1.5))
    _t(fig, 480, 406, "Red: fingerprints agree, geometry does not",
       size=12.5, bold=True, anchor="start")
    _t(fig, 480, 428, "Two identical stripes produce identical fingerprints.",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 480, 444, "The match points the wrong way compared with every",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 480, 460, "other match, so it is thrown out (RANSAC).",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, W / 2, 522,
       "A fingerprint is built so that it survives a change of scale and "
       "rotation: the next photo was taken from somewhere else.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 6b. SIFT in four steps
# ---------------------------------------------------------------------------
# The test patch is a building corner seen from above: an L-shaped roof on
# asphalt, in patch units (0..1 across, 0..1 down). The keypoint is the roof's
# outer corner.
_U0, _U1, _U2 = 0.10, 0.36, 0.58
_V0, _V1, _V2 = 0.40, 0.66, 0.90
L_ROOF = [(_U0, _V0), (_U2, _V0), (_U2, _V2), (_U1, _V2), (_U1, _V1),
          (_U0, _V1)]
L_CORNER = (_U2, _V0)
ASPHALT = "#e6e8ea"
GRADIENT = "#8a8f94"
PATCH_W, PATCH_H = 156, 124
# Card 2 draws three up-pointing gradient arrows on the top edge and two
# right-pointing ones on the side, so the dominant direction is their sum.
ORIENT = math.degrees(math.atan2(3, 2))      # 56 degrees above level


def _on_roof(u, v):
    return ((_U0 <= u <= _U2 and _V0 <= v <= _V1)
            or (_U1 <= u <= _U2 and _V0 <= v <= _V2))


def _patch(fig, x, y, w, h, blur=0.0):
    """Draw the test patch with its top-left at (x, y); return the keypoint.
    blur > 0 fakes a blur by stacking 49 faint copies of the roof shifted up
    to `blur` px each way, so the edges go soft and the middle stays dark."""
    fig.add(rect(x, y, w, h, fill=ASPHALT, stroke=P["line"], stroke_width=1))
    pts = [(round(x + u * w, 1), round(y + v * h, 1)) for (u, v) in L_ROOF]
    if blur <= 0:
        fig.add(polygon(pts, fill=P["dark"]))
    else:
        steps = [i / 3 - 1 for i in range(7)]
        op = 1 - 0.04 ** (1 / len(steps) ** 2)    # all 49 overlapping: 96 %
        grp = g(fill=P["dark"])
        for sx in steps:
            for sy in steps:
                grp.add(polygon([(round(px + sx * blur, 2),
                                  round(py + sy * blur, 2))
                                 for (px, py) in pts],
                                fill_opacity=f"{op:.3f}"))
        fig.add(grp)
    return x + L_CORNER[0] * w, y + L_CORNER[1] * h


def _box_blur(img, r):
    """Separable box blur of a square list-of-lists image."""
    def rows(a):
        return [[sum(row[max(0, i - r):i + r + 1])
                 / len(row[max(0, i - r):i + r + 1]) for i in range(len(row))]
                for row in a]
    cols = rows([list(c) for c in zip(*rows(img))])
    return [list(c) for c in zip(*cols)]


def _sift_descriptor(size, turn):
    """The 4 x 4 cells x 8 directions gradient histogram of the test patch,
    sampled in a size-by-size window centred on the keypoint with the patch
    turned by `turn` degrees, the way SIFT samples it. Returns 16 cells of 8
    values, row by row, scaled 0..1. Direction 0 points right, 2 down."""
    kx, ky = L_CORNER[0] * PATCH_W, L_CORNER[1] * PATCH_H
    c, s = math.cos(math.radians(-turn)), math.sin(math.radians(-turn))
    img = []
    for j in range(size):
        dy = j + 0.5 - size / 2
        row = []
        for i in range(size):
            dx = i + 0.5 - size / 2
            # undo the turn to find where this window pixel sits on the patch
            u = (kx + dx * c - dy * s) / PATCH_W
            v = (ky + dx * s + dy * c) / PATCH_H
            row.append(0.25 if _on_roof(u, v) else 0.9)
        img.append(row)
    img = _box_blur(_box_blur(img, 2), 2)
    cell = size / 4
    hist = [[0.0] * 8 for _ in range(16)]
    for j in range(1, size - 1):
        for i in range(1, size - 1):
            gx = img[j][i + 1] - img[j][i - 1]
            gy = img[j + 1][i] - img[j - 1][i]
            m = math.hypot(gx, gy)
            if m > 1e-9:
                k = round(math.degrees(math.atan2(gy, gx)) / 45) % 8
                hist[int(j // cell) * 4 + int(i // cell)][k] += m
    top = max(max(h) for h in hist)
    rnd = random.Random(61)
    # a real photo has texture everywhere, so no direction is ever quite zero
    return [[0.12 + 0.18 * rnd.random() + 0.7 * v / top for v in h]
            for h in hist]


def build_sift() -> Figure:
    fig = Figure(W, 520, "SIFT in four steps",
                 "SIFT (scale-invariant feature transform) turns the pixels "
                 "around a corner into 128 numbers that the same corner gives "
                 "again in the next photo.")
    cw, gap, x0 = 204, 12, 24
    heads = ("Blur at several scales", "Give it an orientation",
             "Describe the neighbourhood", "The descriptor")
    cxs = []
    for i, head in enumerate(heads):
        x = x0 + i * (cw + gap)
        cxs.append(x + cw / 2)
        fig.add(rect(x, 84, cw, 392, **CARD))
        fig.add(circle(x + cw / 2, 110, 11, fill=BLUE))
        _t(fig, x + cw / 2, 114, str(i + 1), size=12, bold=True,
           fill=P["white"])
        _t(fig, x + cw / 2, 142, head, size=13, bold=True)

    # 1. the same patch, blurrier each time; the corner survives
    cx = cxs[0]
    for k, (blur, lab) in enumerate(((0, "sharp"), (2, "blurred"),
                                     (4.5, "blurred more"))):
        y = 160 + k * 84
        kx, ky = _patch(fig, cx - 70, y, 90, 70, blur)
        fig.add(circle(kx, ky, 8, fill="none", stroke=GREEN, stroke_width=2))
        _t(fig, cx + 30, y + 39, lab, size=11, fill=P["muted"],
           anchor="start")
    _t(fig, cx, 436, "a corner that survives", size=11.5, fill=P["muted"])
    _t(fig, cx, 452, "blurring is a keypoint", size=11.5, fill=P["muted"])

    # 2. gradients point from dark to light; their sum is the orientation
    cx = cxs[1]
    kx, ky = _patch(fig, cx - PATCH_W / 2, 224, PATCH_W, PATCH_H)
    for dx in (14, 32, 50):
        fig.add(arrow(kx - dx, ky + 8, kx - dx, ky - 16, color=GRADIENT,
                      width=1.8, head=6))
    for dy in (16, 36):
        fig.add(arrow(kx - 8, ky + dy, kx + 16, ky + dy, color=GRADIENT,
                      width=1.8, head=6))
    a = math.radians(ORIENT)
    fig.add(arrow(kx, ky, kx + 50 * math.cos(a), ky - 50 * math.sin(a),
                  color=BLUE, width=3.5, head=12))
    fig.add(circle(kx, ky, 8, fill="none", stroke=GREEN, stroke_width=2))
    _t(fig, cx, 436, "turn the patch so this", size=11.5, fill=P["muted"])
    _t(fig, cx, 452, "arrow points up", size=11.5, fill=P["muted"])

    # 3. the turned patch under a 4 x 4 grid, one direction star per cell
    cx = cxs[2]
    size, cell = 144, 36
    wx, wy = cx - size / 2, 228
    turn = ORIENT - 90
    hist = _sift_descriptor(size, turn)
    kx, ky = L_CORNER[0] * PATCH_W, L_CORNER[1] * PATCH_H
    roof = [(round(u * PATCH_W, 1), round(v * PATCH_H, 1)) for (u, v) in L_ROOF]
    fig.add(El("defs", El("clipPath", rect(wx, wy, size, size),
                          id="sift_window")))
    fig.add(rect(wx, wy, size, size, fill=ASPHALT))
    fig.add(g(g(polygon(roof, fill=P["dark"], fill_opacity="0.35"),
                transform=f"translate({cx},{wy + size / 2}) rotate({turn:.2f}) "
                          f"translate({-kx:.1f},{-ky:.1f})"),
              clip_path="url(#sift_window)"))
    grid = g(stroke=BLUE, stroke_width=1)
    for k in range(5):
        grid.add(line(wx + k * cell, wy, wx + k * cell, wy + size))
        grid.add(line(wx, wy + k * cell, wx + size, wy + k * cell))
    fig.add(grid)
    stars = g(stroke=P["ink"], stroke_width=1.4, stroke_linecap="round")
    for n, h in enumerate(hist):
        sx = wx + (n % 4 + 0.5) * cell
        sy = wy + (n // 4 + 0.5) * cell
        for k, v in enumerate(h):
            a, ln = math.radians(k * 45), 2 + 14 * v
            stars.add(line(round(sx, 1), round(sy, 1),
                           round(sx + ln * math.cos(a), 1),
                           round(sy + ln * math.sin(a), 1)))
    fig.add(stars)
    fig.add(arrow(cx, wy - 8, cx, wy - 32, color=BLUE, width=2.5, head=9))
    _t(fig, cx + 10, wy - 16, "now points up", size=11, fill=P["muted"],
       anchor="start")
    _t(fig, cx, 436, "16 cells × 8 directions", size=11.5, fill=P["muted"])
    _t(fig, cx, 452, "= 128 numbers", size=11.5, fill=P["muted"])

    # 4. the 128 values from card 3 as bars, twice
    cx = cxs[3]
    x, span = cx - 90, 180
    vals = [v for h in hist for v in h]
    rnd = random.Random(67)
    twin = [v * (1 + 0.18 * (rnd.random() - 0.5)) for v in vals]
    step = span / len(vals)
    for base, vs, lab in ((240, vals, "128 numbers, the fingerprint"),
                          (334, twin, "the same corner in another photo")):
        bars = g()
        for n, v in enumerate(vs):
            bars.add(rect(round(x + n * step, 2), round(base - 50 * v, 1),
                          0.95, round(50 * v, 1),
                          fill=P["dark"] if (n // 8) % 2 == 0 else GRADIENT))
        fig.add(bars)
        fig.add(line(x, base + 0.5, x + span, base + 0.5, stroke=P["line"],
                     stroke_width=1))
        _t(fig, cx, base + 20, lab, size=11, fill=P["muted"])
    ty = 396
    fig.add(path(f"M{cx - 34},{ty - 6} l6,7 l12,-14", fill="none",
                 stroke=GREEN, stroke_width=3, stroke_linecap="round",
                 stroke_linejoin="round"))
    _t(fig, cx - 8, ty, "a match", size=12.5, bold=True, fill=GREEN,
       anchor="start")

    _t(fig, W / 2, 504,
       "Scale and orientation are built in, so the same corner gets nearly "
       "the same numbers from higher up or turned round.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 6c. RANSAC: let the majority decide
# ---------------------------------------------------------------------------
# Each match is plotted as (u, v): how far across photo A the point sits, and
# how far across photo B. Correct matches all moved the same way between the
# two photos, so they fall near one line; a wrong match lands anywhere.
RS_INLIERS = [(u, 0.12 + 0.72 * u + e) for (u, e) in (
    (0.06, 0.020), (0.12, -0.015), (0.19, 0.010), (0.25, -0.025),
    (0.31, 0.018), (0.38, -0.008), (0.44, 0.025), (0.50, -0.020),
    (0.57, 0.005), (0.63, 0.015), (0.70, -0.022), (0.77, 0.012),
    (0.84, -0.010), (0.92, 0.020))]
RS_OUTLIERS = [(0.12, 0.70), (0.33, 0.93), (0.58, 0.16), (0.86, 0.28),
               (0.55, 0.88)]
RS_GOOD = (RS_INLIERS[2], RS_INLIERS[11])     # two right matches
RS_BAD = (RS_OUTLIERS[0], RS_INLIERS[10])     # a wrong match and a right one
RS_BAND = 11                                  # agreement half-width, px
RS_PLOT = (46, 140, 200, 220)                 # left (in card), top, w, h


def _rs_px(card_x, pt):
    left, top, w, h = RS_PLOT
    return card_x + left + pt[0] * w, top + h - pt[1] * h


def _rs_agrees(pair, pts):
    """For each point, whether it lies within RS_BAND px of the line through
    the pair."""
    (x1, y1), (x2, y2) = (_rs_px(0, p) for p in pair)
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    return [abs(dy * (x - x1) - dx * (y - y1)) / n <= RS_BAND
            for (x, y) in (_rs_px(0, p) for p in pts)]


def _rs_span(card_x, pair):
    """End points, in px, of the line through the pair cut to the plot."""
    (u1, v1), (u2, v2) = pair
    du, dv = u2 - u1, v2 - v1
    lo, hi = -1e9, 1e9
    for p, dp in ((u1, du), (v1, dv)):
        if abs(dp) > 1e-12:
            t0, t1 = -p / dp, (1 - p) / dp
            lo, hi = max(lo, min(t0, t1)), min(hi, max(t0, t1))
    return (_rs_px(card_x, (u1 + lo * du, v1 + lo * dv)),
            _rs_px(card_x, (u1 + hi * du, v1 + hi * dv)))


def build_ransac() -> Figure:
    fig = Figure(W, 500, "RANSAC: let the majority decide",
                 "RANSAC (random sample consensus) finds the wrong matches by "
                 "asking which one geometry most of the matches agree with.")
    pts = RS_INLIERS + RS_OUTLIERS
    n_in = len(RS_INLIERS)
    good, bad = _rs_agrees(RS_GOOD, pts), _rs_agrees(RS_BAD, pts)
    # the labels below say 14 and 3; keep the data honest to them
    assert sum(good) == 14 and not any(good[n_in:]) and sum(bad) == 3
    left, top, w, h = RS_PLOT
    cw, gap, x0 = 266, 21, 30
    heads = ("The matches, some wrong", "Guess from two, count who agrees",
             "Keep the best, drop the rest")
    cards = []
    for i, head in enumerate(heads):
        x = x0 + i * (cw + gap)
        cards.append(x)
        fig.add(rect(x, 84, cw, 368, **CARD))
        _t(fig, x + cw / 2, 112, head, size=13.5, bold=True)
        fig.add(path(f"M{x + left},{top} V{top + h} H{x + left + w}",
                     fill="none", stroke="#9aa7b2", stroke_width=1.2))

    # 1. every match, right and wrong
    x = cards[0]
    for k, p in enumerate(pts):
        px, py = _rs_px(x, p)
        fig.add(circle(px, py, 4.5, fill=P["dark"] if k < n_in else RED))
    _t(fig, x + left + w / 2, top + h + 18, "position in photo A", size=10.5,
       fill=P["muted"])
    yx, yy = x + left - 14, top + h / 2
    fig.add(text(yx, yy, "position in photo B", text_anchor="middle",
                 font_size=10.5, fill=P["muted"],
                 transform=f"rotate(-90 {yx} {yy})"))
    _t(fig, x + cw / 2, 412, "each point is one match;", size=11.5,
       fill=P["muted"])
    _t(fig, x + cw / 2, 428, "a wrong match lands anywhere", size=11.5,
       fill=P["muted"])

    # 2. a good guess and a bad one
    x = cards[1]
    (gx0, gy0), (gx1, gy1) = _rs_span(x, RS_GOOD)
    ln = math.hypot(gx1 - gx0, gy1 - gy0)
    ex, ey = (gx1 - gx0) / ln, (gy1 - gy0) / ln
    nx, ny = -ey * RS_BAND, ex * RS_BAND
    a0 = (gx0 - ex * 20, gy0 - ey * 20)
    a1 = (gx1 + ex * 20, gy1 + ey * 20)
    fig.add(El("defs", El("clipPath", rect(x + left, top, w, h),
                          id="ransac_plot")))
    fig.add(g(polygon([(round(a0[0] + nx, 1), round(a0[1] + ny, 1)),
                       (round(a1[0] + nx, 1), round(a1[1] + ny, 1)),
                       (round(a1[0] - nx, 1), round(a1[1] - ny, 1)),
                       (round(a0[0] - nx, 1), round(a0[1] - ny, 1))],
                      fill="#fdf3e6"),
              clip_path="url(#ransac_plot)"))
    (bx0, by0), (bx1, by1) = _rs_span(x, RS_BAD)
    fig.add(line(bx0, by0, bx1, by1, stroke=P["muted"], stroke_width=1.5,
                 stroke_dasharray="6 4", opacity="0.7"))
    fig.add(line(gx0, gy0, gx1, gy1, stroke=ORANGE, stroke_width=2))
    for k, p in enumerate(pts):
        px, py = _rs_px(x, p)
        fig.add(circle(px, py, 4.5, fill=GREEN if good[k] else "#9aa7b2"))
    for p in RS_BAD:
        px, py = _rs_px(x, p)
        fig.add(circle(px, py, 10, fill="none", stroke=P["muted"],
                       stroke_width=1.3, stroke_dasharray="3 3",
                       opacity="0.8"))
    for p in RS_GOOD:
        px, py = _rs_px(x, p)
        fig.add(circle(px, py, 10, fill="none", stroke=ORANGE,
                       stroke_width=2.5))
    _t(fig, x + left + 0.95 * w, 148, f"{sum(good)} agree", size=13,
       bold=True, fill=GREEN, anchor="end")
    _t(fig, x + left + 6, 238, f"{sum(bad)} agree", size=12, bold=True,
       fill=P["muted"], anchor="start")
    _t(fig, x + cw / 2, 412, "orange rings: two picked at random", size=11.5,
       fill=P["muted"])
    _t(fig, x + cw / 2, 428, "green: inside the band, so they agree",
       size=11.5, fill=P["muted"])

    # 3. the winner, with the outliers struck out
    x = cards[2]
    (gx0, gy0), (gx1, gy1) = _rs_span(x, RS_GOOD)
    fig.add(line(gx0, gy0, gx1, gy1, stroke=BLUE, stroke_width=2.2))
    for k, p in enumerate(pts):
        px, py = _rs_px(x, p)
        if good[k]:
            fig.add(circle(px, py, 4.5, fill=GREEN))
        else:
            fig.add(circle(px, py, 4.5, fill=RED))
            fig.add(line(px - 7, py - 7, px + 7, py + 7, stroke=RED,
                         stroke_width=2))
            fig.add(line(px - 7, py + 7, px + 7, py - 7, stroke=RED,
                         stroke_width=2))
    _t(fig, x + cw / 2, 412, "the outliers are deleted", size=11.5,
       fill=P["muted"])
    _t(fig, x + cw / 2, 428, "before the camera solve", size=11.5,
       fill=P["muted"])

    _t(fig, W / 2, 480,
       "Try many random guesses; the geometry most matches agree with wins. "
       "A stripe matched to the wrong stripe never agrees with the majority.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 8. Dense matching: one pixel, one line, one depth
# ---------------------------------------------------------------------------
def build_dense_matching() -> Figure:
    fig = Figure(W, 540, "From thousands of points to millions",
                 "Once the cameras are known, every pixel can be matched, not "
                 "just the distinctive ones, because the search is one line long.")
    # photo A
    fig.add(rect(40, 96, 250, 180, rx=6, fill="#e6e8ea", stroke=P["line"],
                 stroke_width=1.5))
    _t(fig, 165, 88, "photo A", size=12.5, bold=True)
    fig.add(polygon([(80, 130), (190, 130), (190, 220), (140, 220), (140, 180),
                     (80, 180)], fill="#c2cad2", stroke=P["line"],
                    stroke_width=1))
    fig.add(rect(118, 196, 12, 12, fill="none", stroke=ORANGE, stroke_width=2.5))
    _t(fig, 124, 240, "one pixel on the wall", size=11, fill=ORANGE)
    # photo B
    fig.add(rect(330, 96, 250, 180, rx=6, fill="#e6e8ea", stroke=P["line"],
                 stroke_width=1.5))
    _t(fig, 455, 88, "photo B", size=12.5, bold=True)
    fig.add(polygon([(350, 130), (460, 130), (460, 220), (410, 220), (410, 180),
                     (350, 180)], fill="#c2cad2", stroke=P["line"],
                    stroke_width=1))
    fig.add(line(340, 214, 570, 186, stroke=BLUE, stroke_width=1.8,
                 stroke_dasharray="6 4"))
    for k, x in enumerate((360, 392, 424, 456, 488, 520, 552)):
        y = 214 - (x - 340) * (28 / 230)
        ok = (k == 2)
        fig.add(rect(x - 6, y - 6, 12, 12, fill="none",
                     stroke=GREEN if ok else "#9aa7b2",
                     stroke_width=2.5 if ok else 1.2))
    _t(fig, 455, 250, "its match must lie on this one line", size=11,
       fill=BLUE)
    _t(fig, 455, 266, "try each candidate; keep the best fingerprint", size=11,
       fill=P["muted"])
    fig.add(arrow(295, 186, 325, 186, color=ORANGE, width=2, head=8))

    # side view: depth from two rays
    fig.add(rect(620, 84, 250, 290, **CARD))
    _t(fig, 745, 110, "From the side", size=13, bold=True)
    gy = 330
    fig.add(line(640, gy, 850, gy, stroke="#9aa7b2", stroke_width=2.5,
                 stroke_linecap="round"))
    fig.add(camera(690, 150, 0.7))
    fig.add(camera(800, 150, 0.7))
    _t(fig, 690, 128, "A", size=11, bold=True)
    _t(fig, 800, 128, "B", size=11, bold=True)
    px, py = 752, 286
    fig.add(line(690, 164, px, py, stroke=ORANGE, stroke_width=1.6))
    fig.add(line(800, 164, px, py, stroke=GREEN, stroke_width=1.6))
    fig.add(circle(px, py, 6, fill=BLUE, stroke=P["white"], stroke_width=1.5))
    fig.add(line(px + 40, 164, px + 40, py, stroke=P["muted"], stroke_width=1,
                 stroke_dasharray="3 3"))
    _t(fig, px + 62, 230, "depth", size=11, fill=P["muted"])
    _t(fig, 745, 356, "two rays cross: that is the point", size=11,
       fill=P["muted"])

    # bottom strip: the result
    fig.add(rect(40, 400, 830, 90, **CARD))
    _t(fig, 60, 426, "Repeat for every pixel of every photo",
       size=12.5, bold=True, anchor="start")
    _t(fig, 60, 448, "Thousands of tie points become millions of surface "
       "points. Blank asphalt still gives nothing: no fingerprint, no match.",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, 60, 468, "This is the slow step. It is why a reconstruction runs "
       "for hours while aerotriangulation took minutes.",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, W / 2, 522, "Multi-view stereo, in the appendix. Bentley: "
       "Reconstruction.", size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 9. Points to triangles
# ---------------------------------------------------------------------------
def _profile(x):
    """Height of a simple building-and-ground profile, in px above baseline."""
    if 60 < x < 140:
        return 70
    return 8 + 4 * math.sin(x / 23)


def build_meshing() -> Figure:
    fig = Figure(W, 480, "Points become triangles",
                 "A cloud is not a surface. Joining neighbouring points into "
                 "triangles makes one, and the one rule that matters is how far "
                 "apart two points may be and still be joined.")
    cards = [(30, "Dense points"), (310, "Joined into triangles"),
             (590, "The thin pole problem")]
    for (cx, title) in cards:
        fig.add(rect(cx, 84, 280, 330, **CARD))
        _t(fig, cx + 140, 112, title, size=13.5, bold=True)
    gy = 360
    rnd = random.Random(7)
    # card 1: points along the profile
    for k in range(60):
        x = 20 + k * 4 + rnd.random() * 2
        y = gy - _profile(x) - rnd.random() * 3
        fig.add(circle(30 + 20 + x, y, 1.8, fill=P["dark"]))
    _t(fig, 170, 392, "a side slice through the cloud", size=11, fill=P["muted"])
    # card 2: triangles
    pts = [(20 + k * 12, gy - _profile(20 + k * 12)) for k in range(21)]
    pts2 = [(x + 6, y - 14) for (x, y) in pts]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        c = pts2[i]
        d = pts2[i + 1]
        for tri in ((a, b, c), (b, d, c)):
            fig.add(polygon([(310 + 20 + px, py) for (px, py) in tri],
                            fill="#e8f1fb", stroke=BLUE, stroke_width=0.9))
    _t(fig, 450, 392, "every point joined to its neighbours", size=11,
       fill=P["muted"])
    # card 3: thin pole webbed, then fixed
    for (ox, webbed, lab) in ((610, True, "tolerance loose"),
                              (760, False, "tolerance tight")):
        fig.add(line(ox, gy, ox + 100, gy, stroke="#9aa7b2", stroke_width=2))
        px = ox + 50
        fig.add(line(px, gy, px, gy - 110, stroke=P["dark"], stroke_width=3))
        if webbed:
            fig.add(polygon([(px, gy - 110), (ox + 8, gy), (px, gy)],
                            fill="#e8f1fb", stroke=RED, stroke_width=1))
            fig.add(polygon([(px, gy - 110), (ox + 92, gy), (px, gy)],
                            fill="#e8f1fb", stroke=RED, stroke_width=1))
            fig.add(polygon([(px, gy - 80), (ox + 20, gy), (px, gy - 110)],
                            fill="#e8f1fb", stroke=RED, stroke_width=1))
            fig.add(polygon([(px, gy - 80), (ox + 80, gy), (px, gy - 110)],
                            fill="#e8f1fb", stroke=RED, stroke_width=1))
        _t(fig, ox + 50, gy + 22, lab, size=11,
           fill=RED if webbed else GREEN, bold=True)
    _t(fig, 730, 150, "a pole or a wire has points far", size=11,
       fill=P["muted"])
    _t(fig, 730, 166, "from the ground points beside it;", size=11,
       fill=P["muted"])
    _t(fig, 730, 182, "join them and you get a tent", size=11, fill=P["muted"])
    _t(fig, W / 2, 448,
       "A webbed mesh is not a bad flight. It is a tolerance to change in the "
       "software.", size=12.5, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 11. The surface sampled on a grid
# ---------------------------------------------------------------------------
def _dem_profile(x):
    h = 20 + 10 * math.sin(x / 40)
    if 90 < x < 170:
        h = 95              # building
    if 250 < x < 290:
        h = 20 + 10 * math.sin(x / 40) + 45 * math.exp(-((x - 270) / 14) ** 2)  # tree
    return h


def build_dem_grid() -> Figure:
    fig = Figure(W, 480, "A DEM is the surface sampled on a grid",
                 "Lay a grid over the mesh and ask one question in every cell: "
                 "how high is the surface here? The answer is one number per cell.")
    # left: side view with cells
    fig.add(rect(30, 84, 540, 330, **CARD))
    _t(fig, 300, 112, "From the side", size=13.5, bold=True)
    gy = 370
    x0 = 60
    fig.add(line(x0, gy, x0 + 480, gy, stroke="#9aa7b2", stroke_width=2.5,
                 stroke_linecap="round"))
    cell = 24
    for k in range(20):
        x = x0 + k * cell
        h = _dem_profile(x - x0 + cell / 2)
        fig.add(rect(x + 2, gy - h, cell - 4, h, fill="#e8f1fb", stroke=BLUE,
                     stroke_width=1))
    pts = [(x0 + k * 4, gy - _dem_profile(k * 4)) for k in range(121)]
    fig.add(path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts),
                 fill="none", stroke=P["dark"], stroke_width=2))
    _t(fig, 300, 392, "the mesh (black) and the height recorded in each cell "
       "(blue)", size=11, fill=P["muted"])
    # right: plan view grid with numbers
    fig.add(rect(590, 84, 280, 330, **CARD))
    _t(fig, 730, 112, "From above: the grid of heights", size=13.5, bold=True)
    gx, gy2, c = 612, 134, 29
    rnd = random.Random(11)
    for r in range(8):
        for col in range(8):
            base = 20 + 6 * math.sin((col + r) / 2.5)
            if 2 <= r <= 4 and 1 <= col <= 3:
                h = 95
            elif r == 5 and col == 6:
                h = 62
            else:
                h = base + rnd.random() * 3
            shade = int(235 - (h - 15) * 1.6)
            fig.add(rect(gx + col * c, gy2 + r * c, c, c,
                         fill=f"rgb({shade},{shade + 6},{min(255, shade + 14)})",
                         stroke=P["white"], stroke_width=1))
            _t(fig, gx + col * c + c / 2, gy2 + r * c + c / 2 + 4,
               f"{h:.0f}", size=8.5, fill=P["ink"])
    _t(fig, 730, 392, "one height per cell, the cell is the GSD", size=11,
       fill=P["muted"])
    _t(fig, W / 2, 448,
       "Keep the building and the tree and it is a DSM. Strip them to bare "
       "ground and it is a DTM.", size=12.5, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 12. Relief displacement and the orthophoto
# ---------------------------------------------------------------------------
def build_orthorectification() -> Figure:
    fig = Figure(W, 520, "Why a photo is not a map, and how the mesh fixes it",
                 "A camera sees the top of a building further from the centre "
                 "than its base. Projecting every photo onto the mesh and "
                 "looking straight down removes that lean.")
    for (cx, ortho) in ((250, False), (650, True)):
        fig.add(rect(cx - 200, 84, 400, 330, **CARD))
        _t(fig, cx, 112, "The photo" if not ortho else "The orthophoto",
           size=13.5, bold=True)
        gy = 300
        fig.add(line(cx - 170, gy, cx + 170, gy, stroke="#9aa7b2",
                     stroke_width=2.5, stroke_linecap="round"))
        bx0, bx1, roof = cx + 40, cx + 100, gy - 90
        fig.add(rect(bx0, roof, bx1 - bx0, gy - roof, fill="#c2cad2",
                     stroke=P["line"], stroke_width=1.2))
        if not ortho:
            camx, camy = cx - 60, 150
            fig.add(camera(camx, camy, 0.8))
            # rays to base and roof corner, hitting an image plane
            for (tx, ty, col) in ((bx0, gy, GREEN), (bx0, roof, ORANGE)):
                fig.add(line(camx, camy + 16, tx, ty, stroke=col,
                             stroke_width=1.4, stroke_dasharray="5 4"))
            # ground footprint vs where the roof lands when seen from the camera
            ex = bx0 + (bx0 - camx) * (gy - roof) / (gy - camy - 16) * 0.85
            fig.add(line(bx0, gy + 14, ex, gy + 14, stroke=ORANGE,
                         stroke_width=3))
            fig.add(line(bx0, gy + 10, bx0, gy + 18, stroke=GREEN,
                         stroke_width=2))
            _t(fig, (bx0 + ex) / 2, gy + 34, "the roof lands here in the picture",
               size=11, fill=ORANGE)
            _t(fig, bx0 - 2, gy + 50, "base", size=11, fill=GREEN,
               anchor="end")
            _t(fig, cx, 372, "buildings lean away from the centre of every photo",
               size=11, fill=P["muted"])
            _t(fig, cx, 388, "and two photos disagree about where the roof is",
               size=11, fill=P["muted"])
        else:
            for x in (bx0 + 10, bx0 + 30, bx0 + 50):
                fig.add(arrow(x, 140, x, roof - 6, color=BLUE, width=1.6,
                              head=7))
            for x in (cx - 150, cx - 110, cx - 70, cx - 30, cx + 10, cx + 130,
                      cx + 160):
                fig.add(arrow(x, 140, x, gy - 6, color=BLUE, width=1.2, head=6))
            fig.add(line(bx0, gy + 14, bx1, gy + 14, stroke=GREEN,
                         stroke_width=3))
            _t(fig, (bx0 + bx1) / 2, gy + 34, "roof directly over the base",
               size=11, fill=GREEN)
            _t(fig, cx, 372, "every point viewed from straight above, using the",
               size=11, fill=P["muted"])
            _t(fig, cx, 388, "mesh to know where each pixel sits on the ground",
               size=11, fill=P["muted"])
    _t(fig, W / 2, 448,
       "Orthorectification. Stitch the straightened photos together and the "
       "result is the orthomosaic: a picture you can measure on.",
       size=12.5, fill=P["muted"], italic=True)
    _t(fig, W / 2, 490,
       "Lean that survives into the orthomosaic means the mesh was wrong there, "
       "usually from too little overlap.", size=11.5, fill=P["muted"],
       italic=True)
    return fig


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    # (builder, number, variant, slug): a lettered variant sits beside the
    # figure it extends without moving any number after it
    for builder, number, variant, slug in (
        (build_pipeline_overview, 1, "", "pipeline_overview"),
        (build_triangle_math, 2, "b", "triangle_math"),
        (build_camera_solve, 3, "", "camera_solve"),
        (build_features, 5, "", "features"),
        (build_matching, 6, "", "matching"),
        (build_sift, 6, "b", "sift"),
        (build_ransac, 6, "c", "ransac"),
        (build_dense_matching, 8, "", "dense_matching"),
        (build_meshing, 9, "", "meshing"),
        (build_dem_grid, 11, "", "dem_grid"),
        (build_orthorectification, 10, "", "orthorectification"),
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
