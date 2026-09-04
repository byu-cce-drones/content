"""Figures for the "How a Drone Flies" section.

Usage:
    python fig_tools/fig_flight.py --png
    python fig_tools/fig_flight.py --out docs/week_01/images

Outputs:
    fig04_axes.svg               pitch, roll, and yaw
    fig05_lift_and_weight.svg    descending, hovering, climbing
    fig06_differential_thrust.svg  which motors speed up for each motion
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import (aircraft_mini_side, aircraft_mini_top,  # noqa: E402
                   rotation_arrow)
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    rect, render_png, text, translate)

CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)


def card(cx, top, w, h, label, sub):
    """A panel background with a bold caption and a grey sub-caption.

    `sub` may be a string, or a sequence of lines when the caption is too long
    to sit inside a narrow panel on one line.
    """
    lines = [sub] if isinstance(sub, str) else list(sub)
    first = top + h - 16 - 17 * (len(lines) - 1)
    grp = g(rect(cx - w / 2, top, w, h, **CARD),
            text(cx, first - 24, label, text_anchor="middle", font_size=16,
                 font_weight="bold", fill=P["ink"]))
    for i, ln in enumerate(lines):
        grp.add(text(cx, first + i * 17, ln, text_anchor="middle",
                     font_size=12.5, fill=P["muted"]))
    return grp


# ---------------------------------------------------------------------------
# Figure 4: pitch, roll and yaw
# ---------------------------------------------------------------------------
def build_axes() -> Figure:
    fig = Figure(900, 400,
                 "Figure 4: The three ways a drone can turn",
                 "Every movement a drone makes is a combination of these three "
                 "rotations plus going up or down.")

    cols = (175, 450, 725)
    tops = 84
    h, w = 288, 264

    # pitch: side view, nose tilted down
    fig.add(card(cols[0], tops, w, h, "Pitch",
                 ("nose tips down or up,", "so it flies forward or back")))
    fig.add(translate(cols[0], tops + 120,
                      g(aircraft_mini_side(0.95), transform="rotate(18)")))
    fig.add(rotation_arrow(cols[0], tops + 120, 62, clockwise=True,
                           start_deg=200, sweep_deg=120, width=3))
    fig.add(circle(cols[0], tops + 120, 4, fill=P["muted"]))
    fig.add(text(cols[0], tops + 182, "side view", text_anchor="middle",
                 font_size=12, font_style="italic", fill=P["muted"]))

    # roll: head-on view, tilted to one side
    fig.add(card(cols[1], tops, w, h, "Roll",
                 ("leans left or right,", "so it slides sideways")))
    fig.add(translate(cols[1], tops + 120,
                      g(aircraft_mini_side(0.95, nose=False),
                        transform="rotate(-18)")))
    fig.add(rotation_arrow(cols[1], tops + 120, 62, clockwise=False,
                           start_deg=340, sweep_deg=120, width=3))
    fig.add(circle(cols[1], tops + 120, 4, fill=P["muted"]))
    fig.add(text(cols[1], tops + 182, "seen head-on", text_anchor="middle",
                 font_size=12, font_style="italic", fill=P["muted"]))

    # yaw: top view, spinning about the center
    fig.add(card(cols[2], tops, w, h, "Yaw",
                 ("spins in place, so the nose", "points somewhere new")))
    fig.add(translate(cols[2], tops + 120, aircraft_mini_top(0.9)))
    fig.add(rotation_arrow(cols[2], tops + 120, 60, clockwise=True,
                           start_deg=150, sweep_deg=240, width=3))
    fig.add(text(cols[2], tops + 182, "seen from above", text_anchor="middle",
                 font_size=12, font_style="italic", fill=P["muted"]))

    return fig


# ---------------------------------------------------------------------------
# Figure 5: lift against weight
# ---------------------------------------------------------------------------
def build_lift() -> Figure:
    fig = Figure(900, 430,
                 "Figure 5: Lift against weight",
                 "The propellers push air down. What the aircraft does next "
                 "depends only on how that lift compares with its weight.")

    cols = (190, 450, 710)
    tops, h, w = 84, 310, 250
    cases = (
        (26, "Descends", "lift is less than weight"),
        (44, "Hovers", "lift exactly balances weight"),
        (64, "Climbs", "lift is greater than weight"),
    )

    for cx, (lift, label, sub) in zip(cols, cases):
        fig.add(card(cx, tops, w, h, label, sub))
        mid = tops + 150
        fig.add(translate(cx, mid, aircraft_mini_side(0.95, nose=False)))
        # lift arrows, one above each visible rotor
        for mx in (-34, 34):
            fig.add(arrow(cx + mx, mid - 24, cx + mx, mid - 24 - lift,
                          width=3.5))
        fig.add(text(cx, mid - 36 - lift, "lift", text_anchor="middle",
                     font_size=12.5, fill=P["accent"]))
        # weight always the same length, drawn downward from the body
        fig.add(arrow(cx, mid + 24, cx, mid + 68, color=P["muted"], width=3.5))
        fig.add(text(cx, mid + 88, "weight", text_anchor="middle",
                     font_size=12.5, fill=P["muted"]))

    return fig


# ---------------------------------------------------------------------------
# Figure 6: differential thrust
# ---------------------------------------------------------------------------
SPEED = {"slow": (11, "#c3ccd4"), "same": (15, "#8fa3b5"), "fast": (21, P["accent"])}


def quad_speeds(fl, fr, rl, rr):
    """Top view where each rotor's circle size and color shows its speed."""
    motors = {"fl": (-34, -27), "fr": (34, -27), "rl": (-34, 27), "rr": (34, 27)}
    speeds = {"fl": fl, "fr": fr, "rl": rl, "rr": rr}
    grp = g()
    grp.add(g(*[line(mx * 0.3, my * 0.5, mx, my) for mx, my in motors.values()],
              stroke=P["line"], stroke_width=5, stroke_linecap="round"))
    for key, (mx, my) in motors.items():
        r, color = SPEED[speeds[key]]
        grp.add(circle(mx, my, r, fill=color, stroke=P["line"],
                       stroke_width=1.2))
    grp.add(rect(-12, -22, 24, 44, rx=6, fill=P["body"], stroke=P["line"],
                 stroke_width=1.5))
    grp.add(g(*[line(-7, -30, 0, -40), line(0, -40, 7, -30)],
              stroke=P["dark"], stroke_width=3, stroke_linecap="round",
              fill="none"))
    return grp


