"""Figures for the "Common Flight Issues" page.

Numbering continues the week: Flight Basics ends at Figure 16, so this page
starts at 17.

Usage:
    python fig_tools/fig_issues.py --png
    python fig_tools/fig_issues.py --out docs/week_01/images

Outputs:
    w01_fig17_compass_siting.svg      where you calibrate, and what it costs
    w01_fig18_wind_and_height.svg     why descending helps when wind wins
    w01_fig19_antenna_orientation.svg which way the antennas must face
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import (aircraft_mini_side, aircraft_mini_top, car,  # noqa: E402
                   person)
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    path, polygon, rect, render_png, text, translate)

CARD = dict(rx=12, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)


def compass(cx, cy, r, needle_deg, needle_colour):
    """A compass rose. needle_deg is measured clockwise from true north."""
    grp = g(circle(cx, cy, r, fill=P["white"], stroke=P["line"],
                   stroke_width=2))
    for a in range(0, 360, 30):
        rad = math.radians(a - 90)
        inner = r - (10 if a % 90 == 0 else 6)
        grp.add(line(cx + inner * math.cos(rad), cy + inner * math.sin(rad),
                     cx + r * math.cos(rad), cy + r * math.sin(rad),
                     stroke="#b6c2cc", stroke_width=2))
    grp.add(text(cx, cy - r + 18, "N", text_anchor="middle", font_size=12,
                 font_weight="bold", fill=P["muted"]))
    rad = math.radians(needle_deg - 90)
    tip = (cx + (r - 14) * math.cos(rad), cy + (r - 14) * math.sin(rad))
    tail = (cx - (r - 26) * math.cos(rad), cy - (r - 26) * math.sin(rad))
    nx, ny = -math.sin(rad), math.cos(rad)
    grp.add(polygon([tip, (tail[0] + nx * 8, tail[1] + ny * 8),
                     (tail[0] - nx * 8, tail[1] - ny * 8)],
                    fill=needle_colour, stroke=P["line"], stroke_width=1))
    grp.add(circle(cx, cy, 4, fill=P["line"]))
    return grp


# ---------------------------------------------------------------------------
# Figure 17: where you calibrate the compass
# ---------------------------------------------------------------------------
def build_compass_siting() -> Figure:
    fig = Figure(900, 560,
                 "Figure 17: Where you calibrate the compass",
                 "The aircraft never knows its compass is wrong. It flies "
                 "confidently on bad information.")

    for cx, bad in ((250, True), (650, False)):
        top = 84
        fig.add(rect(cx - 190, top, 380, 434, **CARD))
        fig.add(text(cx, top + 32,
                     "Calibrated over metal" if bad else "Calibrated on open ground",
                     text_anchor="middle", font_size=15, font_weight="bold",
                     fill=P["bad"] if bad else P["ink"]))

        # compass, with the needle pulled off true in the bad case
        fig.add(compass(cx, top + 118, 56, 42 if bad else 0,
                        P["bad"] if bad else P["accent"]))
        fig.add(text(cx, top + 196,
                     "believes north is 40 degrees off" if bad
                     else "believes north correctly",
                     text_anchor="middle", font_size=12.5,
                     fill=P["bad"] if bad else P["muted"]))

        # the ground it is standing on
        gy = top + 300
        fig.add(line(cx - 150, gy, cx + 150, gy, stroke="#9aa7b2",
                     stroke_width=3, stroke_linecap="round"))
        if bad:
            fig.add(rect(cx - 150, gy, 300, 30, fill="#d8d2c4"))
            grid = g(stroke="#9a8f78", stroke_width=2)
            for i in range(9):
                grid.add(line(cx - 142 + i * 36, gy + 4, cx - 142 + i * 36, gy + 26))
            for j in range(2):
                grid.add(line(cx - 148, gy + 9 + j * 11, cx + 148, gy + 9 + j * 11))
            fig.add(grid)
            fig.add(text(cx, gy + 48, "slab with rebar, vehicles, steel decking",
                         text_anchor="middle", font_size=11.5, fill=P["muted"]))
            fig.add(car(cx + 96, gy - 18, 0.62))
        else:
            fig.add(rect(cx - 150, gy, 300, 30, fill="#e4ead9"))
            tufts = g(stroke="#8aa06e", stroke_width=2, stroke_linecap="round")
            for i in range(13):
                x = cx - 140 + i * 24
                tufts.add(line(x, gy - 1, x - 4, gy - 9))
                tufts.add(line(x, gy - 1, x + 4, gy - 9))
            fig.add(tufts)
            fig.add(text(cx, gy + 48, "open ground, clear of metal",
                         text_anchor="middle", font_size=11.5, fill=P["muted"]))

        fig.add(translate(cx - 70, gy - 16, aircraft_mini_side(0.62, nose=False)))

        # what happens next
        fig.add(text(cx, top + 400,
                     "flies off in the wrong direction" if bad
                     else "goes where you send it",
                     text_anchor="middle", font_size=13.5, font_weight="bold",
                     fill=P["bad"] if bad else "#2f8f4e"))

    fig.add(text(450, 540,
                 "Return to Home uses the same compass, so a bad calibration "
                 "sends the aircraft away rather than back.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Figure 18: antenna orientation
# ---------------------------------------------------------------------------
def wedge(cx, cy, r, a0, a1, **attrs):
    """A pie slice from (cx, cy), angles in screen degrees (-90 is straight up)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return path(f"M{cx},{cy} L{x0:.1f},{y0:.1f} "
                f"A{r},{r} 0 0,1 {x1:.1f},{y1:.1f} Z", **attrs)


