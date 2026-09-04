"""Proposed figures for the Topic 6 thermal page.

The page currently has three photographs and no diagrams, so the three things
students actually get wrong are all explained in prose: what the camera is
reading, why a shiny surface lies to it, and when to fly.

Usage:
    python fig_tools/fig_thermal.py --png
    python fig_tools/fig_thermal.py --out docs/week_06/images
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_side  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line, path,  # noqa: E402
                    polygon, rect, render_png, text, translate)

CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)
HOT, WARM, COOL, COLD = "#d94f38", "#e8a33d", "#6f9bc4", "#3d5a80"


def swatch_ramp(x, y, w, h):
    """The palette bar every thermal image is read against."""
    stops = ("#2b2d5e", "#3d5a80", "#6f9bc4", "#e8a33d", "#d94f38", "#f7e8b0")
    grp = g()
    for i, c in enumerate(stops):
        grp.add(rect(x + i * w / len(stops), y, w / len(stops) + 0.5, h, fill=c))
    grp.add(rect(x, y, w, h, fill="none", stroke=P["line"], stroke_width=1))
    grp.add(text(x, y + h + 13, "cold", font_size=10, fill=P["muted"]))
    grp.add(text(x + w, y + h + 13, "hot", text_anchor="end", font_size=10,
                 fill=P["muted"]))
    return grp


# ---------------------------------------------------------------------------
# Figure A: the camera reads a surface, nothing more
# ---------------------------------------------------------------------------
def build_what_it_sees() -> Figure:
    fig = Figure(900, 450, "What a thermal camera is actually reading",
                 "It measures the temperature of the surface facing it. "
                 "Anything hidden shows up only if it warms that surface.")

    fig.add(rect(30, 84, 520, 330, **CARD))
    fig.add(text(290, 114, "A warm pipe behind a wall", text_anchor="middle",
                 font_size=15, font_weight="bold", fill=P["ink"]))

    wx, wy, wh = 360, 150, 210
    fig.add(rect(wx, wy, 46, wh, fill="#cbd3da", stroke=P["line"],
                 stroke_width=1.5))
    fig.add(text(wx + 23, wy - 12, "wall", text_anchor="middle", font_size=11,
                 fill=P["muted"]))
    fig.add(circle(wx + 74, wy + 106, 16, fill=HOT, stroke=P["line"],
                   stroke_width=1.5))
    fig.add(text(wx + 96, wy + 110, "hot pipe", font_size=11, fill=P["muted"]))

    # heat conducting through to the near face
    for i, (dy, col) in enumerate(((-30, WARM), (0, HOT), (30, WARM))):
        fig.add(arrow(wx + 58, wy + 106 + dy, wx + 50, wy + 106 + dy,
                      color=col, width=2.5, head=7))
    for i in range(14):
        t = abs(i - 6.5) / 6.5
        fig.add(rect(wx - 7, wy + 40 + i * 9, 7, 9,
                     fill=HOT if t < 0.28 else (WARM if t < 0.62 else COOL)))
    fig.add(text(wx - 12, wy + 30, "the surface the camera sees",
                 text_anchor="end", font_size=11, fill=P["ink"]))

    fig.add(translate(150, 196, aircraft_mini_side(0.62, nose=False)))
    fig.add(arrow(196, 214, wx - 22, wy + 100, color=P["muted"], width=2,
                  head=8, ))
    fig.add(swatch_ramp(96, 340, 160, 14))
    fig.add(text(290, 392, "The pipe is invisible. The warm stripe it leaves on the",
                 text_anchor="middle", font_size=11.5, fill=P["muted"]))
    fig.add(text(290, 408, "wall face is not.", text_anchor="middle",
                 font_size=11.5, fill=P["muted"]))

    fig.add(rect(570, 84, 300, 330, **CARD))
    fig.add(text(720, 114, "What it cannot do", text_anchor="middle",
                 font_size=15, font_weight="bold", fill=P["ink"]))
    for i, (claim, why) in enumerate((
        ("See through a wall", "it reads the wall's face"),
        ("See through glass", "glass is a mirror at these wavelengths"),
        ("See under water", "the surface is all it gets"),
        ("Trust a shiny surface", "polished metal reflects, see below"),
    )):
        y = 164 + i * 62
        fig.add(circle(602, y - 4, 11, fill="none", stroke=P["bad"],
                       stroke_width=2.5))
        fig.add(g(line(596, y - 10, 608, y + 2), line(608, y - 10, 596, y + 2),
                  stroke=P["bad"], stroke_width=2.5, stroke_linecap="round"))
        fig.add(text(622, y, claim, font_size=12.5, font_weight="bold",
                     fill=P["ink"]))
        fig.add(text(622, y + 17, why, font_size=11, fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Figure B: emissivity, and the false hotspot
# ---------------------------------------------------------------------------
def build_emissivity() -> Figure:
    fig = Figure(900, 470, "Why a thermal image can lie to you",
                 "The camera measures radiation and converts it to a "
                 "temperature. How well a surface radiates changes the answer.")

    # same temperature, two readings
    fig.add(rect(30, 84, 400, 340, **CARD))
    fig.add(text(230, 114, "Same temperature, two readings",
                 text_anchor="middle", font_size=15, font_weight="bold",
                 fill=P["ink"]))
    plate_y = 300
    fig.add(rect(90, plate_y, 280, 22, fill=HOT, stroke=P["line"],
                 stroke_width=1.5))
    fig.add(text(230, plate_y + 40, "one hot plate, both blocks at 40 °C",
                 text_anchor="middle", font_size=11.5, fill=P["muted"]))
    for cx, label, sub, col, reading, emis in (
        (160, "Painted concrete", "rough, dull", "#b9b0a4", "40 °C", "0.95"),
        (300, "Polished metal", "shiny", "#c9d2da", "22 °C", "0.10"),
    ):
        fig.add(rect(cx - 44, plate_y - 76, 88, 76, fill=col,
                     stroke=P["line"], stroke_width=1.5))
        fig.add(text(cx, plate_y - 88, label, text_anchor="middle",
                     font_size=11.5, font_weight="bold", fill=P["ink"]))
        fig.add(text(cx, plate_y - 74, sub, text_anchor="middle",
                     font_size=10.5, fill=P["muted"]))
        good = reading == "40 °C"
        fig.add(rect(cx - 40, plate_y - 60, 80, 30, rx=5, fill=P["white"],
                     stroke=P["ink"], stroke_width=1.5))
        fig.add(text(cx, plate_y - 39, reading, text_anchor="middle",
                     font_size=15, font_weight="bold",
                     fill=HOT if good else COLD))
        fig.add(text(cx, plate_y - 8, f"emissivity {emis}", text_anchor="middle",
                     font_size=10.5, fill=P["muted"]))
    fig.add(text(230, 396, "The metal is exactly as hot. It just radiates badly,",
                 text_anchor="middle", font_size=11.5, fill=P["muted"]))
    fig.add(text(230, 412, "so the camera reads it far too cold.",
                 text_anchor="middle", font_size=11.5, fill=P["muted"]))

    # reflection, the other direction
    fig.add(rect(460, 84, 410, 340, **CARD))
    fig.add(text(665, 114, "A hotspot that is not hot", text_anchor="middle",
                 font_size=15, font_weight="bold", fill=P["ink"]))
    fig.add(circle(790, 168, 22, fill="#f4d03f", stroke="#d4b02f",
                   stroke_width=2))
    fig.add(text(790, 204, "sun", text_anchor="middle", font_size=11,
                 fill=P["muted"]))
    roof = ((520, 300), (700, 254))
    fig.add(polygon([(520, 300), (700, 254), (700, 276), (520, 322)],
                    fill="#c9d2da", stroke=P["line"], stroke_width=1.5))
    fig.add(text(560, 344, "bare metal roof", font_size=11.5, fill=P["muted"]))
    fig.add(arrow(772, 186, 664, 258, color="#d4b02f", width=2.5, head=8))
    fig.add(arrow(648, 262, 552, 196, color=HOT, width=2.5, head=8))
    fig.add(translate(510, 176, aircraft_mini_side(0.56, nose=False)))
    fig.add(polygon([(616, 275), (652, 266), (652, 279), (616, 288)],
                    fill=HOT, stroke=P["line"], stroke_width=1))
    fig.add(text(665, 388, "The camera sees reflected sky and sun, not the roof.",
                 text_anchor="middle", font_size=11.5, fill=P["muted"]))
    fig.add(text(665, 404, "Check every hotspot against the ordinary photo.",
                 text_anchor="middle", font_size=11.5, fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Figure C: when to fly
# ---------------------------------------------------------------------------
def build_timing() -> Figure:
    fig = Figure(900, 500, "When to fly a thermal survey",
                 "Thermal contrast comes from things heating and cooling at "
                 "different rates. Fly when that difference is largest.")

    x0, x1, ybase, yamp = 96, 838, 356, 122

    def tod(h):
        return x0 + (x1 - x0) * h / 24

    def temp(h):
        # coolest around 03:00, warmest around 15:00, and never flat
        return ybase - yamp * (0.5 + 0.5 * math.cos((h - 15) * 2 * math.pi / 24))

    # the windows worth flying, and the ones that waste a battery
    for h0, h1, col, label, sub in (
        (11.5, 16.0, "#fbe0dc", "avoid for roofs", "full solar load"),
        (9.0, 11.0, "#dff0d8", "bridge decks", "about 4 h after sunrise"),
        (19.5, 22.0, "#dff0d8", "roof moisture", "1 to 2 h after sunset"),
    ):
        fig.add(rect(tod(h0), 132, tod(h1) - tod(h0), ybase - 132, fill=col))

    fig.add(line(x0, ybase, x1, ybase, stroke=P["muted"], stroke_width=2))
    fig.add(path("M" + " L".join(f"{tod(h/4):.0f},{temp(h/4):.0f}"
                                 for h in range(97)),
                 fill="none", stroke=HOT, stroke_width=3))

    for h, lbl in ((6.5, "sunrise"), (18.5, "sunset")):
        fig.add(line(tod(h), 132, tod(h), ybase + 8, stroke=P["muted"],
                     stroke_width=1.5, stroke_dasharray="5 4"))
        fig.add(text(tod(h), 124, lbl, text_anchor="middle", font_size=11,
                     fill=P["muted"]))
    for h in (0, 6, 12, 18, 24):
        fig.add(text(tod(h), ybase + 24, f"{h:02d}:00", text_anchor="middle",
                     font_size=11, fill=P["muted"]))
    fig.add(g(text(0, 0, "surface temperature", text_anchor="middle",
                   font_size=12, fill=P["muted"]),
              transform=f"translate({x0 - 26},{(132 + ybase) / 2}) rotate(-90)"))

    for h0, h1, col, label, sub in (
        (11.5, 16.0, None, "avoid for roofs", "full solar load"),
        (9.0, 11.0, None, "bridge decks", "about 4 h after sunrise"),
        (19.5, 22.0, None, "roof moisture", "1 to 2 h after sunset"),
    ):
        mid = (tod(h0) + tod(h1)) / 2
        top = 152 if label != "avoid for roofs" else 186
        fig.add(text(mid, top, label, text_anchor="middle", font_size=12,
                     font_weight="bold",
                     fill=P["bad"] if label == "avoid for roofs" else "#2f8f4e"))
        fig.add(text(mid, top + 15, sub, text_anchor="middle", font_size=10.5,
                     fill=P["muted"]))

    for h in (6.5, 18.5):
        fig.add(circle(tod(h), temp(h), 6, fill=P["white"], stroke=P["ink"],
                       stroke_width=2))
    for i, ln in enumerate(("thermal crossover:", "everything passes through",
                            "the same temperature, so", "there is nothing to see")):
        fig.add(text(tod(18.5) - 12, temp(18.5) + 26 + i * 14, ln,
                     text_anchor="end", font_size=10.5, fill=P["bad"]))

    fig.add(text(450, 420,
                 "Wet insulation holds heat, so it glows after sunset. A "
                 "delaminated bridge deck heats faster than sound concrete, so "
                 "it shows in the morning.",
                 text_anchor="middle", font_size=12.5, fill=P["muted"]))
    fig.add(text(450, 452,
                 "Near sunrise and sunset everything passes through the same "
                 "temperature. Fly then and you will see nothing at all.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    fig.add(text(450, 476,
                 "Wait at least 24 hours after rain, and skip the survey if it "
                 "is windy.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()
    for builder, number, slug in ((build_what_it_sees, 4, "thermal_what_it_sees"),
                                  (build_emissivity, 5, "thermal_emissivity"),
                                  (build_timing, 6, "thermal_timing")):
        fname = os.path.join(args.out, figure_name(6, number, slug))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
