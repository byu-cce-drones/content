"""Final project figures, for the project pages and the Week 10 lecture deck.

    w10_fig01_turn_ins.svg      the four turn-ins and the flight days, Nov 3 to Dec 10
    w10_fig02_group_orbit.svg   a 3D model of your group: an ascending circle around it
    w10_fig03_trip_budget.svg   the 50-minute trip: a near site fits, a far one does not

Figure 1 is on the Final Weeks Schedule, Figure 2 on Example Projects and
Figure 3 on the Project Proposal, numbered in nav order. Dates are the fall
2026 ones from schedule.md; change DATES and rerun each semester.

Usage:
    python fig_tools/fig_final_project.py --out review --png
    python fig_tools/fig_final_project.py --out docs/final_project/images
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_side, aircraft_mini_top, person  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (El, Figure, circle, figure_name, g, line, path,  # noqa: E402
                    rect, render_png, text, translate)

W = 900
BLUE = P["accent"]
ORANGE = P["warn"]
GREEN = "#2f8f4e"
RED = P["bad"]
GRAY = "#8a96a3"
BLUE_FILL = "#e8f1fb"
ORANGE_FILL = "#fdf3e6"
GREEN_FILL = "#e6f4ea"
RED_FILL = "#fdecea"
GRAY_FILL = "#eef1f4"


def _t(fig, x, y, s, size=12, bold=False, fill=None, anchor="middle",
       italic=False):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 font_style="italic" if italic else None,
                 fill=fill or P["ink"]))


def _card(fig, cx, y, w, lines, fill, stroke, h=None, sizes=None):
    """A rounded card centred on cx, top at y, one text line per entry; the
    first line is bold."""
    h = h or 14 + 17 * len(lines)
    fig.add(rect(cx - w / 2, y, w, h, rx=8, fill=fill, stroke=stroke,
                 stroke_width=1.5))
    for i, s in enumerate(lines):
        size = (sizes or [13.5] + [12] * 10)[i]
        _t(fig, cx, y + 19 + 17 * i, s, size=size, bold=(i == 0),
           fill=P["ink"] if i == 0 else P["muted"])
    return y + h


# ---------------------------------------------------------------------------
# 1. The four turn-ins and the flight days
# ---------------------------------------------------------------------------
# Day 0 is Tue Nov 3 2026; the axis runs Mon Nov 2 to Sun Dec 13.
DATES = {"Nov 3": 0, "Nov 5": 2, "Nov 12": 9, "Nov 19": 16, "Nov 24": 21,
         "Nov 26": 23, "Dec 3": 30, "Dec 7": 34, "Dec 8": 35, "Dec 10": 37}
X0, PX = 40, 20          # x of Mon Nov 2, pixels per day


def _x(date):
    return X0 + (DATES[date] + 1) * PX


def build_turn_ins() -> Figure:
    fig = Figure(W, 368, "Figure 1: The final project, week by week",
                 "Fall 2026. Learning Suite has the official dates; if they "
                 "differ, Learning Suite wins.")
    ay = 176                                   # top of the week band
    for k in range(6):                         # Weeks 10 to 15, Mon to Sun
        x = X0 + 7 * k * PX
        fig.add(rect(x, ay, 7 * PX, 26, fill="#dfe6ee" if k % 2 else "#eaf0f6"))
        _t(fig, x + 3.5 * PX, ay + 17, f"Week {10 + k}", size=12, bold=True,
           fill=P["muted"])

    # turn-ins above the band: (centre, width, dates the stems go to, lines)
    above = [
        (110, 150, ["Nov 5"], ["1. Proposal", "Thu Nov 5, 11:59 PM", "2.5 %"]),
        (450, 230, ["Nov 19", "Nov 26"],
         ["2. Flight and Data Processing", "one week after your flight",
          "5 %"]),
        (690, 116, ["Dec 7"], ["3. Slides", "Mon Dec 7", "2.5 % with talk"]),
        (818, 110, ["Dec 10"], ["4. Memo", "Thu Dec 10", "5 %"]),
    ]
    for cx, w, stems, lines in above:
        bottom = _card(fig, cx, 76, w, lines, BLUE_FILL, BLUE)
        for d in stems:
            fig.add(line(_x(d), bottom, _x(d), ay, stroke=BLUE,
                         stroke_width=1.5))
            fig.add(circle(_x(d), ay, 3.5, fill=BLUE))

    # class days below the band: (centre, row, width, dates, lines, colours)
    below = [
        (70, 1, 110, ["Nov 3"], ["Today", "form groups of 2"],
         P["white"], P["ink"]),
        (140, 0, 140, ["Nov 5"], ["Thursday lab", "proposal and LAANC"],
         P["white"], GRAY),
        (272, 0, 120, ["Nov 12"], ["Flight day 1", "5 groups"],
         ORANGE_FILL, ORANGE),
        (402, 0, 120, ["Nov 19"], ["Flight day 2", "4 groups"],
         ORANGE_FILL, ORANGE),
        (470, 1, 96, ["Nov 24"], ["Work day", "TA help"], GRAY_FILL, GRAY),
        (548, 0, 112, ["Nov 26"], ["Thanksgiving", "no class"],
         GRAY_FILL, GRAY),
        (660, 1, 96, ["Dec 3"], ["Work day", "TA help"], GRAY_FILL, GRAY),
        (790, 0, 150, ["Dec 8", "Dec 10"], ["Presentations", "Dec 8 and 10"],
         GREEN_FILL, GREEN),
    ]
    by = ay + 26
    for cx, row, w, stems, lines, fill, stroke in below:
        top = by + 22 + row * 56
        for d in stems:
            fig.add(line(_x(d), by, _x(d), top, stroke=stroke,
                         stroke_width=1.5))
            fig.add(circle(_x(d), by, 3.5, fill=stroke))
        _card(fig, cx, top, w, lines, fill, stroke, sizes=[13, 11.5])

    _t(fig, W / 2, 354,
       "Flights leave EB B122 at 8:00 or 9:00 and last 50 minutes. Final "
       "project work cannot be turned in late.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 2. A 3D model of your group: the ascending circle
# ---------------------------------------------------------------------------
def _top_view(fig, cx, cy):
    """Plan view: the group in the middle, the drone on a ring around it with
    the camera pointed in."""
    R, r_group = 150, 46
    _t(fig, cx, 82, "From above", size=14, bold=True)
    fig.add(circle(cx, cy, r_group + 14, fill=RED_FILL, stroke=RED,
                   stroke_width=1.5, stroke_dasharray="5 4"))
    for px, py in [(-18, -16), (14, -20), (-24, 14), (4, 6), (24, 18),
                   (-4, 30)]:
        fig.add(circle(cx + px, cy + py, 9, fill="#9aa5b1", stroke=P["line"],
                       stroke_width=1))
        fig.add(circle(cx + px, cy + py, 4.5, fill=P["dark"]))
    fig.add(circle(cx, cy, R, fill="none", stroke=BLUE, stroke_width=2,
                   stroke_dasharray="7 5"))
    for k in range(8):
        a = math.radians(k * 45 + 22.5)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        # camera ray toward the group
        fig.add(line(x, y, cx + (r_group + 18) * math.cos(a),
                     cy + (r_group + 18) * math.sin(a), stroke=BLUE,
                     stroke_width=1.2, stroke_dasharray="3 3"))
        # nose (camera) points at the centre
        rot = math.degrees(a) - 90
        fig.add(g(aircraft_mini_top(0.32),
                  transform=f"translate({x:.1f},{y:.1f}) rotate({rot:.1f})"))
    # radius, measured from the group's edge out to the ring
    fig.add(line(cx, cy, cx, cy - R, stroke=P["line"], stroke_width=1.2))
    _t(fig, cx + 8, cy - R / 2 - 18, "20 to 30 ft", size=12.5, bold=True,
       anchor="start")
    _t(fig, cx + 8, cy - R / 2 - 3, "(6 to 9 m)", size=12, fill=P["muted"],
       anchor="start")
    _t(fig, cx, cy + r_group + 34, "Never over the group", size=12.5,
       bold=True, fill=RED)
    _t(fig, cx, cy + R + 32, "Camera pointed in the whole way round,",
       size=12.5, fill=P["muted"])
    _t(fig, cx, cy + R + 48, "a photo every 10° or so", size=12.5,
       fill=P["muted"])


def _side_view(fig, cx, ground):
    """Side view: the circle climbs in a spiral, tilting the camera down as it
    goes up."""
    ft = 7.0                       # pixels per foot
    rx, ry = 140, 20               # the circle seen at a shallow angle
    h0, h1, turns = 8, 34, 2.75       # feet at the start and end, turns flown
    _t(fig, cx, 82, "From the side", size=14, bold=True)
    fig.add(line(cx - 215, ground, cx + 215, ground, stroke=P["line"],
                 stroke_width=2))
    for k, dx in enumerate([-60, -30, 0, 30, 60]):
        fig.add(g(person(cx + dx, ground, scale=1.8 if k % 2 else 2.0,
                         fill="#7d8894"), stroke=P["white"], stroke_width=0.6))

    # the spiral: back halves dashed (behind the group), front halves solid
    n = 360
    pts = []
    for i in range(n + 1):
        th = 2 * math.pi * turns * i / n
        h = h0 + (h1 - h0) * i / n
        pts.append((cx + rx * math.sin(th), ground - h * ft + ry * math.cos(th),
                    math.cos(th) >= 0))
    seg = [pts[0]]
    for p in pts[1:]:
        if p[2] != seg[-1][2]:
            seg.append(p)
            _spiral_segment(fig, seg)
            seg = [p]
        else:
            seg.append(p)
    _spiral_segment(fig, seg)

    # drones at the side of the first and last turn, camera aimed at the group
    aim = (cx, ground - 6 * ft * 0.6)
    for th_turn, h in [(0.25, h0 + (h1 - h0) * 0.25 / turns),
                       (turns, h1)]:
        x = cx + rx * math.sin(2 * math.pi * th_turn)
        y = ground - h * ft
        fig.add(line(x, y + 4, aim[0] + (18 if x > cx else -18), aim[1],
                     stroke=BLUE, stroke_width=1.2, stroke_dasharray="4 3"))
        fig.add(translate(x, y, aircraft_mini_side(0.55, nose=False)))
    lx = cx + rx + 40
    _t(fig, lx, ground - h1 * ft - 4, "End about 35 ft", size=12.5,
       bold=True, anchor="start")
    _t(fig, lx, ground - h1 * ft + 12, "camera about −45°", size=12,
       fill=P["muted"], anchor="start")
    _t(fig, lx, ground - (h0 + 2) * ft - 4, "Start about 8 ft", size=12.5,
       bold=True, anchor="start")
    _t(fig, lx, ground - (h0 + 2) * ft + 12, "camera about −15°", size=12,
       fill=P["muted"], anchor="start")
    _t(fig, cx, ground + 24, "The group holds still for 3 to 5 minutes.",
       size=12.5, fill=P["muted"])
    _t(fig, cx, ground + 40, "Anyone who moves becomes a blur or a ghost.",
       size=12.5, fill=P["muted"])


def _spiral_segment(fig, seg):
    if len(seg) < 2:
        return
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y, _ in seg)
    front = seg[1][2]
    fig.add(path(d, fill="none", stroke=BLUE, stroke_width=2 if front else 1.5,
                 stroke_dasharray=None if front else "5 5",
                 stroke_opacity=1 if front else 0.55))


def build_group_orbit() -> Figure:
    fig = Figure(W, 480, "Figure 2: A 3D model of your group",
                 "An ascending circle, the same pattern DJI's tower missions "
                 "fly. Numbers are a starting point; tune them in your "
                 "proposal.")
    _top_view(fig, 215, 262)
    fig.add(line(430, 70, 430, 456, stroke="#dde3e9", stroke_width=1.5))
    _side_view(fig, 600, 410)
    return fig


# ---------------------------------------------------------------------------
# 3. The 50-minute trip
# ---------------------------------------------------------------------------
STEPS = [  # (name, colour)
    ("Check out drone", "#c9d3dd"),
    ("Walk to site", "#9fb1c4"),
    ("Set up and pre-flight checklist", "#f6d7a7"),
    ("Fly", BLUE),
    ("Extra photos, tape a check", "#9fd3ae"),
    ("Post-flight and pack up", "#f6d7a7"),
    ("Walk back", "#9fb1c4"),
]


def _bar(fig, y, minutes, x0, px):
    x = x0
    for (name, colour), m in zip(STEPS, minutes):
        w = m * px
        fig.add(rect(x, y, w, 34, fill=colour, stroke=P["white"],
                     stroke_width=1.5))
        _t(fig, x + w / 2, y + 22, str(m), size=13, bold=True,
           fill=P["white"] if colour == BLUE else P["ink"])
        x += w
    return x


def build_trip_budget() -> Figure:
    fig = Figure(W, 372, "Figure 3: Does the trip fit in 50 minutes?",
                 "From EB B122 and back. The next trip needs the drone, so "
                 "plan for 40 and keep 10 for wind, people and batteries.")
    x0, px = 190, 12.0
    lim40, lim50 = x0 + 40 * px, x0 + 50 * px
    near = [3, 5, 7, 8, 5, 4, 5]
    far = [3, 12, 7, 8, 5, 4, 12]
    rows = [(106, near, "Site 5 minutes away", f"{sum(near)} min",
             f"fits, {50 - sum(near)} min to spare", GREEN),
            (186, far, "Site 12 minutes away", f"{sum(far)} min",
             "does not fit", RED)]
    for y, mins, name, total, verdict, colour in rows:
        _t(fig, x0 - 14, y + 16, name, size=13.5, bold=True, anchor="end")
        _t(fig, x0 - 14, y + 32, verdict, size=12, bold=True, fill=colour,
           anchor="end")
        end = _bar(fig, y, mins, x0, px)
        _t(fig, end + 8, y + 22, total, size=13, bold=True, fill=colour,
           anchor="start")
        if sum(mins) > 50:
            fig.add(rect(lim50, y - 4, end - lim50, 42, fill=RED,
                         fill_opacity=0.18, stroke=RED, stroke_width=1.2))
    for x, lab, colour, dash in [(lim40, "plan for 40", ORANGE, "6 4"),
                                 (lim50, "50: trip over", RED, None)]:
        fig.add(line(x, 84, x, 236, stroke=colour, stroke_width=2,
                     stroke_dasharray=dash))
        _t(fig, x, 78, lab, size=12, bold=True, fill=colour)

    # legend, one entry per colour
    lx, ly = 70, 276
    legend = [("Check out the drone", "#c9d3dd"), ("Walking", "#9fb1c4"),
              ("Checklists, set up, pack", "#f6d7a7"), ("Fly", BLUE),
              ("Extra photos, tape a check", "#9fd3ae")]
    for i, (name, colour) in enumerate(legend):
        col, row = i % 3, i // 3
        x, y = lx + col * 260, ly + row * 28
        fig.add(rect(x, y - 12, 16, 16, rx=3, fill=colour))
        _t(fig, x + 24, y + 1, name, size=12.5, anchor="start")
    _t(fig, W / 2, 344,
       "Minutes are an example. Time your own walk, and take the flight "
       "time from your plan.", size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, number, slug in (
        (build_turn_ins, 1, "turn_ins"),
        (build_group_orbit, 2, "group_orbit"),
        (build_trip_budget, 3, "trip_budget"),
    ):
        fname = os.path.join(args.out, figure_name(10, number, slug))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