def antenna_panel(fig, cx, top, good):
    """One panel. The aircraft sits up and to the right in both, at -45 degrees;
    only the antenna orientation changes.

    An antenna radiates from its broad face and is deaf along its own axis. So
    the good case lays the antennas across the line to the aircraft, and the bad
    case points them straight at it.
    """
    fig.add(rect(cx - 190, top, 380, 372, **CARD))
    fig.add(text(cx, top + 32,
                 "Antennas across the line to the aircraft" if good
                 else "Antennas pointed at the aircraft",
                 text_anchor="middle", font_size=14.5, font_weight="bold",
                 fill="#2f8f4e" if good else P["bad"]))

    base_y = top + 300
    apex = (cx, base_y - 34)
    drone = (apex[0] + 99, apex[1] - 99)

    if good:
        fig.add(wedge(apex[0], apex[1], 175, -75, -15, fill="#cfe3f7",
                      stroke=P["accent"], stroke_width=1.5))
        fig.add(text(cx + 128, top + 108, "strong", text_anchor="middle",
                     font_size=12, font_weight="bold", fill=P["accent"]))
    else:
        fig.add(wedge(apex[0], apex[1], 175, -58, -32, fill="#fbe0dc",
                      stroke="#e8b4ac", stroke_width=1.5, stroke_dasharray="6 5"))
        fig.add(text(cx + 150, top + 118, "weak spot", text_anchor="middle",
                     font_size=12, font_weight="bold", fill=P["bad"]))

    # controller, with the antennas laid across the line to the drone or along it
    fig.add(rect(cx - 46, base_y - 34, 92, 40, rx=12, fill=P["body"],
                 stroke=P["line"], stroke_width=2))
    for offset, ang in zip((-26, 26), (-52, -38) if good else (38, 52)):
        fig.add(g(rect(-5, -50, 10, 50, rx=3, fill=P["dark"],
                       stroke=P["line"], stroke_width=1.2),
                  transform=f"translate({cx + offset},{base_y - 34}) rotate({ang})"))

    fig.add(translate(*drone, aircraft_mini_top(0.62)))
    fig.add(text(drone[0], drone[1] - 38, "aircraft", text_anchor="middle",
                 font_size=11.5, fill=P["muted"]))

    bars = 4 if good else 1
    for i in range(4):
        h = 8 + i * 6
        fig.add(rect(cx - 156 + i * 14, base_y - 12 - h, 10, h, rx=2,
                     fill=("#2f8f4e" if good else P["bad"]) if i < bars
                     else "#dde3e9"))

    fig.add(text(cx, top + 340,
                 "strong link, full range" if good
                 else "weak link, the aircraft may drop out",
                 text_anchor="middle", font_size=13, font_weight="bold",
                 fill="#2f8f4e" if good else P["bad"]))


