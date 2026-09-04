"""Figures for the "A Basic Flight" section.

Usage:
    python fig_tools/fig_sequence.py --png
    python fig_tools/fig_sequence.py --out docs/week_01/images

Outputs:
    fig10_flight_sequence.svg   nine steps, grouped into three phases
    fig11_practice_pattern.svg  the box pattern to practice first
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_side, aircraft_mini_top  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    path, polygon, rect, render_png, text, translate)

CARD_W, CARD_H = 270, 150
COLS = (155, 450, 745)


# ---------------------------------------------------------------------------
# Step icons, all drawn at the local origin in roughly a 50 x 50 box
# ---------------------------------------------------------------------------
def icon_site():
    grp = g(rect(-22, -17, 44, 34, rx=4, fill="#e8edf2", stroke=P["line"],
                 stroke_width=1.5))
    grp.add(g(line(-8, -17, -8, 17), line(8, -17, 8, 17),
              stroke="#b6c2cc", stroke_width=1.2))
    grp.add(path("M4,-2 a9,9 0 1,1 18,0 c0,7 -9,16 -9,16 c0,0 -9,-9 -9,-16 z",
                 fill=P["bad"], stroke=P["line"], stroke_width=1.2))
    grp.add(circle(13, -2, 3.4, fill=P["white"]))
    return grp


def icon_unfold():
    grp = g(rect(-7, -13, 14, 26, rx=4, fill=P["body"], stroke=P["line"],
                 stroke_width=1.5))
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        grp.add(line(sx * 4, sy * 8, sx * 20, sy * 15, stroke=P["line"],
                     stroke_width=4, stroke_linecap="round"))
        grp.add(circle(sx * 20, sy * 15, 5, fill="#e8edf2", stroke="#b6c2cc",
                       stroke_width=1.2))
    grp.add(path("M-26,-4 a14,14 0 0,1 6,-13", fill="none", stroke=P["accent"],
                 stroke_width=2.2, stroke_linecap="round"))
    grp.add(polygon([(-19, -19), (-13, -13), (-21, -11)], fill=P["accent"]))
    return grp


def icon_battery():
    grp = g(rect(-20, -8, 36, 22, rx=3, fill="#c2cad2", stroke=P["line"],
                 stroke_width=1.5))
    grp.add(rect(16, -2, 5, 10, rx=2, fill=P["line"]))
    grp.add(g(*[line(-13 + i * 9, -3, -13 + i * 9, 9) for i in range(3)],
              stroke="#8fa3b5", stroke_width=3.5, stroke_linecap="round"))
    grp.add(arrow(-2, -28, -2, -14, width=2.5, head=8))
    return grp


def icon_power():
    grp = g(circle(0, 2, 16, fill="none", stroke=P["accent"], stroke_width=3.5))
    grp.add(rect(-2.2, -22, 4.4, 18, rx=2, fill=P["bg"]))
    grp.add(line(0, -18, 0, 0, stroke=P["accent"], stroke_width=3.5,
                 stroke_linecap="round"))
    return grp


def icon_satellites():
    grp = g()
    for r in (10, 17, 24):
        grp.add(path(f"M{-r},-4 a{r},{r} 0 0,1 {2 * r},0", fill="none",
                     stroke=P["accent"], stroke_width=2.2,
                     stroke_linecap="round"))
    grp.add(path("M-11,4 l11,-9 l11,9 v13 h-22 z", fill=P["body"],
                 stroke=P["line"], stroke_width=1.5))
    grp.add(text(0, 16, "H", text_anchor="middle", font_size=10,
                 font_weight="bold", fill=P["ink"]))
    return grp


def ground(y=18, half=26):
    return line(-half, y, half, y, stroke=P["muted"], stroke_width=2.5,
                stroke_linecap="round")


def icon_takeoff():
    return g(ground(), translate(0, 2, aircraft_mini_side(0.42, nose=False)),
             arrow(24, 2, 24, -20, width=2.5, head=8))


def icon_fly():
    grp = g(path("M-2,6 q16,2 22,-10 q4,-8 6,-12", fill="none",
                 stroke=P["accent"], stroke_width=2.2, stroke_dasharray="5 4",
                 stroke_linecap="round"))
    grp.add(translate(-18, 4, aircraft_mini_top(0.42)))
    return grp


def icon_land():
    return g(ground(), translate(0, 2, aircraft_mini_side(0.42, nose=False)),
             arrow(24, -20, 24, 2, width=2.5, head=8))


def icon_data():
    grp = g(rect(-28, -16, 20, 32, rx=3, fill="#c2cad2", stroke=P["line"],
                 stroke_width=1.5))
    grp.add(g(*[line(-24 + i * 5, -16, -24 + i * 5, -9) for i in range(4)],
              stroke="#8fa3b5", stroke_width=2.5))
    grp.add(arrow(-4, 0, 8, 0, width=2.5, head=8))
    # a folder for the images to land in
    grp.add(path("M13,-13 h9 l4,5 h6 v21 h-19 z", fill=P["body"],
                 stroke=P["line"], stroke_width=1.5))
    return grp


PHASES = (
    ("Set up", (
        (icon_site, ("Check the site,", "the weather and the airspace")),
        (icon_unfold, ("Unfold the arms, inspect", "the propellers")),
        (icon_battery, ("Fit the battery and take", "off the gimbal cover")),
    )),
    ("Start up", (
        (icon_power, ("Power on the controller,", "then the aircraft")),
        (icon_satellites, ("Wait for satellites and the", "home point message")),
        (icon_takeoff, ("Take off, hover at eye level,", "check it responds")),
    )),
    ("Fly and finish", (
        (icon_fly, ("Fly the job, watching", "battery and distance")),
        (icon_land, ("Land, power off the aircraft,", "then the controller")),
        (icon_data, ("Copy the images off the card", "and log the flight")),
    )),
)


def build_sequence() -> Figure:
    fig = Figure(900, 680,
                 "Figure 10: A flight from start to finish",
                 "The order matters. Most incidents come from a step skipped "
                 "on the ground, not from difficult flying.")

    step = 1
    for row, (phase, entries) in enumerate(PHASES):
        header_y = 84 + row * 198
        top = header_y + 12
        fig.add(text(20, header_y, phase, font_size=15, font_weight="bold",
                     fill=P["accent"]))
        for col, (icon, lines) in enumerate(entries):
            cx = COLS[col]
            fig.add(rect(cx - CARD_W / 2, top, CARD_W, CARD_H, rx=10,
                         fill=P["white"], stroke="#dde3e9", stroke_width=1.5))
            fig.add(circle(cx - 105, top + 26, 14, fill=P["accent"]))
            fig.add(text(cx - 105, top + 31, step, text_anchor="middle",
                         font_size=13, font_weight="bold", fill=P["white"]))
            fig.add(translate(cx, top + 60, icon()))
            for i, ln in enumerate(lines):
                fig.add(text(cx, top + 110 + i * 18, ln, text_anchor="middle",
                             font_size=12, fill=P["muted"]))
            if col < 2:
                fig.add(arrow(cx + CARD_W / 2 + 4, top + CARD_H / 2,
                              cx + CARD_W / 2 + 20, top + CARD_H / 2,
                              color="#b6c2cc", width=3, head=9))
            step += 1
    return fig


# ---------------------------------------------------------------------------
# Figure 11: the box pattern
# ---------------------------------------------------------------------------
def build_practice() -> Figure:
    fig = Figure(900, 470,
                 "Figure 11: The box, the first pattern to practice",
                 "Fly it slowly, one side at a time, pausing in a hover at "
                 "every corner.")

    # ground
    fig.add(rect(60, 84, 780, 320, rx=10, fill="#eef4ea", stroke="#cfdcc6",
                 stroke_width=1.5))

    box = (240, 175, 660, 330)   # left, top, right, bottom of the flight path
    l, t, r, b = box
    fig.add(rect(l, t, r - l, b - t, fill="none", stroke=P["accent"],
                 stroke_width=2.5, stroke_dasharray="8 6"))

    # direction of travel along each side
    fig.add(arrow(l + 150, t, l + 230, t, width=3))
    fig.add(arrow(r, t + 45, r, t + 100, width=3))
    fig.add(arrow(r - 110, b, r - 200, b, width=3))
    fig.add(arrow(l, b - 45, l, b - 100, width=3))

    # corners, numbered in flying order
    for i, (x, y) in enumerate(((l, t), (r, t), (r, b), (l, b))):
        fig.add(circle(x, y, 15, fill=P["white"], stroke=P["accent"],
                       stroke_width=2.5))
        fig.add(text(x, y + 5, i + 1, text_anchor="middle", font_size=13,
                     font_weight="bold", fill=P["accent"]))

    # the aircraft sits along the first leg, so corner 1 stays readable
    fig.add(translate(l + 78, t, aircraft_mini_top(0.62)))

    # pilot
    fig.add(circle(450, 366, 11, fill=P["dark"]))
    fig.add(path("M439,386 a11,13 0 0,1 22,0 z", fill=P["dark"]))
    fig.add(text(450, 350, "you", text_anchor="middle", font_size=12.5,
                 fill=P["muted"]))

    fig.add(text(450, 118, "Keep the nose pointed away from you for every side",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    fig.add(text(450, 440,
                 "Then repeat it with the nose always pointing the way you are "
                 "flying, and notice how different it feels.",
                 text_anchor="middle", font_size=12.5, fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, name in (
            (build_sequence, figure_name(1, 10, "flight_sequence")),
            (build_practice, figure_name(1, 11, "practice_pattern"))):
        fname = os.path.join(args.out, name)
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
