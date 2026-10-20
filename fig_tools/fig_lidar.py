"""LiDAR figures for the Week 8 reading (gen_reading/lidar.md).

    w06_fig01_lidar_returns.svg          one pulse, several returns; DSM and DTM
    w06_fig01b_canopy_gaps.svg           photos see the canopy, pulses find the gaps
    w06_fig01c_ground_classification.svg classify, keep ground, grid: the DTM

Figure 1 replaced a drawing that asserted the last return is ground but drew two
unrelated scatters of dots with no pulse, no returns, and nothing connecting
them, so the mechanism was invisible and the claim had to be taken on trust. It
shows the mechanism twice: one pulse producing several returns on the left, then
a whole flight's worth as a classified cross-section on the right, with the two
surfaces drawn through the points they come from.

1b and 1c are lettered variants that sit beside Figure 1 in the reading and on
the Week 8 slides, so adding them moved no other w06_ number. 1b answers "can a
laser map the ground under a tree?" (through the gaps, not through the leaves,
and the arithmetic for how many pulses get there). 1c is the processing step
that turns a cloud into a bare-earth terrain model.

Usage:
    python fig_tools/fig_lidar.py [--out review] [--png]

Figures go to review/ for a look, then to docs/gen_reading/images/.
"""
from __future__ import annotations

import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_side, car  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line, path,  # noqa: E402
                    rect, render_png, text, translate)

W = 900
CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)
GROUND = "#8a6a45"
VEG = "#4a8a4a"
BEAM = "#4a90d9"
BUILT = "#6b7f95"          # classified building points
OTHER = "#9aa7b2"          # classified "other": the car


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


def _t(fig, x, y, s, size=12, bold=False, fill=None, anchor="middle",
       italic=False):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 font_style="italic" if italic else None,
                 fill=fill or P["ink"]))


# ===========================================================================
# Figure 1: one pulse, several returns; many pulses, two surfaces
# ===========================================================================
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


def build_lidar_returns() -> Figure:
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


# ===========================================================================
# Figure 1b: photos see the canopy; pulses reach the ground through the gaps
# ===========================================================================
# One scene drawn twice, once per card, in card-local coordinates. The crowns
# are clusters of leaf blobs with real slits between them, and every pulse is
# intersected with those blobs, so where a line stops is geometry, not art.
# Pulses are vertical: this is a section along the flight line, and each pulse
# left the aircraft when it was directly overhead (as in Figure 1).
GAP_SCENE_W = 410                 # card width
GAP_GROUND = 336                  # ground line, card-local y
GAP_LINE_Y = 118                  # the flight line, card-local y
GAP_DRONE_X = 205
GAP_RAYS = [26 + k * 15.4 for k in range(24)]   # x of each pulse

# (cx, cy, r) leaf clusters, card-local. Each crown is built around one or two
# vertical slits a pulse can pass down (x = 103; 180 and 226; 303).
GAP_CROWNS = (
    # crown A, trunk at x = 80, slit 100..106
    ((84, 198, 14), (62, 214, 14), (74, 240, 14), (88, 262, 12),
     (58, 248, 12), (122, 202, 14), (142, 222, 13), (121, 238, 13),
     (136, 258, 13), (119, 281, 12)),
    # crown B, trunk at x = 203, slits 177..183 and 223..229
    ((163, 206, 14), (150, 230, 13), (164, 252, 13), (155, 274, 12),
     (203, 190, 15), (196, 216, 13), (210, 214, 13), (200, 242, 14),
     (204, 268, 13), (243, 208, 14), (255, 230, 12), (242, 252, 13),
     (250, 274, 11)),
    # crown C, trunk at x = 322, slit 300..306
    ((286, 204, 14), (270, 226, 13), (284, 248, 14), (276, 272, 12),
     (290, 284, 10), (320, 200, 14), (342, 220, 13), (320, 240, 14),
     (338, 262, 13), (322, 284, 12)),
)
GAP_TRUNKS = ((80, 250), (203, 256), (322, 262))   # x, top y of the trunk


def _leaves(pad=0.0):
    return [(cx, cy, r + pad) for crown in GAP_CROWNS for cx, cy, r in crown]


def _crown_spans():
    return [(min(cx - r for cx, _, r in crown), max(cx + r for cx, _, r in crown))
            for crown in GAP_CROWNS]