def build_antenna_orientation() -> Figure:
    fig = Figure(900, 540,
                 "Figure 19: Which way the antennas must face",
                 "An antenna radiates from its broad face, not its tip. "
                 "Pointing the tips at the drone aims the weakest part at it.")
    antenna_panel(fig, 250, 84, True)
    antenna_panel(fig, 650, 84, False)
    fig.add(text(450, 508,
                 "Turn so the antennas lie across your line to the aircraft. "
                 "Do not aim them at it like a remote control.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
# Figure 19: wind against height
# ---------------------------------------------------------------------------
def build_wind_and_height() -> Figure:
    fig = Figure(900, 500,
                 "Figure 18: Why descending helps when the wind wins",
                 "Wind is stronger with height. Losing altitude buys back the "
                 "speed you need to get home.")

    ground_y = 396
    fig.add(rect(40, 84, 820, ground_y - 84, rx=10, fill="#e8f2fb",
                 stroke="#cfe0ee", stroke_width=1.5))
    fig.add(rect(40, ground_y, 820, 18, fill="#e4ead9"))
    fig.add(line(40, ground_y, 860, ground_y, stroke="#9aa7b2",
                 stroke_width=3, stroke_linecap="round"))

    # buildings, which set the "rooftop level" the text refers to
    for bx, bw, bh in ((150, 78, 96), (240, 58, 70), (310, 66, 84)):
        fig.add(rect(bx, ground_y - bh, bw, bh, fill="#c2cad2",
                     stroke=P["line"], stroke_width=1.5))
    roof_y = ground_y - 96
    fig.add(line(60, roof_y, 840, roof_y, stroke="#9aa7b2", stroke_width=1.5,
                 stroke_dasharray="7 6"))
    fig.add(text(840, roof_y - 8, "rooftop level", text_anchor="end",
                 font_size=12, fill=P["muted"]))

    # wind, stronger the higher you go
    for wy, length in ((132, 150), (196, 112), (252, 78), (330, 44)):
        fig.add(arrow(415, wy, 415 + length, wy, color="#8fa3b5", width=3))
    fig.add(text(400, 118, "wind", text_anchor="end", font_size=13,
                 font_weight="bold", fill=P["muted"]))
    fig.add(text(400, 138, "stronger", text_anchor="end", font_size=11.5,
                 fill=P["muted"]))
    fig.add(text(400, 336, "lighter", text_anchor="end", font_size=11.5,
                 fill=P["muted"]))

    # high: fighting the wind and losing
    fig.add(translate(700, 150, aircraft_mini_side(0.72, nose=False)))
    fig.add(arrow(672, 150, 618, 150, color=P["bad"], width=3))
    fig.add(text(700, 108, "no progress into wind", text_anchor="middle",
                 font_size=12.5, font_weight="bold", fill=P["bad"]))

    # descend
    fig.add(arrow(760, 178, 760, 306, width=3))
    fig.add(text(788, 246, "descend", font_size=12.5, font_weight="bold",
                 fill=P["accent"]))

    # low: making headway home
    fig.add(translate(700, 336, aircraft_mini_side(0.72, nose=False)))
    fig.add(arrow(662, 336, 520, 336, width=3))
    fig.add(text(600, 316, "makes headway home", text_anchor="middle",
                 font_size=12.5, font_weight="bold", fill="#2f8f4e"))

    fig.add(person(96, ground_y, 1.3))
    fig.add(text(96, ground_y + 34, "you", text_anchor="middle", font_size=12.5,
                 fill=P["muted"]))

    fig.add(text(450, 476,
                 "Turn back while there is battery to fly into the wind, not "
                 "after the warning.",
                 text_anchor="middle", font_size=13, font_style="italic",
                 fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, number, slug in (
        (build_compass_siting, 17, "compass_siting"),
        (build_wind_and_height, 18, "wind_and_height"),
        (build_antenna_orientation, 19, "antenna_orientation"),
    ):
        fname = os.path.join(args.out, figure_name(1, number, slug))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
