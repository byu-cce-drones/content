"""Diagrams for the Thermal Imaging reading (Week 8).

The page's photographs show results; these four show the mechanisms behind the
things students get wrong: what the camera is reading, whether the file it
saved is a measurement at all, why a shiny surface lies to it, and when to fly.

    w06_fig04_thermal_what_it_sees.svg     the camera reads a surface, nothing more
    w06_fig04b_radiometric_vs_jpg.svg      a radiometric file vs. a colour JPG
    w06_fig05_thermal_emissivity.svg       emissivity, and the false hotspot
    w06_fig06_thermal_timing.svg           when to fly

The w06_ set is one sequence across the three sensor readings (LiDAR, Thermal,
Multispectral). 4b is a lettered variant that sits beside Figure 4, so adding
it moved no number.

Usage:
    python fig_tools/fig_thermal.py --png
    python fig_tools/fig_thermal.py --out docs/gen_reading/images
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
# Figure A-b: a radiometric file vs. a colour JPG
# ---------------------------------------------------------------------------
RAMP = ("#2b2d5e", "#3d5a80", "#6f9bc4", "#e8a33d", "#d94f38", "#f7e8b0")

# one small pavement patch with a warm spot, in degrees C, read left to right
SCENE = (
    (18.4, 18.6, 18.9, 19.1, 18.5),
    (18.3, 19.8, 23.6, 24.1, 18.8),
    (18.6, 20.4, 24.9, 23.2, 18.7),
    (18.2, 18.5, 19.3, 18.9, 18.4),
)
BAR_1 = (15.0, 30.0)   # the colour bar the camera picked for this frame
BAR_2 = (5.0, 45.0)    # the bar it picks once something hotter enters the next


def ramp_colour(t: float) -> str:
    """Interpolate the thermal palette at t in [0, 1]."""
    t = min(max(t, 0.0), 1.0) * (len(RAMP) - 1)
    i = min(int(t), len(RAMP) - 2)
    f = t - i
    a = [int(RAMP[i][k:k + 2], 16) for k in (1, 3, 5)]
    b = [int(RAMP[i + 1][k:k + 2], 16) for k in (1, 3, 5)]
    return "#" + "".join(f"{round(a[k] + (b[k] - a[k]) * f):02x}"
                         for k in range(3))


def _scaled(temp: float, bar) -> float:
    return (temp - bar[0]) / (bar[1] - bar[0])


def pixel_grid(x, y, cell, bar, labels: bool):
    """The scene as a block of pixels, coloured against one bar."""
    grp = g()
    for r, row in enumerate(SCENE):
        for c, temp in enumerate(row):
            t = _scaled(temp, bar)
            px, py = x + c * cell, y + r * cell
            grp.add(rect(px, py, cell, cell, fill=ramp_colour(t),
                         stroke=P["white"], stroke_width=1.5))
            if labels:
                grp.add(text(px + cell / 2, py + cell / 2 + 5, f"{temp:.1f}",
                             text_anchor="middle", font_size=13.5,
                             font_weight="bold",
                             fill=P["white"] if t < 0.5 else P["ink"]))
    w, h = cell * len(SCENE[0]), cell * len(SCENE)
    grp.add(rect(x, y, w, h, fill="none", stroke=P["line"], stroke_width=1.5))
    return grp


def colour_bar(x, y, w, h, bar, marker: float | None = None, label=""):
    """A colour bar with its end temperatures and an optional marked value."""
    grp = g()
    n = 48
    for i in range(n):
        grp.add(rect(x + i * w / n, y, w / n + 0.6, h, fill=ramp_colour(i / (n - 1))))
    grp.add(rect(x, y, w, h, fill="none", stroke=P["line"], stroke_width=1))
    grp.add(text(x, y + h + 14, f"{bar[0]:.0f} °C", font_size=11,
                 fill=P["muted"]))
    grp.add(text(x + w, y + h + 14, f"{bar[1]:.0f} °C", text_anchor="end",
                 font_size=11, fill=P["muted"]))
    if marker is not None:
        mx = x + w * _scaled(marker, bar)
        grp.add(polygon([(mx, y - 2), (mx - 6, y - 11), (mx + 6, y - 11)],
                        fill=P["ink"]))
        grp.add(text(mx, y - 15, label or f"{marker:.0f} °C",
                     text_anchor="middle", font_size=11.5, font_weight="bold",
                     fill=P["ink"]))
    return grp


def build_radiometric_vs_jpg() -> Figure:
    fig = Figure(900, 548, "A picture or a measurement?",
                 "The same thermal scene saved two ways. The pixels look alike; "
                 "only one file still knows how hot anything was.")

    cell = 50
    gw, gh = cell * 5, cell * 4          # 250 x 200
    top = 136
    warm_rc = (2, 2)                      # the hottest pixel, row and column

    def ring(gx):
        r, c = warm_rc
        return rect(gx + c * cell + 2, top + r * cell + 2, cell - 4, cell - 4,
                    fill="none", stroke=P["ink"], stroke_width=2.5)

    # --- left: the radiometric file -------------------------------------
    lx = 30
    fig.add(rect(lx, 72, 410, 414, **CARD))
    fig.add(text(lx + 205, 100, "Radiometric file (TIFF / R-JPEG)",
                 text_anchor="middle", font_size=15, font_weight="bold",
                 fill=P["ink"]))
    fig.add(text(lx + 205, 119, "every pixel holds a temperature, in °C",
                 text_anchor="middle", font_size=12, fill=P["muted"]))
    gx = lx + (410 - gw) / 2
    fig.add(pixel_grid(gx, top, cell, BAR_1, labels=True))
    fig.add(ring(gx))
    fig.add(text(lx + 205, 362, "24.9 °C is a number: read it, compare it, keep it.",
                 text_anchor="middle", font_size=12.5, fill=P["ink"]))
    fig.add(text(lx + 205, 396, "The colour is only a display choice. Change the",
                 text_anchor="middle", font_size=12, fill=P["muted"]))
    fig.add(text(lx + 205, 413, "palette or the bar and the numbers do not move.",
                 text_anchor="middle", font_size=12, fill=P["muted"]))
    fig.add(text(lx + 205, 456, "Warm spot: 24.9 − 18.4 = 6.5 °C above the pavement.",
                 text_anchor="middle", font_size=12.5, font_weight="bold",
                 fill=P["ink"]))

    # --- right: the colour JPG ------------------------------------------
    rx = 460
    fig.add(rect(rx, 72, 410, 414, **CARD))
    fig.add(text(rx + 205, 100, "Colour JPG", text_anchor="middle",
                 font_size=15, font_weight="bold", fill=P["ink"]))
    fig.add(text(rx + 205, 119, "every pixel holds a colour; the bar is "
                 "rescaled every frame",
                 text_anchor="middle", font_size=12, fill=P["muted"]))
    gx2 = rx + (410 - gw) / 2
    fig.add(pixel_grid(gx2, top, cell, BAR_1, labels=False))
    fig.add(ring(gx2))
    fig.add(text(rx + 205, 360, "The same pixel is orange. How hot is orange?",
                 text_anchor="middle", font_size=12.5, fill=P["ink"]))

    # two frames, two bars, one orange
    t_warm = _scaled(SCENE[warm_rc[0]][warm_rc[1]], BAR_1)
    orange = ramp_colour(t_warm)
    by, bw = 420, 150
    for bar, bx, head in ((BAR_1, rx + 32, "this frame"),
                          (BAR_2, rx + 228, "next frame")):
        temp = bar[0] + t_warm * (bar[1] - bar[0])
        fig.add(text(bx + bw / 2, by - 30, head, text_anchor="middle",
                     font_size=12, font_weight="bold", fill=P["ink"]))
        fig.add(colour_bar(bx, by, bw, 12, bar, marker=temp,
                           label=f"{temp:.0f} °C"))
    fig.add(rect(rx + 192, by - 3, 26, 18, fill=orange, stroke=P["line"],
                 stroke_width=1))
    fig.add(text(rx + 205, by - 26, "same", text_anchor="middle", font_size=10.5,
                 fill=P["muted"]))
    fig.add(text(rx + 205, by - 14, "colour", text_anchor="middle", font_size=10.5,
                 fill=P["muted"]))
    fig.add(text(rx + 205, 460, "Something hotter enters the next frame, the bar",
                 text_anchor="middle", font_size=12, fill=P["muted"]))
    fig.add(text(rx + 205, 476, "stretches, and the same orange now means 31 °C.",
                 text_anchor="middle", font_size=12, fill=P["muted"]))

    fig.add(text(450, 518, "You can measure, compare and mosaic only the left one. "
                 "Check the save format before takeoff.",
                 text_anchor="middle", font_size=13.5, font_weight="bold",
                 fill=P["ink"]))
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
    # (builder, number, variant, slug): a lettered variant sits beside the
    # figure it extends without moving any number after it
    for builder, number, variant, slug in (
        (build_what_it_sees, 4, "", "thermal_what_it_sees"),
        (build_radiometric_vs_jpg, 4, "b", "radiometric_vs_jpg"),
        (build_emissivity, 5, "", "thermal_emissivity"),
        (build_timing, 6, "", "thermal_timing"),
    ):
        fname = os.path.join(args.out, figure_name(6, number, slug, variant))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
