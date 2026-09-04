"""Figure: parts of a quadcopter, top view, labeled and numbered variants.

Usage:
    python fig_tools/fig_aircraft.py --png
    python fig_tools/fig_aircraft.py --out docs/week_01/images

Outputs:
    fig01_aircraft_parts.svg              names on every callout (for the page)
    fig01b_aircraft_parts_numbered.svg    number badges only (for homework)
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_top, shift  # noqa: E402
from svgkit import (Callouts, Figure, figure_name, render_png,  # noqa: E402
                    translate)

TITLE = "Figure 1: Parts of a quadcopter"
SUBTITLE = ("Layout varies by model. Lighter aircraft often have fewer sensors, "
            "and some have no gimbal at all.")


def build(mode: str) -> Figure:
    fig = Figure(900, 620, TITLE, SUBTITLE)

    ox, oy = 450, 340
    part, local = aircraft_top()
    a = shift(local, ox, oy)
    fig.add(translate(ox, oy, part))

    c = Callouts()
    # top
    c.add("Camera and gimbal", (450, 112), "middle", (450, 120), a["camera"], n=1)
    # left
    c.add("Propellers", (185, 200), "end", (190, 196), a["propeller"], n=2,
          sub="opposite corners match")
    c.add("Motors", (185, 295), "end", (190, 291), a["motor"], n=3)
    c.add("Arms", (185, 390), "end", (190, 386), a["arm"], n=4,
          sub="fold in for transport")
    # right
    c.add("Obstacle sensors", (715, 200), "start", (710, 196), a["sensors"], n=5)
    c.add("Satellite receiver", (715, 305), "start", (710, 301), a["gnss"], n=6,
          sub="and compass, inside the body")
    c.add("Battery", (715, 400), "start", (710, 396), a["battery"], n=7)
    # bottom, approached from opposite sides so the leaders stay apart
    c.add("Status light", (330, 570), "middle", (345, 558), a["status_light"], n=8)
    c.add("Landing feet", (580, 570), "middle", (565, 558), a["feet"], n=9)

    fig.add(c.leaders())
    fig.add(c.names() if mode == "names" else c.numbers())
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review", help="output folder")
    ap.add_argument("--png", action="store_true", help="also render PNGs")
    args = ap.parse_args()

    for mode, name in (
            ("names", figure_name(1, 1, "aircraft_parts")),
            ("numbers", figure_name(1, 1, "aircraft_parts_numbered", "b"))):
        fname = os.path.join(args.out, name)
        build(mode).save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
