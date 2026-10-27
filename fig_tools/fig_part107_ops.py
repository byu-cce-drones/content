"""Part 107 airspace, operations, weather and loading figures (Week 3 / Week 9).

Seven drawings for the Part 107 overview reading and the two Part 107 lecture
decks, all in the w05_ series:

    w05_fig11b_class_e_floors.svg      where Class E starts: SFC, 700, 1,200 ft
    w05_fig11c_traffic_pattern.svg     reading a left-hand traffic pattern
    w05_fig16_metar.svg                an annotated METAR
    w05_fig19_density_altitude.svg     hot and high: density altitude
    w05_fig20_cg_envelope.svg          weight and balance: where the CG sits
    w05_fig20b_load_factor.svg         turning adds weight: load factor
    w05_fig24_hazardous_attitudes.svg  five hazardous attitudes, five antidotes

11b, 11c and 20b are lettered variants that sit beside the figure they
extend, so no number on the page moves. Sources: FAA Pilot's Handbook of
Aeronautical Knowledge (FAA-H-8083-25C) chapters 2, 5, 11 and 14; the FAA
Chart Users' Guide (VFR Terms and Symbols); AC 107-2A; 14 CFR 107.41 and
107.43. The METAR is a made-up example in the real format, not an observation.

Usage:
    python fig_tools/fig_part107_ops.py --png
    python fig_tools/fig_part107_ops.py --out docs/part_107_license/images
"""
from __future__ import annotations

import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_side  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (El, Figure, arrow, circle, figure_name, g,  # noqa: E402
                    line, path, polygon, rect, render_png, text,
                    translate)

W = 900
CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)
GREEN = "#2f8f4e"
GREEN_BG = "#e9f6ee"
ORANGE = P["warn"]
ORANGE_BG = "#fdf3e6"
BLUE = P["accent"]
BLUE_BG = "#e8f1fb"
RED = P["bad"]
RED_BG = "#fdecea"
# sectional-chart conventions, not the house palette: these two are what the
# chart prints, so students see the same colours they will see on the test
CHART_MAGENTA = "#c2318c"
CHART_BLUE = "#2f6db5"
CHART_PAPER = "#fbf8ee"
GROUND = "#8B6914"            # the ground line colour of w05_fig11


def _t(fig, x, y, s, size=12, bold=False, fill=None, anchor="middle",
       italic=False):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 font_style="italic" if italic else None,
                 fill=fill or P["ink"]))


def _lines(fig, x, y, lines, size=11.5, fill=None, anchor="start", gap=16,
           bold=False):
    for i, s in enumerate(lines):
        _t(fig, x, y + i * gap, s, size=size, fill=fill or P["muted"],
           anchor=anchor, bold=bold)


def _pill(fig, cx, cy, w, label, fg, bg, size=12):
    fig.add(rect(cx - w / 2, cy - 13, w, 26, rx=13, fill=bg, stroke=fg,
                 stroke_width=1.5))
    _t(fig, cx, cy + 4.5, label, size=size, bold=True, fill=fg)


# ---------------------------------------------------------------------------
# 11b. Where Class E starts
# ---------------------------------------------------------------------------
PX_PER_FT = 0.11


def _airport_symbol(fig, cx, cy, colour):
    fig.add(circle(cx, cy, 7, fill="none", stroke=colour, stroke_width=1.8))
    fig.add(line(cx - 5, cy, cx + 5, cy, stroke=colour, stroke_width=2.5))


def _vignette_ring(fig, cx, cy, r, colour, steps=10, step=1.6):
    """A shaded band with a hard outer edge fading inward, the way the chart
    prints a Class E floor: the soft side faces the lower floor."""
    for k in range(steps):
        fig.add(circle(cx, cy, r - k * step, fill="none", stroke=colour,
                       stroke_width=step + 0.4,
                       opacity=f"{0.55 * (1 - k / steps):.2f}"))


def _vignette_edge(fig, x, y0, y1, colour, steps=10, step=1.8):
    """The same band along a gently curved edge: hard on the left, fading to
    the right."""
    for k in range(steps):
        xx = x + k * step
        fig.add(path(f"M{xx},{y0} Q{xx + 18},{(y0 + y1) / 2} {xx},{y1}",
                     fill="none", stroke=colour, stroke_width=step + 0.4,
                     opacity=f"{0.55 * (1 - k / steps):.2f}"))