def _first_hit(x, leaves):
    """Where a vertical pulse at x first meets a leaf blob, from the top;
    None if it reaches the ground."""
    best = None
    for cx, cy, r in leaves:
        if abs(x - cx) < r:
            y = cy - math.sqrt(r * r - (x - cx) ** 2)
            if best is None or y < best:
                best = y
    return None if best is None else (x, best)


def _gap_scene(fig, ox, oy):
    """Ground, trunks and leaf blobs; returns nothing. Coordinates are offset
    by (ox, oy), the card's top-left."""
    fig.add(line(ox + 22, oy + GAP_GROUND, ox + GAP_SCENE_W - 22,
                 oy + GAP_GROUND, stroke=GROUND, stroke_width=3,
                 stroke_linecap="round"))
    for tx, ty in GAP_TRUNKS:
        fig.add(line(ox + tx, oy + GAP_GROUND, ox + tx, oy + ty,
                     stroke="#7a5a3a", stroke_width=4, stroke_linecap="round"))
    for crown in GAP_CROWNS:
        for cx, cy, r in crown:
            fig.add(circle(ox + cx, oy + cy, r, fill=VEG, opacity="0.55"))
    fig.add(line(ox + 22, oy + GAP_LINE_Y, ox + GAP_SCENE_W - 22,
                 oy + GAP_LINE_Y, stroke="#c5cdd5", stroke_width=1.5,
                 stroke_dasharray="4 4"))
    fig.add(translate(ox + GAP_DRONE_X, oy + GAP_LINE_Y - 12,
                      aircraft_mini_side(0.55)))
    _t(fig, ox + GAP_SCENE_W - 24, oy + GAP_LINE_Y - 8, "flight line",
       size=11, fill=P["muted"], anchor="end")


