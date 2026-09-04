"""Figures for the Week 3 Flight Practice lab.

Usage:
    python fig_tools/fig_flight_practice.py --png
    python fig_tools/fig_flight_practice.py --out docs/labs/images

Outputs:
    labfp_fig01_calibration.svg    pairing, gyro calibration and trim
    labfp_fig02_course_layout.svg  an example obstacle course, plan view

Naming: this lab is unnumbered on purpose (see planning/week3_lab_outline.md),
so its figures carry the prefix "labfp_" for flight practice. svgkit.figure_name()
formats a numeric week or lab number and cannot produce that prefix, so the name
is built here with figure_name_fp(), following the same pattern: prefix, figure
number, slug. The number in the file name is the number printed in the title.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_top, controller, person, stick  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, g, line, path, polygon,  # noqa: E402
                    rect, render_png, text, translate)

PREFIX = "labfp"


def figure_name_fp(number: int, slug: str) -> str:
    """labfp_figMM_slug.svg — the unnumbered-lab twin of svgkit.figure_name()."""
    return f"{PREFIX}_fig{number:02d}_{slug}.svg"


# ---------------------------------------------------------------------------
# Figure 1: pairing, gyro calibration, trim
# ---------------------------------------------------------------------------
COLS = (155, 450, 745)
PANEL_W, PANEL_H = 280, 356
PANEL_TOP = 62
CAPTION_TOP = 292                 # panel-relative, so all three captions align
SCALE = 0.58                      # controller scale inside a panel

# stick centres in the controller's own coordinates
LEFT_STICK = (90, 92)
RIGHT_STICK = (330, 92)
STICK_R = 32


class Panel:
    """One panel: a controller drawn small, with things placed on it.

    Extra marks are positioned in the controller's own coordinates and mapped
    into figure coordinates, so arrows and badges keep the standard line
    weights instead of being shrunk with the drawing.
    """

    def __init__(self, cx: int, heading: str, caption: list[str]):
        self.cx = cx
        self.top = PANEL_TOP
        self.s = SCALE
        self.ox = cx - 210 * self.s          # local x=210 is the body centre
        self.oy = self.top + 103             # leaves room for the antennas
        self.grp = g(rect(cx - PANEL_W / 2, self.top, PANEL_W, PANEL_H, rx=10,
                          fill=P["white"], stroke="#dde3e9", stroke_width=1.5))
        self.grp.add(text(cx, self.top + 28, heading, text_anchor="middle",
                          font_size=15, font_weight="bold", fill=P["ink"]))
        for i, ln in enumerate(caption):
            self.grp.add(text(cx, self.top + CAPTION_TOP + i * 17, ln,
                              text_anchor="middle", font_size=12.5,
                              fill=P["muted"]))

    # local (controller) coordinates -> figure coordinates
    def x(self, lx: float) -> float:
        return self.ox + self.s * lx

    def y(self, ly: float) -> float:
        return self.oy + self.s * ly

    @property
    def body_bottom(self) -> float:
        return self.y(190)

    def add_controller(self, left: str, right: str) -> "Panel":
        """Draw the controller, then put a stick glyph on each well.

        left/right are "off" (pale, not used) or a "dx,dy" push, so the panel
        shows at a glance which stick the step actually moves.

        A pushed stick is drawn here rather than by parts.stick(), using the
        same proportions, because parts.stick() draws its push arrow in the
        stick's own units: shrunk to panel scale that arrow comes out at a
        third of the house line weight and disappears on the page. A stick
        that is not in use has no arrow, so it comes straight from parts.
        """
        body, _ = controller(screen="none", mode_labels=False)
        self.grp.add(translate(self.ox, self.oy, body, scale=self.s))
        for (lx, ly), spec in ((LEFT_STICK, left), (RIGHT_STICK, right)):
            if spec == "off":
                self.grp.add(g(stick(0, 0, STICK_R, active=False),
                               transform=f"translate({self.x(lx)},"
                                         f"{self.y(ly)}) scale({self.s})"))
                continue
            dx, dy = (float(v) for v in spec.split(","))
            cx, cy, r = self.x(lx), self.y(ly), STICK_R * self.s
            self.grp.add(circle(cx, cy, r, fill=P["white"], stroke=P["line"],
                                stroke_width=1.5))
            self.grp.add(circle(cx, cy, r * 0.34, fill="none",
                                stroke="#cccccc", stroke_width=1,
                                stroke_dasharray="3 3"))
            self.grp.add(circle(cx + dx * r * 0.52, cy + dy * r * 0.52,
                                r * 0.34, fill=P["dark"], stroke=P["line"],
                                stroke_width=1.2))
            if dx or dy:
                mag = (dx ** 2 + dy ** 2) ** 0.5
                ux, uy = dx / mag, dy / mag
                self.grp.add(arrow(cx + ux * r * 1.05, cy + uy * r * 1.05,
                                   cx + ux * (r + 24), cy + uy * (r + 24),
                                   width=2.5, head=9))
        return self

    def add_note(self, note: str, dy: float = 26) -> "Panel":
        """One italic line in the band between the drawing and the caption."""
        self.grp.add(text(self.x(210), self.body_bottom + dy, note,
                          text_anchor="middle", font_size=12,
                          font_style="italic", fill=P["muted"]))
        return self

    def add_arrow(self, lx1, ly1, lx2, ly2, width=2.5, head=9) -> "Panel":
        self.grp.add(arrow(self.x(lx1), self.y(ly1), self.x(lx2), self.y(ly2),
                           width=width, head=head))
        return self

    def add_badge(self, lx, ly, n) -> "Panel":
        self.grp.add(circle(self.x(lx), self.y(ly), 11, fill=P["accent"]))
        self.grp.add(text(self.x(lx), self.y(ly) + 4, n, text_anchor="middle",
                          font_size=12, font_weight="bold", fill=P["white"]))
        return self


def build_calibration() -> Figure:
    fig = Figure(900, 446,
                 "Figure 1: Pairing, gyro calibration, and trim on the "
                 "controller",
                 "Stick positions are for the Holy Stone HS210. Other models "
                 "use a different corner — check the manual.")

    # (a) pair: left stick up, then down
    a = Panel(COLS[0], "a. Pair",
              ["Left stick up, then down.",
               "Solid lights = paired."])
    a.add_controller(left="0,0", right="off")
    a.add_arrow(90, 52, 90, 10)
    a.add_badge(52, 26, 1)
    a.add_arrow(90, 132, 90, 174)
    a.add_badge(52, 152, 2)
    a.add_note("drone on a flat, level surface, nose away")
    fig.add(a.grp)

    # (b) gyro calibration: both sticks held in the lower-left corner
    b = Panel(COLS[1], "b. Calibrate the gyro",
              ["Both sticks to the lower-left corner",
               "and hold. Lights blink fast, then solid;",
               "one long beep = done. Drone still",
               "and level."])
    b.add_controller(left="-0.72,0.72", right="-0.72,0.72")
    b.add_note("hold both sticks there until the beep")
    fig.add(b.grp)

    # (c) trim: throttle stick pressed in, direction stick against the drift
    c = Panel(COLS[2], "c. Trim (only if it still drifts)",
              ["Press the throttle stick in, push the",
               "direction stick against the drift."])
    c.add_controller(left="0,0", right="1,0")
    # two rings mark the stick that is pressed in rather than pushed over
    for r in (44, 52):
        c.grp.add(circle(c.x(90), c.y(92), r * SCALE, fill="none",
                         stroke=P["accent"], stroke_width=1.6,
                         stroke_dasharray="4 4"))
    c.grp.add(text(c.x(90), c.body_bottom + 24, "press in", text_anchor="middle",
                   font_size=12, fill=P["accent"]))
    # the drone drifts one way, the stick pushes the other
    drift_y = c.body_bottom + 44
    c.grp.add(translate(c.cx + 66, drift_y, aircraft_mini_top(0.34)))
    c.grp.add(arrow(c.cx + 40, drift_y, c.cx + 6, drift_y, width=2.5, head=8))
    c.grp.add(text(c.cx + 34, c.body_bottom + 24, "drone drifts",
                   text_anchor="middle", font_size=12, fill=P["muted"]))
    fig.add(c.grp)

    return fig


# ---------------------------------------------------------------------------
# Figure 2: an example obstacle course, plan view
# ---------------------------------------------------------------------------
BOUND = (60, 90, 845, 445)          # left, top, right, bottom
ROW_TOP, ROW_BOT = 180, 335          # the two rows the route runs along
GATES = ((225, "gate 1", "B"), (345, "gate 2", "C"), (465, "gate 3", "D"))
CONES = (740, 660, 580, 500)
BOX = (600, 148, 740, 212)           # left, top, right, bottom


def pad(cx, cy, r=26):
    """A marked landing pad seen from above."""
    return g(circle(cx, cy, r, fill=P["white"], stroke=P["accent"],
                    stroke_width=2.5),
             circle(cx, cy, r * 0.55, fill="none", stroke=P["accent"],
                    stroke_width=1.5, stroke_dasharray="4 4"),
             line(cx - r * 0.34, cy, cx + r * 0.34, cy, stroke=P["accent"],
                  stroke_width=1.5),
             line(cx, cy - r * 0.34, cx, cy + r * 0.34, stroke=P["accent"],
                  stroke_width=1.5))


def gate(x, y=ROW_TOP, half=26):
    """A pair of posts seen from above, with the opening between them."""
    return g(line(x, y - half, x, y + half, stroke="#b6c2cc",
                  stroke_width=1.5, stroke_dasharray="5 5"),
             circle(x, y - half, 7, fill=P["dark"], stroke=P["line"],
                    stroke_width=1.5),
             circle(x, y + half, 7, fill=P["dark"], stroke=P["line"],
                    stroke_width=1.5))


def cone(x, y):
    return g(polygon([(x, y - 14), (x - 10, y + 11), (x + 10, y + 11)],
                     fill=P["warn"], stroke=P["line"], stroke_width=1.2),
             line(x - 13, y + 11, x + 13, y + 11, stroke=P["line"],
                  stroke_width=2, stroke_linecap="round"))


def badge(x, y, letter, label=None, label_dy=25):
    grp = g(circle(x, y, 11, fill=P["accent"]),
            text(x, y + 4, letter, text_anchor="middle", font_size=12,
                 font_weight="bold", fill=P["white"]))
    if label:
        grp.add(text(x, y + label_dy, label, text_anchor="middle",
                     fill=P["ink"]))
    return grp


def route_marker(x, y, dx, dy, length=24):
    """A short arrow on the route, showing which way it is flown."""
    mag = (dx ** 2 + dy ** 2) ** 0.5
    ux, uy = dx / mag, dy / mag
    return arrow(x - ux * length / 2, y - uy * length / 2,
                 x + ux * length / 2, y + uy * length / 2, width=2.5, head=9)


def build_course() -> Figure:
    fig = Figure(900, 535,
                 "Figure 2: An example obstacle course, seen from above",
                 "Your TA lays the course out on the day; the elements are the "
                 "same, the order and spacing change.")

    l, t, r, b = BOUND
    fig.add(rect(l, t, r - l, b - t, rx=10, fill="#eef4ea", stroke="#cfdcc6",
                 stroke_width=1.5))
    fig.add(rect(l, t, r - l, b - t, rx=10, fill="none", stroke=P["muted"],
                 stroke_width=2, stroke_dasharray="10 7"))

    # the box to climb over
    bl, bt, br, bb = BOX
    fig.add(rect(bl, bt, br - bl, bb - bt, rx=6, fill="#e8edf2",
                 stroke=P["line"], stroke_width=1.5))

    # the route, drawn as a dotted line before the elements sit on top of it
    pts = [(150, ROW_TOP), (800, ROW_TOP), (800, ROW_BOT),
           (740, ROW_BOT - 36), (660, ROW_BOT + 36), (580, ROW_BOT - 36),
           (500, ROW_BOT + 36), (450, ROW_BOT), (356, ROW_BOT)]
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    fig.add(path(d, fill="none", stroke=P["accent"], stroke_width=3.5,
                 stroke_dasharray="1 9", stroke_linecap="round"))

    for x, y, dx, dy in ((190, ROW_TOP, 1, 0), (405, ROW_TOP, 1, 0),
                         (555, ROW_TOP, 1, 0), (800, 262, 0, 1),
                         (700, ROW_BOT, -80, 72), (405, ROW_BOT, -1, 0)):
        fig.add(route_marker(x, y, dx, dy))

    # elements, in the order they are flown
    fig.add(pad(120, ROW_TOP))
    # nose pointed the way the route leaves the pad
    fig.add(g(aircraft_mini_top(0.45),
              transform=f"translate(120,{ROW_TOP}) rotate(90)"))
    fig.add(badge(120, 112, "A", "start pad"))

    for x, label, letter in GATES:
        fig.add(gate(x))
        fig.add(badge(x, 112, letter, label))

    fig.add(badge(670, 112, "E", "box — climb over"))
    fig.add(text(670, 202, "gain altitude here", text_anchor="middle",
                 font_size=12, font_style="italic", fill=P["muted"]))

    for x in CONES:
        fig.add(cone(x, ROW_BOT))
    fig.add(badge(620, 382, "F", "cone slalom"))

    fig.add(pad(330, ROW_BOT))
    fig.add(badge(330, 382, "G", "finish pad"))

    # the pilot stands outside the boundary, on the near edge
    fig.add(person(450, 492, scale=1.7))
    fig.add(text(450, 516, "pilot stays here", text_anchor="middle",
                 font_size=12.5, fill=P["muted"]))
    fig.add(text(l + 8, 470, "dashed line = flight area boundary",
                 font_size=12.5, fill=P["muted"]))
    return fig


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    for builder, name in (
            (build_calibration, figure_name_fp(1, "calibration")),
            (build_course, figure_name_fp(2, "course_layout"))):
        fname = os.path.join(args.out, name)
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
