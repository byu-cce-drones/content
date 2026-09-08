"""Illustrations for the Topic 1 overview page.

These carry captions but no figure numbers, because nothing refers to them by
number. That keeps the numbered sequence on Flight Basics and Common Flight
Issues untouched.

Usage:
    python fig_tools/fig_overview.py --png
    python fig_tools/fig_overview.py --out docs/gen_reading/images

Outputs:
    w01_overview_photo_placeholder.svg  stand-in until a real photo arrives
    w01_overview_semester.svg           the semester at a glance, six
                                        areas of study over fifteen weeks
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
# The semester at a glance
# ---------------------------------------------------------------------------
# Each area of study, drawn as a bar over the weeks it actually runs. The week
# numbers are the ones in the site nav; change them here and in mkdocs.yml
# together. Weeks are inclusive on both ends.
AREAS = (
    (1, "Fly it", 1, 3,
     "meet the aircraft, earn your TRUST certificate, two flying labs"),
    (2, "Measure it", 4, 5,
     "GIS tools, checklists, and one site measured four different ways"),
    (3, "Plan it", 6, 7,
     "design a mapping flight, then fly it at Rock Canyon"),
    (4, "Process it", 7, 8,
     "turn a pile of photos into a map; what other sensors can see"),
    (5, "Get certified", 9, 9,
     "the FAA Part 107 exam"),
    (6, "Prove it", 10, 15,
     "the final project: plan, fly, process, report, present"),
)

N_WEEKS = 15
STRIP_X, CELL = 100, 50          # left edge of Week 1, width of one week
STRIP_TOP, STRIP_H = 410, 30
LANE_TOP, LANE_H = 62, 57        # top of area 1's lane, and the lane pitch
BAR_DY, BAR_H = 38, 14           # bar offset inside its lane, and bar height
RIGHT_EDGE = 876                 # text may not run past here

# rough Arial advance widths, used only to keep a long note on the canvas
_W_NAME, _W_NOTE = 9.3, 6.4


def _week_x(week: int) -> float:
    """Left edge of a week cell."""
    return STRIP_X + (week - 1) * CELL


def _week_cx(week: int) -> float:
    return _week_x(week) + CELL / 2


def _span_bar(fig: Figure, num: int, bx: float, bw: float, by: float) -> None:
    """A rounded span bar with its numbered badge at the left end."""
    fig.add(rect(bx, by, bw, BAR_H, rx=BAR_H / 2, fill=P["screen"],
                 stroke=P["accent"], stroke_width=2))
    fig.add(circle(bx + 11, by + BAR_H / 2, 11, fill=P["accent"]))
    fig.add(text(bx + 11, by + BAR_H / 2 + 4, num, text_anchor="middle",
                 font_size=12, font_weight="bold", fill=P["white"]))


def build_semester() -> Figure:
    fig = Figure(900, 470, "The semester at a glance",
                 "Six areas of study. One hour of lecture and one lab a week, "
                 "and you fly in Week 2, not at the end.")

    # faint week gridlines, so a bar can be read against the strip below
    for wk in range(1, N_WEEKS + 2):
        fig.add(line(_week_x(wk), LANE_TOP - 2, _week_x(wk), STRIP_TOP,
                     stroke=P["off"], stroke_width=1, opacity=0.5))

    # --- the six areas, one lane each, in semester order -------------------
    for i, (num, name, w_first, w_last, note) in enumerate(AREAS):
        top = LANE_TOP + i * LANE_H
        bx = _week_x(w_first)
        bw = (w_last - w_first + 1) * CELL
        by = top + BAR_DY

        # Week 3 marker for Get certified: the rules are introduced long
        # before the exam sits in Week 9.
        if num == 5:
            mx = _week_cx(3)
            fig.add(line(mx, by + BAR_H / 2, bx, by + BAR_H / 2,
                         stroke=P["accent"], stroke_width=1.5,
                         stroke_dasharray="5 5"))
            fig.add(circle(mx, by + BAR_H / 2, 6, fill=P["accent"]))
            fig.add(text(mx, top + 28, "rules introduced", text_anchor="middle",
                         font_size=11, fill=P["muted"]))

        _span_bar(fig, num, bx, bw, by)

        # keep a long note on the canvas even when its bar starts far right
        tw = max(len(name) * _W_NAME, len(note) * _W_NOTE)
        tx = max(20, min(bx, RIGHT_EDGE - tw))
        fig.add(text(tx, top + 13, name, font_size=16, font_weight="bold",
                     fill=P["ink"]))
        fig.add(text(tx, top + 28, note, font_size=12.5, fill=P["muted"]))

    # --- the week strip ----------------------------------------------------
    fig.add(text(STRIP_X - 8, STRIP_TOP + 20, "Week", text_anchor="end",
                 font_size=12, fill=P["muted"]))
    for wk in range(1, N_WEEKS + 1):
        break_week = wk == 13
        fig.add(rect(_week_x(wk), STRIP_TOP, CELL, STRIP_H,
                     fill=P["white"] if break_week else P["body"],
                     stroke=P["body"] if break_week else P["white"],
                     stroke_width=2))
        fig.add(text(_week_cx(wk), STRIP_TOP + 20, wk, text_anchor="middle",
                     font_size=12, fill=P["ink"]))

    fig.add(text(_week_cx(13), STRIP_TOP + 46, "Thanksgiving",
                 text_anchor="middle", font_size=11, fill=P["muted"]))
    fig.add(text(_week_cx(15), STRIP_TOP + 46, "final presentations",
                 text_anchor="middle", font_size=11, fill=P["muted"]))
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
