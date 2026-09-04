"""Figures: what each control stick does, and why nose-in flying feels reversed.

Usage:
    python fig_tools/fig_sticks.py --png
    python fig_tools/fig_sticks.py --out docs/week_01/images

Outputs:
    fig08_stick_controls.svg   eight panels, two across and four down
    fig09_nose_in.svg          the same right-stick input, seen two ways
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import (aircraft_mini_side, aircraft_mini_top,  # noqa: E402
                   rotation_arrow, stick_pair)
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, figure_name, g, render_png,  # noqa: E402
                    rect, text, translate)

# Two wide panels per row keeps each one large enough to read on the page.
COLS = (265, 635)
PANEL_W, PANEL_H = 340, 170


def panel(cx, top, side, dx, dy, label, sub, motion):
    """One panel, read left to right: sticks, then what the aircraft does."""
    grp = g(rect(cx - PANEL_W / 2, top, PANEL_W, PANEL_H, rx=10,
                 fill=P["white"], stroke="#dde3e9", stroke_width=1.5))
    grp.add(translate(cx - 92, top + 62, stick_pair(side, dx, dy, 17, 32)))
    grp.add(translate(cx + 88, top + 62, motion))
    grp.add(text(cx, top + 128, label, text_anchor="middle", font_size=16,
                 font_weight="bold", fill=P["ink"]))
    grp.add(text(cx, top + 149, sub, text_anchor="middle", font_size=12.5,
                 fill=P["muted"]))
    return grp


def vertical_motion(up: bool):
    """Side view, for climb and descend."""
    return g(aircraft_mini_side(0.8, nose=False),
             arrow(54, 18 if up else -18, 54, -34 if up else 34, width=2.5))


def yaw_motion(clockwise: bool):
    return g(aircraft_mini_top(0.8),
             rotation_arrow(0, 0, 40, clockwise=clockwise, start_deg=150,
                            sweep_deg=230, width=2.5))


def linear_motion(dx: float, dy: float):
    if dy:
        return g(aircraft_mini_top(0.8),
                 arrow(36, dy * 20, 36, dy * 48, width=2.5))
    return g(aircraft_mini_top(0.8),
             arrow(dx * 40, 0, dx * 72, 0, width=2.5))


def build_sticks() -> Figure:
    fig = Figure(900, 900,
                 "Figure 8: What each stick does",
                 "Mode 2 layout, the default on nearly every ready-to-fly drone. "
                 "All directions are relative to the nose of the aircraft.")

    rows = [
        (92, "Left stick — altitude and heading", "left", 104, [
            (0, -1, "Climb", "rises straight up", vertical_motion(True)),
            (0, 1, "Descend", "comes straight down", vertical_motion(False)),
            (-1, 0, "Turn left", "nose swings left", yaw_motion(False)),
            (1, 0, "Turn right", "nose swings right", yaw_motion(True)),
        ]),
        (500, "Right stick — moving over the ground", "right", 514, [
            (0, -1, "Fly forward", "in the direction the nose points",
             linear_motion(0, -1)),
            (0, 1, "Fly backward", "away from the nose", linear_motion(0, 1)),
            (-1, 0, "Slide left", "nose keeps pointing the same way",
             linear_motion(-1, 0)),
            (1, 0, "Slide right", "nose keeps pointing the same way",
             linear_motion(1, 0)),
        ]),
    ]

    for header_y, heading, side, first_top, cases in rows:
        fig.add(text(95, header_y, heading, font_size=15, font_weight="bold",
                     fill=P["ink"]))
        for i, (dx, dy, label, sub, motion) in enumerate(cases):
            cx = COLS[i % 2]
            top = first_top + (i // 2) * (PANEL_H + 14)
            fig.add(panel(cx, top, side, dx, dy, label, sub, motion))

    return fig


def build_nose_in() -> Figure:
    fig = Figure(900, 470,
                 "Figure 9: The same input, flying away and flying toward you",
                 "The aircraft always moves relative to its own nose, which is "
                 "why nose-in flight catches out new pilots.")

    for cx, heading, title, result in (
        (260, 0, "Nose pointing away from you",
         "The drone slides to YOUR right"),
        (640, 180, "Nose pointing back at you",
         "The drone slides to YOUR left"),
    ):
        fig.add(rect(cx - 165, 84, 330, 340, rx=12, fill=P["white"],
                     stroke="#dde3e9", stroke_width=1.5))
        fig.add(text(cx, 112, title, text_anchor="middle", font_weight="bold",
                     fill=P["ink"]))

        # the same stick input in both panels
        fig.add(translate(cx, 168, stick_pair("right", 1, 0, 22, 42)))
        fig.add(text(cx, 214, "right stick pushed right", text_anchor="middle",
                     font_size=12.5, fill=P["muted"]))

        # aircraft, rotated to face away or toward the pilot
        fig.add(translate(cx, 292, g(aircraft_mini_top(0.95),
                                     transform=f"rotate({heading})")))
        nose_y = 292 - 46 if heading == 0 else 292 + 46
        fig.add(text(cx - 62, nose_y + 4, "nose", text_anchor="middle",
                     font_size=11, font_style="italic", fill=P["muted"]))

        # ground-frame motion: right for nose-away, left for nose-toward
        direction = 1 if heading == 0 else -1
        fig.add(arrow(cx + direction * 52, 292, cx + direction * 118, 292,
                      width=3.5))
        fig.add(text(cx, 372, result, text_anchor="middle",
                     font_weight="bold", fill=P["bad"]))
        fig.add(text(cx, 398, "arrow shows movement over the ground",
                     text_anchor="middle", font_size=12.5, fill=P["muted"]))

    # pilot marker between the panels
    fig.add(text(450, 300, "you", text_anchor="middle", font_size=12,
                 fill=P["muted"]))
    fig.add(text(450, 322, "▲", text_anchor="middle", font_size=14,
                 fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, name in (
            (build_sticks, figure_name(1, 8, "stick_controls")),
            (build_nose_in, figure_name(1, 9, "nose_in"))):
        fname = os.path.join(args.out, name)
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
