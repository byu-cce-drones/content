"""Figures for the "Automated Flight Functions" section.

Usage:
    python fig_tools/fig_automation.py --png
    python fig_tools/fig_automation.py --out docs/week_01/images

Outputs:
    fig12_home_point.svg        holding position, with and without satellites
    fig13_obstacle_coverage.svg where the sensors look, and where they do not
    fig14_battery_states.svg    what the aircraft does as the battery drains
    fig15_return_to_home.svg    the Return to Home flight profile
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_side, aircraft_mini_top  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    path, polygon, rect, render_png, text, translate)


def home_marker(x, y, scale=1.0):
    """A small house with an H, marking the take-off point."""
    return translate(x, y, g(
        path("M-13,2 l13,-11 l13,11 v15 h-26 z", fill=P["body"],
             stroke=P["line"], stroke_width=1.5),
        text(0, 14, "H", text_anchor="middle", font_size=11,
             font_weight="bold", fill=P["ink"]),
        transform=f"scale({scale})" if scale != 1 else None))


def satellite_arcs(live=True):
    color = P["accent"] if live else "#c8d0d8"
    grp = g()
    for r in (12, 20, 28):
        grp.add(path(f"M{-r},0 a{r},{r} 0 0,1 {2 * r},0", fill="none",
                     stroke=color, stroke_width=2.4, stroke_linecap="round"))
    if not live:
        grp.add(g(line(-14, -22, 14, 2), line(14, -22, -14, 2),
                  stroke=P["bad"], stroke_width=3, stroke_linecap="round"))
    return grp


# ---------------------------------------------------------------------------
# Figure 12: position hold
# ---------------------------------------------------------------------------
def build_home_point() -> Figure:
    fig = Figure(900, 440,
                 "Figure 12: Holding position, with and without satellites",
                 "A drone that knows where it is will sit still. One that does "
                 "not will drift, and it will not tell you loudly.")

    for cx, live, title, caption in (
        (255, True, "Satellites locked",
         ("The aircraft holds its position", "and knows where home is")),
        (645, False, "Satellite signal lost",
         ("The aircraft drifts with the wind", "and must be flown by hand")),
    ):
        fig.add(rect(cx - 175, 84, 350, 320, rx=12, fill=P["white"],
                     stroke="#dde3e9", stroke_width=1.5))
        fig.add(text(cx, 114, title, text_anchor="middle", font_size=15,
                     font_weight="bold", fill=P["ink"]))
        fig.add(translate(cx, 158, satellite_arcs(live)))

        ground_y = 300
        fig.add(line(cx - 140, ground_y, cx + 140, ground_y, stroke="#9aa7b2",
                     stroke_width=3, stroke_linecap="round"))
        fig.add(home_marker(cx - 60, ground_y - 18))
        # the spot directly above the take-off point
        fig.add(line(cx - 60, ground_y - 22, cx - 60, 214, stroke="#c8d0d8",
                     stroke_width=1.5, stroke_dasharray="5 4"))

        if live:
            fig.add(translate(cx - 60, 214, aircraft_mini_side(0.7, nose=False)))
            fig.add(text(cx - 60, 254, "stays put", text_anchor="middle",
                         font_size=12, fill=P["accent"]))
        else:
            fig.add(translate(cx + 40, 214, aircraft_mini_side(0.7, nose=False)))
            for wy in (196, 232):
                fig.add(arrow(cx - 128, wy, cx - 92, wy, color="#9aa7b2",
                              width=2.5, head=8))
            fig.add(text(cx - 110, 182, "wind", text_anchor="middle",
                         font_size=12, fill=P["muted"]))
            fig.add(arrow(cx - 34, 214, cx + 4, 214, color=P["bad"], width=3))
            fig.add(text(cx + 40, 254, "drifts", text_anchor="middle",
                         font_size=12, fill=P["bad"]))

        for i, ln in enumerate(caption):
            fig.add(text(cx, 348 + i * 18, ln, text_anchor="middle",
                         font_size=12.5, fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Figure 13: obstacle sensor coverage
# ---------------------------------------------------------------------------
def wedge(cx, cy, r, a0, a1, **attrs):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return path(f"M{cx},{cy} L{x0:.1f},{y0:.1f} "
                f"A{r},{r} 0 {large},1 {x1:.1f},{y1:.1f} Z", **attrs)


def build_obstacle_coverage() -> Figure:
    fig = Figure(900, 470,
                 "Figure 13: Where the obstacle sensors look",
                 "Coverage varies a lot between models. Many small drones watch "
                 "forward and down only.")

    cx, cy, r = 398, 250, 155
    fig.add(wedge(cx, cy, r, -125, -55, fill="#cfe3f7", stroke=P["accent"],
                  stroke_width=1.5))
    fig.add(wedge(cx, cy, r, 55, 125, fill="#cfe3f7", stroke=P["accent"],
                  stroke_width=1.5))
    fig.add(wedge(cx, cy, r, -55, 55, fill="#fbe0dc", stroke="#e8b4ac",
                  stroke_width=1.5))
    fig.add(wedge(cx, cy, r, 125, 235, fill="#fbe0dc", stroke="#e8b4ac",
                  stroke_width=1.5))
    fig.add(translate(cx, cy, aircraft_mini_top(1.05)))

    fig.add(text(cx, cy - r - 16, "sees ahead", text_anchor="middle",
                 font_size=13, font_weight="bold", fill=P["accent"]))
    fig.add(text(cx, cy + r + 26, "sees behind", text_anchor="middle",
                 font_size=13, font_weight="bold", fill=P["accent"]))
    fig.add(text(cx - r - 14, cy + 5, "blind", text_anchor="end",
                 font_size=13, font_weight="bold", fill=P["bad"]))
    fig.add(text(cx + r + 14, cy + 5, "blind", text_anchor="start",
                 font_size=13, font_weight="bold", fill=P["bad"]))

    # what the sensors cannot see, whichever way they point
    bx = 700
    fig.add(rect(bx - 60, 110, 180, 270, rx=10, fill=P["white"],
                 stroke="#dde3e9", stroke_width=1.5))
    fig.add(text(bx + 30, 140, "Missed even in view", text_anchor="middle",
                 font_size=13, font_weight="bold", fill=P["ink"]))
    for i, item in enumerate(("water", "glass and mirrors", "thin branches",
                              "power lines", "plain white walls",
                              "anything in the dark")):
        y = 174 + i * 32
        fig.add(circle(bx - 38, y - 4, 4, fill=P["bad"]))
        fig.add(text(bx - 26, y, item, font_size=12.5, fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Figure 14: battery states
# ---------------------------------------------------------------------------
def build_battery_states() -> Figure:
    fig = Figure(900, 340,
                 "Figure 14: What happens as the battery drains",
                 "The aircraft starts making decisions for you. Exact "
                 "percentages vary by model and rise the further away you are.")

    x0, x1, y, h = 80, 820, 130, 52
    bands = (
        (0.44, "#5cb85c", "Normal flying", ("you are in", "full control")),
        (0.20, "#f0ad4e", "Low battery warning", ("it asks you", "to come back")),
        (0.20, "#e8873a", "Return to Home", ("it starts flying", "home by itself")),
        (0.16, "#d9534f", "Forced landing", ("it comes down", "where it is")),
    )

    x = x0
    for frac, color, label, lines in bands:
        w = (x1 - x0) * frac
        fig.add(rect(x, y, w, h, fill=color, stroke=P["white"],
                     stroke_width=2))
        mid = x + w / 2
        fig.add(text(mid, y + h + 30, label, text_anchor="middle",
                     font_size=13, font_weight="bold", fill=P["ink"]))
        for i, ln in enumerate(lines):
            fig.add(text(mid, y + h + 52 + i * 17, ln, text_anchor="middle",
                         font_size=12, fill=P["muted"]))
        x += w

    fig.add(text(x0, y - 14, "battery full", font_size=12.5, fill=P["muted"]))
    fig.add(text(x1, y - 14, "empty", text_anchor="end", font_size=12.5,
                 fill=P["muted"]))
    fig.add(arrow(x0 + 90, y - 20, x1 - 60, y - 20, color="#b6c2cc", width=2.5))

    fig.add(text(450, 300,
                 "Plan to land during the green. The moment the aircraft "
                 "decides for you, you have already left it too late.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Figure 15: Return to Home profile
# ---------------------------------------------------------------------------
def build_return_to_home() -> Figure:
    fig = Figure(900, 480,
                 "Figure 15: What Return to Home actually does",
                 "It climbs first, then flies a straight line home. It does not "
                 "steer around anything on the way.")

    ground_y, home_x, craft_x = 372, 150, 760
    safe_y, unsafe_y = 168, 300

    fig.add(rect(40, 84, 820, ground_y - 84, rx=10, fill="#f2f6fa",
                 stroke="#dde3e9", stroke_width=1.5))
    fig.add(line(40, ground_y, 860, ground_y, stroke="#9aa7b2", stroke_width=3,
                 stroke_linecap="round"))

    # a tree line in the way
    for tx in (430, 480, 530):
        fig.add(polygon([(tx, 232), (tx - 26, ground_y), (tx + 26, ground_y)],
                        fill="#7fa87f", stroke="#5f855f", stroke_width=1.5))

    # the same flight with the RTH altitude set too low, drawn first
    fig.add(line(craft_x, unsafe_y, home_x, unsafe_y, stroke=P["bad"],
                 stroke_width=2.5, stroke_dasharray="6 5"))
    fig.add(circle(505, unsafe_y, 14, fill="none", stroke=P["bad"],
                   stroke_width=3))
    fig.add(line(496, unsafe_y - 9, 514, unsafe_y + 9, stroke=P["bad"],
                 stroke_width=3, stroke_linecap="round"))
    fig.add(text(645, unsafe_y - 14, "RTH altitude set too low",
                 text_anchor="middle", font_size=12.5, fill=P["bad"]))

    # the safe profile: climb, cross, descend
    fig.add(path(f"M{craft_x},{safe_y + 60} V{safe_y} H{home_x} V{ground_y - 26}",
                 fill="none", stroke=P["accent"], stroke_width=3,
                 stroke_dasharray="9 6"))
    fig.add(arrow(craft_x, safe_y + 26, craft_x, safe_y + 6, width=3))
    fig.add(arrow(620, safe_y, 545, safe_y, width=3))
    fig.add(arrow(home_x, ground_y - 60, home_x, ground_y - 34, width=3))

    fig.add(translate(craft_x, safe_y + 88, aircraft_mini_side(0.72, nose=False)))
    fig.add(home_marker(home_x, ground_y - 18))

    # numbered markers sit on the path, and are explained in the legend below
    for n, (x, y) in enumerate(((craft_x, safe_y + 44), (440, safe_y),
                                (home_x, ground_y - 90))):
        fig.add(circle(x, y, 13, fill=P["accent"], stroke=P["white"],
                       stroke_width=2))
        fig.add(text(x, y + 5, n + 1, text_anchor="middle", font_size=12,
                     font_weight="bold", fill=P["white"]))

    for x, n, label in ((180, 1, "climb to the set altitude"),
                        (450, 2, "fly straight home"),
                        (715, 3, "descend and land")):
        fig.add(circle(x - 92, 414, 12, fill=P["accent"]))
        fig.add(text(x - 92, 418, n, text_anchor="middle", font_size=11,
                     font_weight="bold", fill=P["white"]))
        fig.add(text(x - 74, 419, label, font_size=12.5, fill=P["muted"]))

    fig.add(text(450, 456,
                 "Set the Return to Home altitude above the tallest thing "
                 "between you and the aircraft, every site, every time.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, name in (
        (build_home_point, figure_name(1, 12, "home_point")),
        (build_obstacle_coverage, figure_name(1, 13, "obstacle_coverage")),
        (build_battery_states, figure_name(1, 14, "battery_states")),
        (build_return_to_home, figure_name(1, 15, "return_to_home")),
    ):
        fname = os.path.join(args.out, name)
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