def build_canopy_gaps() -> Figure:
    fig = Figure(W, 636,
                 "Photos see the canopy; pulses reach the ground through the gaps",
                 "A leaf stops a laser pulse just as it blocks a camera's view. "
                 "The difference is the holes between leaves: a pulse that finds "
                 "one keeps going.")
    cards = ((30, "Photographs: the surface is the canopy top"),
             (460, "LiDAR: some pulses find a gap"))
    oy = 84
    for cx, head in cards:
        fig.add(rect(cx, oy, GAP_SCENE_W, 416, **CARD))
        _t(fig, cx + GAP_SCENE_W / 2, oy + 30, head, size=15, bold=True)

    # --- left: camera rays end on the leaf mass; a hole is not a surface ---
    ox = cards[0][0]
    _gap_scene(fig, ox, oy)
    envelope = _leaves(pad=7)
    ends = []
    for tx in GAP_RAYS:
        hit = _first_hit(tx, envelope)
        if hit is None:
            hit = (tx, GAP_GROUND)
        ends.append(hit)
        fig.add(line(ox + tx, oy + GAP_LINE_Y, ox + hit[0], oy + hit[1],
                     stroke=P["muted"], stroke_width=1, opacity="0.55"))
    for hx, hy in ends:
        fig.add(circle(ox + hx, oy + hy, 2.6, fill=P["bad"]))
    fig.add(path("M" + " L".join(f"{ox + x:.1f},{oy + y:.1f}" for x, y in ends),
                 fill="none", stroke=P["bad"], stroke_width=2.2,
                 stroke_dasharray="7 5"))
    # where the ground is hidden: no photo ever saw it
    for a, b in _crown_spans():
        fig.add(line(ox + a, oy + GAP_GROUND + 9, ox + b, oy + GAP_GROUND + 9,
                     stroke=P["bad"], stroke_width=3, opacity="0.75"))
    _t(fig, ox + 205, oy + GAP_GROUND + 30,
       "red: ground that no photo ever saw", size=12, fill=P["bad"])
    _t(fig, ox + 205, oy + GAP_GROUND + 47,
       "the model there is a guess copied from the canopy", size=11.5,
       fill=P["muted"])
    # legend
    ly = oy + 62
    fig.add(line(ox + 26, ly, ox + 56, ly, stroke=P["bad"], stroke_width=2.2,
                 stroke_dasharray="7 5"))
    _t(fig, ox + 64, ly + 4, "the surface the photos reconstruct", size=12,
       anchor="start")
    _t(fig, ox + 64, ly + 20, "every camera ray stops at the first leaf",
       size=11.5, fill=P["muted"], anchor="start")

    # --- right: real leaves, real holes ---
    ox = cards[1][0]
    _gap_scene(fig, ox, oy)
    leaves = _leaves()
    canopy_pulses, ground_through = 0, 0
    through_pts, leaf_pts = [], []
    spans = _crown_spans()
    for tx in GAP_RAYS:
        hit = _first_hit(tx, leaves)
        under_canopy = any(a <= tx <= b for a, b in spans)
        if hit is None:
            fig.add(line(ox + tx, oy + GAP_LINE_Y, ox + tx, oy + GAP_GROUND,
                         stroke=BEAM, stroke_width=1.8 if under_canopy else 1,
                         opacity="1" if under_canopy else "0.5"))
            if under_canopy:
                through_pts.append((tx, GAP_GROUND))
                ground_through += 1
                canopy_pulses += 1
            else:
                fig.add(circle(ox + tx, oy + GAP_GROUND, 2.6, fill=GROUND))
        else:
            fig.add(line(ox + tx, oy + GAP_LINE_Y, ox + hit[0], oy + hit[1],
                         stroke=BEAM, stroke_width=1, opacity="0.6"))
            leaf_pts.append(hit)
            canopy_pulses += 1
    for hx, hy in leaf_pts:
        fig.add(circle(ox + hx, oy + hy, 3.4, fill=BEAM, stroke=P["white"],
                       stroke_width=1))
    for hx, hy in through_pts:
        fig.add(circle(ox + hx, oy + hy, 4.5, fill=GROUND, stroke=P["white"],
                       stroke_width=1.2))
    # the drawing has to agree with the arithmetic below: about one in five
    assert 3 <= ground_through <= 5 and 14 <= canopy_pulses <= 20, (
        ground_through, canopy_pulses)
    # legend
    ly = oy + 62
    fig.add(circle(ox + 34, ly - 1, 3.4, fill=BEAM, stroke=P["white"],
                   stroke_width=1))
    _t(fig, ox + 46, ly + 4, "stopped by a leaf: a canopy return", size=12,
       anchor="start")
    fig.add(circle(ox + 34, ly + 17, 4.5, fill=GROUND, stroke=P["white"],
                   stroke_width=1.2))
    _t(fig, ox + 46, ly + 22, "through a gap: a ground return", size=12,
       anchor="start")
    _t(fig, ox + 205, oy + GAP_GROUND + 30,
       f"here: {canopy_pulses} pulses over the crowns, "
       f"{ground_through} reached the ground", size=12, fill=P["ink"])
    _t(fig, ox + 205, oy + GAP_GROUND + 47,
       "a leaf is not transparent; the pulse went between leaves",
       size=11.5, fill=P["muted"])

    # --- the arithmetic, side by side ---
    by = 520
    fig.add(rect(30, by, GAP_SCENE_W, 62, rx=8, fill="#fdeeee",
                 stroke=P["bad"], stroke_width=1.2))
    _t(fig, 235, by + 26, "Photographs: 0 ground points under the crowns",
       size=14, bold=True)
    _t(fig, 235, by + 46, "the ground has to be seen in two photos to be "
       "modelled", size=11.5, fill=P["muted"])
    fig.add(rect(460, by, GAP_SCENE_W, 62, rx=8, fill="#e8f1fb", stroke=BEAM,
                 stroke_width=1.2))
    _t(fig, 665, by + 26, "20 % gaps × 200 pulses/m² ≈ 40 ground points/m²",
       size=14, bold=True)
    _t(fig, 665, by + 46, "plenty for a terrain model on a 1 m grid",
       size=11.5, fill=P["muted"])

    _t(fig, W / 2, 614,
       "Dense evergreen canopy leaves few gaps; bare winter branches leave "
       "many, so a deciduous site maps best with the leaves off.",
       size=13, fill=P["muted"], italic=True)
    return fig


# ===========================================================================
# Figure 1c: from points to a bare-earth DTM
# ===========================================================================
# One cross-section drawn three times: every point, every point labelled,
# then only the ground points with a surface through them. Card-local.
CL_W = 255                            # card width
CL_GROUND = 210                       # mean ground height, card-local y
CL_X0, CL_X1 = 14, 241                # the slice, card-local x
CL_TREES = ((44, 118, 30), (90, 96, 25))   # x, crown height, crown radius
CL_BUILDING = (122, 166, 92)          # x0, x1, height
CL_CAR = 200                          # x of the car


def _cl_ground(x):
    return CL_GROUND + 9 * math.sin((x - 20) / 28)


