"""Tiny zero-dependency SVG builder for course figures.

Every figure script in this folder builds a tree of elements with the helpers
below and writes plain SVG. No third-party packages are needed, so a TA can run
the scripts with any Python 3.8+ interpreter.

Style constants (palette, font, title placement) live here so every figure on
the site looks the same. Change them here, re-run the scripts, and every figure
updates together.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from xml.sax.saxutils import escape

# ---------------------------------------------------------------------------
# Shared style
# ---------------------------------------------------------------------------
PALETTE = {
    "bg": "#f9f9f9",       # figure background
    "ink": "#1a1a1a",      # titles and labels
    "muted": "#555555",    # subtitles, secondary labels
    "line": "#333333",     # outlines
    "body": "#d0d7de",     # plastic bodies (controller, aircraft)
    "dark": "#444444",     # dark plastic parts
    "accent": "#4a90d9",   # leader lines, highlights, number badges
    "screen": "#dceefb",   # screens, sky
    "ok": "#27ae60",       # green lights
    "warn": "#f39c12",     # amber
    "bad": "#e74c3c",      # red
    "off": "#cccccc",      # inactive
    "white": "#ffffff",
}
FONT = "Arial, Helvetica, sans-serif"
LABEL_SIZE = 14
TITLE_SIZE = 17
SUBTITLE_SIZE = 12


# ---------------------------------------------------------------------------
# File naming
# ---------------------------------------------------------------------------
def figure_name(week: int, number: int | None, slug: str,
                variant: str = "") -> str:
    """Build a figure's file name from its week and figure number.

    Every numbered figure is named wNN_figMM_slug.svg, so an exported file
    still says which week and which figure it is once it is out of the
    repository. Pass number=None for an illustration that nothing refers to by
    number; it becomes wNN_slug.svg and takes no number from the sequence.
    Deriving the name here keeps it from drifting away from the number printed
    inside the drawing.
    """
    if number is None:
        # an illustration nothing cross-references, so it carries no number
        return f"w{week:02d}_{slug}.svg"
    return f"w{week:02d}_fig{number:02d}{variant}_{slug}.svg"


# ---------------------------------------------------------------------------
# Elements
# ---------------------------------------------------------------------------
def _attr_name(key: str) -> str:
    """class_ -> class, stroke_width -> stroke-width, viewBox stays viewBox."""
    return key.rstrip("_").replace("_", "-")


def _attrs(attrs: dict) -> str:
    return "".join(
        f' {_attr_name(k)}="{v}"' for k, v in attrs.items() if v is not None
    )


class El:
    """A generic SVG element. Children may be El instances or raw strings."""

    def __init__(self, tag: str, *children, **attrs):
        self.tag = tag
        self.children = list(children)
        self.attrs = attrs

    def add(self, *els) -> "El":
        self.children.extend(e for e in els if e is not None)
        return self

    def render(self, indent: int = 0) -> str:
        pad = "  " * indent
        a = _attrs(self.attrs)
        if not self.children:
            return f"{pad}<{self.tag}{a}/>"
        if all(isinstance(c, str) for c in self.children):
            return f"{pad}<{self.tag}{a}>{''.join(self.children)}</{self.tag}>"
        inner = "\n".join(
            c.render(indent + 1) if isinstance(c, El) else f"{pad}  {c}"
            for c in self.children
        )
        return f"{pad}<{self.tag}{a}>\n{inner}\n{pad}</{self.tag}>"

    def __str__(self) -> str:
        return self.render()


class Comment(El):
    def __init__(self, text: str):
        super().__init__("!--")
        self.text = text

    def render(self, indent: int = 0) -> str:
        return f"{'  ' * indent}<!-- {self.text} -->"


def comment(text: str) -> Comment:
    return Comment(text)


def g(*children, **attrs) -> El:
    return El("g", *children, **attrs)


def rect(x, y, w, h, **attrs) -> El:
    return El("rect", x=x, y=y, width=w, height=h, **attrs)


def circle(cx, cy, r, **attrs) -> El:
    return El("circle", cx=cx, cy=cy, r=r, **attrs)


def line(x1, y1, x2, y2, **attrs) -> El:
    return El("line", x1=x1, y1=y1, x2=x2, y2=y2, **attrs)


def path(d, **attrs) -> El:
    return El("path", d=d, **attrs)


def polygon(points, **attrs) -> El:
    pts = " ".join(f"{x},{y}" for x, y in points)
    return El("polygon", points=pts, **attrs)


def text(x, y, s, **attrs) -> El:
    return El("text", escape(str(s)), x=x, y=y, **attrs)


def arrow(x1, y1, x2, y2, color: str | None = None, width: float = 3,
          head: float = 10) -> El:
    """A straight arrow from (x1, y1) to (x2, y2), with a solid head."""
    import math

    color = color or PALETTE["accent"]
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1
    ux, uy = dx / length, dy / length
    # stop the shaft where the head begins, so the tip stays sharp
    sx, sy = x2 - ux * head, y2 - uy * head
    nx, ny = -uy, ux
    return g(
        line(x1, y1, sx, sy, stroke=color, stroke_width=width,
             stroke_linecap="round"),
        polygon([(x2, y2),
                 (sx + nx * head * 0.5, sy + ny * head * 0.5),
                 (sx - nx * head * 0.5, sy - ny * head * 0.5)], fill=color),
    )


def translate(x, y, *children, scale: float | None = None) -> El:
    t = f"translate({x},{y})"
    if scale is not None and scale != 1:
        t += f" scale({scale})"
    return g(*children, transform=t)


# ---------------------------------------------------------------------------
# Figure canvas
# ---------------------------------------------------------------------------
class Figure(El):
    """An SVG canvas with the course's standard background and title block.

    Title sits at y=28, subtitle at y=46. Content should start below y=60.
    """

    def __init__(self, width: int, height: int, title: str | None = None,
                 subtitle: str | None = None):
        super().__init__(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            viewBox=f"0 0 {width} {height}",
            font_family=FONT,
            font_size=LABEL_SIZE,
        )
        self.width, self.height = width, height
        self.add(rect(0, 0, width, height, fill=PALETTE["bg"], rx=8))
        if title:
            self.add(text(width / 2, 28, title, text_anchor="middle",
                          font_size=TITLE_SIZE, font_weight="bold",
                          fill=PALETTE["ink"]))
        if subtitle:
            self.add(text(width / 2, 46, subtitle, text_anchor="middle",
                          font_size=SUBTITLE_SIZE, fill=PALETTE["muted"]))

    def save(self, filename: str) -> str:
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        with open(filename, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(self.render() + "\n")
        return filename


# ---------------------------------------------------------------------------
# Callouts: labels with leader lines, in "names" or "numbers" mode
# ---------------------------------------------------------------------------
class Callouts:
    """Collects labeled callouts and renders them as names or as number badges.

    add(label, at, anchor, start, target, n, sub)
        label   text shown in names mode
        at      (x, y) baseline position of the label text
        anchor  "start" | "middle" | "end" text-anchor
        start   (x, y) where the leader line begins, next to the label
        target  (x, y) the part being pointed at (gets a dot)
        n       number shown in numbers mode; repeat a number for paired parts
        sub     optional smaller second line under the label
    """

    def __init__(self):
        self.items: list[dict] = []

    def add(self, label, at, anchor, start, target, n=None, sub=None,
            bold=False) -> "Callouts":
        self.items.append(dict(label=label, at=at, anchor=anchor, start=start,
                               target=target, n=n, sub=sub, bold=bold))
        return self

    def leaders(self) -> El:
        lines = g(stroke=PALETTE["accent"], stroke_width=1.5, fill="none")
        dots = g(fill=PALETTE["accent"])
        for it in self.items:
            (sx, sy), (tx, ty) = it["start"], it["target"]
            lines.add(line(sx, sy, tx, ty))
            dots.add(circle(tx, ty, 3))
        return g(comment("leader lines"), lines, dots)

    def names(self) -> El:
        grp = g(id="names", fill=PALETTE["ink"])
        for it in self.items:
            x, y = it["at"]
            grp.add(text(x, y, it["label"], text_anchor=it["anchor"],
                         font_weight="bold" if it["bold"] else None))
            if it["sub"]:
                grp.add(text(x, y + 16, it["sub"], text_anchor=it["anchor"],
                             font_size=SUBTITLE_SIZE, fill=PALETTE["muted"]))
        return grp

    def numbers(self) -> El:
        grp = g(id="numbers")
        for it in self.items:
            if it["n"] is None:
                continue
            x, y = it["at"]
            dx = {"end": -10, "start": 10, "middle": 0}[it["anchor"]]
            badge = translate(x + dx, y - 4,
                              circle(0, 0, 11, fill=PALETTE["accent"]),
                              text(0, 4, it["n"], text_anchor="middle",
                                   font_size=12, font_weight="bold",
                                   fill=PALETTE["white"]))
            grp.add(badge)
        return grp


# ---------------------------------------------------------------------------
# Optional PNG render through Inkscape, for checking figures
# ---------------------------------------------------------------------------
INKSCAPE_CANDIDATES = [
    "inkscape",
    r"C:\Program Files\Inkscape\bin\inkscape.com",
    r"C:\Program Files\Inkscape\bin\inkscape.exe",
    r"C:\Program Files (x86)\Inkscape\bin\inkscape.com",
    "/Applications/Inkscape.app/Contents/MacOS/inkscape",
    "/usr/bin/inkscape",
]


def find_inkscape() -> str | None:
    """Locate the Inkscape executable.

    Set the INKSCAPE environment variable to override, for example:
        set INKSCAPE=D:\\Tools\\Inkscape\\bin\\inkscape.com
    """
    override = os.environ.get("INKSCAPE")
    if override:
        return override
    for cand in INKSCAPE_CANDIDATES:
        if os.path.isfile(cand) or shutil.which(cand):
            return cand
    return None


def render_png(svg_path: str, width: int = 1350) -> str | None:
    """Render an SVG to a PNG next to it. Returns the PNG path or None.

    PNGs are for checking a figure only. The site always uses the SVG.
    """
    exe = find_inkscape()
    if not exe:
        print("Inkscape not found; skipping PNG render. "
              "Set the INKSCAPE environment variable to its full path.")
        return None
    png_path = os.path.splitext(svg_path)[0] + ".png"
    subprocess.run(
        [exe, svg_path, "--export-type=png",
         f"--export-filename={png_path}", f"--export-width={width}"],
        check=True, capture_output=True,
    )
    return png_path
