"""Figures for the Measurement Fundamentals reading.

The page teaches general engineering measurement, so none of these drawings has
an aircraft in it. A drone is one method on a list that also contains a pair of
boots, and it belongs in the accuracy-versus-effort figure, not in the
definitions.

Figure 5 (accuracy vs. effort) already exists as w01_overview_accuracy_effort.svg
and is re-saved here under its w00 number from the same builder, so the two
copies cannot drift apart.

Usage:
    python fig_tools/fig_measurement.py --png
    python fig_tools/fig_measurement.py --out docs/gen_reading/images

Outputs:
    w00_fig01_accuracy_precision.svg   four targets: the two ideas are independent
    w00_fig02_pacing_spread.svg        same average, different spread; sigma
    w00_fig03_error_sources.svg        instrument, method, operator, reference
    w00_fig04_accuracy_ladder.svg      how much accuracy does the decision need
    w00_fig05_accuracy_effort.svg      what it costs to buy more (re-saved)
    w00_fig06_significant_figures.svg  the digits you can defend
    w00_fig07_ground_truth.svg         checking against something independent
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    path, polygon, rect, render_png, text)

W = 900
CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)


def _name(number: int, slug: str) -> str:
    """w00_figNN_slug.svg. The page sits above the numbered topics, so w00."""
    return figure_name(0, number, slug)


def _label(fig, x, y, s, size=14, bold=False, fill=None, anchor="middle"):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 fill=fill or P["ink"]))


# ---------------------------------------------------------------------------
# Figure 1 - four targets
# ---------------------------------------------------------------------------
PANELS = [
    ("Accurate, not precise", "Right on average, badly scattered",
     [(-38, -22), (30, -34), (44, 26), (-30, 36), (-6, -48), (10, 42)]),
    ("Precise, not accurate", "Repeatable, and repeatably wrong",
     [(40, -46), (52, -38), (44, -34), (50, -44), (46, -40), (38, -40)]),
    ("Accurate and precise", "What you are aiming for",
     [(4, -3), (-5, 4), (2, 6), (-3, -5), (6, 1), (-1, -2)]),
    ("Neither", "Scattered, and off as well",
     [(10, 8), (66, 14), (30, 60), (70, 52), (46, 22), (14, 46)]),
]


def build_targets() -> Figure:
    fig = Figure(W, 452, "Accuracy and precision are two different things",
                 "The bullseye is the true value. Each dot is one measurement "
                 "of the same thing.")
    cy = 196
    for i, (title, sub, shots) in enumerate(PANELS):
        cx = 30 + 210 * i + 105
        fig.add(rect(cx - 100, 76, 200, 240, **CARD))
        for r, fill in ((78, "#eef3f8"), (56, "#dce7f2"),
                        (34, "#c6d9ec"), (13, "#a9c8e4")):
            fig.add(circle(cx, cy, r, fill=fill, stroke="#b9c6d2",
                           stroke_width=1))
        fig.add(line(cx - 84, cy, cx + 84, cy, stroke="#b9c6d2",
                     stroke_width=1))
        fig.add(line(cx, cy - 84, cx, cy + 84, stroke="#b9c6d2",
                     stroke_width=1))
        dots = g(fill=P["bad"], stroke=P["white"], stroke_width=1.2)
        for dx, dy in shots:
            dots.add(circle(cx + dx, cy + dy, 5.5))
        fig.add(dots)
        _label(fig, cx, 348, title, size=14.5, bold=True)
        _label(fig, cx, 368, sub, size=11.5, fill=P["muted"])

    fig.add(rect(30, 388, W - 60, 46, rx=8, fill="#eef3f8",
                 stroke="#d5dfe8", stroke_width=1))
    _label(fig, W / 2, 406,
           "Averaging fixes scatter. It does not fix an error that pushes "
           "every measurement the same way.", size=12.5)
    _label(fig, W / 2, 424,
           "That is why you need both numbers, and why one of them cannot "
           "stand in for the other.", size=11.5, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 2 - same average, different spread
# ---------------------------------------------------------------------------
WALKERS = [
    ("Walker A", [38, 39, 38], "precise", P["ok"]),
    ("Walker B", [35, 42, 39], "not precise", P["warn"]),
]
LO, HI = 34, 43
AX0, AX1 = 175, 700


def _sx(v: float) -> float:
    return AX0 + (v - LO) * (AX1 - AX0) / (HI - LO)


def _stdev(vals) -> float:
    m = sum(vals) / len(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


def build_spread() -> Figure:
    fig = Figure(W, 492, "Precision is the spread, and it has a number",
                 "Two students pace the same 100 ft three times. Their step "
                 "counts:")
    for row, (who, vals, verdict, colour) in enumerate(WALKERS):
        top = 92 + row * 168
        base = top + 78
        fig.add(rect(30, top, W - 60, 152, **CARD))
        _label(fig, 52, top + 30, who, size=14.5, bold=True, anchor="start")

        fig.add(line(AX0 - 14, base, AX1 + 14, base, stroke="#9aa7b2",
                     stroke_width=2))
        for v in range(LO, HI + 1):
            x = _sx(v)
            fig.add(line(x, base, x, base + 6, stroke="#b9c6d2",
                         stroke_width=1.5))
            _label(fig, x, base + 22, str(v), size=10.5, fill=P["muted"])

        seen: dict[int, int] = {}
        for v in vals:
            k = seen.get(v, 0)
            seen[v] = k + 1
            fig.add(circle(_sx(v), base - 14 - 17 * k, 7, fill=colour,
                           stroke=P["white"], stroke_width=1.5))

        m = sum(vals) / len(vals)
        sd = _stdev(vals)
        fig.add(line(_sx(m), base - 62, _sx(m), base + 2, stroke=P["ink"],
                     stroke_width=1.5, stroke_dasharray="4 3"))
        _label(fig, _sx(m), base - 68, f"mean {m:.1f}", size=11.5, bold=True)

        a, b = _sx(min(vals)), _sx(max(vals))
        fig.add(path(f"M{a},{base + 34} L{a},{base + 42} L{b},{base + 42} "
                     f"L{b},{base + 34}", fill="none", stroke=colour,
                     stroke_width=2))
        _label(fig, (a + b) / 2, base + 58, "spread", size=11,
               fill=P["muted"])

        fig.add(rect(AX1 + 42, top + 34, 158, 60, rx=8, fill="#f4f7fa",
                     stroke=colour, stroke_width=1.5))
        _label(fig, AX1 + 121, top + 58, f"σ = {sd:.1f} steps", size=14,
               bold=True, fill=colour)
        _label(fig, AX1 + 121, top + 78, verdict, size=12, fill=P["muted"])

    fig.add(rect(30, 432, W - 60, 46, rx=8, fill="#eef3f8",
                 stroke="#d5dfe8", stroke_width=1))
    _label(fig, W / 2, 450,
           "Both walkers average about the same count. Only one of them can "
           "tell you how far to trust a single walk.", size=12.5)
    _label(fig, W / 2, 468,
           "This figure is only about precision. Accuracy needs the tape.",
           size=11.5, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 3 - where the error comes from
# ---------------------------------------------------------------------------
SOURCES = [
    ("The instrument", "A tape that has stretched, or a scale too coarse",
     "Check it against a known length", (30, 82), (296, 214)),
    ("The method", "Treating a lot that is not rectangular as a rectangle",
     "Match the method to the shape", (566, 82), (604, 214)),
    ("The operator", "Stretching your stride while calibrating a pace",
     "Repeat the measurement, then average", (30, 316), (296, 306)),
    ("The reference", "A benchmark that moved, or imagery three years old",
     "Use a reference you can verify", (566, 316), (604, 306)),
]


def build_error_sources() -> Figure:
    fig = Figure(W, 486, "Four places the error comes from",
                 "Only one of them is the instrument's fault.")

    fig.add(rect(322, 176, 256, 168, rx=8, fill="#eef3f8", stroke="#c6d3de",
                 stroke_width=1.5))
    fig.add(path("M348,318 L372,240 L470,214 L552,252 L536,318 Z",
                 fill="#e4ead9", stroke=P["line"], stroke_width=1.5))
    fig.add(line(348, 336, 552, 336, stroke=P["accent"], stroke_width=2))
    for x in (348, 552):
        fig.add(line(x, 328, x, 344, stroke=P["accent"], stroke_width=2))
    _label(fig, 450, 200, "one measurement", size=12, fill=P["muted"])
    _label(fig, 450, 358, "210 ft", size=14, bold=True, fill=P["accent"])

    for title, example, fix, (bx, by), (tx, ty) in SOURCES:
        fig.add(rect(bx, by, 304, 118, **CARD))
        _label(fig, bx + 18, by + 28, title, size=14.5, bold=True,
               anchor="start")
        _label(fig, bx + 18, by + 52, example, size=11.5, fill=P["muted"],
               anchor="start")
        _label(fig, bx + 18, by + 82, "→  " + fix, size=12,
               fill=P["ok"], anchor="start")
        sx = bx + 304 + 8 if bx < 300 else bx - 8
        fig.add(line(sx, by + 58, tx, ty, stroke=P["accent"],
                     stroke_width=1.5))
        fig.add(circle(tx, ty, 3.5, fill=P["accent"]))

    _label(fig, W / 2, 462,
           "Repeating a measurement exposes the operator. It hides the other "
           "three.", size=12.5, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 4 - how much accuracy does the decision need
# ---------------------------------------------------------------------------
RUNGS = [
    ("meters", "Is there a boulder in this field?", "pacing, or free imagery"),
    ("about 1 m", "Roughly how much asphalt does this lot need?",
     "free imagery, or a wheel"),
    ("10 cm", "How much fill was moved this week?",
     "aerial survey with ground control"),
    ("1 cm", "Does this pipe fall the whole way to the outlet?",
     "level, or survey-grade GNSS"),
    ("1 mm", "Has this beam settled since last month?",
     "total station, or dial gauges"),
]


def build_ladder() -> Figure:
    fig = Figure(W, 502, "The decision sets the accuracy, not the equipment",
                 "Work down the list only as far as the question actually "
                 "requires.")
    top, step = 96, 74
    fig.add(line(150, top - 12, 150, top + step * len(RUNGS) - 26,
                 stroke="#b9c6d2", stroke_width=3))
    for i, (need, question, tool) in enumerate(RUNGS):
        y = top + step * i
        fig.add(rect(178, y - 24, 692, 58, **CARD))
        fig.add(circle(150, y + 4, 9, fill=P["accent"]))
        _label(fig, 128, y + 9, need, size=13.5, bold=True, anchor="end")
        _label(fig, 200, y - 2, question, size=13.5, anchor="start")
        _label(fig, 200, y + 20, tool, size=11.5, fill=P["muted"],
               anchor="start")

    fig.add(arrow(60, top - 4, 60, top + step * (len(RUNGS) - 1) + 14,
                  color="#b6c2cc", width=3, head=10))
    for i, ch in enumerate("MORE"):
        _label(fig, 42, 168 + i * 18, ch, size=11.5, fill=P["muted"])
    for i, ch in enumerate("COST"):
        _label(fig, 42, 268 + i * 18, ch, size=11.5, fill=P["muted"])

    fig.add(rect(30, 442, W - 60, 44, rx=8, fill="#eef3f8",
                 stroke="#d5dfe8", stroke_width=1))
    _label(fig, W / 2, 460,
           "Accuracy you do not need is wasted money. Accuracy you do need "
           "and did not buy is a failure", size=12.5)
    _label(fig, W / 2, 477, "you will not find out about until it matters.",
           size=12.5)
    return fig


# ---------------------------------------------------------------------------
# Figure 6 - the digits you can defend
# ---------------------------------------------------------------------------
def build_sigfigs() -> Figure:
    fig = Figure(W, 402, "Your calculator does not know how good your "
                         "measurement is",
                 "42 paces at 2.53 ft per pace, with a pace good to about "
                 "three percent.")

    fig.add(rect(60, 84, 360, 96, **CARD))
    _label(fig, 240, 112, "what the calculator says", size=11.5,
           fill=P["muted"])
    fig.add(text(240, 156, "106.", text_anchor="end", font_size=34,
                 font_weight="bold", fill=P["ink"]))
    fig.add(text(240, 156, "26", text_anchor="start", font_size=34,
                 font_weight="bold", fill="#c3ccd4"))
    fig.add(line(240, 146, 288, 146, stroke=P["bad"], stroke_width=2.5))
    _label(fig, 264, 176, "decoration", size=11, fill=P["bad"])

    fig.add(arrow(444, 132, 496, 132, color="#b6c2cc", width=3, head=10))

    fig.add(rect(520, 84, 320, 96, rx=10, fill="#eef7f0", stroke=P["ok"],
                 stroke_width=2))
    _label(fig, 680, 112, "what you report", size=11.5, fill=P["muted"])
    fig.add(text(680, 156, "106 ± 3 ft", text_anchor="middle",
                 font_size=34, font_weight="bold", fill=P["ok"]))

    base, lo, hi = 268, 300, 720
    fig.add(line(lo, base, hi, base, stroke="#9aa7b2", stroke_width=2))
    fig.add(rect(lo + 105, base - 18, 210, 36, rx=6, fill="#dce7f2",
                 stroke=P["accent"], stroke_width=1.5))
    fig.add(line(lo + 210, base - 26, lo + 210, base + 26, stroke=P["accent"],
                 stroke_width=2.5))
    _label(fig, lo + 210, base - 34, "106", size=13, bold=True,
           fill=P["accent"])
    _label(fig, lo + 105, base + 40, "103", size=11.5, fill=P["muted"])
    _label(fig, lo + 315, base + 40, "109", size=11.5, fill=P["muted"])
    _label(fig, lo + 210, base + 62,
           "three percent of 106 ft is about 3 ft, so the answer lives "
           "anywhere in here", size=11.5, fill=P["muted"])

    fig.add(rect(30, 336, W - 60, 46, rx=8, fill="#eef3f8",
                 stroke="#d5dfe8", stroke_width=1))
    _label(fig, W / 2, 354,
           "Quote no more digits than your uncertainty supports, and put the "
           "uncertainty next to the number.", size=12.5)
    _label(fig, W / 2, 372,
           "Extra digits do not make a measurement look careful. They make it "
           "look unexamined.", size=11.5, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# Figure 7 - checking against something independent
# ---------------------------------------------------------------------------
CHECKS = [(0.04, "A"), (-0.07, "B"), (0.02, "C"), (-0.05, "D")]


def build_ground_truth() -> Figure:
    fig = Figure(W, 470, "A check is only worth anything if it is independent",
                 "Four known points, measured again by your method. The gap "
                 "is what you report.")
    base = 196
    fig.add(line(90, base, 810, base, stroke="#9aa7b2", stroke_width=2))
    _label(fig, 812, base + 4, "known", size=11, fill=P["muted"],
           anchor="start")
    _label(fig, 812, base + 18, "value", size=11, fill=P["muted"],
           anchor="start")

    scale = 720.0
    for i, (res, tag) in enumerate(CHECKS):
        x = 176 + i * 176
        y = base - res * scale
        fig.add(polygon([(x - 9, base + 12), (x + 9, base + 12), (x, base)],
                        fill=P["ink"]))
        colour = P["ok"] if abs(res) <= 0.05 else P["warn"]
        fig.add(line(x, base, x, y, stroke=colour, stroke_width=2.5))
        fig.add(circle(x, y, 7, fill=colour, stroke=P["white"],
                       stroke_width=1.5))
        _label(fig, x, base + 34, f"point {tag}", size=12, bold=True)
        _label(fig, x, y - 16 if res > 0 else y + 26,
               f"{res:+.2f} m", size=12, bold=True, fill=colour)

    fig.add(rect(30, 318, 420, 76, **CARD))
    _label(fig, 50, 344, "What this tells you", size=13.5, bold=True,
           anchor="start")
    _label(fig, 50, 368,
           "Largest gap is 0.07 m. That is the honest claim,", size=12,
           fill=P["muted"], anchor="start")
    _label(fig, 50, 385, "not the finest detail you can see.", size=12,
           fill=P["muted"], anchor="start")

    fig.add(rect(470, 318, 400, 76, rx=10, fill="#fdf3e6", stroke=P["warn"],
                 stroke_width=1.5))
    _label(fig, 490, 344, "Independent means independent", size=13.5,
           bold=True, anchor="start")
    _label(fig, 490, 368,
           "Measuring the same way twice tests precision.", size=12,
           fill=P["muted"], anchor="start")
    _label(fig, 490, 385, "Only a different source tests accuracy.", size=12,
           fill=P["muted"], anchor="start")

    _label(fig, W / 2, 432,
           "When someone asks whether your measurement is any good, this is "
           "the answer you give them.", size=12.5, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    builders = [
        (1, "accuracy_precision", build_targets),
        (2, "pacing_spread", build_spread),
        (3, "error_sources", build_error_sources),
        (4, "accuracy_ladder", build_ladder),
        (6, "significant_figures", build_sigfigs),
        (7, "ground_truth", build_ground_truth),
    ]

    # Figure 5 is the existing accuracy-vs-effort drawing, re-saved under its
    # w00 number from the one builder, so the two copies cannot drift.
    try:
        from fig_overview import build_accuracy_effort
        builders.append((5, "accuracy_effort", build_accuracy_effort))
    except ImportError as exc:  # pragma: no cover
        print("skipping figure 5:", exc)

    for number, slug, builder in sorted(builders):
        fname = os.path.join(args.out, _name(number, slug))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
