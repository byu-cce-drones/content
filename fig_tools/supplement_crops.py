"""Crop figures from the FAA Airman Knowledge Testing Supplement for the Part 107 slides.

Source: FAA-CT-8080-2H, *Airman Knowledge Testing Supplement for Sport Pilot, Recreational Pilot,
Remote Pilot, and Private Pilot* (2018). The reduced copy in the repository is
`docs/part_107_license/images/sport_rec_private_akts_FAA-CT-8080-2H_small.pdf` (113 pages:
Appendix 1 legends on pages 13-32, Appendix 2 Figures 1-82 on pages 35-113). It is a work of the
US Government and in the public domain (17 U.S.C. 105). Every crop keeps the credit and the FAA's
"not for navigation" warning in a caption strip under the image:

    FAA-CT-8080-2H, Figure N. Public domain. Not for navigation.

What it does
------------
Each row of `CROPS` below names one output: file stem, the supplement label ("Figure 23" or
"Legend 1"), the 0-based page index, the crop box, the render dpi, a title line and an optional
rotation. The box is in PDF points (x0, y0, x1, y1; origin top-left, a page is 594 x 774 pt) or,
if every value is at most 1, in fractions of the page. The script checks that the label is
printed on the page it was given and, if not, searches the PDF for it and says so.

The sectional excerpts in the reduced PDF are 150 dpi rasters, so rendering them above 200 dpi
adds pixels but no detail. The legend and Figures 2 and 12 are vector.

Each crop is written as PNG or JPG (quality 85), whichever is smaller, at most 1600 px wide and
at most `--max-kb` (default 350) kilobytes, with no EXIF, XMP or text chunks. A stale copy with
the other extension is removed so a crop never exists twice.

Usage
-----
Run with the full Anaconda interpreter; in Git Bash add `< /dev/null`:

    C:/Users/williagp/anaconda3/python.exe fig_tools/supplement_crops.py < /dev/null

which is the same as

    C:/Users/williagp/anaconda3/python.exe fig_tools/supplement_crops.py \\
        docs/part_107_license/images/sport_rec_private_akts_FAA-CT-8080-2H_small.pdf \\
        --out review < /dev/null

Options: `--only NAME [NAME ...]` makes just those crops; `--with-title` adds the title line
above the credit in the strip (off by default, because the slide carries its own title);
`--max-kb` changes the size cap; `--list` prints the table and exits.

Approved crops go to `docs/part_107_license/images/` (copy them, or run with
`--out docs/part_107_license/images`). Needs PyMuPDF (`fitz`) and Pillow.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
DEFAULT_PDF = REPO / "docs/part_107_license/images/sport_rec_private_akts_FAA-CT-8080-2H_small.pdf"
DEFAULT_OUT = REPO / "review"

MAX_WIDTH = 1600
STRIP_BG = (249, 249, 249)    # svgkit PALETTE["bg"]
STRIP_INK = (26, 26, 26)      # svgkit PALETTE["ink"]
RULE = (200, 200, 200)


@dataclass(frozen=True)
class Crop:
    name: str          # output file stem
    label: str         # "Figure 23" or "Legend 1": printed on the page and in the credit
    page: int          # 0-based page index in the PDF
    box: tuple         # (x0, y0, x1, y1) in points, or fractions of the page if all <= 1
    dpi: int           # 150-200
    title: str         # one line saying what the crop is for
    rotate: int = 0    # degrees clockwise applied after rendering (the legend is printed sideways)


# Page indices are 0-based (the PDF viewer's page number minus one). Boxes were set by rendering
# each page and looking at it; the sample-question numbers are those of the FAA's UAG sample set.
CROPS = [
    Crop("w05_supp_fig02_load_factor", "Figure 2", 35, (32, 50, 526, 412), 150,
         "Load factor chart: table and curve (FAA sample Q7, 30 degree bank)"),
    Crop("w05_supp_fig12_metar", "Figure 12", 45, (32, 50, 526, 162), 200,
         "Aviation routine weather reports (FAA sample Q25 KMDW, Q26 KJFK)"),
    Crop("w05_supp_fig21_moa", "Figure 21", 53, (240, 300, 512, 505), 200,
         "Devils Lake West MOA and area 2 (FAA sample Q10)"),
    Crop("w05_supp_fig22_coeur_dalene", "Figure 22", 54, (86, 335, 335, 500), 200,
         "Coeur d'Alene (COE), CTAF 122.8, and area 2 (FAA sample Q5)"),
    Crop("w05_supp_fig23_savannah", "Figure 23", 55, (262, 440, 510, 650), 200,
         "Savannah Class C with the 41/13 shelf and area 3 (FAA sample Q8)"),
    Crop("w05_supp_fig26_jamestown", "Figure 26", 58, (180, 412, 392, 575), 200,
         "Jamestown (JMS) surface Class E, dashed magenta, and area 4 (FAA sample Q13)"),
    Crop("w05_supp_fig26_cooperstown", "Figure 26", 58, (395, 178, 548, 325), 200,
         "Cooperstown (S32), runway 13/31, and area 2 (FAA sample Q18)"),
    Crop("w05_supp_fig59_mtr", "Figure 59", 89, (48, 322, 272, 462), 200,
         "VR1667 military training route and area 2 (FAA sample Q30)"),
    Crop("w05_supp_legend_airspace", "Legend 1", 12, (128, 169, 349.5, 376), 200,
         "Sectional legend: Class B, C, D, E floors, MOA, restricted, MTR", rotate=90),
]


def find_label(doc: fitz.Document, label: str, hint: int) -> int:
    """Return the page carrying `label` (e.g. "Figure 23."), preferring `hint`."""
    pat = re.compile(re.escape(label) + r"\.", re.I)
    if 0 <= hint < len(doc) and pat.search(doc[hint].get_text()):
        return hint
    for i, page in enumerate(doc):
        if pat.search(page.get_text()) and "Contents" not in page.get_text()[:200]:
            print(f"  note: {label} not on page index {hint}; using {i}", file=sys.stderr)
            return i
    raise SystemExit(f"{label} not found in the PDF")


def render(doc: fitz.Document, crop: Crop, page_index: int) -> Image.Image:
    page = doc[page_index]
    r = page.rect
    x0, y0, x1, y1 = crop.box
    if max(crop.box) <= 1:
        x0, x1 = r.x0 + x0 * r.width, r.x0 + x1 * r.width
        y0, y1 = r.y0 + y0 * r.height, r.y0 + y1 * r.height
    clip = fitz.Rect(x0, y0, x1, y1) & r
    pix = page.get_pixmap(dpi=crop.dpi, clip=clip, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if crop.rotate:
        img = img.rotate(-crop.rotate, expand=True)   # PIL rotates counter-clockwise
    if img.width > MAX_WIDTH:
        img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)), Image.LANCZOS)
    return img


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"] if bold else \
            ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf"]
    for name in names:
        for base in ("", "C:/Windows/Fonts/"):
            try:
                return ImageFont.truetype(base + name, size)
            except OSError:
                pass
    return ImageFont.load_default(size)


def fit_font(text: str, width: int, size: int, bold: bool = False):
    """Largest font no bigger than `size` px that sets `text` within `width` px."""
    while size > 9:
        font = load_font(size, bold)
        if font.getlength(text) <= width:
            return font
        size -= 1
    return load_font(size, bold)


def add_strip(img: Image.Image, crop: Crop, with_title: bool) -> Image.Image:
    """Append the credit strip (and optionally the title line) below the image."""
    pad = max(8, img.width // 90)
    size = max(14, round(img.width / 42))
    credit = f"FAA-CT-8080-2H, {crop.label}. Public domain. Not for navigation."
    lines = []
    if with_title:
        lines.append((crop.title, fit_font(crop.title, img.width - 2 * pad, size, bold=True)))
    lines.append((credit, fit_font(credit, img.width - 2 * pad, size)))
    heights = [f.getbbox("Ag")[3] for _, f in lines]
    gap = pad // 2
    strip_h = 2 * pad + sum(heights) + gap * (len(lines) - 1)
    out = Image.new("RGB", (img.width, img.height + strip_h), STRIP_BG)
    out.paste(img, (0, 0))
    draw = ImageDraw.Draw(out)
    draw.line([(0, img.height), (img.width, img.height)], fill=RULE, width=1)
    y = img.height + pad
    for (text, font), h in zip(lines, heights):
        draw.text((pad, y), text, font=font, fill=STRIP_INK)
        y += h + gap
    return out


def encode(img: Image.Image, max_kb: int) -> tuple[str, bytes]:
    """Smaller of optimized PNG and JPG q85; lower JPG quality, then scale, to meet max_kb."""
    def png(im):
        b = io.BytesIO()
        im.save(b, "PNG", optimize=True)
        return b.getvalue()

    def jpg(im, q):
        b = io.BytesIO()
        im.save(b, "JPEG", quality=q, optimize=True, progressive=True, subsampling="4:2:0")
        return b.getvalue()

    candidates = [(".png", png(img)), (".jpg", jpg(img, 85))]
    ext, data = min(candidates, key=lambda c: len(c[1]))
    q = 85
    while len(data) > max_kb * 1024 and q > 60:
        q -= 5
        ext, data = ".jpg", jpg(img, q)
    while len(data) > max_kb * 1024:
        img = img.resize((round(img.width * 0.9), round(img.height * 0.9)), Image.LANCZOS)
        ext, data = ".jpg", jpg(img, q)
    return ext, data


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF,
                    help="FAA-CT-8080-2H PDF (default: the reduced copy in the repository)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output folder (default review/)")
    ap.add_argument("--only", nargs="+", metavar="NAME", help="make only these crops")
    ap.add_argument("--with-title", action="store_true", help="add the title line to the strip")
    ap.add_argument("--max-kb", type=int, default=350, help="size cap per file (default 350)")
    ap.add_argument("--list", action="store_true", help="print the crop table and exit")
    args = ap.parse_args()

    if args.list:
        for c in CROPS:
            print(f"{c.name:32s} {c.label:10s} p.{c.page:<3d} {c.box} {c.dpi} dpi  {c.title}")
        return

    crops = [c for c in CROPS if not args.only or c.name in args.only]
    unknown = set(args.only or []) - {c.name for c in CROPS}
    if unknown:
        raise SystemExit(f"unknown crop name(s): {', '.join(sorted(unknown))}")

    doc = fitz.open(args.pdf)
    args.out.mkdir(parents=True, exist_ok=True)
    for c in crops:
        page_index = find_label(doc, c.label, c.page)
        img = add_strip(render(doc, c, page_index), c, args.with_title)
        ext, data = encode(img, args.max_kb)
        for stale in (".png", ".jpg"):
            p = args.out / (c.name + stale)
            if stale != ext and p.exists():
                p.unlink()
        dest = args.out / (c.name + ext)
        dest.write_bytes(data)
        with Image.open(dest) as im:
            w, h = im.size
        print(f"{dest.name:36s} {w:5d} x {h:<5d} {len(data) / 1024:6.0f} KB  "
              f"page index {page_index} (PDF page {page_index + 1})")


if __name__ == "__main__":
    main()
