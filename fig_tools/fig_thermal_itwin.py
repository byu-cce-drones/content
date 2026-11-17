"""The thermal iTwin route, for the Thermal Mosaic in iTwin page.

    w10_fig04_thermal_itwin_route.svg   SD card -> script -> iTwin -> QGIS,
                                        with the files carried by each arrow

Numbered in the w10_ (final project) sequence because the page sits after
Flight and Data Processing in the Weeks 10-15 nav; Figures 1-3 are in
fig_final_project.py. The SVG lives in docs/software/images/, the owning
section's folder.

Usage:
    python fig_tools/fig_thermal_itwin.py --out review --png
    python fig_tools/fig_thermal_itwin.py --out docs/software/images
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Figure, arrow, circle, figure_name, line, path,  # noqa: E402
                    rect, render_png, text)

W, H = 900, 366
BLUE = P["accent"]
ORANGE = "#d9822b"
GREEN = "#2f8f4e"
GRAY = "#8a96a3"
BLUE_FILL = "#e8f1fb"
ORANGE_FILL = "#fdf3e6"
GREEN_FILL = "#e6f4ea"
GRAY_FILL = "#eef1f4"


def _t(fig, x, y, s, size=12, bold=False, fill=None, anchor="middle",
       italic=False, mono=False):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 font_style="italic" if italic else None,
                 font_family="Consolas, 'Courier New', monospace" if mono
                 else None,
                 fill=fill or P["ink"]))


def build_route() -> Figure:
    fig = Figure(W, H, "Figure 4: From the SD card to °C on a map",
                 "The iTwin route for Autel thermal photos. iTwin only ever "
                 "sees grey levels; the scale file turns them back into °C.")

    # four stages: (title, lines, fill, stroke)
    stages = [
        ("SD card", ["your whole", "flight folder,", "nothing renamed"],
         GRAY_FILL, GRAY),
        ("Python notebook", ["05_itwin_export", "drops bad frames,",
                             "one °C scale"], BLUE_FILL, BLUE),
        ("iTwin Capture", ["aerotriangulation,", "Orthophoto/DSM,",
                           "colour correction off"], ORANGE_FILL, ORANGE),
        ("QGIS", ["Raster Calculator:", "grey → °C,", "pseudocolour"],
         GREEN_FILL, GREEN),
    ]
    bw, bh, top = 158, 104, 112
    gap = (W - 2 * 28 - 4 * bw) / 3
    xs = [28 + i * (bw + gap) for i in range(4)]
    for x, (title, lines, fill, stroke) in zip(xs, stages):
        fig.add(rect(x, top, bw, bh, rx=10, fill=fill, stroke=stroke,
                     stroke_width=2))
        _t(fig, x + bw / 2, top + 26, title, size=14.5, bold=True)
        for i, s in enumerate(lines):
            _t(fig, x + bw / 2, top + 50 + 17 * i, s, size=12.5,
               fill=P["muted"])

    # what each arrow carries, written above it
    carried = [
        [".irg  .TIFF", ".jpg  .mrk"],
        ["itwin_images", "IRX_nnnn.tif"],
        ["orthophoto", "GeoTIFF, grey"],
    ]
    ay = top + bh / 2
    for i, lines in enumerate(carried):
        x1, x2 = xs[i] + bw + 6, xs[i + 1] - 6
        fig.add(arrow(x1, ay, x2, ay, color=P["line"], width=2.5))
        for k, s in enumerate(lines):
            _t(fig, (x1 + x2) / 2, top - 26 + 16 * k, s, size=12,
               bold=(k == 0), mono=True)
        fig.add(line((x1 + x2) / 2, top - 4, (x1 + x2) / 2, ay - 6,
                     stroke=GRAY, stroke_width=1, stroke_dasharray="2 3"))

    # the scale file goes round iTwin, from the notebook to QGIS
    sx = xs[1] + bw / 2
    qx = xs[3] + bw / 2
    by = top + bh + 54
    fig.add(path(f"M {sx} {top + bh} L {sx} {by} L {qx} {by} "
                 f"L {qx} {top + bh + 12}",
                 fill="none", stroke=BLUE, stroke_width=2.2,
                 stroke_dasharray="7 5"))
    fig.add(path(f"M {qx - 7} {top + bh + 14} L {qx} {top + bh + 2} "
                 f"L {qx + 7} {top + bh + 14} Z", fill=BLUE))
    fig.add(circle(sx, top + bh, 3.5, fill=BLUE))
    mid = (sx + qx) / 2
    fig.add(rect(mid - 128, by - 15, 256, 30, rx=6, fill=P["bg"]))
    _t(fig, mid, by + 5, "temperature_scale.json", size=13.5, bold=True,
       fill=BLUE, mono=True)
    _t(fig, mid, by + 30,
       "the grey-to-°C formula and the ground pixel size; keep it with "
       "your results", size=12, fill=P["muted"])

    _t(fig, W / 2, H - 18,
       "Temperatures come from the .irg and .TIFF files. The .jpg holds only "
       "the GPS position and a coloured picture.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    fname = os.path.join(args.out, figure_name(10, 4, "thermal_itwin_route"))
    build_route().save(fname)
    print("wrote", fname)
    if args.png:
        png = render_png(fname)
        if png:
            print("wrote", png)


if __name__ == "__main__":
    main()
