"""Figure: a typical drone controller, labeled and numbered variants.

Usage:
    python fig_tools/fig_controller.py                # writes SVGs to review/
    python fig_tools/fig_controller.py --out docs/week_01/images
    python fig_tools/fig_controller.py --png          # also render PNGs for checking
    python fig_tools/fig_controller.py --screen builtin

Outputs:
    fig07_controller.svg            names on every callout (for the page)
    fig07b_controller_numbered.svg  number badges only (for the homework)
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import controller, shift  # noqa: E402
from svgkit import (Callouts, Figure, figure_name, render_png,  # noqa: E402
                    translate)

TITLE = "Figure 7: A typical drone controller"
SUBTITLE = ("Only the two sticks work the same on every controller. "
            "Buttons, switches, labels, and screens vary by model.")


def build(mode: str, screen: str) -> Figure:
    fig = Figure(900, 630, TITLE, SUBTITLE)

    # controller body origin, in figure coordinates
    ox, oy = 240, 330
    part, local = controller(screen=screen)
    a = shift(local, ox, oy)
    fig.add(translate(ox, oy, part))

    c = Callouts()
    # above the controller
    c.add("Gimbal tilt dial", (240, 110), "middle", (240, 118), a["gimbal_dial"], n=7)
    c.add("Shutter / record button", (660, 110), "middle", (660, 118), a["shutter"], n=8)
    if "screen" in a:
        label = ("Phone holder or built-in screen" if screen == "phone"
                 else "Built-in screen")
        c.add(label, (450, a["screen"][1] - 39), "middle",
              (450, a["screen"][1] - 33), a["screen"], n=10)
    # left side
    c.add("Antenna", (200, 245), "end", (205, 241), a["antenna_left"], n=9)
    c.add("Return-to-Home / pause", (200, 330), "end", (205, 326), a["rth"], n=5)
    c.add("Left stick", (200, 422), "end", (205, 418), a["left_stick"], n=1,
          sub="climb / descend, turn left / right", bold=True)
    # right side
    c.add("Antenna", (700, 245), "start", (695, 241), a["antenna_right"], n=9)
    c.add("Flight mode switch", (700, 330), "start", (695, 326), a["mode_switch"], n=6)
    c.add("Right stick", (700, 422), "start", (695, 418), a["right_stick"], n=2,
          sub="forward / back, slide left / right", bold=True)
    # below
    c.add("Power button", (380, 570), "end", (385, 563), a["power"], n=3)
    c.add("Battery level lights", (520, 570), "start", (515, 563), a["battery"], n=4)
    c.add("Charging / data port", (450, 610), "middle", (450, 595), a["port"], n=11)

    fig.add(c.leaders())
    fig.add(c.names() if mode == "names" else c.numbers())
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review", help="output folder")
    ap.add_argument("--screen", default="phone",
                    choices=["phone", "builtin", "none"])
    ap.add_argument("--png", action="store_true", help="also render PNGs")
    args = ap.parse_args()

    outputs = {
        "names": os.path.join(args.out, figure_name(1, 7, "controller")),
        "numbers": os.path.join(
            args.out, figure_name(1, 7, "controller_numbered", "b")),
    }
    for mode, fname in outputs.items():
        build(mode, args.screen).save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