def build_class_e_floors() -> Figure:
    fig = Figure(W, 560, "Figure 11b: Where Class E starts",
                 "Three ways the sectional draws the floor of Class E, and "
                 "what each one means for a drone at or below 400 ft.")
    panels = (
        ("Class E from the surface", "dashed magenta line", 0,
         "Authorization needed", RED, RED_BG,
         ("Controlled from the ground up.", "Ask ATC first: LAANC or",
          "FAA DroneZone (14 CFR 107.41).")),
        ("Class E from 700 ft AGL", "magenta vignette (shaded band)", 700,
         "No authorization", GREEN, GREEN_BG,
         ("Class G below 700 ft.", "Your 400 ft is uncontrolled",
          "airspace: fly, no permission needed.")),
        ("Class E from 1,200 ft AGL", "blue vignette, or no line at all", 1200,
         "No authorization", GREEN, GREEN_BG,
         ("The default over most of the US.", "Class G up to 1,200 ft, so",
          "the same answer: fly.")),
    )
    pw, step, x0 = 270, 285, 30
    for i, (head, sym, floor, verdict, fg, bg, notes) in enumerate(panels):
        x = x0 + i * step
        cx = x + pw / 2
        _t(fig, cx, 80, head, size=14, bold=True)

        # the chart symbol
        sx, sy, sw, sh = cx - 90, 92, 180, 112
        fig.add(rect(sx, sy, sw, sh, rx=6, fill=CHART_PAPER, stroke="#d8d2c0",
                     stroke_width=1))
        mx, my = cx, sy + sh / 2
        if floor == 0:
            fig.add(circle(mx, my, 42, fill="none", stroke=CHART_MAGENTA,
                           stroke_width=2.2, stroke_dasharray="7 4"))
            _airport_symbol(fig, mx, my, CHART_MAGENTA)
        elif floor == 700:
            _vignette_ring(fig, mx, my, 46, CHART_MAGENTA)
            _airport_symbol(fig, mx, my, CHART_MAGENTA)
            _t(fig, mx, my + 32, "700", size=10, fill=CHART_MAGENTA)
        else:
            _vignette_edge(fig, mx - 10, sy + 6, sy + sh - 6, CHART_BLUE)
            _t(fig, mx - 42, my + 4, "G", size=13, bold=True, fill=P["muted"])
            _t(fig, mx + 44, my - 4, "E", size=13, bold=True, fill=CHART_BLUE)
            _t(fig, mx + 44, my + 12, "1,200", size=10, fill=CHART_BLUE)
        _t(fig, cx, sy + sh + 18, sym, size=11.5, fill=P["muted"],
           italic=True)

        # the cross-section
        bx, by, bw, bh = cx - 115, 238, 230, 185
        ground_y = by + bh
        floor_y = ground_y - floor * PX_PER_FT
        fig.add(rect(bx, by, bw, bh, fill="#c7ddf2", opacity="0.55"))
        if floor:
            fig.add(rect(bx, floor_y, bw, ground_y - floor_y, fill="#28a745",
                         opacity="0.28"))
            fig.add(line(bx, floor_y, bx + bw, floor_y, stroke=CHART_BLUE,
                         stroke_width=1.5))
            _t(fig, bx + bw - 6, floor_y - 5, f"{floor:,} ft AGL", size=11,
               bold=True, fill=CHART_BLUE, anchor="end")
            _t(fig, bx + bw - 10, (floor_y + ground_y) / 2 + 6, "G", size=20,
               bold=True, fill="#1e7e34", anchor="end")
        else:
            _t(fig, bx + bw - 6, ground_y - 6, "SFC", size=11, bold=True,
               fill=CHART_BLUE, anchor="end")
        _t(fig, bx + bw - 10, by + 30, "E", size=20, bold=True,
           fill="#2c6fad", anchor="end")
        fig.add(rect(bx, by, bw, bh, fill="none", stroke="#9aa7b2",
                     stroke_width=1))
        fig.add(line(bx, ground_y, bx + bw, ground_y, stroke=GROUND,
                     stroke_width=3))
        # the 400 ft line and the drone on it
        y400 = ground_y - 400 * PX_PER_FT
        fig.add(line(bx, y400, bx + bw, y400, stroke=RED, stroke_width=1.5,
                     stroke_dasharray="7 4"))
        fig.add(translate(bx + 76, y400 - 9, aircraft_mini_side(0.5)))
        _t(fig, bx + 6, y400 - 6, "400 ft", size=10.5, bold=True, fill=RED,
           anchor="start")

        # the verdict
        _pill(fig, cx, 446, 196, verdict, fg, bg)
        _lines(fig, cx, 478, notes, size=11.5, anchor="middle", gap=15)

    _t(fig, W / 2, 540,
       "Only surface Class E needs authorization for a drone below 400 ft. "
       "Symbols redrawn from the chart legend, not to scale.",
       size=12.5, fill=P["ink"], bold=True)
    return fig


# ---------------------------------------------------------------------------
# 11c. Reading a traffic pattern
# ---------------------------------------------------------------------------
RWY_HDG = 130                 # runway 13: landing toward 130 degrees magnetic


def _heading_unit(hdg):
    """Screen unit vector for a compass heading, north up: (east, -north)."""
    a = math.radians(hdg)
    return math.sin(a), -math.cos(a)


def _tp(cx, cy, x, y):
    """Local pattern coordinates to screen. Local +x runs along the landing
    heading; local +y is to the pilot's right. So the left side of the
    runway is local -y."""
    ux, uy = _heading_unit(RWY_HDG)          # along the runway
    rx, ry = _heading_unit(RWY_HDG + 90)     # to the right of it
    return cx + x * ux + y * rx, cy + x * uy + y * ry