def build_thrust() -> Figure:
    fig = Figure(900, 456,
                 "Figure 6: Which motors speed up",
                 "A drone has no steering. It moves by running some rotors "
                 "faster than others. The chevron marks the nose.")

    cols = (148, 350, 552, 754)
    tops, h, w = 84, 268, 196
    cases = (
        (("same",) * 4, "Hover", ("all four rotors", "at the same speed"), None),
        (("slow", "slow", "fast", "fast"), "Fly forward",
         ("rear pair faster,", "so the nose tips down"), (0, -1)),
        (("fast", "slow", "fast", "slow"), "Slide right",
         ("left pair faster,", "so it leans right"), (1, 0)),
        (("slow", "fast", "fast", "slow"), "Turn right",
         ("one diagonal pair", "faster than the other"), "yaw"),
    )

    for cx, (speeds, label, sub, motion) in zip(cols, cases):
        fig.add(card(cx, tops, w, h, label, sub))
        mid = tops + 112
        fig.add(translate(cx, mid, quad_speeds(*speeds)))
        if motion == "yaw":
            fig.add(rotation_arrow(cx, mid, 62, clockwise=True, start_deg=155,
                                   sweep_deg=230, width=3))
        elif motion:
            dx, dy = motion
            fig.add(arrow(cx + dx * 62, mid + dy * 56,
                          cx + dx * 84, mid + dy * 84, width=3))

    # legend
    ly = 402
    fig.add(text(140, ly, "Rotor speed:", font_size=13, fill=P["muted"]))
    for i, (key, name) in enumerate((("slow", "slower"), ("same", "normal"),
                                     ("fast", "faster"))):
        r, color = SPEED[key]
        x = 258 + i * 132
        fig.add(circle(x, ly - 5, r * 0.62, fill=color, stroke=P["line"],
                       stroke_width=1.2))
        fig.add(text(x + 20, ly, name, font_size=13, fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, name in (
            (build_axes, figure_name(1, 4, "axes")),
            (build_lift, figure_name(1, 5, "lift_and_weight")),
            (build_thrust, figure_name(1, 6, "differential_thrust"))):
        fname = os.path.join(args.out, name)
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
