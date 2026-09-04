"""Topic 6 Figure 10: where the multispectral bands sit on the spectrum.

The page named the bands but never showed them, so "red edge" and "NIR" were
just words. This puts them on a wavelength axis, against what the eye can see,
against what an ordinary camera records, and against Landsat, which most survey
cameras were quietly designed to imitate.

Usage:
    python fig_tools/fig_spectral.py --png
    python fig_tools/fig_spectral.py --out docs/week_06/images
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, line, path,  # noqa: E402
                    rect, render_png, text)

NM0, NM1 = 400, 900
X0, X1 = 222, 868
NIR_GREY = "#5d5d63"
CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)


def x(nm):
    return X0 + (nm - NM0) * (X1 - X0) / (NM1 - NM0)


def visible_rgb(nm):
    """Bruton's approximation. Close enough to read as a spectrum."""
    if nm < 440:
        r, gr, b = -(nm - 440) / 60.0, 0.0, 1.0
    elif nm < 490:
        r, gr, b = 0.0, (nm - 440) / 50.0, 1.0
    elif nm < 510:
        r, gr, b = 0.0, 1.0, -(nm - 510) / 20.0
    elif nm < 580:
        r, gr, b = (nm - 510) / 70.0, 1.0, 0.0
    elif nm < 645:
        r, gr, b = 1.0, -(nm - 645) / 65.0, 0.0
    else:
        r, gr, b = 1.0, 0.0, 0.0
    if nm > 690:
        f = max(0.35, 0.35 + 0.65 * (740 - nm) / 50.0)
    elif nm < 420:
        f = 0.35 + 0.65 * (nm - 390) / 30.0
    else:
        f = 1.0
    return "#%02x%02x%02x" % tuple(int(255 * ((c * f) ** 0.85))
                                   for c in (r, gr, b))


# --- the two cameras, and the satellite they resemble -----------------------
DRONE = (("Blue", 475, 32), ("Green", 560, 27), ("Red", 668, 14),
         ("Red edge", 717, 12), ("NIR", 842, 57))
LANDSAT = (("Blue", 482, 60), ("Green", 561, 57), ("Red", 655, 37),
           ("NIR", 865, 28))
RGBCAM = (("Blue", 400, 520, "#4a6fd9"), ("Green", 450, 630, "#3f9e4f"),
          ("Red", 560, 700, "#d94a3f"))

BAND_FILL = {"Blue": "#4a6fd9", "Green": "#3f9e4f", "Red": "#d94a3f",
             "Red edge": "#a63b8f", "Coastal": "#6ec6e8", "NIR": NIR_GREY}


def spectrum_strip(fig):
    y, h = 250, 34
    nm = float(NM0)
    while nm < 700:
        fig.add(rect(x(nm), y, x(nm + 2.5) - x(nm) + 0.8, h,
                     fill=visible_rgb(nm), stroke="none"))
        nm += 2.5
    fig.add(rect(x(700), y, x(NM1) - x(700), h, fill=NIR_GREY, stroke="none"))
    fig.add(rect(X0, y, X1 - X0, h, fill="none", stroke=P["line"],
                 stroke_width=1.5))

    fig.add(text((X0 + x(700)) / 2, 242, "what your eye can see",
                 text_anchor="middle", font_size=12, font_weight="bold",
                 fill=P["ink"]))
    fig.add(text((x(700) + X1) / 2, 242,
                 "near-infrared: invisible, and where the signal is",
                 text_anchor="middle", font_size=12, font_weight="bold",
                 fill=P["ink"]))

    for nm in range(400, 901, 100):
        fig.add(line(x(nm), y + h, x(nm), y + h + 6, stroke=P["line"],
                     stroke_width=1.5))
        fig.add(text(x(nm), y + h + 20, str(nm), text_anchor="middle",
                     font_size=11, fill=P["muted"]))
    fig.add(text(X0 - 14, y + 22, "wavelength (nm)", text_anchor="end",
                 font_size=11.5, fill=P["muted"]))


BASE, SCALE = 196, 1.55
CURVE = ((400, 4), (430, 4.5), (460, 5), (500, 7), (550, 13), (570, 12),
         (600, 7), (640, 4.5), (670, 3.5), (690, 5.5), (700, 10),
         (710, 17), (720, 27), (730, 38), (740, 48), (750, 54),
         (770, 57), (800, 58), (850, 58), (900, 57))


def refl_y(pct):
    return BASE - pct * SCALE


