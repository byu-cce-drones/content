"""Illustrations for the Topic 1 overview page.

These carry captions but no figure numbers, because nothing refers to them by
number. That keeps the numbered sequence on Flight Basics and Common Flight
Issues untouched.

Usage:
    python fig_tools/fig_overview.py --png
    python fig_tools/fig_overview.py --out docs/week_01/images

Outputs:
    w01_overview_photo_placeholder.svg  stand-in until a real photo arrives
    w01_overview_semester.svg           the six weeks at a glance
    w01_overview_accuracy_effort.svg    picking a measurement method
    w01_overview_products.svg           one site, four things a drone gives you
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_top, person  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    path, polygon, rect, render_png, text, translate)

CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)


# ---------------------------------------------------------------------------
# Placeholder, so the page lays out correctly before the photo exists
# ---------------------------------------------------------------------------
def build_placeholder() -> Figure:
    fig = Figure(900, 400, None, None)
    fig.add(rect(30, 30, 840, 340, rx=14, fill="#eef1f4", stroke="#c5cdd5",
                 stroke_width=2.5, stroke_dasharray="12 9"))
    cx, cy = 450, 172
    fig.add(rect(cx - 62, cy - 38, 124, 82, rx=10, fill="#c5cdd5"))
    fig.add(rect(cx - 22, cy - 52, 44, 16, rx=5, fill="#c5cdd5"))
    fig.add(circle(cx, cy + 3, 26, fill=P["white"]))
    fig.add(circle(cx, cy + 3, 15, fill="#c5cdd5"))
    fig.add(translate(cx + 132, cy - 14, aircraft_mini_top(0.62)))
    fig.add(person(cx - 140, cy + 42, 1.5, fill="#c5cdd5"))
    fig.add(text(450, 272, "Photo to come", text_anchor="middle", font_size=19,
                 font_weight="bold", fill=P["muted"]))
    fig.add(text(450, 300, "students flying on campus", text_anchor="middle",
                 font_size=14, fill="#8fa3b5"))
    return fig


# ---------------------------------------------------------------------------
# The six weeks
# ---------------------------------------------------------------------------
def icon_drone():
    return aircraft_mini_top(0.52)


def icon_laptop():
    return g(rect(-30, -22, 60, 40, rx=4, fill="#5a6570", stroke=P["line"],
                 stroke_width=1.5),
             rect(-24, -16, 48, 28, rx=2, fill=P["screen"]),
             rect(-40, 18, 80, 7, rx=3, fill="#8f9aa6", stroke=P["line"],
                  stroke_width=1.2))


def icon_ruler():
    grp = g(rect(-38, -12, 76, 26, rx=3, fill="#e8d9a8", stroke=P["line"],
                 stroke_width=1.5))
    for i in range(7):
        x = -30 + i * 10
        grp.add(line(x, -12, x, -12 + (13 if i % 2 == 0 else 8),
                     stroke=P["line"], stroke_width=1.5))
    return grp


def icon_grid():
    grp = g()
    for i in range(4):
        y = -18 + i * 12
        grp.add(line(-34, y, 34, y, stroke=P["accent"], stroke_width=2.5,
                     stroke_linecap="round"))
    grp.add(path("M34,-18 q10,6 0,12 M-34,-6 q-10,6 0,12 M34,6 q10,6 0,12",
                 fill="none", stroke=P["accent"], stroke_width=2.5))
    grp.add(rect(-40, 22, 80, 5, rx=2, fill="#c2cad2"))
    return grp


def icon_badge():
    return g(path("M0,-26 l26,10 v18 q0,18 -26,26 q-26,-8 -26,-26 v-18 z",
                  fill="#cfe3f7", stroke=P["accent"], stroke_width=2),
             path("M-10,2 l7,8 l15,-16", fill="none", stroke=P["accent"],
                  stroke_width=3.5, stroke_linecap="round",
                  stroke_linejoin="round"))


def icon_spectrum():
    grp = g()
    for i, c in enumerate(("#c0392b", "#e67e22", "#f4d03f", "#27ae60",
                           "#2980b9", "#6c3483")):
        grp.add(rect(-36 + i * 12, -18, 11, 36, rx=2, fill=c))
    return grp


WEEKS = (
    (1, icon_drone, "Fly it", "meet the aircraft and get it in the air"),
    (2, icon_laptop, "Process it", "turn a pile of photos into a map"),
    (3, icon_ruler, "Measure it", "measure one site four different ways"),
    (4, icon_grid, "Plan it", "design a flight that collects good data"),
    (5, icon_badge, "Get certified", "the FAA Part 107 exam"),
    (6, icon_spectrum, "See more", "thermal, multispectral, and LiDAR"),
)


def build_semester() -> Figure:
    fig = Figure(900, 440, "Six weeks, start to finish",
                 "One hour a week, and you fly in the first lab rather than the last week.")
    cols, w, h = (155, 450, 745), 270, 158
    for i, (num, icon, title, sub) in enumerate(WEEKS):
        cx = cols[i % 3]
        top = 84 + (i // 3) * 174
        fig.add(rect(cx - w / 2, top, w, h, **CARD))
        fig.add(circle(cx - 105, top + 26, 15, fill=P["accent"]))
        fig.add(text(cx - 105, top + 31, num, text_anchor="middle",
                     font_size=13, font_weight="bold", fill=P["white"]))
        fig.add(translate(cx + 12, top + 44, icon()))
        fig.add(text(cx, top + 108, title, text_anchor="middle", font_size=16,
                     font_weight="bold", fill=P["ink"]))
        fig.add(text(cx, top + 132, sub, text_anchor="middle", font_size=12.5,
                     fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Accuracy against effort
# ---------------------------------------------------------------------------
METHODS = (
    (178, 392, "Pacing", "free, roughly a meter"),
    (268, 344, "Handheld GPS", "seconds, a few meters"),
    (356, 236, "Tape or wheel", "slow, very accurate, small areas"),
    (566, 182, "Drone survey", "hours, centimeters, whole site"),
    (760, 126, "Survey crew", "days, millimeters"),
)


def build_accuracy_effort() -> Figure:
    fig = Figure(900, 500, "Picking a measurement method",
                 "There is no best method, only the cheapest one that still "
                 "answers the question.")

    x0, x1, y0, y1 = 120, 830, 430, 100
    fig.add(arrow(x0, y0, x1, y0, color="#8fa3b5", width=2.5))
    fig.add(arrow(x0, y0, x0, y1, color="#8fa3b5", width=2.5))
    fig.add(text(x1, y0 + 28, "more time, cost and effort", text_anchor="end",
                 font_size=13, fill=P["muted"]))
    fig.add(g(text(0, 0, "more accurate", text_anchor="end", font_size=13,
                   fill=P["muted"]),
              transform=f"translate({x0 - 16},{y1 + 8}) rotate(-90)"))

    for px, py, name, note in METHODS:
        drone = name == "Drone survey"
        if drone:
            fig.add(circle(px, py, 20, fill="none", stroke=P["accent"],
                           stroke_width=2, stroke_dasharray="4 4"))
        fig.add(circle(px, py, 10, fill=P["accent"] if drone else "#8fa3b5",
                       stroke=P["line"], stroke_width=1.5))
        fig.add(text(px, py - 30, name, text_anchor="middle", font_size=13.5,
                     font_weight="bold",
                     fill=P["accent"] if drone else P["ink"]))
        fig.add(text(px, py - 13, note, text_anchor="middle", font_size=11.5,
                     fill=P["muted"]))

    fig.add(text(450, 476,
                 "This course is about knowing which dot to reach for, and "
                 "being able to explain why.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# One site, four products
# ---------------------------------------------------------------------------
def build_products() -> Figure:
    fig = Figure(900, 350, "One flight, four things you can use",
                 "The same set of photos becomes each of these in turn.")
    cols, w, h, top = (128, 340, 552, 764), 180, 190, 84

    for i, (cx, title, sub) in enumerate((
        (cols[0], "Photos", "hundreds, overlapping"),
        (cols[1], "A map", "one flat, scaled image"),
        (cols[2], "A surface", "height at every point"),
        (cols[3], "A number", "volume, area, distance"),
    )):
        fig.add(rect(cx - w / 2, top, w, h, **CARD))
        mid = top + 62
        if i == 0:
            for j, (dx, dy) in enumerate(((-14, -10), (0, 0), (14, 10))):
                fig.add(rect(cx - 32 + dx, mid - 26 + dy, 64, 48, rx=3,
                             fill=P["white"], stroke=P["line"],
                             stroke_width=1.5))
            fig.add(rect(cx - 18, mid - 4, 36, 26, rx=2, fill="#cfe3f7"))
        elif i == 1:
            fig.add(rect(cx - 44, mid - 30, 88, 60, rx=3, fill="#e4ead9",
                         stroke=P["line"], stroke_width=1.5))
            fig.add(rect(cx - 30, mid - 18, 34, 22, fill="#c2cad2",
                         stroke="#9aa7b2", stroke_width=1))
            fig.add(path(f"M{cx - 44},{mid + 12} L{cx + 44},{mid + 4}",
                         stroke="#9aa7b2", stroke_width=4))
        elif i == 2:
            fig.add(path(f"M{cx - 46},{mid + 26} L{cx - 18},{mid - 12} "
                         f"L{cx + 6},{mid + 8} L{cx + 46},{mid - 24}",
                         fill="none", stroke=P["accent"], stroke_width=3,
                         stroke_linejoin="round"))
            for gx in range(-46, 47, 23):
                fig.add(line(cx + gx, mid + 30, cx + gx, mid + 38,
                             stroke="#c5cdd5", stroke_width=1.5))
            fig.add(line(cx - 46, mid + 30, cx + 46, mid + 30,
                         stroke="#9aa7b2", stroke_width=2))
        else:
            fig.add(path(f"M{cx - 44},{mid + 26} L{cx - 6},{mid - 22} "
                         f"L{cx + 44},{mid + 26} Z", fill="#e8d9a8",
                         stroke=P["line"], stroke_width=1.5))
            fig.add(text(cx, mid + 6, "1,840", text_anchor="middle",
                         font_size=14, font_weight="bold", fill=P["ink"]))
            fig.add(text(cx, mid + 20, "cubic yards", text_anchor="middle",
                         font_size=10, fill=P["muted"]))

        fig.add(text(cx, top + 138, title, text_anchor="middle", font_size=15,
                     font_weight="bold", fill=P["ink"]))
        fig.add(text(cx, top + 160, sub, text_anchor="middle", font_size=11.5,
                     fill=P["muted"]))
        if i < 3:
            fig.add(arrow(cx + w / 2 + 6, top + h / 2, cx + w / 2 + 26,
                          top + h / 2, color="#b6c2cc", width=3, head=9))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, slug in (
        (build_placeholder, "overview_photo_placeholder"),
        (build_semester, "overview_semester"),
        (build_accuracy_effort, "overview_accuracy_effort"),
        (build_products, "overview_products"),
    ):
        fname = os.path.join(args.out, figure_name(1, None, slug))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