def _airplane(scale=1.0):
    """A small airplane seen from above, nose toward +x."""
    return g(path("M14,0 L-10,-3 L-10,3 Z", fill=P["dark"]),
             path("M-1,-16 L4,-1 L4,1 L-1,16 L-5,16 L-3,1 L-3,-1 L-5,-16 Z",
                  fill=P["dark"]),
             path("M-11,-6 L-7,0 L-11,6 L-13,6 L-12,0 L-13,-6 Z",
                  fill=P["dark"]),
             transform=f"scale({scale})")


def build_traffic_pattern() -> Figure:
    fig = Figure(W, 600, "Figure 11c: Reading a traffic pattern",
                 "Runway 13, standard left-hand pattern, north up. Where is "
                 "an aircraft that reports “midfield left downwind, "
                 "runway 13”?")
    # geometry check, in code: the left downwind of runway 13 lies to the
    # north-east, which the FAA sample answer calls east of the runway
    dx, dy = _tp(0, 0, 0, -1)
    assert dx > 0 and dy < 0, "left downwind of runway 13 should be NE"
    assert abs(math.degrees(math.atan2(dx, -dy)) - 40) < 1e-6

    cx, cy = 600, 320
    L, PL, D = 95, 200, 115    # half runway, half pattern, downwind offset

    # the runway, drawn in its own rotated frame
    rw = g(transform=f"translate({cx},{cy}) rotate({RWY_HDG - 90})")
    rw.add(rect(-L, -9, 2 * L, 18, fill=P["dark"]))
    for k in range(-3, 4):
        rw.add(line(k * 24 - 7, 0, k * 24 + 7, 0, stroke=P["white"],
                    stroke_width=1.5))
    fig.add(rw)
    # runway numbers kept upright so they can be read; on the real runway
    # they are painted to be read by the landing pilot
    for lx, num in ((-L + 22, "13"), (L - 22, "31")):
        sx, sy = _tp(cx, cy, lx, 0)
        _t(fig, sx, sy + 5, num, size=13, bold=True, fill=P["white"])

    # the pattern as one loop, arrowheads mid-leg
    legs = [("upwind", (L + 8, 0), (PL, 0)),
            ("crosswind", (PL, 0), (PL, -D)),
            ("downwind", (PL, -D), (-PL, -D)),
            ("base", (-PL, -D), (-PL, 0)),
            ("final", (-PL, 0), (-L - 8, 0))]
    pts = [_tp(cx, cy, *legs[0][1])] + [_tp(cx, cy, *b) for _, _, b in legs]
    fig.add(path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts),
                 fill="none", stroke=BLUE, stroke_width=3,
                 stroke_linejoin="round", stroke_linecap="round"))
    for name, a, b in legs:
        (ax, ay), (bx, by) = _tp(cx, cy, *a), _tp(cx, cy, *b)
        mx, my = (ax + bx) / 2, (ay + by) / 2
        ln = math.hypot(bx - ax, by - ay)
        ex, ey = (bx - ax) / ln, (by - ay) / ln
        fig.add(arrow(mx - ex * 9, my - ey * 9, mx + ex * 9, my + ey * 9,
                      color=BLUE, width=3, head=12))
    # leg labels, horizontal, pushed outward from the loop
    labels = {"upwind": ((L + PL) / 2, 24, "middle"),
              "final": (-(L + PL) / 2, 24, "middle"),
              "crosswind": (PL + 22, -D / 2 - 2, "start"),
              "base": (-PL - 22, -D / 2 - 2, "end"),
              "downwind": (70, -D - 18, "end")}
    for name, (lx, ly, anchor) in labels.items():
        sx, sy = _tp(cx, cy, lx, ly)
        if name == "crosswind":
            sx, sy = sx + 8, sy
        if name == "base":
            sx, sy = sx - 8, sy
        if name == "downwind":
            # the leg climbs to the right, so the label hangs off its upper
            # end and runs left, clear of the line
            sx, sy = sx - 6, sy + 4
        _t(fig, sx, sy, name, size=13, bold=True, fill=BLUE, anchor=anchor)

    # abeam midfield: a dashed tie from the runway midpoint to the downwind
    ax, ay = _tp(cx, cy, 0, 0)
    bx, by = _tp(cx, cy, 0, -D)
    fig.add(line(ax, ay, bx, by, stroke=P["muted"], stroke_width=1.2,
                 stroke_dasharray="4 3"))
    plane = g(_airplane(1.1), transform=f"translate({bx:.1f},{by:.1f}) "
              f"rotate({RWY_HDG - 90 + 180})")
    fig.add(circle(bx, by, 17, fill=ORANGE_BG, stroke=ORANGE, stroke_width=2))
    fig.add(plane)
    _t(fig, bx + 24, by - 30, "midfield left downwind", size=13, bold=True,
       fill=ORANGE, anchor="start")
    _t(fig, bx + 24, by - 14, "heading 310°, runway on the left",
       size=11.5, fill=P["muted"], anchor="start")
    _t(fig, bx + 24, by + 2, "north-east of the runway", size=11.5,
       fill=P["muted"], anchor="start")

    # north arrow
    nx, ny = 840, 110
    fig.add(arrow(nx, ny + 34, nx, ny - 6, color=P["ink"], width=2.5,
                  head=10))
    _t(fig, nx, ny - 12, "N", size=14, bold=True)

    # the explanation card
    fig.add(rect(30, 84, 300, 350, **CARD))
    _t(fig, 180, 112, "How to read it", size=13.5, bold=True)
    y = 140
    for head, body in (
        ("Runway number = heading ÷ 10",
         ("Runway 13 lands toward 130° magnetic.",
          "Runway 31 is the same strip from the",
          "other end, heading 310°.")),
        ("Standard pattern: all turns left",
         ("Unless the chart says RP, right pattern.",)),
        ("Downwind: parallel, opposite way",
         ("The runway stays on the pilot’s left,",
          "so the downwind of runway 13 is flown on",
          "310° along the north-east side.")),
        ("The test answer",
         ("“Midfield left downwind, runway 13” puts",
          "the aircraft east of the runway (FAA",
          "sample question, Figure 26, area 2).")),
    ):
        _t(fig, 50, y, head, size=12.5, bold=True, anchor="start")
        _lines(fig, 50, y + 18, body, size=11.5, gap=15)
        y += 22 + 15 * len(body) + 16

    fig.add(rect(30, 450, 300, 70, rx=8, fill=ORANGE_BG, stroke=ORANGE,
                 stroke_width=1.5))
    _t(fig, 50, 474, "Why a drone pilot cares", size=12.5, bold=True,
       anchor="start")
    _lines(fig, 50, 492, ("Stay out of the pattern (14 CFR 107.43).",
                          "Hear a position report, know where to look."),
           size=11.5, gap=15)

    _t(fig, W / 2, 576,
       "Upwind, crosswind, downwind, base, final: five legs, four left "
       "turns. Draw the pattern from the runway number and the answer "
       "falls out.", size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 16. Reading a METAR
# ---------------------------------------------------------------------------
METAR = ["METAR", "KPVU", "211553Z", "34008KT", "10SM", "BKN045", "08/M02",
         "A3012"]
METAR_NOTES = [
    ("Report type", ("Routine hourly observation.",
                     "SPECI = a special report",
                     "when conditions change.")),
    ("Station", ("Provo Municipal Airport.",
                 "K + the three-letter US code.")),
    ("Day and time, Zulu (UTC)", ("21st of the month, 15:53 Z.",
                                  "Utah: 08:53 MST (UTC−7),",
                                  "Summer: 09:53 MDT (UTC−6).")),
    ("Wind", ("From 340° true at 8 knots.",
              "G15 = gusts to 15 knots:",
              "34008G15KT. Calm is 00000KT.")),
    ("Visibility", ("10 statute miles.",
                    "Part 107 needs at least 3 SM.")),
    ("Sky condition", ("Broken clouds, base 4,500 ft AGL.",
                       "FEW, SCT, BKN, OVC in eighths;",
                       "a ceiling is BKN or OVC only.")),
    ("Temperature / dew point", ("8 °C and −2 °C (M = minus).",
                                 "Close together means fog or",
                                 "low cloud is likely.")),
    ("Altimeter", ("30.12 inches of mercury.",
                   "Standard is 29.92.")),
]


def build_metar() -> Figure:
    fig = Figure(W, 520, "Figure 16: Reading a METAR",
                 "An example in the real format, not an actual observation: "
                 "a winter morning at Provo. Read it group by group.")
    n = len(METAR)
    spacing = 100
    xs = [100 + i * spacing for i in range(n)]
    sy = 118
    fig.add(rect(30, sy - 30, W - 60, 46, rx=8, fill=P["white"],
                 stroke="#dde3e9", stroke_width=1.5))
    for x, grp in zip(xs, METAR):
        fig.add(text(x, sy + 1, grp, text_anchor="middle", font_size=20,
                     font_weight="bold", fill=P["ink"],
                     font_family="Consolas, 'Courier New', monospace"))
    # row A under the even groups, row B under the odd ones; the odd leaders
    # drop straight through the gaps between the row A cards
    cw, ch = 176, 108
    rows = {0: 178, 1: 318}
    for i, (x, grp, (head, body)) in enumerate(zip(xs, METAR, METAR_NOTES)):
        top = rows[i % 2]
        fig.add(line(x, sy + 10, x, top, stroke=BLUE, stroke_width=1.5))
        fig.add(circle(x, sy + 10, 3, fill=BLUE))
        fig.add(rect(x - cw / 2, top, cw, ch, **CARD))
        _t(fig, x - cw / 2 + 10, top + 22, head, size=12.5, bold=True,
           anchor="start")
        _lines(fig, x - cw / 2 + 10, top + 42, body, size=11.5, gap=15)
    # traps
    fig.add(rect(30, 448, W - 60, 50, rx=8, fill=ORANGE_BG, stroke=ORANGE,
                 stroke_width=1.5))
    _t(fig, W / 2, 468, "Three traps the test sets", size=12.5, bold=True)
    _t(fig, W / 2, 487,
       "Cloud heights are AGL, in hundreds of feet.  ·  Wind is from "
       "the direction given, in degrees true.  ·  Times are Zulu, "
       "not local.", size=12, fill=P["ink"])
    return fig


# ---------------------------------------------------------------------------
# 19. Hot and high: density altitude
# ---------------------------------------------------------------------------
def density_altitude(elev_ft: float, temp_c: float) -> float:
    """Rule-of-thumb density altitude: standard temperature is 15 C at sea
    level falling 2 C per 1,000 ft, and each degree above standard adds about
    120 ft. Good enough for the point the figure makes."""
    std = 15 - 2 * elev_ft / 1000
    return elev_ft + 120 * (temp_c - std)


def _sun(fig, cx, cy, r=12):
    for k in range(8):
        a = math.radians(k * 45)
        fig.add(line(cx + math.cos(a) * (r + 4), cy + math.sin(a) * (r + 4),
                     cx + math.cos(a) * (r + 10), cy + math.sin(a) * (r + 10),
                     stroke=ORANGE, stroke_width=2.5, stroke_linecap="round"))
    fig.add(circle(cx, cy, r, fill="#fbd27a", stroke=ORANGE, stroke_width=2))


def build_density_altitude() -> Figure:
    fig = Figure(W, 540, "Figure 19: Hot and high: density altitude",
                 "The same aircraft on two days. Thin air gives the "
                 "propellers less to push on, and the aircraft flies as if it "
                 "were much higher than it is.")
    cases = (
        (30, "Cool day near sea level", 1000, 10, 140, False),
        (460, "Hot day at Provo elevation", 4500, 35, 45, True),
    )
    for (px, head, elev, temp, n_dots, hot) in cases:
        pw, py, ph = 410, 84, 310
        da = density_altitude(elev, temp)
        fig.add(rect(px, py, pw, ph, rx=10, fill="#eaf3fb", stroke="#dde3e9",
                     stroke_width=1.5))
        _t(fig, px + pw / 2, py + 26, head, size=14, bold=True)
        # ground: low and flat, or a raised plateau
        gy = py + ph - 28 if not hot else py + ph - 70
        fig.add(path(f"M{px + 1},{py + ph - 1} V{gy + 10} "
                     f"Q{px + 60},{gy - 6} {px + 150},{gy} "
                     f"T{px + pw - 1},{gy + 4} V{py + ph - 1} Z",
                     fill="#d9cfae", stroke="#b4a37a", stroke_width=1))
        _t(fig, px + pw - 12, py + ph - 8, f"{elev:,} ft elevation", size=11,
           fill="#6e5f36", anchor="end", bold=True)
        # air molecules
        rnd = random.Random(elev)
        for _ in range(n_dots):
            x = px + 14 + rnd.random() * (pw - 28)
            y = py + 44 + rnd.random() * (gy - 14 - (py + 44))
            fig.add(circle(round(x, 1), round(y, 1), 2.4, fill="#8fb0cc",
                           opacity="0.8"))
        # temperature badge
        bx, by = px + 20, py + 56
        if hot:
            _sun(fig, bx + 14, by + 10)
            _t(fig, bx + 46, by + 15, f"{temp} °C", size=14, bold=True,
               fill=ORANGE, anchor="start")
        else:
            fig.add(circle(bx + 14, by + 10, 11, fill="#dceefb", stroke=BLUE,
                           stroke_width=2))
            _t(fig, bx + 38, by + 15, f"{temp} °C", size=14, bold=True,
               fill=BLUE, anchor="start")
        # the aircraft and its thrust arrows
        ax, ay = px + pw / 2, gy - 120
        fig.add(translate(ax, ay, aircraft_mini_side(1.5)))
        thrust = 26 if hot else 50
        col = ORANGE if hot else GREEN
        for mx in (-51, 51):
            fig.add(arrow(ax + mx, ay - 34, ax + mx, ay - 34 - thrust,
                          color=col, width=3.5, head=11))
        _t(fig, ax, ay - 34 - thrust - 10,
           "less thrust per rev" if hot else "full thrust", size=12,
           bold=True, fill=col)
        # the number
        label = f"Density altitude ≈ {round(da, -2):,.0f} ft"
        fig.add(rect(px + 40, gy - 76, pw - 80, 40, rx=8,
                     fill=ORANGE_BG if hot else GREEN_BG,
                     stroke=col, stroke_width=1.5))
        _t(fig, px + pw / 2, gy - 59, label, size=13, bold=True)
        _t(fig, px + pw / 2, gy - 44,
           "thin air: more throttle for the same hover" if hot else
           "the air is nearly as dense as at sea level", size=11,
           fill=P["muted"])

    # what the exam tests
    fig.add(rect(30, 410, W - 60, 54, rx=8, fill=BLUE_BG, stroke=BLUE,
                 stroke_width=1.5))
    _t(fig, W / 2, 432, "High density altitude reduces propeller efficiency "
       "and performance.", size=14, bold=True)
    _t(fig, W / 2, 452, "Less thrust and less lift: a weaker climb, more "
       "throttle to hover, a shorter flight, and a longer takeoff for a "
       "fixed wing.", size=12, fill=P["ink"])
    _t(fig, W / 2, 492, "Density altitude rises with elevation, temperature "
       "and humidity. Rule of thumb: about 120 ft per °C above the "
       "standard day", size=11.5, fill=P["muted"])
    _t(fig, W / 2, 508, "(15 °C at sea level, 2 °C cooler per "
       "1,000 ft). Pilot’s Handbook of Aeronautical Knowledge, "
       "chapter 11.", size=11.5, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# 20. Weight and balance
# ---------------------------------------------------------------------------
def _cg_symbol(cx, cy, r=8):
    """The checkered centre-of-gravity symbol."""
    return g(circle(cx, cy, r, fill=P["white"], stroke=P["ink"],
                    stroke_width=1.5),
             path(f"M{cx},{cy} L{cx + r},{cy} A{r},{r} 0 0 0 {cx},{cy - r} Z",
                  fill=P["ink"]),
             path(f"M{cx},{cy} L{cx - r},{cy} A{r},{r} 0 0 0 {cx},{cy + r} Z",
                  fill=P["ink"]))


def _loaded_quad(fig, cx, cy, payload_x, tilt, front, rear, cg_x):
    """A side-view quadcopter (nose to the right) with a payload box at
    payload_x, tilted by `tilt` degrees, thrust arrows of lengths front and
    rear, and the CG symbol at cg_x. All in local units before scaling."""
    s = 2.0
    grp = g(transform=f"translate({cx},{cy}) rotate({tilt})")
    body = g(transform=f"scale({s})")
    body.add(aircraft_mini_side(1.0))
    body.add(rect(payload_x - 9, 12, 18, 12, rx=2, fill="#6f7f8f",
                  stroke=P["line"], stroke_width=0.8))
    body.add(circle(payload_x, 18, 3, fill=P["screen"], stroke=P["line"],
                    stroke_width=0.6))
    grp.add(body)
    for mx, ln in ((34 * s, front), (-34 * s, rear)):
        grp.add(arrow(mx, -22 * s, mx, -22 * s - ln, color=BLUE, width=3,
                      head=10))
    grp.add(_cg_symbol(cg_x * s, 1 * s, 9))
    fig.add(grp)
    return grp


def build_cg_envelope() -> Figure:
    fig = Figure(W, 516, "Figure 20: Weight and balance: where the centre of "
                 "gravity sits",
                 "Loading and performance is about 2 % of the knowledge test: "
                 "a small but tested topic.")
    panels = (
        ("Balanced", 0, 0, 44, 44, 0, GREEN, GREEN_BG,
         ("Payload under the centre of lift.",
          "Equal motor effort, level hover,",
          "full margin to fight wind.")),
        ("Nose-heavy", 26, 7, 60, 28, 13, ORANGE, ORANGE_BG,
         ("Payload mounted forward, so the",
          "front motors work harder just to",
          "hold level: less margin, worse",
          "control, drifts in a gust.")),
        ("Tail-heavy", -26, -7, 28, 60, -13, ORANGE, ORANGE_BG,
         ("The same problem in reverse. The",
          "rear motors carry the load and the",
          "aircraft wants to pitch up.")),
    )
    pw, step, x0 = 270, 285, 30
    for i, (head, pl_x, tilt, front, rear, cg_x, fg, bg, notes) in \
            enumerate(panels):
        x = x0 + i * step
        cx = x + pw / 2
        fig.add(rect(x, 84, pw, 272, **CARD))
        _pill(fig, cx, 110, 150, head, fg, bg, size=13)
        # the centre of lift, midway between the motors
        fig.add(line(cx, 150, cx, 278, stroke=P["muted"], stroke_width=1.2,
                     stroke_dasharray="4 3"))
        _t(fig, cx, 146, "centre of lift", size=10.5, fill=P["muted"])
        _loaded_quad(fig, cx, 212, pl_x, tilt, front, rear, cg_x)
        # the checkered symbol is explained once in the legend below; a
        # label beside it would sit on the arms
        _lines(fig, x + 16, 296, notes, size=11.5, gap=14.5)
    fig.add(_cg_symbol(60, 382, 9))
    _t(fig, 76, 386, "centre of gravity (CG): where the aircraft balances",
       size=11.5, fill=P["muted"], anchor="start")
    fig.add(arrow(440, 390, 440, 372, color=BLUE, width=3, head=10))
    _t(fig, 452, 386, "thrust each motor must give to hold level",
       size=11.5, fill=P["muted"], anchor="start")

    fig.add(rect(30, 410, W - 60, 50, rx=8, fill=BLUE_BG, stroke=BLUE,
                 stroke_width=1.5))
    _t(fig, W / 2, 431, "Load per the manufacturer’s flight manual; "
       "changing the payload changes the CG.", size=13.5, bold=True)
    _t(fig, W / 2, 450, "Test question: where are the loading instructions? "
       "In the Pilot’s Operating Handbook or UAS Flight Manual.",
       size=12, fill=P["ink"])
    _t(fig, W / 2, 492, "A camera moved to the front, a bigger battery, a "
       "sensor hung off one arm: every change moves the CG and costs "
       "control margin.", size=11.5, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 20b. Turning adds weight: load factor
# ---------------------------------------------------------------------------
BANKS = (0, 30, 45, 60)
EXAMPLE_WEIGHT = 33


def load_factor(bank_deg: float) -> float:
    return 1 / math.cos(math.radians(bank_deg))


def build_load_factor() -> Figure:
    lf = {b: load_factor(b) for b in BANKS}
    # the numbers the figure prints, checked against the arithmetic
    assert [round(lf[b], 2) for b in BANKS] == [1.0, 1.15, 1.41, 2.0]
    assert round(EXAMPLE_WEIGHT * lf[30]) == 38
    fig = Figure(W, 560, "Figure 20b: Turning adds weight: load factor",
                 "In a level turn the lift must hold the aircraft up and "
                 "pull it round the corner, so the structure carries more "
                 "than the aircraft weighs.")
    cw, x0, top = 205, 30, 84
    for i, b in enumerate(BANKS):
        x = x0 + i * (cw + 7)
        cx = x + cw / 2
        fig.add(rect(x, top, cw, 230, **CARD))
        _t(fig, cx, top + 26, f"{b}° bank", size=14, bold=True)
        hy = top + 150
        fig.add(line(x + 20, hy, x + cw - 20, hy, stroke="#9aa7b2",
                     stroke_width=1.2, stroke_dasharray="5 4"))
        # head-on aircraft, banked to the right
        fig.add(g(aircraft_mini_side(1.4, nose=False),
                  transform=f"translate({cx},{hy}) rotate({b})"))
        # weight straight down, lift along the aircraft's up, longer by the
        # load factor
        wl = 44
        fig.add(arrow(cx, hy + 10, cx, hy + 10 + wl, color=P["dark"],
                      width=3, head=10))
        _t(fig, cx + 10, hy + 10 + wl, "weight", size=11, fill=P["dark"],
           anchor="start")
        ll = wl * lf[b]
        ux, uy = math.sin(math.radians(b)), -math.cos(math.radians(b))
        fig.add(arrow(cx, hy - 30, cx + ux * ll, hy - 30 + uy * ll,
                      color=BLUE, width=3.5, head=11))
        _t(fig, cx + ux * ll + (12 if b else 0),
           hy - 30 + uy * ll - (6 if not b else -4), "lift", size=11,
           fill=BLUE, anchor="start" if b else "middle")
        fig.add(rect(x + 30, top + 192, cw - 60, 28, rx=14,
                     fill=BLUE_BG if b else GREEN_BG,
                     stroke=BLUE if b else GREEN, stroke_width=1.5))
        _t(fig, cx, top + 211, f"{lf[b]:.2f} G", size=14, bold=True,
           fill=BLUE if b else GREEN)

    # the curve
    gx, gy, gw, gh = 70, 338, 300, 150
    fig.add(rect(30, 326, 400, 190, **CARD))
    _t(fig, 230, 350, "Load factor against bank angle", size=12.5, bold=True)
    gy += 26
    gh -= 40
    fig.add(path(f"M{gx},{gy} V{gy + gh} H{gx + gw}", fill="none",
                 stroke="#9aa7b2", stroke_width=1.2))
    bmax, lmax = 70, 3.0

    def pt(b):
        return (gx + gw * b / bmax,
                gy + gh - gh * (load_factor(b) - 1) / (lmax - 1))

    fig.add(path("M" + " L".join(f"{pt(b)[0]:.1f},{pt(b)[1]:.1f}"
                                 for b in range(0, 69)),
                 fill="none", stroke=BLUE, stroke_width=2.5))
    for b in BANKS[1:]:
        px_, py_ = pt(b)
        fig.add(circle(px_, py_, 4.5, fill=BLUE, stroke=P["white"],
                       stroke_width=1.5))
        _t(fig, px_ - 8, py_ - 8, f"{lf[b]:.2f}", size=10.5, bold=True,
           fill=BLUE, anchor="end")
    for b in (0, 30, 45, 60):
        _t(fig, pt(b)[0], gy + gh + 14, f"{b}°", size=10.5,
           fill=P["muted"])
    for v in (1, 2, 3):
        yy = gy + gh - gh * (v - 1) / (lmax - 1)
        _t(fig, gx - 6, yy + 4, f"{v} G", size=10.5, fill=P["muted"],
           anchor="end")
    _t(fig, 230, 508, "load factor = 1 ÷ cos(bank)", size=11.5,
       fill=P["muted"])

    # the worked example
    fig.add(rect(450, 326, 420, 190, rx=10, fill=ORANGE_BG, stroke=ORANGE,
                 stroke_width=1.5))
    _t(fig, 660, 352, "Worked example (FAA sample question)", size=12.5,
       bold=True)
    _lines(fig, 470, 380,
           (f"A {EXAMPLE_WEIGHT} lb aircraft holds altitude in a 30° "
            "banked turn.",
            "What load must its structure support?"), size=12,
           fill=P["ink"], gap=17)
    _t(fig, 470, 428, f"{EXAMPLE_WEIGHT} lb × {lf[30]:.3f} ≈ "
       f"{EXAMPLE_WEIGHT * lf[30]:.0f} lb", size=18, bold=True,
       anchor="start")
    _lines(fig, 470, 456,
           ("The test gives you the curve: FAA-CT-8080-2H, Figure 2.",
            "Read the load factor at the bank angle, multiply by the weight.",
            "The answer choices are far enough apart that 1.15 is enough."),
           size=11.5, gap=15)

    _t(fig, W / 2, 544, "The same aircraft weighs 33 lb on the ground and "
       "has to be built for 66 lb at 60° of bank. Steep turns, hard "
       "pull-ups and gusts all add load.", size=11.5, fill=P["muted"],
       italic=True)
    return fig


# ---------------------------------------------------------------------------
# 24. Five hazardous attitudes and their antidotes
# ---------------------------------------------------------------------------
# Wording from the Pilot's Handbook of Aeronautical Knowledge, chapter 2,
# "The five hazardous attitudes" table, checked against FAA-H-8083-25C.
ATTITUDES = (
    ("Anti-authority", "“Don’t tell me.”",
     "Follow the rules. They are usually right."),
    ("Impulsivity", "“Do it quickly.”",
     "Not so fast. Think first."),
    ("Invulnerability", "“It won’t happen to me.”",
     "It could happen to me."),
    ("Macho", "“I can do it.”",
     "Taking chances is foolish."),
    ("Resignation", "“What’s the use?”",
     "I’m not helpless. I can make a difference."),
)


def build_hazardous_attitudes() -> Figure:
    fig = Figure(W, 520, "Figure 24: Five hazardous attitudes and their "
                 "antidotes",
                 "Recognise the thought, name the attitude, say the antidote. "
                 "Wording from the FAA Pilot’s Handbook, chapter 2.")
    lx, lw, rx, rw = 40, 380, 480, 380
    _t(fig, lx + lw / 2, 86, "The attitude, and what it sounds like",
       size=13, bold=True, fill=RED)
    _t(fig, rx + rw / 2, 86, "The antidote: say it to yourself", size=13,
       bold=True, fill=GREEN)
    y0, rh, gap = 100, 60, 12
    for i, (name, thought, antidote) in enumerate(ATTITUDES):
        y = y0 + i * (rh + gap)
        fig.add(rect(lx, y, lw, rh, rx=10, fill=RED_BG, stroke=RED,
                     stroke_width=1.5))
        fig.add(circle(lx + 30, y + rh / 2, 15, fill=RED))
        _t(fig, lx + 30, y + rh / 2 + 5, str(i + 1), size=13, bold=True,
           fill=P["white"])
        _t(fig, lx + 56, y + 25, name, size=14, bold=True, anchor="start")
        _t(fig, lx + 56, y + 45, thought, size=13, italic=True,
           fill=P["muted"], anchor="start")
        fig.add(arrow(lx + lw + 10, y + rh / 2, rx - 10, y + rh / 2,
                      color=BLUE, width=3, head=12))
        fig.add(rect(rx, y, rw, rh, rx=10, fill=GREEN_BG, stroke=GREEN,
                     stroke_width=1.5))
        _t(fig, rx + 20, y + rh / 2 + 5, antidote, size=13.5, bold=True,
           anchor="start")
    _t(fig, W / 2, 478, "The test tells a short story and asks which "
       "attitude it shows. “Fly first, ask questions later” is "
       "impulsivity;", size=12, fill=P["ink"])
    _t(fig, W / 2, 496, "“watch this” is macho; “the rules "
       "are for other people” is anti-authority.", size=12,
       fill=P["ink"])
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
        (build_class_e_floors, 11, "b", "class_e_floors"),
        (build_traffic_pattern, 11, "c", "traffic_pattern"),
        (build_metar, 16, "", "metar"),
        (build_density_altitude, 19, "", "density_altitude"),
        (build_cg_envelope, 20, "", "cg_envelope"),
        (build_load_factor, 20, "b", "load_factor"),
        (build_hazardous_attitudes, 24, "", "hazardous_attitudes"),
    ):
        fname = os.path.join(args.out, figure_name(5, number, slug, variant))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