def reflectance(fig):
    fig.add(rect(30, 64, 840, 154, **CARD))
    fig.add(line(X0, BASE, X1, BASE, stroke="#c5cdd5", stroke_width=1.2))
    fig.add(path("M" + " L".join("%.0f,%.0f" % (x(w), refl_y(r))
                                 for w, r in CURVE),
                 fill="none", stroke="#2f7d32", stroke_width=3.2))

    for i, ln in enumerate(("how much light", "a healthy leaf",
                            "sends back")):
        fig.add(text(X0 - 14, 152 + i * 15, ln, text_anchor="end",
                     font_size=11.5, fill=P["muted"]))

    fig.add(text(x(550), refl_y(13) - 11, "a little green",
                 text_anchor="middle", font_size=10.5, fill=P["muted"]))
    fig.add(text(x(640), 212, "red absorbed for photosynthesis",
                 text_anchor="middle", font_size=10.5, fill="#c0392b"))
    fig.add(line(x(748), 180, x(731), 156, stroke="#a63b8f", stroke_width=1.2))
    fig.add(text(x(752), 186, "the red edge: the steep climb",
                 font_size=10.5, font_weight="bold", fill="#a63b8f"))
    fig.add(text(x(866), 134, "leaf structure", text_anchor="end",
                 font_size=10.5, fill="#2f7d32"))
    fig.add(text(x(866), 148, "reflects NIR hard", text_anchor="end",
                 font_size=10.5, fill="#2f7d32"))

    # the two bands NDVI is built from, tied back to the curve so the size
    # of the gap between them is the thing you actually look at
    yb = 82
    fig.add(line(x(668), yb, x(842), yb, stroke=P["ink"], stroke_width=1.6))
    for w, pct in ((668, 3.5), (842, 58)):
        fig.add(line(x(w), yb, x(w), yb + 7, stroke=P["ink"], stroke_width=1.6))
        fig.add(line(x(w), yb + 9, x(w), refl_y(pct) - 5, stroke=P["ink"],
                     stroke_width=1, stroke_dasharray="3 4"))
        fig.add(circle(x(w), refl_y(pct), 4.5, fill=P["ink"]))
    fig.add(text((x(668) + x(842)) / 2, yb - 8,
                 "NDVI is the size of the gap between these two",
                 text_anchor="middle", font_size=12, font_weight="bold",
                 fill=P["ink"]))


def band_row(fig, bands, top, h, row_label, sub, stagger, guides=False):
    fig.add(text(X0 - 14, top + h / 2 - 3, row_label, text_anchor="end",
                 font_size=12.5, font_weight="bold", fill=P["ink"]))
    fig.add(text(X0 - 14, top + h / 2 + 13, sub, text_anchor="end",
                 font_size=10.5, fill=P["muted"]))
    for name, c, w in bands:
        xa, xb = x(c - w / 2.0), x(c + w / 2.0)
        if guides:
            fig.add(line(x(c), 284, x(c), top, stroke="#ccd4dc",
                         stroke_width=1, stroke_dasharray="3 4"))
        fig.add(rect(xa, top, max(xb - xa, 5), h, rx=2.5, fill=BAND_FILL[name],
                     stroke=P["line"], stroke_width=1.2))
        ty = top + h + (30 if name in stagger else 15)
        if name in stagger:
            fig.add(line(x(c), top + h + 3, x(c), ty - 11, stroke="#ccd4dc",
                         stroke_width=1))
        fig.add(text(x(c), ty, name, text_anchor="middle", font_size=11,
                     font_weight="bold", fill=P["ink"]))
        fig.add(text(x(c), ty + 13, "%d nm" % c, text_anchor="middle",
                     font_size=10, fill=P["muted"]))


def rgb_row(fig, top, h):
    fig.add(text(X0 - 14, top + h / 2 - 3, "An ordinary color camera",
                 text_anchor="end", font_size=12.5, font_weight="bold",
                 fill=P["ink"]))
    fig.add(text(X0 - 14, top + h / 2 + 13, "three wide, overlapping bands",
                 text_anchor="end", font_size=10.5, fill=P["muted"]))
    for i, (name, lo, hi, col) in enumerate(RGBCAM):
        fig.add(rect(x(lo), top + i * 4, x(hi) - x(lo), h - 8, rx=3, fill=col,
                     opacity="0.5", stroke=P["line"], stroke_width=1.2))
    fig.add(arrow(x(716), top + h / 2, x(703), top + h / 2, color=P["muted"],
                  width=1.6, head=6))
    fig.add(text(x(722), top + h / 2 + 4,
                 "it stops here, and records nothing past red",
                 font_size=11, font_style="italic", fill=P["muted"]))


def build() -> Figure:
    fig = Figure(900, 668,
                 "Where the multispectral bands sit on the spectrum",
                 "Centers and widths vary between cameras. These are typical "
                 "of a five-band survey camera.")
    reflectance(fig)
    spectrum_strip(fig)
    band_row(fig, DRONE, 326, 34, "A multispectral camera",
             "five narrow, separate bands", stagger=("Red edge",), guides=True)
    rgb_row(fig, 430, 34)
    band_row(fig, LANDSAT, 522, 26, "Landsat 8 and 9",
             "the satellite equivalents", stagger=())
    fig.add(text(450, 646,
                 "Landsat also carries two shortwave-infrared bands at 1610 "
                 "and 2200 nm, far off the right of this chart, that no drone "
                 "camera has.",
                 text_anchor="middle", font_size=12, font_style="italic",
                 fill=P["muted"]))
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()
    fname = os.path.join(args.out, figure_name(6, 10, "spectral_bands"))
    build().save(fname)
    print("wrote", fname)
    if args.png:
        png = render_png(fname)
        if png:
            print("wrote", png)


if __name__ == "__main__":
    main()