def _cl_points():
    """The cloud, as (x, y, class) in card-local coordinates. Classes are
    ground, veg, building and other. Seeded, so the three panels agree."""
    rnd = random.Random(19)
    pts = []
    bx0, bx1, bh = CL_BUILDING
    roof_y = _cl_ground((bx0 + bx1) / 2) - bh
    # ground: dense in the open, sparse under crowns, none under the roof
    x = float(CL_X0)
    while x <= CL_X1:
        under_tree = any(abs(x - tx) < r for tx, _, r in CL_TREES)
        under_car = abs(x - CL_CAR) < 17
        if bx0 - 2 < x < bx1 + 2 or under_car:
            x += 4
            continue
        if not under_tree or rnd.random() < 0.4:
            pts.append((x, _cl_ground(x) - rnd.random() * 1.5, "ground"))
        x += 4
    # canopy: scattered inside each crown
    for tx, th, r in CL_TREES:
        cy = _cl_ground(tx) - th
        for _ in range(42):
            a, d = rnd.random() * 2 * math.pi, math.sqrt(rnd.random()) * r
            pts.append((tx + d * math.cos(a), cy + d * math.sin(a) * 0.9,
                        "veg"))
    # roof and the near wall
    for k in range(11):
        pts.append((bx0 + 2 + k * (bx1 - bx0 - 4) / 10,
                    roof_y - rnd.random() * 1.5, "building"))
    for k in range(6):
        pts.append((bx1 - 1 + rnd.random() * 1.5,
                    roof_y + 6 + k * (bh - 12) / 5, "building"))
    # the car: a few points along its top
    cy = _cl_ground(CL_CAR)
    for dx, dy in ((-19, -6), (-13, -13), (-7, -15), (0, -15), (6, -15),
                   (12, -9), (18, -6)):
        pts.append((CL_CAR + dx, cy + dy + rnd.random() * 1.2, "other"))
    return pts


def _cl_ghosts(fig, ox, oy):
    """The objects behind the points, faint, so the reader knows what the
    points came from."""
    grp = g(opacity="0.28")
    for tx, th, r in CL_TREES:
        gy = _cl_ground(tx)
        grp.add(line(ox + tx, oy + gy, ox + tx, oy + gy - th + r * 0.5,
                     stroke="#7a5a3a", stroke_width=3))
        grp.add(circle(ox + tx, oy + gy - th, r, fill=VEG))
    bx0, bx1, bh = CL_BUILDING
    gy = _cl_ground((bx0 + bx1) / 2)
    grp.add(rect(ox + bx0, oy + gy - bh, bx1 - bx0, bh, fill="#c2cad2",
                 stroke=P["line"], stroke_width=1))
    grp.add(car(ox + CL_CAR, oy + _cl_ground(CL_CAR) - 9.5, 0.6))
    grp.add(path("M" + " L".join(f"{ox + x:.1f},{oy + _cl_ground(x):.1f}"
                                 for x in range(CL_X0, CL_X1 + 1, 4)),
                 fill="none", stroke=GROUND, stroke_width=1.5))
    fig.add(grp)


CL_COLOURS = {"ground": GROUND, "veg": "#2f6b2f", "building": BUILT,
              "other": OTHER}


