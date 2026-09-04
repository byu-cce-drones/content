"""Figure: the sensors a drone can carry.

Usage:
    python fig_tools/fig_payloads.py --png
    python fig_tools/fig_payloads.py --out docs/week_01/images

Outputs:
    fig03_payloads.svg   one card per payload type
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, circle, figure_name, g, line, path,  # noqa: E402
                    rect, render_png, text, translate)

CARD_W, CARD_H = 160, 208
COLS = (100, 275, 450, 625, 800)


def camera_body(lens_fill=None):
    """Shared camera housing, so every camera-shaped payload matches."""
    grp = g(rect(-10, -30, 20, 8, rx=3, fill=P["dark"]),
            rect(-30, -22, 60, 42, rx=7, fill="#5a6570", stroke=P["line"],
                 stroke_width=1.5))
    if lens_fill:
        grp.add(circle(0, 0, 15, fill=P["line"]))
        grp.add(circle(0, 0, 11, fill=lens_fill))
    return grp


def icon_camera():
    grp = camera_body("#2b3a47")
    grp.add(circle(0, 0, 5, fill=P["screen"]))
    grp.add(circle(-4, -4, 2.5, fill=P["white"]))
    return grp


def icon_thermal():
    grp = camera_body("#c0392b")
    grp.add(circle(0, 0, 7.5, fill="#e67e22"))
    grp.add(circle(0, 0, 4, fill="#f4d03f"))
    return grp


def icon_multispectral():
    grp = camera_body(None)
    bands = (("#c0392b", -17, -6), ("#7b241c", 0, -6), ("#27ae60", 17, -6),
             ("#2980b9", -9, 11), ("#7f8c8d", 9, 11))
    for fill, x, y in bands:
        grp.add(circle(x, y, 6.5, fill=fill, stroke=P["line"],
                       stroke_width=1.2))
    return grp


def icon_lidar():
    grp = g(rect(-19, -28, 38, 18, rx=5, fill="#5a6570", stroke=P["line"],
                 stroke_width=1.5))
    grp.add(circle(0, -19, 5, fill="#2b3a47"))
    for dx, dy in ((-27, 18), (-14, 23), (0, 25), (14, 23), (27, 18)):
        grp.add(line(0, -10, dx, dy, stroke=P["accent"], stroke_width=2,
                     stroke_dasharray="3 3"))
        grp.add(circle(dx, dy, 2.6, fill=P["accent"]))
    grp.add(line(-32, 28, 32, 28, stroke=P["muted"], stroke_width=2.5,
                 stroke_linecap="round"))
    return grp


def icon_gas():
    grp = g(rect(-19, -4, 38, 26, rx=5, fill="#5a6570", stroke=P["line"],
                 stroke_width=1.5))
    for y in (4, 10, 16):
        grp.add(line(-11, y, 11, y, stroke="#98a4b0", stroke_width=2,
                     stroke_linecap="round"))
    for x in (-11, 0, 11):
        grp.add(path(f"M{x},-8 q6,-7 0,-14 q-6,-7 0,-11", fill="none",
                     stroke=P["accent"], stroke_width=2,
                     stroke_linecap="round"))
    return grp


PAYLOADS = (
    (icon_camera, "Standard camera", ("color photos and video,", "what your eye sees")),
    (icon_thermal, "Thermal", ("surface temperature,", "shown as an image")),
    (icon_multispectral, "Multispectral", ("light beyond visible,", "such as near infrared")),
    (icon_lidar, "LiDAR", ("distance, by timing", "laser pulses")),
    (icon_gas, "Gas detector", ("methane, CO and other", "gases in the air")),
)


def build() -> Figure:
    fig = Figure(900, 310,
                 "Figure 3: What a drone can carry",
                 "Most small drones have one fixed camera. Larger aircraft take "
                 "interchangeable payloads, so one airframe serves many jobs.")

    top = 70
    for cx, (icon, name, lines) in zip(COLS, PAYLOADS):
        fig.add(rect(cx - CARD_W / 2, top, CARD_W, CARD_H, rx=10,
                     fill=P["white"], stroke="#dde3e9", stroke_width=1.5))
        fig.add(translate(cx, top + 62, icon()))
        fig.add(text(cx, top + 128, name, text_anchor="middle", font_size=15,
                     font_weight="bold", fill=P["ink"]))
        for i, ln in enumerate(lines):
            fig.add(text(cx, top + 156 + i * 17, ln, text_anchor="middle",
                         font_size=12, fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    fname = os.path.join(args.out, figure_name(1, 3, "payloads"))
    build().save(fname)
    print("wrote", fname)
    if args.png:
        png = render_png(fname)
        if png:
            print("wrote", png)


if __name__ == "__main__":
    main()
