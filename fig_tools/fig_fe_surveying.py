"""Figures for the FE Surveying Review (Week 12 deck and reading).

Numbered in the order the deck uses them, which is the order the reading will
follow. Three figures are plotted from the worked examples' own numbers, so a
drawing cannot disagree with the arithmetic beside it:

    Figure 7  the level run BM-1 to BM-2 (rod readings and elevations)
    Figure 8  the four-sided traverse (adjusted coordinates, angles, distances)
    Figure 11 the crest vertical curve (g1, g2, L, PVI)

Figures 5 and 6 carry official values for the BYU Engineering Building: the NGS
GEOID18 geoid height, the USGS ground elevation, and the NGS NCAT state plane
and UTM scale and combined factors (sources beside each builder).

If a worked example changes, change the numbers here and re-run.

Usage:
    python fig_tools/fig_fe_surveying.py --out docs/gen_reading/images
    python fig_tools/fig_fe_surveying.py --png          (needs Inkscape)

Outputs (all w12_ in docs/gen_reading/images/):
    w12_fig01_right_triangle.svg     right triangle; reducing a slope distance
    w12_fig02_azimuth_bearing.svg    one direction as an azimuth and a bearing
    w12_fig03_field_angles.svg       interior, deflection, angle to the right
    w12_fig04_oblique_triangle.svg   side a opposite angle A
    w12_fig05_height_systems.svg     ground, geoid, ellipsoid; h = H + N
    w12_fig06_grid_ground.svg        ground, ellipsoid and grid lengths at BYU
    w12_fig07_leveling_run.svg       the BM-1 to BM-2 level run, to scale
    w12_fig08_traverse.svg           the worked traverse, to scale
    w12_fig09_average_end_area.svg   two end areas and the prism between them
    w12_fig10_horizontal_curve.svg   parts of a simple circular curve
    w12_fig11_vertical_curve.svg     the worked crest curve, to scale
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    path, polygon, rect, render_png, text)

WEEK = 12
CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)
FILL = "#dce7f2"        # light blue fill for areas
EDGE = "#3d6f9e"        # darker blue for the drawn geometry
GRID = "#b9c6d2"        # light lines: axes, construction
ORANGE = "#e67e22"      # the second quantity when two are compared


def _title(number: int, s: str) -> str:
    return f"Figure {number}: {s}"


def _t(fig, x, y, s, size=14, bold=False, fill=None, anchor="middle",
       italic=False):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 font_style="italic" if italic else None,
                 fill=fill or P["ink"]))


def _az(cx, cy, az, r):
    """Point at azimuth az (degrees clockwise from screen-up) and radius r."""
    a = math.radians(az)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def _arc(cx, cy, r, az1, az2, clockwise=True, color=None, width=2.5,
         head=9, dashed=False):
    """Circular arc from az1 to az2 with an arrowhead at az2."""
    color = color or P["accent"]
    sweep = (az2 - az1) % 360 if clockwise else (az1 - az2) % 360
    x1, y1 = _az(cx, cy, az1, r)
    x2, y2 = _az(cx, cy, az2, r)
    d = (f"M {x1:.1f} {y1:.1f} A {r} {r} 0 {1 if sweep > 180 else 0} "
         f"{1 if clockwise else 0} {x2:.1f} {y2:.1f}")
    out = g(path(d, fill="none", stroke=color, stroke_width=width,
                 stroke_dasharray="6 4" if dashed else None))
    if head:
        a = math.radians(az2)
        tx, ty = math.cos(a), math.sin(a)      # clockwise tangent on screen
        if not clockwise:
            tx, ty = -tx, -ty
        nx, ny = -ty, tx
        bx, by = x2 - tx * head, y2 - ty * head
        out.add(polygon([(x2, y2), (bx + nx * head * 0.5, by + ny * head * 0.5),
                         (bx - nx * head * 0.5, by - ny * head * 0.5)],
                        fill=color))
    return out


def _leader(fig, start, target, color=None):
    color = color or P["accent"]
    fig.add(line(*start, *target, stroke=color, stroke_width=1.5))
    fig.add(circle(*target, 3, fill=color))


def _right_mark(fig, x, y, ux, uy, vx, vy, s=12):
    """Small square marking a right angle at (x, y) between unit dirs u, v."""
    pts = [(x + ux * s, y + uy * s), (x + ux * s + vx * s, y + uy * s + vy * s),
           (x + vx * s, y + vy * s)]
    fig.add(path(f"M {pts[0][0]:.1f} {pts[0][1]:.1f} L {pts[1][0]:.1f} "
                 f"{pts[1][1]:.1f} L {pts[2][0]:.1f} {pts[2][1]:.1f}",
                 fill="none", stroke=P["line"], stroke_width=1.5))


# ---------------------------------------------------------------------------
# Figure 1 - right triangle, and reducing a slope distance
# ---------------------------------------------------------------------------
def build_right_triangle(number: int) -> Figure:
    fig = Figure(900, 340, _title(number, "Right triangles, and reducing a "
                                  "slope distance"),
                 "Every computation that follows uses horizontal distance. "
                 "Reduce a slope distance first.")
    for x in (30, 465):
        fig.add(rect(x, 66, 405, 254, **CARD))
    _t(fig, 232, 92, "Right triangle", bold=True)
    _t(fig, 667, 92, "Slope distance to horizontal", bold=True)

    # left: right triangle
    ax, ay, bx, by, cx_, cy_ = 80, 280, 360, 280, 360, 120
    fig.add(polygon([(ax, ay), (bx, by), (cx_, cy_)], fill=FILL, stroke=EDGE,
                    stroke_width=2.5))
    _right_mark(fig, bx, by, -1, 0, 0, -1)
    fig.add(_arc(ax, ay, 50, 90, 90 - math.degrees(math.atan2(160, 280)),
                 clockwise=False, color=P["ink"], width=1.8, head=0))
    _t(fig, ax + 64, ay - 10, "θ", size=16, bold=True)
    _t(fig, 220, 304, "b, adjacent", anchor="middle")
    _t(fig, 372, 205, "a, opposite", anchor="start")
    _t(fig, 196, 188, "c, hypotenuse", anchor="end")

    # right: slope distance S at vertical angle alpha, zenith angle z
    ox, oy = 520, 280
    alpha = 28
    sx, sy = _az(ox, oy, 90 - alpha, 300)
    fig.add(line(ox, oy, sx, sy, stroke=EDGE, stroke_width=3.5))
    fig.add(line(ox, oy, sx, oy, stroke=P["ink"], stroke_width=1.8,
                 stroke_dasharray="7 5"))
    fig.add(line(sx, oy, sx, sy, stroke=ORANGE, stroke_width=2.2,
                 stroke_dasharray="7 5"))
    _right_mark(fig, sx, oy, -1, 0, 0, -1)
    fig.add(line(ox, oy, ox, 118, stroke=GRID, stroke_width=1.5,
                 stroke_dasharray="4 4"))
    fig.add(_arc(ox, oy, 62, 90, 90 - alpha, clockwise=False, color=P["ink"],
                 width=1.8, head=0))
    fig.add(_arc(ox, oy, 40, 0, 90 - alpha, clockwise=True, color=GRID,
                 width=1.8, head=0))
    fig.add(circle(ox, oy, 5, fill=P["ink"]))
    _t(fig, ox + 72, oy - 10, "α", size=16, bold=True)
    _t(fig, ox + 16, oy - 46, "z", size=15, bold=True, fill=P["muted"])
    _t(fig, 640, 196, "S, slope distance", anchor="end", fill=EDGE, bold=True)
    _t(fig, (ox + sx) / 2, 304, "H = S cos α", bold=True)
    _t(fig, sx - 10, (oy + sy) / 2 - 8, "V = S sin α", anchor="end",
       fill=ORANGE, bold=True)
    _t(fig, 545, 130, "From a zenith angle z:", anchor="start", size=12,
       fill=P["muted"])
    _t(fig, 545, 146, "H = S sin z,  V = S cos z", anchor="start", size=12,
       fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 2 - azimuth and bearing
# ---------------------------------------------------------------------------
def build_azimuth_bearing(number: int) -> Figure:
    W, H = 600, 500
    fig = Figure(W, H, _title(number, "One direction, two ways"),
                 "Azimuth: 0° to 360°, clockwise from north. Bearing: under "
                 "90°, from N or S toward E or W.")
    cx, cy, R = 300, 262, 150
    az = 125
    fig.add(circle(cx, cy, R, fill=P["white"], stroke=GRID, stroke_width=1.5))
    fig.add(line(cx, cy - R - 18, cx, cy + R + 18, stroke="#999999",
                 stroke_width=1.2))
    fig.add(line(cx - R - 18, cy, cx + R + 18, cy, stroke="#999999",
                 stroke_width=1.2))
    for s, x, y in (("N", cx, cy - R - 26), ("S", cx, cy + R + 40),
                    ("E", cx + R + 34, cy + 6), ("W", cx - R - 34, cy + 6)):
        _t(fig, x, y, s, size=18, bold=True)
    for s, x, y in (("NE", cx + R + 10, cy - R + 10), ("NW", cx - R - 10,
                    cy - R + 10), ("SW", cx - R - 10, cy + R),
                    ("SE", cx + R + 10, cy + R)):
        _t(fig, x, y, s, fill=P["muted"])
    fig.add(_arc(cx, cy, 55, 0, az, clockwise=True, color=P["accent"]))
    fig.add(_arc(cx, cy, 100, 180, az, clockwise=False, color=ORANGE))
    ex, ey = _az(cx, cy, az, R + 12)
    fig.add(arrow(cx, cy, ex, ey, color=P["ink"], width=3, head=14))
    fig.add(circle(cx, cy, 4, fill=P["ink"]))

    m = _az(cx, cy, 60, 55)
    lx, ly = cx + 105, cy - 118
    _leader(fig, (lx - 4, ly + 6), m)
    _t(fig, lx, ly, "Azimuth 125°", anchor="start", bold=True)
    _t(fig, lx, ly + 17, "from north, clockwise", anchor="start", size=12,
       fill=P["muted"])
    m = _az(cx, cy, 152, 100)
    lx, ly = 28, cy + 60
    _leader(fig, (lx + 118, ly - 5), m, color=ORANGE)
    _t(fig, lx, ly, "Bearing S 55° E", anchor="start", bold=True)
    _t(fig, lx, ly + 17, "from south, toward east", anchor="start", size=12,
       fill=P["muted"])
    _t(fig, W / 2, H - 14, "SE quadrant: bearing = 180° − azimuth = "
       "180° − 125° = 55°", size=12, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 3 - angles as they are measured in the field
# ---------------------------------------------------------------------------
def build_field_angles(number: int) -> Figure:
    fig = Figure(900, 360, _title(number, "Three ways to measure an angle "
                                  "in the field"),
                 "Every angle is turned at a station, from one line to another.")
    for x in (30, 320, 610):
        fig.add(rect(x, 64, 260, 276, **CARD))
    _t(fig, 160, 90, "Interior angle", bold=True)
    _t(fig, 450, 90, "Deflection angle", bold=True)
    _t(fig, 740, 90, "Angle to the right", bold=True)

    # interior: a pentagon, arc inside at the top vertex
    cx, cy, r = 160, 205, 82
    pts = [_az(cx, cy, a, r) for a in (0, 72, 144, 216, 288)]
    fig.add(polygon(pts, fill=FILL, stroke=EDGE, stroke_width=2.5))
    top = pts[0]

    def _dir(p, q):
        return math.degrees(math.atan2(q[0] - p[0], -(q[1] - p[1]))) % 360

    fig.add(_arc(top[0], top[1], 30, _dir(top, pts[1]), _dir(top, pts[4]),
                 clockwise=True, color=P["ink"], width=2, head=0))
    _t(fig, top[0], top[1] + 50, "108°", size=13, bold=True)
    fig.add(circle(*top, 4.5, fill=P["ink"]))
    _t(fig, 160, 312, "Inside a closed figure.", size=12, fill=P["muted"])
    _t(fig, 160, 328, "n sides: they sum to (n − 2) × 180°", size=12,
       fill=P["muted"])

    # deflection: line runs east, turns 35° right; arc from the extension
    vx, vy = 450, 175
    fig.add(line(340, 175 + 0, vx, vy, stroke=EDGE, stroke_width=3))
    ex, ey = _az(vx, vy, 90, 120)
    fig.add(line(vx, vy, ex, ey, stroke=GRID, stroke_width=2,
                 stroke_dasharray="7 5"))
    nx, ny = _az(vx, vy, 125, 125)
    fig.add(line(vx, vy, nx, ny, stroke=EDGE, stroke_width=3))
    fig.add(_arc(vx, vy, 70, 90, 125, clockwise=True, color=P["accent"]))
    fig.add(circle(vx, vy, 4.5, fill=P["ink"]))
    _t(fig, 532, 205, "35° R", anchor="start", bold=True, fill=P["accent"])
    _t(fig, 540, 146, "extension of", anchor="middle", size=12,
       fill=P["muted"])
    _t(fig, 540, 161, "the previous line", anchor="middle", size=12,
       fill=P["muted"])
    _t(fig, 450, 312, "From the previous line, extended.", size=12,
       fill=P["muted"])
    _t(fig, 450, 328, "Always marked R or L. Route surveys.", size=12,
       fill=P["muted"])

    # angle to the right: BS at az 240, FS at az 30, clockwise BS -> FS
    sx, sy = 740, 210
    bsx, bsy = _az(sx, sy, 240, 105)
    fsx, fsy = _az(sx, sy, 30, 105)
    fig.add(line(sx, sy, bsx, bsy, stroke=EDGE, stroke_width=3))
    fig.add(line(sx, sy, fsx, fsy, stroke=EDGE, stroke_width=3))
    fig.add(_arc(sx, sy, 42, 240, 30, clockwise=True, color=P["accent"]))
    fig.add(circle(sx, sy, 4.5, fill=P["ink"]))
    _t(fig, bsx - 6, bsy + 18, "backsight", anchor="middle", bold=True)
    _t(fig, fsx + 4, fsy - 8, "foresight", anchor="middle", bold=True)
    _t(fig, sx - 56, sy - 44, "150°", anchor="end", bold=True,
       fill=P["accent"])
    _t(fig, 740, 312, "Clockwise from backsight to foresight.", size=12,
       fill=P["muted"])
    _t(fig, 740, 328, "The total-station convention.", size=12,
       fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 4 - oblique triangle
# ---------------------------------------------------------------------------
def build_oblique_triangle(number: int) -> Figure:
    fig = Figure(600, 400, _title(number, "Naming an oblique triangle"),
                 "Each side carries the lower-case letter of the angle "
                 "opposite it.")
    A, B, C = (90, 330), (520, 290), (250, 100)
    fig.add(polygon([A, B, C], fill=FILL, stroke=EDGE, stroke_width=2.5))

    def ang(p, q):
        return math.degrees(math.atan2(q[0] - p[0], -(q[1] - p[1]))) % 360

    for p, q1, q2, lab, off in ((A, B, C, "A", (-22, 22)),
                                (B, C, A, "B", (18, 20)),
                                (C, A, B, "C", (0, -16))):
        a1, a2 = ang(p, q1), ang(p, q2)
        # draw the arc the short way round, inside the triangle
        cw = (a2 - a1) % 360 < 180
        fig.add(_arc(p[0], p[1], 34, a1, a2, clockwise=cw, color=P["ink"],
                     width=1.8, head=0))
        fig.add(circle(*p, 5, fill=P["ink"]))
        _t(fig, p[0] + off[0], p[1] + off[1], lab, size=18, bold=True)
    for (p, q), lab, off in (((B, C), "a", (16, -6)), ((A, C), "b", (-18, -4)),
                             ((A, B), "c", (0, 24))):
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        _t(fig, mx + off[0], my + off[1], lab, size=18, bold=True,
           fill=EDGE, italic=True)
    _t(fig, 300, 382, "Law of sines: a / sin A = b / sin B = c / sin C     "
       "Law of cosines: a² = b² + c² − 2bc cos A", size=12, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 5 - the level run, from the worked example
# ---------------------------------------------------------------------------
LEVEL_RUN = dict(
    start=("BM-1", 100.00),
    # (BS on the previous point, FS on the next point, next point name)
    setups=[(5.42, 3.26, "TP-1"), (7.18, 8.41, "TP-2"), (4.95, 6.07, "BM-2")],
)


def build_leveling_run(number: int) -> Figure:
    fig = Figure(900, 440, _title(number, "The level run from BM-1 to BM-2"),
                 "Vertical scale exaggerated. HI = elevation + BS; the next "
                 "elevation = HI − FS.")
    name, elev = LEVEL_RUN["start"]
    pts = [(name, elev)]
    his = []
    for bs, fs, nxt in LEVEL_RUN["setups"]:
        hi = elev + bs
        elev = hi - fs
        his.append((bs, fs, hi))
        pts.append((nxt, elev))

    x0, dx = 90, 240            # rod stations, instruments halfway between
    def Y(e):                   # 98 ft at y=400, 22 px per foot
        return 400 - (e - 98.0) * 22

    # ground: rod points plus a gentle rise under each instrument
    ground_mid = [100.9, 103.8, 100.4]
    prof = []
    for i, (_, e) in enumerate(pts):
        prof.append((x0 + i * dx, e))
        if i < len(ground_mid):
            prof.append((x0 + i * dx + dx / 2, ground_mid[i]))
    poly = [(40, Y(prof[0][1]) + 6)] + [(x, Y(e)) for x, e in prof] + \
           [(860, Y(prof[-1][1]) - 2), (860, 420), (40, 420)]
    fig.add(polygon(poly, fill="#e9eef3", stroke="#8a9aab", stroke_width=2))

    # rods
    for i, (nm, e) in enumerate(pts):
        x = x0 + i * dx
        top = max(e + 10.0, (his[i][2] if i < len(his) else 0) + 1.2,
                  (his[i - 1][2] if i > 0 else 0) + 1.2)
        fig.add(rect(x - 5, Y(top), 10, Y(e) - Y(top), fill=EDGE))
        fig.add(circle(x, Y(e), 4, fill=P["ink"]))
        _t(fig, x, Y(e) + 22, nm, bold=True)
        _t(fig, x, Y(e) + 38, f"{e:.2f}", size=12, fill=P["muted"])

    # instruments and lines of sight
    for i, (bs, fs, hi) in enumerate(his):
        xi = x0 + i * dx + dx / 2
        gy = Y(ground_mid[i])
        hy = Y(hi)
        for lx in (-16, 0, 16):
            fig.add(line(xi, hy + 8, xi + lx, gy, stroke=P["ink"],
                         stroke_width=1.6))
        fig.add(rect(xi - 18, hy - 5, 36, 10, rx=3, fill=P["ink"]))
        xl, xr = x0 + i * dx + 6, x0 + (i + 1) * dx - 6
        fig.add(arrow(xi - 20, hy, xl, hy, color=P["accent"], width=2,
                      head=8))
        fig.add(arrow(xi + 20, hy, xr, hy, color=ORANGE, width=2, head=8))
        _t(fig, (xl + xi) / 2, hy - 8, f"BS {bs:.2f}", size=13, bold=True,
           fill=P["accent"])
        _t(fig, (xr + xi) / 2, hy - 8, f"FS {fs:.2f}", size=13, bold=True,
           fill=ORANGE)
        _t(fig, xi, hy - 26, f"HI {hi:.2f}", size=12, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 6 - the closed traverse, from the worked example
# ---------------------------------------------------------------------------
TRAVERSE = dict(
    points=[("A", 5000.00, 5000.00), ("B", 5256.22, 5443.91),
            ("C", 5625.63, 5210.86), ("D", 5383.76, 4774.64)],  # N, E
    legs=["512.53", "436.83", "498.81", "444.99"],               # AB, BC...
    angles=["90°25′15″", "87°45′00″", "93°15′00″", "88°34′45″"],  # adjusted
    az_ab="Az 60°00′00″",
)


def build_traverse(number: int) -> Figure:
    W, H = 640, 560
    fig = Figure(W, H, _title(number, "The traverse in the worked example"),
                 "Drawn to scale from the adjusted coordinates. Run "
                 "counterclockwise; adjusted interior angles shown.")
    pts = TRAVERSE["points"]
    n0 = min(p[1] for p in pts)
    e0 = min(p[2] for p in pts)
    s = 0.62                                      # px per ft
    ox, oy = 150, 488

    def XY(N, E):
        return ox + (E - e0) * s, oy - (N - n0) * s

    xy = [XY(N, E) for _, N, E in pts]
    cxm = sum(p[0] for p in xy) / 4
    cym = sum(p[1] for p in xy) / 4
    fig.add(polygon(xy, fill=FILL, stroke=EDGE, stroke_width=2.5))
    for i in range(4):
        p, q = xy[i], xy[(i + 1) % 4]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        ux, uy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        # direction arrow along the leg
        fig.add(arrow(mx - ux * 22, my - uy * 22, mx + ux * 22, my + uy * 22,
                      color=EDGE, width=2.5, head=11))
        # leg label outside the figure, anchored away from the line
        ox_, oy_ = mx - cxm, my - cym
        Lo = math.hypot(ox_, oy_)
        ox_, oy_ = ox_ / Lo, oy_ / Lo
        name = pts[i][0] + pts[(i + 1) % 4][0]
        label = f"{name}  {TRAVERSE['legs'][i]} ft"
        if abs(ox_) > 0.6:
            anchor = "start" if ox_ > 0 else "end"
            _t(fig, mx + ox_ * 26, my + oy_ * 26 + 5, label, size=13,
               bold=True, anchor=anchor)
        else:
            _t(fig, mx + ox_ * 30, my + oy_ * 30 + 5, label, size=13,
               bold=True)
    for k, ((nm, _, _), (x, y), angle) in enumerate(
            zip(pts, xy, TRAVERSE["angles"])):
        fig.add(circle(x, y, 6, fill=P["ink"]))
        vx, vy = x - cxm, y - cym
        Lv = math.hypot(vx, vy)
        _t(fig, x + vx / Lv * 24, y + vy / Lv * 24 + 6, nm, size=18,
           bold=True)
        r_in = 125 if k == 0 else 72      # clear of the azimuth arc at A
        _t(fig, x - vx / Lv * r_in, y - vy / Lv * r_in + 5, angle, size=12,
           fill=P["muted"])
    # north arrow and azimuth of AB at A
    ax, ay = xy[0]
    fig.add(line(ax, ay, ax, ay - 90, stroke=GRID, stroke_width=1.5,
                 stroke_dasharray="5 4"))
    fig.add(_arc(ax, ay, 60, 0, 60, clockwise=True, color=ORANGE, width=2))
    _t(fig, ax + 8, ay - 70, TRAVERSE["az_ab"], anchor="start", size=12,
       bold=True, fill=ORANGE)
    fig.add(arrow(48, 150, 48, 86, color=P["ink"], width=2.5, head=12))
    _t(fig, 48, 172, "N", size=16, bold=True)
    _t(fig, 48, 188, "grid", size=11, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 7 - average end area
# ---------------------------------------------------------------------------
def build_average_end_area(number: int) -> Figure:
    fig = Figure(900, 400, _title(number, "Volume between two cross-sections"),
                 "Average end area uses the two ends. The prismoidal formula "
                 "also uses the section measured halfway, Aₘ.")
    s = 4.2                        # px per ft in the section plane
    shift = (300, -150)            # 100 ft along the alignment, in oblique view

    def section(cx, cy, depth, bottom=20.0, slope=1.5):
        top = bottom + 2 * slope * depth
        return [(cx - top / 2 * s, cy), (cx + top / 2 * s, cy),
                (cx + bottom / 2 * s, cy + depth * s),
                (cx - bottom / 2 * s, cy + depth * s)]

    c1 = (230, 285)
    s1 = section(*c1, 7.8)                         # 247 ft², drawn as 245
    s2 = section(c1[0] + shift[0], c1[1] + shift[1], 9.3)     # 316, as 318
    sm = section(c1[0] + shift[0] / 2, c1[1] + shift[1] / 2, 8.6)
    # prism edges first, so the sections sit on top
    for a, b in zip(s1, s2):
        fig.add(line(*a, *b, stroke=GRID, stroke_width=1.5))
    # ground lines
    for sec in (s1, s2):
        fig.add(line(sec[0][0] - 40, sec[0][1], sec[1][0] + 40, sec[1][1],
                     stroke="#8a9aab", stroke_width=2))
    fig.add(polygon(s2, fill=FILL, stroke=EDGE, stroke_width=2.5))
    fig.add(polygon(sm, fill="none", stroke=ORANGE, stroke_width=2,
                    stroke_dasharray="7 5"))
    fig.add(polygon(s1, fill=FILL, stroke=EDGE, stroke_width=2.5))
    _t(fig, c1[0], c1[1] + 18, "A₁ = 245 ft²", bold=True)
    _t(fig, c1[0], c1[1] + 62, "Sta 10+00", fill=P["muted"])
    c2 = (c1[0] + shift[0], c1[1] + shift[1])
    _t(fig, c2[0], c2[1] + 20, "A₂ = 318 ft²", bold=True)
    _t(fig, c2[0] + 150, c2[1] + 20, "Sta 11+00", fill=P["muted"])
    # middle-section callout, upper left where the drawing is empty
    _leader(fig, (200, 150), (sm[0][0] + 6, sm[0][1] + 3), color=ORANGE)
    _t(fig, 196, 136, "Aₘ, measured at 10+50", anchor="end", bold=True,
       fill=ORANGE)
    _t(fig, 196, 152, "prismoidal formula only", anchor="end", size=12,
       fill=P["muted"])
    # length: a dimension line parallel to the alignment, below the prism
    b1, b2 = s1[2], s2[2]
    off = (34, 30)
    d1 = (b1[0] + off[0], b1[1] + off[1])
    d2 = (b2[0] + off[0], b2[1] + off[1])
    mx, my = (d1[0] + d2[0]) / 2, (d1[1] + d2[1]) / 2
    fig.add(arrow(mx, my, *d1, color=P["muted"], width=1.6, head=8))
    fig.add(arrow(mx, my, *d2, color=P["muted"], width=1.6, head=8))
    for b, d in ((b1, d1), (b2, d2)):
        fig.add(line(b[0] + 4, b[1] + 4, d[0] + 4, d[1] + 4, stroke=GRID,
                     stroke_width=1.2, stroke_dasharray="3 3"))
    _t(fig, mx + 14, my + 22, "L = 100 ft", anchor="start", bold=True,
       fill=P["muted"])
    # the formulas
    _t(fig, 690, 330, "V = L (A₁ + A₂) / 2", bold=True, fill=EDGE)
    _t(fig, 690, 352, "= 100 (245 + 318) / 2 = 28,150 ft³", size=13)
    _t(fig, 690, 372, "÷ 27 = 1,042.6 yd³", size=13)
    return fig


# ---------------------------------------------------------------------------
# Figure 8 - parts of a horizontal curve
# ---------------------------------------------------------------------------
def build_horizontal_curve(number: int) -> Figure:
    W, H = 760, 500
    fig = Figure(W, H, _title(number, "Parts of a simple horizontal curve"),
                 "Δ at the PI equals the central angle. Stationing follows "
                 "the curve: PT = PC + L, never PI + T.")
    ox, oy, R, half = 380, 90, 260, 35.0
    pc = _az(ox, oy, 180 + half, R)
    pt = _az(ox, oy, 180 - half, R)
    sec = R / math.cos(math.radians(half))
    pi_ = (ox, oy + sec)
    mid = (ox, oy + R)
    chord_y = pc[1]

    # radii and the centre angle
    for p in (pc, pt):
        fig.add(line(ox, oy, *p, stroke=GRID, stroke_width=1.8,
                     stroke_dasharray="7 5"))
    fig.add(line(ox, oy, *pi_, stroke=GRID, stroke_width=1.2,
                 stroke_dasharray="3 4"))
    fig.add(_arc(ox, oy, 50, 180 + half, 180 - half, clockwise=False,
                 color=P["ink"], width=2, head=0))
    _t(fig, ox, oy + 76, "Δ", size=18, bold=True)
    _t(fig, (ox + pc[0]) / 2 - 16, (oy + pc[1]) / 2, "R", size=16, bold=True,
       fill=P["muted"])
    _t(fig, (ox + pt[0]) / 2 + 16, (oy + pt[1]) / 2, "R", size=16, bold=True,
       fill=P["muted"])
    fig.add(circle(ox, oy, 5, fill=P["ink"]))
    _t(fig, ox, oy - 12, "O, centre", size=13, bold=True)

    # tangents, the back tangent extended past the PI, and Δ at the PI
    ux, uy = pi_[0] - pc[0], pi_[1] - pc[1]
    Lt = math.hypot(ux, uy)
    ux, uy = ux / Lt, uy / Lt
    vx, vy = pt[0] - pi_[0], pt[1] - pi_[1]
    vx, vy = vx / Lt, vy / Lt
    b0 = (pc[0] - ux * 110, pc[1] - uy * 110)
    f1 = (pt[0] + vx * 110, pt[1] + vy * 110)
    fig.add(line(*b0, *pi_, stroke=P["ink"], stroke_width=2.5))
    fig.add(line(*pi_, *f1, stroke=P["ink"], stroke_width=2.5))
    ext = (pi_[0] + ux * 90, pi_[1] + uy * 90)
    fig.add(line(*pi_, *ext, stroke=GRID, stroke_width=2,
                 stroke_dasharray="7 5"))
    a_ext = math.degrees(math.atan2(ux, -uy)) % 360
    a_fwd = math.degrees(math.atan2(vx, -vy)) % 360
    fig.add(_arc(pi_[0], pi_[1], 54, a_ext, a_fwd, clockwise=False,
                 color=P["accent"], width=2))
    _t(fig, pi_[0] + 70, pi_[1] + 8, "Δ", size=18, bold=True,
       fill=P["accent"])
    _t(fig, b0[0] - 4, b0[1] - 10, "back tangent", size=12, anchor="start",
       fill=P["muted"])
    _t(fig, f1[0] + 4, f1[1] - 10, "forward tangent", size=12, anchor="end",
       fill=P["muted"])

    # the curve and the long chord
    fig.add(path(f"M {pc[0]:.1f} {pc[1]:.1f} A {R} {R} 0 0 0 {pt[0]:.1f} "
                 f"{pt[1]:.1f}", fill="none", stroke=EDGE, stroke_width=4.5))
    fig.add(line(*pc, *pt, stroke=P["accent"], stroke_width=2,
                 stroke_dasharray="8 5"))
    _t(fig, ox - 80, chord_y - 9, "LC, long chord", size=13, bold=True,
       fill=P["accent"])

    # M and E along the centre line, labelled with leaders
    fig.add(line(ox + 5, chord_y, ox + 5, mid[1], stroke=P["ink"],
                 stroke_width=2))
    fig.add(line(ox + 5, mid[1], ox + 5, pi_[1], stroke=ORANGE,
                 stroke_width=2))
    m_at = (ox + 5, (chord_y + mid[1]) / 2)
    _leader(fig, (ox + 40, chord_y - 14), m_at)
    _t(fig, ox + 44, chord_y - 10, "M, middle ordinate", anchor="start",
       size=13, bold=True)
    e_at = (ox + 5, (mid[1] + pi_[1]) / 2)
    _leader(fig, (ox - 52, pi_[1] + 22), e_at, color=ORANGE)
    _t(fig, ox - 56, pi_[1] + 30, "E, external", anchor="end", size=13,
       bold=True, fill=ORANGE)

    # T on each tangent, outside the V
    nb = (-uy, ux)                 # outward from the back tangent
    nf = (-vy, vx)                 # outward from the forward tangent
    mb = ((pc[0] + pi_[0]) / 2, (pc[1] + pi_[1]) / 2)
    mf = ((pt[0] + pi_[0]) / 2, (pt[1] + pi_[1]) / 2)
    _t(fig, mb[0] + nb[0] * 20, mb[1] + nb[1] * 20 + 6, "T", size=16,
       bold=True)
    _t(fig, mf[0] + nf[0] * 20, mf[1] + nf[1] * 20 + 6, "T", size=16,
       bold=True)
    # L along the arc
    _leader(fig, (219, 352), _az(ox, oy, 197, R))
    _t(fig, 215, 357, "L, length along the curve", anchor="end", size=13,
       bold=True, fill=EDGE)

    for p, lab, dxl in ((pc, "PC", -12), (pt, "PT", 12)):
        fig.add(circle(*p, 6, fill=P["ink"]))
        _t(fig, p[0] + dxl, p[1] + 26, lab, size=15, bold=True,
           anchor="end" if dxl < 0 else "start")
    fig.add(circle(*pi_, 6, fill=P["ink"]))
    _t(fig, pi_[0] - 4, pi_[1] + 30, "PI", size=15, bold=True)
    return fig


# ---------------------------------------------------------------------------
# Figure 9 - the crest vertical curve, from the worked example
# ---------------------------------------------------------------------------
VCURVE = dict(g1=2.4, g2=-1.8, L=600.0, pvi_sta=2800.0, pvi_elev=4250.00)


def _sta(x):
    return f"{int(x // 100)}+{x % 100:05.2f}"


def build_vertical_curve(number: int) -> Figure:
    g1, g2, L = VCURVE["g1"], VCURVE["g2"], VCURVE["L"]
    pvi, ev = VCURVE["pvi_sta"], VCURVE["pvi_elev"]
    A = g2 - g1
    pvc, pvt = pvi - L / 2, pvi + L / 2
    e_pvc = ev - g1 / 100 * L / 2
    e_pvt = ev + g2 / 100 * L / 2
    xh = -g1 * L / A

    def y_curve(x):
        return e_pvc + g1 / 100 * x + A / (200 * L) * x * x

    W, H = 900, 420
    fig = Figure(W, H, _title(number, "The crest curve in the worked example"),
                 "Vertical scale exaggerated. A = g₂ − g₁ = "
                 f"{A:+.1f} %; ".replace("-", "−") +
                 f"the high point is x = −g₁L/A = {xh:.2f} ft past the PVC.")
    s0, s1 = pvc - 150, pvt + 150

    def X(sta):
        return 70 + (sta - s0) / (s1 - s0) * 760

    def Y(e):
        return 330 - (e - 4240.0) * 22

    # tangents
    fig.add(line(X(s0), Y(e_pvc - g1 / 100 * 150), X(pvi), Y(ev),
                 stroke=P["ink"], stroke_width=2, stroke_dasharray="8 6"))
    fig.add(line(X(pvi), Y(ev), X(s1), Y(e_pvt + g2 / 100 * 150),
                 stroke=P["ink"], stroke_width=2, stroke_dasharray="8 6"))
    # curve
    d = "M " + " L ".join(f"{X(pvc + x):.1f} {Y(y_curve(x)):.1f}"
                          for x in [i * L / 60 for i in range(61)])
    fig.add(path(d, fill="none", stroke=EDGE, stroke_width=4.5))
    # station ticks and L bracket
    base = 372
    for sta in (pvc, pvt):
        fig.add(line(X(sta), Y(y_curve(sta - pvc)) + 8, X(sta), base,
                     stroke=GRID, stroke_width=1.5, stroke_dasharray="4 4"))
    fig.add(arrow(X(pvi), base, X(pvc) + 2, base, color=P["muted"], width=1.6,
                  head=8))
    fig.add(arrow(X(pvi), base, X(pvt) - 2, base, color=P["muted"], width=1.6,
                  head=8))
    _t(fig, X(pvi), base + 20, f"L = {L:.0f} ft, measured horizontally",
       size=13, bold=True, fill=P["muted"])
    # high point
    hx, hy = X(pvc + xh), Y(y_curve(xh))
    fig.add(line(hx, hy, hx, base - 4, stroke=P["accent"], stroke_width=1.5,
                 stroke_dasharray="4 4"))
    fig.add(circle(hx, hy, 6, fill=P["accent"]))
    _t(fig, hx + 12, hy + 52, f"High point {_sta(pvc + xh)}", anchor="start",
       size=13, bold=True, fill=P["accent"])
    _t(fig, hx + 12, hy + 68, f"elev {y_curve(xh):,.2f}", anchor="start",
       size=12, fill=P["muted"])
    # points
    # labels sit where no line runs: below-right of the PVC (under the
    # curve), above the PVI, above-right of the PVT (the tangent drops away)
    for sta, e, lab, anchor, dx_, dy_ in (
            (pvc, e_pvc, "PVC", "start", 12, 26),
            (pvi, ev, "PVI", "middle", 0, -34),
            (pvt, e_pvt, "PVT", "start", 14, -30)):
        fig.add(circle(X(sta), Y(e), 6, fill=P["ink"]))
        _t(fig, X(sta) + dx_, Y(e) + dy_, f"{lab} {_sta(sta)}",
           anchor=anchor, size=13, bold=True)
        _t(fig, X(sta) + dx_, Y(e) + dy_ + 16, f"elev {e:,.2f}",
           anchor=anchor, size=12, fill=P["muted"])
    _t(fig, X(pvc) - 40, Y(e_pvc) + 6, f"g₁ = {g1:+.1f} %", anchor="end",
       bold=True)
    _t(fig, X(s1), Y(e_pvt + g2 / 100 * 150) + 24,
       f"g₂ = {g2:+.1f} %".replace("-", "−"), anchor="end", bold=True)
    return fig


# ---------------------------------------------------------------------------
# Figure 5 - height systems (ground, geoid, ellipsoid)
# N is the NGS GEOID18 value at the BYU Engineering Building (40.2466 N,
# 111.6476 W): https://geodesy.noaa.gov/api/geoid/ght?lat=40.2466&lon=-111.6476
# ---------------------------------------------------------------------------
GEOID_N_BYU = -16.93


def _blob(cx, cy, rx, ry, wobble, n=180):
    """Closed path: an ellipse plus wobble(az) px along the radius."""
    pts = []
    for i in range(n):
        az = 360 * i / n
        a = math.radians(az)
        r = (rx * ry) / math.hypot(ry * math.sin(a), rx * math.cos(a))
        r += wobble(az)
        pts.append(_az(cx, cy, az, r))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def build_height_systems(number: int) -> Figure:
    fig = Figure(900, 500, _title(number, "Three surfaces, two heights"),
                 "Not to scale. GNSS measures h above the ellipsoid; plans use "
                 "H above the geoid. A geoid model supplies N.")
    GROUND_FILL = "#ece6dc"
    GROUND_EDGE = "#9a8a72"

    # ---- left: the whole Earth ------------------------------------------
    fig.add(rect(30, 64, 250, 416, **CARD))
    _t(fig, 155, 90, "The whole Earth", bold=True)
    cx, cy, rx, ry = 155, 250, 100, 88          # flattening exaggerated

    def wob(az):                                 # geoid lumps, exaggerated
        return 7 * math.sin(math.radians(3 * az + 40)) + \
            5 * math.sin(math.radians(5 * az + 10))

    fig.add(path(_blob(cx, cy, rx, ry, lambda a: 0), fill=P["white"],
                 stroke=EDGE, stroke_width=2.5))
    fig.add(path(_blob(cx, cy, rx, ry, wob), fill="none", stroke=ORANGE,
                 stroke_width=2.2, stroke_dasharray="6 4"))
    # the site: a small box on the surface where the geoid dips below the
    # ellipsoid, as it does in Utah; zoom lines lead right to the site panel
    site_az = 60
    a = math.radians(site_az)
    r_site = (rx * ry) / math.hypot(ry * math.sin(a), rx * math.cos(a))
    bx, by = _az(cx, cy, site_az, r_site - 2)
    fig.add(rect(bx - 13, by - 11, 26, 22, fill="none", stroke=P["ink"],
                 stroke_width=1.5))
    fig.add(line(bx + 13, by - 11, 310, 150, stroke=GRID, stroke_width=1,
                 stroke_dasharray="4 4"))
    fig.add(line(bx + 13, by + 11, 310, 300, stroke=GRID, stroke_width=1,
                 stroke_dasharray="4 4"))
    _t(fig, 155, 378, "Ellipsoid: a smooth oval,", size=12, fill=EDGE,
       bold=True)
    _t(fig, 155, 394, "slightly flattened at the poles", size=12,
       fill=P["muted"])
    _t(fig, 155, 418, "Geoid: lumpy, above and below", size=12, fill=ORANGE,
       bold=True)
    _t(fig, 155, 434, "the ellipsoid (lumps exaggerated)", size=12,
       fill=P["muted"])
    _t(fig, 155, 462, "Box: a site in Utah, enlarged at right", size=12,
       fill=P["muted"])

    # ---- right: at the site ---------------------------------------------
    x0, x1 = 310, 870
    fig.add(rect(x0, 64, x1 - x0, 416, **CARD))
    _t(fig, (x0 + x1) / 2, 90, "At the site", bold=True)

    def ground_y(x):
        return 196 + 14 * math.sin((x - 330) / 70) + 6 * math.sin((x - 330) / 23)

    gx = [x0 + 1 + i * 4 for i in range(int((x1 - x0 - 2) / 4) + 1)]
    gpts = [(x, ground_y(x)) for x in gx]
    fig.add(polygon(gpts + [(gx[-1], 250), (gx[0], 250)], fill=GROUND_FILL,
                    stroke="none"))
    fig.add(path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in gpts),
                 fill="none", stroke=GROUND_EDGE, stroke_width=2.5))
    _t(fig, x1 - 14, ground_y(x1 - 14) - 12, "ground", anchor="end",
       bold=True, fill=GROUND_EDGE)
    # break marks: the ground is far above the two reference surfaces
    for yb in (262, 270):
        fig.add(path(f"M {x0 + 12} {yb} " + " ".join(
            f"L {x0 + 12 + 10 * k} {yb + (4 if k % 2 else -4)}"
            for k in range(1, 54)), fill="none", stroke=GRID,
            stroke_width=1.2))
    _t(fig, x1 - 16, 292, "the ground is far higher than drawn", anchor="end",
       size=12, fill=P["muted"])

    ell_y = 360
    fig.add(line(x0 + 10, ell_y, x1 - 10, ell_y, stroke=EDGE, stroke_width=3))
    _t(fig, x1 - 14, ell_y - 8, "ellipsoid", anchor="end", bold=True,
       fill=EDGE)

    def geoid_y(x):
        return ell_y + 40 + 5 * math.sin((x - 330) / 55)

    gd = [(x, geoid_y(x)) for x in gx]
    fig.add(path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in gd),
                 fill="none", stroke=ORANGE, stroke_width=2.5,
                 stroke_dasharray="8 5"))
    _t(fig, x1 - 14, geoid_y(x1 - 14) + 20, "geoid, about mean sea level",
       anchor="end", bold=True, fill=ORANGE)

    # the point P and a GNSS rover on a pole
    px = 560
    py = ground_y(px)
    fig.add(line(px, py, px, py - 54, stroke=P["ink"], stroke_width=2.5))
    fig.add(rect(px - 16, py - 64, 32, 10, rx=5, fill=P["ink"]))
    fig.add(circle(px, py, 5, fill=P["ink"]))
    _t(fig, px + 12, py - 30, "GNSS rover", anchor="start", size=12,
       fill=P["muted"])
    _t(fig, px - 10, py + 22, "P", size=15, bold=True, anchor="end")
    fig.add(line(470, py, 640, py, stroke=GRID, stroke_width=1.2,
                 stroke_dasharray="3 3"))

    # H: geoid up to P
    hx = 490
    fig.add(arrow(hx, geoid_y(hx), hx, py + 2, color=P["ink"], width=2.2,
                  head=10))
    _t(fig, hx - 10, 318, "H", anchor="end", size=18, bold=True)
    _t(fig, hx - 10, 336, "orthometric height:", anchor="end", size=12,
       fill=P["muted"])
    _t(fig, hx - 10, 350, "the elevation on plans (NAVD 88)", anchor="end",
       size=12, fill=P["muted"])
    # h: ellipsoid up to P
    ex_ = 630
    fig.add(arrow(ex_, ell_y, ex_, py + 2, color=EDGE, width=2.2, head=10))
    _t(fig, ex_ + 10, 316, "h", anchor="start", size=18, bold=True, fill=EDGE)
    _t(fig, ex_ + 10, 334, "ellipsoid height:", anchor="start", size=12,
       fill=P["muted"])
    _t(fig, ex_ + 10, 348, "what GNSS measures", anchor="start", size=12,
       fill=P["muted"])
    # N: ellipsoid down to the geoid (negative here)
    nx = 760
    fig.add(arrow(nx, ell_y, nx, geoid_y(nx) - 1, color=ORANGE, width=2.2,
                  head=9))
    _t(fig, nx - 10, ell_y + 26, "N", anchor="end", size=16, bold=True,
       fill=ORANGE)
    _t(fig, (x0 + x1) / 2, 452, f"h = H + N.   At BYU, N = {GEOID_N_BYU:.2f} m "
       "(NGS GEOID18), so h = H − 16.93 m".replace("-", "−"), size=13,
       bold=True)
    _t(fig, (x0 + x1) / 2, 470, "A GNSS height reads about 17 m lower than "
       "the plan elevation of the same point.", size=12, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 6 - grid versus ground (state plane and UTM)
# Values for the BYU Engineering Building (40.2466 N, 111.6476 W), 2026-11-17:
#   ground elevation 1,416.82 m, USGS EPQS
#     https://epqs.nationalmap.gov/v1/json?x=-111.6476&y=40.2466&wkid=4326&units=Meters
#   h = 1,416.82 + (-16.93) = 1,399.89 m (GEOID18, see Figure 5)
#   NGS NCAT, SPCS 83 Utah Central (4302) and UTM 12:
#     https://geodesy.noaa.gov/api/ncat/llh?lat=40.2466&lon=-111.6476&eht=1399.89
#     &inDatum=nad83(2011)&outDatum=nad83(2011)&spcZone=4302
# The elevation factor is derived: combined / scale (0.99978 for both).
# ---------------------------------------------------------------------------
BYU_SPC = dict(scale=0.99992458, combined=0.99970504)
BYU_UTM = dict(scale=0.99963734, combined=0.99941786)
BYU_GROUND_M = 1416.82


def build_grid_ground(number: int) -> Figure:
    k, c = BYU_SPC["scale"], BYU_SPC["combined"]
    ef = c / k
    fig = Figure(900, 500, _title(number, "Grid distance is not ground "
                                  "distance"),
                 "Not to scale. A tape measures on the ground; state plane "
                 "and UTM coordinates live on the grid.")
    GROUND_EDGE = "#9a8a72"
    GRID_C = P["ink"]

    # ---- left: where the scale is exact ---------------------------------
    fig.add(rect(30, 64, 290, 416, **CARD))
    _t(fig, 175, 90, "Where the grid scale is exact", bold=True)
    ccx, ccy, R = 175, 380, 200             # a piece of the Earth
    arc_pts = [_az(ccx, ccy, a, R) for a in range(-38, 39)]
    fig.add(path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in arc_pts),
                 fill="none", stroke=EDGE, stroke_width=3))
    # secant projection surface: cuts the arc at two standard lines
    std = 22
    ys = ccy - R * math.cos(math.radians(std))
    xs1 = ccx - R * math.sin(math.radians(std))
    xs2 = ccx + R * math.sin(math.radians(std))
    fig.add(line(45, ys, 305, ys, stroke=GRID_C, stroke_width=2.2,
                 stroke_dasharray="8 5"))
    for xs in (xs1, xs2):
        fig.add(circle(xs, ys, 5, fill=P["accent"]))
    _t(fig, ccx, ys + 20, "k < 1", size=13, bold=True)
    _t(fig, 62, ys - 9, "k > 1", size=13, bold=True)
    _t(fig, 288, ys - 9, "k > 1", size=13, bold=True)
    bx = ccx - 34
    fig.add(circle(bx, ys, 5, fill=ORANGE))
    _leader(fig, (bx, ys + 70), (bx, ys + 5), color=ORANGE)
    _t(fig, bx, ys + 86, f"BYU: k = {k:.5f}", size=12, bold=True,
       fill=ORANGE)
    _t(fig, bx, ys + 101, "(Utah Central zone)", size=12, fill=P["muted"])
    _leader(fig, (250, ys + 50), (xs2, ys + 4))
    _t(fig, 250, ys + 66, "k = 1 on the", size=12, bold=True,
       fill=P["accent"])
    _t(fig, 250, ys + 81, "standard lines", size=12, bold=True,
       fill=P["accent"])
    _t(fig, 175, 340, "Solid: the ellipsoid.  Dashed: the projection.",
       size=12, fill=P["ink"])
    for i, s_ in enumerate((
            "Utah's three zones use a cone",
            "(Lambert conformal conic); UTM and",
            "north–south zones use a cylinder",
            "(transverse Mercator). Either way the",
            "surface cuts the Earth along two lines",
            "where the scale is exact. That is why",
            "a state is split into zones.")):
        _t(fig, 175, 368 + 15 * i, s_, size=12, fill=P["muted"])

    # ---- right: three lengths for one line ------------------------------
    x0, x1 = 340, 870
    fig.add(rect(x0, 64, x1 - x0, 416, **CARD))
    _t(fig, (x0 + x1) / 2, 90, "One line at BYU, three lengths", bold=True)
    mid = 640
    # converging normals toward the Earth's centre (far below)
    gy_, ry_, gw_, rw_ = 150, 352, 320, 276
    ew_ = gw_ - (gw_ - rw_) * (262 - gy_) / (ry_ - gy_)
    levels = [("ground", gy_, gw_), ("ellipsoid", 262, ew_), ("grid", ry_, rw_)]
    for side in (-1, 1):
        fig.add(line(mid + side * gw_ / 2, gy_, mid + side * rw_ / 2, ry_,
                     stroke=GRID, stroke_width=1.2, stroke_dasharray="4 4"))
    # ground
    gy, gw = levels[0][1], levels[0][2]
    fig.add(path(f"M {x0 + 20} {gy + 10} Q {mid - 200} {gy - 18} "
                 f"{mid - gw / 2} {gy} L {mid + gw / 2} {gy} "
                 f"Q {mid + 200} {gy + 14} {x1 - 20} {gy - 6}",
                 fill="none", stroke=GROUND_EDGE, stroke_width=3))
    for xx in (mid - gw / 2, mid + gw / 2):
        fig.add(circle(xx, gy, 5, fill=P["ink"]))
    _t(fig, mid - gw / 2 - 10, gy - 10, "A", anchor="end", bold=True)
    _t(fig, mid + gw / 2 + 10, gy - 10, "B", anchor="start", bold=True)
    _t(fig, mid, gy - 14, "ground distance: what you tape", size=13,
       bold=True, fill=GROUND_EDGE)
    _t(fig, mid, gy + 22, "1,000.000 ft", size=13)
    # ellipsoid (a gentle arc)
    ey, ew = levels[1][1], levels[1][2]
    fig.add(path(f"M {mid - ew / 2} {ey + 4} Q {mid} {ey - 8} {mid + ew / 2} "
                 f"{ey + 4}", fill="none", stroke=EDGE, stroke_width=3))
    _t(fig, mid, ey - 14, "on the ellipsoid", size=13, bold=True, fill=EDGE)
    _t(fig, mid, ey + 24, f"{1000 * ef:,.3f} ft", size=13)
    # grid (straight, with ticks)
    ry, rw = levels[2][1], levels[2][2]
    fig.add(line(mid - rw / 2, ry, mid + rw / 2, ry, stroke=GRID_C,
                 stroke_width=3))
    for i in range(9):
        xx = mid - rw / 2 + i * rw / 8
        fig.add(line(xx, ry - 6, xx, ry + 6, stroke=GRID_C, stroke_width=1.5))
    _t(fig, mid, ry - 14, "on the grid: what coordinates give", size=13,
       bold=True)
    _t(fig, mid, ry + 26, f"{1000 * c:,.3f} ft", size=13, bold=True)
    # the two factors, on the left between levels
    fx = x0 + 22
    _t(fig, fx, (gy + ey) / 2 + 2, "× elevation factor", anchor="start",
       size=12, bold=True, fill=EDGE)
    _t(fig, fx, (gy + ey) / 2 + 18, f"{ef:.5f}", anchor="start", size=12,
       fill=P["muted"])
    _t(fig, fx, (ey + ry) / 2 + 6, "× scale factor k", anchor="start",
       size=12, bold=True)
    _t(fig, fx, (ey + ry) / 2 + 22, f"{k:.5f}", anchor="start", size=12,
       fill=P["muted"])
    # summary
    _t(fig, (x0 + x1) / 2, 420, f"Combined factor = k × elevation factor = "
       f"{c:.8f}  (NGS, Utah Central)", size=13, bold=True)
    _t(fig, (x0 + x1) / 2, 440, f"Grid is {1000 * (1 - c):.3f} ft shorter "
       f"per 1,000 ft (about 3½ in). In UTM Zone 12: "
       f"{1000 * (1 - BYU_UTM['combined']):.3f} ft.", size=12,
       fill=P["muted"])
    _t(fig, (x0 + x1) / 2, 458, f"Ground at BYU: {BYU_GROUND_M:,.0f} m "
       f"({BYU_GROUND_M / 0.3048006:,.0f} ft) above the geoid. Higher "
       "ground, smaller elevation factor.", size=12, fill=P["muted"])
    return fig


DRAFTS: list = []      # (number, slug, builder) for figures still in review


# ---------------------------------------------------------------------------
BUILDERS = [
    (1, "right_triangle", build_right_triangle),
    (2, "azimuth_bearing", build_azimuth_bearing),
    (3, "field_angles", build_field_angles),
    (4, "oblique_triangle", build_oblique_triangle),
    (5, "height_systems", build_height_systems),
    (6, "grid_ground", build_grid_ground),
    (7, "leveling_run", build_leveling_run),
    (8, "traverse", build_traverse),
    (9, "average_end_area", build_average_end_area),
    (10, "horizontal_curve", build_horizontal_curve),
    (11, "vertical_curve", build_vertical_curve),
]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--drafts", action="store_true",
                    help="build only the figures still in review")
    args = ap.parse_args()
    for number, slug, builder in (DRAFTS if args.drafts else BUILDERS):
        fname = os.path.join(args.out, figure_name(WEEK, number, slug))
        builder(number).save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