def build_ground_classification() -> Figure:
    fig = Figure(W, 466, "From points to a bare-earth DTM",
                 "Every point gets a label, and only the ground points build "
                 "the terrain model. Where cover was dense, the surface "
                 "between them is interpolated and less certain.")
    gap = 37
    cards = [30 + i * (CL_W + gap) for i in range(3)]
    heads = ("1. All the points", "2. Classified", "3. Ground only, gridded")
    oy = 84
    for x, head in zip(cards, heads):
        fig.add(rect(x, oy, CL_W, 328, **CARD))
        _t(fig, x + CL_W / 2, oy + 28, head, size=15, bold=True)
    for (x, label) in ((cards[0], "classify"), (cards[1], "keep ground")):
        ax0, ax1 = x + CL_W + 4, x + CL_W + gap - 4
        fig.add(arrow(ax0, oy + 180, ax1, oy + 180, color=BEAM, width=2.5,
                      head=9))
        _t(fig, (ax0 + ax1) / 2, oy + 166, label, size=12, bold=True,
           fill=BEAM)

    pts = _cl_points()
    sy = oy + 50                      # scene offset inside the card

    # 1. every point, one colour
    ox = cards[0]
    _cl_ghosts(fig, ox, sy)
    for x, y, _ in pts:
        fig.add(circle(round(ox + x, 1), round(sy + y, 1), 2.5,
                       fill=P["dark"]))
    _t(fig, ox + CL_W / 2, oy + 300, "a slice through the cloud: canopy,",
       size=11.5, fill=P["muted"])
    _t(fig, ox + CL_W / 2, oy + 316, "a roof, a parked car, the ground",
       size=11.5, fill=P["muted"])

    # 2. the same points, labelled
    ox = cards[1]
    _cl_ghosts(fig, ox, sy)
    for x, y, cls in pts:
        fig.add(circle(round(ox + x, 1), round(sy + y, 1), 2.5,
                       fill=CL_COLOURS[cls]))
    for k, (cls, name) in enumerate((("ground", "ground"),
                                     ("veg", "vegetation"),
                                     ("building", "building"),
                                     ("other", "other: the car"))):
        lx = ox + 24 + (k % 2) * 118
        ly = oy + 56 + (k // 2) * 18
        fig.add(circle(lx, ly - 4, 4, fill=CL_COLOURS[cls]))
        _t(fig, lx + 10, ly, name, size=12, anchor="start")
    _t(fig, ox + CL_W / 2, oy + 300, "a filter sorts them by shape:",
       size=11.5, fill=P["muted"])
    _t(fig, ox + CL_W / 2, oy + 316, "the lowest smooth surface is ground",
       size=11.5, fill=P["muted"])

    # 3. ground points only, with the surface through them
    ox = cards[2]
    _cl_ghosts(fig, ox, sy)
    ground = [(x, y) for x, y, cls in pts if cls == "ground"]
    for x, y in ground:
        fig.add(circle(round(ox + x, 1), round(sy + y, 1), 2.5, fill=GROUND))
    # the DTM: solid where points are near, dashed where none are
    xs = list(range(CL_X0, CL_X1 + 1, 3))
    gx = sorted(x for x, _ in ground)

    def near(x):
        return any(abs(x - px) <= 6 for px in gx)

    runs, cur, state = [], [], None
    for x in xs:
        s = near(x)
        if state is None or s == state:
            cur.append(x)
        else:
            runs.append((state, cur))
            cur = [cur[-1], x]
        state = s
    runs.append((state, cur))
    for solid, run in runs:
        d = "M" + " L".join(f"{ox + x:.1f},{sy + _cl_ground(x):.1f}"
                            for x in run)
        fig.add(path(d, fill="none", stroke=BEAM, stroke_width=3.5,
                     stroke_linecap="round",
                     stroke_dasharray=None if solid else "6 5"))
    # the grid: one height per cell
    for k in range(0, 11):
        x = CL_X0 + k * (CL_X1 - CL_X0) / 10
        fig.add(line(ox + x, sy + _cl_ground(x) - 7, ox + x,
                     sy + _cl_ground(x) + 7, stroke=BEAM, stroke_width=1))
    # legend
    lx, ly = ox + 24, oy + 56
    fig.add(line(lx, ly - 4, lx + 28, ly - 4, stroke=BEAM, stroke_width=3.5,
                 stroke_linecap="round"))
    _t(fig, lx + 36, ly, "DTM through the ground points", size=12,
       anchor="start")
    fig.add(line(lx, ly + 14, lx + 28, ly + 14, stroke=BEAM, stroke_width=3.5,
                 stroke_linecap="round", stroke_dasharray="6 5"))
    _t(fig, lx + 36, ly + 18, "interpolated: no points under it", size=12,
       anchor="start")
    _t(fig, ox + CL_W / 2, oy + 300, "grid it: one height per cell, the",
       size=11.5, fill=P["muted"])
    _t(fig, ox + CL_W / 2, oy + 316, "ticks; the trees and roof are gone",
       size=11.5, fill=P["muted"])

    _t(fig, W / 2, 444,
       "Software does the sorting with filters such as a cloth simulation "
       "filter. Check its answer where the cover was dense or the ground "
       "steep.", size=13, fill=P["muted"], italic=True)
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
        (build_lidar_returns, 1, "", "lidar_returns"),
        (build_canopy_gaps, 1, "b", "canopy_gaps"),
        (build_ground_classification, 1, "c", "ground_classification"),
    ):
        fname = os.path.join(args.out, figure_name(6, number, slug, variant))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
