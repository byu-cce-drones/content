"""Multispectral figures for the Week 8 reading (gen_reading/multispectral.md).

    w06_fig10_spectral_bands.svg        where the five bands sit on the spectrum
    w06_fig10b_ratio_cancels_light.svg  shade changes the bands, not the index
    w06_fig10c_calibration.svg          light sensor and panel: two flights made comparable

Figure 10 puts "red edge" and "NIR" on a wavelength axis, against what the
eye can see, what an ordinary camera records, and Landsat, which most survey
cameras were quietly designed to imitate. The two lettered variants sit beside
it in the reading (Why ratios rather than band values; Radiometric
calibration) and on the Week 8 deck, so adding them moved no number. The w06_
prefix is the sensors topic; the files live in docs/gen_reading/images/.

Usage:
    python fig_tools/fig_spectral.py --png
    python fig_tools/fig_spectral.py --out docs/gen_reading/images
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_side  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, g, line,  # noqa: E402
                    path, polygon, rect, render_png, text, translate)

W = 900
NM0, NM1 = 400, 900
X0, X1 = 222, 868
NIR_GREY = "#5d5d63"
RED_BAND = "#d94a3f"
GREEN = "#2f8f4e"
SUN = "#f4d03f"
SUN_EDGE = "#d4b02f"
CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)


def _t(fig, x, y, s, size=12, bold=False, fill=None, anchor="middle",
       italic=False):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 font_style="italic" if italic else None,
                 fill=fill or P["ink"]))


# ---------------------------------------------------------------------------
# 10. Where the bands sit on the spectrum
# ---------------------------------------------------------------------------
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
          ("Red", 560, 700, RED_BAND))

BAND_FILL = {"Blue": "#4a6fd9", "Green": "#3f9e4f", "Red": RED_BAND,
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


def build_spectral_bands() -> Figure:
    fig = Figure(W, 668,
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


# ---------------------------------------------------------------------------
# 10b. Shade changes the bands, not the index
# ---------------------------------------------------------------------------
# The three lawn patches from the Week 8 class question. Raw values are
# illustrative digital numbers; NDVI is computed from them below, so the
# numbers drawn can never disagree with the formula drawn.
PATCHES = (
    ("A", "sunlit, healthy grass", 4000, 400, "#4e9a3c", False),
    ("B", "the same grass, in shade", 2000, 200, "#4e9a3c", True),
    ("C", "sunlit, stressed grass", 2800, 1200, "#a9a94c", False),
)
NDVI_NOTE = {"A": "healthy",
             "B": "healthy: shade halved both bands",
             "C": "stressed: the gap has closed"}


def ndvi(nir, red):
    return (nir - red) / (nir + red)


def _sun(fig, cx, cy, r=9, rays=8, ray=5):
    for k in range(rays):
        a = math.radians(k * 360 / rays)
        fig.add(line(round(cx + (r + 3) * math.cos(a), 1),
                     round(cy + (r + 3) * math.sin(a), 1),
                     round(cx + (r + 3 + ray) * math.cos(a), 1),
                     round(cy + (r + 3 + ray) * math.sin(a), 1),
                     stroke=SUN_EDGE, stroke_width=2, stroke_linecap="round"))
    fig.add(circle(cx, cy, r, fill=SUN, stroke=SUN_EDGE, stroke_width=1.5))


def build_ratio_cancels_light() -> Figure:
    fig = Figure(W, 520, "Why a ratio: shade changes the bands, not the index",
                 "Illustrative numbers. In real shade the cancellation is "
                 "close, not exact.")
    cw, gap, x0 = 264, 24, 30
    top, bottom = 76, 446
    base, vmax, hmax = 336, 4000, 150          # bar baseline and scale
    bw = 44
    centres = []
    for i, (name, desc, nir, red, colour, shade) in enumerate(PATCHES):
        cx0 = x0 + i * (cw + gap)
        cx = cx0 + cw / 2
        centres.append(cx)
        fig.add(rect(cx0, top, cw, bottom - top, **CARD))
        fig.add(circle(cx0 + 24, top + 26, 11, fill=P["accent"]))
        _t(fig, cx0 + 24, top + 30, name, size=12, bold=True, fill=P["white"])
        _t(fig, cx0 + 42, top + 30, desc, size=13, bold=True, anchor="start")

        # the lawn patch, with a sun on it or a shadow over it
        px, py, pw, ph = cx - 45, 118, 90, 46
        fig.add(rect(px, py, pw, ph, rx=4, fill=colour, stroke=P["line"],
                     stroke_width=1.2))
        for k in range(7):                       # a few blades of grass
            gx = px + 10 + k * 12
            fig.add(path(f"M{gx},{py + ph - 6} q3,-10 6,-16", fill="none",
                         stroke="#2f6e28" if not shade else "#2a5a24",
                         stroke_width=1.2))
        if shade:
            fig.add(rect(px, py, pw, ph, rx=4, fill="#1a1a1a", opacity="0.45"))
            _t(fig, cx, py + ph / 2 + 5, "in shade", size=11.5, bold=True,
               fill=P["white"])
        else:
            _sun(fig, px + pw + 20, py + 12)

        # NIR and Red as paired bars, raw values on top
        for j, (lab, val, col) in enumerate((("NIR", nir, NIR_GREY),
                                             ("Red", red, RED_BAND))):
            bx = cx - bw - 8 + j * (bw + 16)
            h = val * hmax / vmax
            fig.add(rect(bx, base - h, bw, h, fill=col, stroke=P["line"],
                         stroke_width=1))
            _t(fig, bx + bw / 2, base - h - 6, f"{val:,}", size=12, bold=True)
            _t(fig, bx + bw / 2, base + 16, lab, size=11.5, bold=True,
               fill=P["muted"])
        fig.add(line(cx - 90, base, cx + 90, base, stroke=P["line"],
                     stroke_width=1.2))
        _t(fig, cx - 96, base - 2, "raw", size=10.5, fill=P["muted"],
           anchor="end")
        _t(fig, cx - 96, base + 11, "values", size=10.5, fill=P["muted"],
           anchor="end")

        # the index, big, with the verdict under it
        v = ndvi(nir, red)
        good = v > 0.6
        _t(fig, cx, 382, "NDVI", size=11.5, bold=True, fill=P["muted"])
        _t(fig, cx, 412, f"{v:.2f}", size=28, bold=True,
           fill=GREEN if good else P["warn"])
        _t(fig, cx, 434, NDVI_NOTE[name], size=11, fill=P["muted"])

    # the equals and not-equals between the big numbers
    for k, sym, col in ((0, "=", GREEN), (1, "≠", P["warn"])):
        gx = (centres[k] + centres[k + 1]) / 2
        _t(fig, gx, 414, sym, size=26, bold=True, fill=col)

    _t(fig, W / 2, 478, "NDVI = (NIR − Red) / (NIR + Red)", size=15,
       bold=True)
    _t(fig, W / 2, 504,
       "On NIR alone, B looks like the odd one out. On the index, C is: "
       "shade scaled both bands together and the ratio cancelled it.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 10c. Making two flights comparable
# ---------------------------------------------------------------------------
PANEL_RULES = (
    ("Near solar noon", "within about 2.5 h of it"),
    ("Panel flat, about a third of the frame",
     "no shadow from you: sun at your back, then step aside"),
    ("Uniform sky", "clear or completely overcast, not partly cloudy"),
)


def _leader(fig, x1, y1, x2, y2):
    fig.add(line(x1, y1, x2, y2, stroke=P["accent"], stroke_width=1.5))
    fig.add(circle(x2, y2, 3, fill=P["accent"]))


def build_calibration() -> Figure:
    fig = Figure(W, 520, "Making two flights comparable",
                 "A ratio steadies one flight. A light sensor and a panel of "
                 "known reflectance tie every flight to the same scale.")
    # --- the scene ----------------------------------------------------------
    sx0, sy0, sw, sh = 30, 76, 530, 354
    fig.add(rect(sx0, sy0, sw, sh, **CARD))
    ground = 388
    gb = sy0 + sh - 1                            # grass strip, rounded below
    fig.add(path(f"M{sx0 + 1},{ground} H{sx0 + sw - 1} V{gb - 9} "
                 f"a9,9 0 0 1 -9,9 H{sx0 + 10} a9,9 0 0 1 -9,-9 Z",
                 fill="#d7e9c8", stroke="none"))
    fig.add(line(sx0 + 1, ground, sx0 + sw - 1, ground, stroke="#8aa87a",
                 stroke_width=1.5))
    for k in range(26):                          # grass
        gx = sx0 + 14 + k * 20
        fig.add(path(f"M{gx},{ground} q3,-8 6,-13 M{gx + 8},{ground} "
                     f"q-2,-7 -4,-11", fill="none", stroke="#6f9a5c",
                     stroke_width=1.2))

    # the sun, high and to the right
    sunx, suny = 488, 134
    for k in range(12):
        a = math.radians(k * 30)
        fig.add(line(round(sunx + 27 * math.cos(a), 1),
                     round(suny + 27 * math.sin(a), 1),
                     round(sunx + 36 * math.cos(a), 1),
                     round(suny + 36 * math.sin(a), 1),
                     stroke=SUN_EDGE, stroke_width=2.5, stroke_linecap="round"))
    fig.add(circle(sunx, suny, 22, fill=SUN, stroke=SUN_EDGE, stroke_width=2))

    # the panel on the ground, and the aircraft hovering low over it
    panx, pany = 372, ground - 2
    fig.add(polygon([(panx - 44, pany), (panx + 44, pany), (panx + 54, pany + 12),
                     (panx - 34, pany + 12)], fill="#ececec", stroke=P["line"],
                    stroke_width=1.5))
    fig.add(polygon([(panx - 28, pany + 2), (panx + 28, pany + 2),
                     (panx + 34, pany + 10), (panx - 22, pany + 10)],
                    fill="#bfbfbf", stroke="none"))
    ax, ay = 300, 232
    fig.add(polygon([(ax, ay + 22), (panx - 48, pany - 2), (panx + 48, pany - 2)],
                    fill=P["accent"], opacity="0.08"))
    for ex in (panx - 48, panx + 48):
        fig.add(line(ax, ay + 22, ex, pany - 2, stroke=P["accent"],
                     stroke_width=1, stroke_dasharray="4 4"))
    fig.add(translate(ax, ay, aircraft_mini_side(1.0, nose=True)))
    # the upward-facing light sensor on top of the body
    fig.add(rect(ax - 7, ay - 17, 14, 9, rx=2, fill=P["dark"]))
    fig.add(circle(ax, ay - 17, 5, fill=P["white"], stroke=P["line"],
                   stroke_width=1.2))
    # the camera underneath
    fig.add(circle(ax, ay + 13, 4, fill=P["screen"], stroke=P["line"],
                   stroke_width=1.2))

    # sunlight to the sensor and to the ground
    fig.add(arrow(sunx - 30, suny + 18, ax + 10, ay - 25, color=SUN_EDGE,
                  width=2.5, head=9))
    fig.add(arrow(sunx - 10, suny + 36, panx + 18, pany - 24, color=SUN_EDGE,
                  width=2.5, head=9))

    # labels with leaders
    _t(fig, 50, 118, "Light sensor on top:", size=13, bold=True,
       anchor="start")
    _t(fig, 50, 136, "records how bright the sky is", size=12.5,
       anchor="start")
    _t(fig, 50, 152, "for every photo", size=12.5, anchor="start")
    _leader(fig, 150, 160, ax - 3, ay - 21)

    _t(fig, 50, 296, "Panel of known reflectance:", size=13, bold=True,
       anchor="start")
    _t(fig, 50, 314, "photographed before and after the flight,",
       size=12.5, anchor="start")
    _t(fig, 50, 330, "hovering low so it fills a third of the frame",
       size=12.5, anchor="start")
    _leader(fig, 200, 340, panx - 20, pany + 6)

    _t(fig, sx0 + sw / 2, 416,
       "the sky brightness and the panel together say how bright "
       "“white” was that day",
       size=11.5, fill=P["muted"], italic=True)

    # --- the rules ----------------------------------------------------------
    rx0, rw = 580, 290
    fig.add(rect(rx0, sy0, rw, sh, **CARD))
    _t(fig, rx0 + rw / 2, 108, "Three rules for the panel shot", size=13.5,
       bold=True)
    y = 150
    for k, (head, sub) in enumerate(PANEL_RULES):
        fig.add(circle(rx0 + 30, y - 5, 11, fill=P["accent"]))
        _t(fig, rx0 + 30, y - 1, str(k + 1), size=12, bold=True,
           fill=P["white"])
        _t(fig, rx0 + 50, y, head, size=13, bold=True, anchor="start")
        # wrap the second line by hand so it stays inside the card
        words, lines, cur = sub.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > 34:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for j, ln in enumerate(lines):
            _t(fig, rx0 + 50, y + 18 + j * 16, ln, size=11.5,
               fill=P["muted"], anchor="start")
        y += 46 + 16 * len(lines)
    _t(fig, rx0 + rw / 2, 384, "Partly cloudy is the worst case:", size=11.5,
       fill=P["muted"], italic=True)
    _t(fig, rx0 + rw / 2, 400, "the light changes between the panel", size=11.5,
       fill=P["muted"], italic=True)
    _t(fig, rx0 + rw / 2, 416, "shot and the photos it corrects.", size=11.5,
       fill=P["muted"], italic=True)

    # --- what it buys you: the chain along the bottom -----------------------
    chips = (("Raw brightness", "depends on the sun that day"),
             ("Reflectance, 0 to 1", "a property of the ground"),
             ("May and August compared", "same legend on both maps"))
    chw, chg, chy, chh = 250, 40, 450, 52
    cx0 = (W - (3 * chw + 2 * chg)) / 2
    for k, (head, sub) in enumerate(chips):
        cxk = cx0 + k * (chw + chg)
        last = k == 2
        fig.add(rect(cxk, chy, chw, chh, rx=8,
                     fill="#e8f1fb" if last else P["white"],
                     stroke=P["accent"], stroke_width=1.5))
        _t(fig, cxk + chw / 2, chy + 22, head, size=13, bold=True)
        _t(fig, cxk + chw / 2, chy + 40, sub, size=11, fill=P["muted"])
        if k < 2:
            fig.add(arrow(cxk + chw + 4, chy + chh / 2, cxk + chw + chg - 4,
                          chy + chh / 2, color=P["accent"], width=2.5, head=9))
    return fig


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    # the drawn NDVI values must be the ones the class question quotes
    assert [round(ndvi(n, r), 2) for _, _, n, r, _, _ in PATCHES] == \
        [0.82, 0.82, 0.40]

    # (builder, number, variant, slug): a lettered variant sits beside the
    # figure it extends without moving any number after it
    for builder, number, variant, slug in (
        (build_spectral_bands, 10, "", "spectral_bands"),
        (build_ratio_cancels_light, 10, "b", "ratio_cancels_light"),
        (build_calibration, 10, "c", "calibration"),
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
