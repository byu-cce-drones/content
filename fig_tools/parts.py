"""Reusable drawing parts: one controller, one aircraft, one stick glyph.

Every part is drawn in its own local coordinates and returned together with a
dictionary of anchor points (in the same local coordinates) that figure scripts
use to attach callouts. Place a part with svgkit.translate(x, y, part) and add
(x, y) to the anchors.

Keep the geometry here stable: students should recognize the same controller
and the same aircraft in every figure across the course.
"""
from __future__ import annotations

import math

from svgkit import PALETTE as P
from svgkit import El, circle, comment, g, line, path, polygon, rect, text


# ---------------------------------------------------------------------------
# Controller
# ---------------------------------------------------------------------------
def controller(screen: str = "phone", mode_labels: bool = True):
    """A generic two-stick controller, 420 x 190 body at local origin (0, 0).

    screen: "phone"   a phone held in a clamp above the body
            "builtin" a screen built into the top of the body
            "none"    no screen

    Returns (element, anchors). Anchors point at the part edges that leader
    lines should touch.
    """
    grp = g(comment("generic controller"))

    # antennas
    grp.add(g(line(15, 2, -2, -95), line(405, 2, 422, -95),
              stroke=P["line"], stroke_width=7, stroke_linecap="round"))

    # screen options (drawn before the body so the body overlaps the join)
    if screen == "phone":
        grp.add(rect(136, -55, 14, 60, rx=3, fill="#555555"))
        grp.add(rect(270, -55, 14, 60, rx=3, fill="#555555"))
        grp.add(rect(130, -115, 160, 90, rx=10, fill=P["white"],
                     stroke=P["line"], stroke_width=2))
        grp.add(rect(140, -105, 140, 70, rx=4, fill=P["screen"],
                     stroke="#9bbbe0", stroke_width=1))
        screen_anchor = (210, -115)
    elif screen == "builtin":
        grp.add(rect(115, -78, 190, 90, rx=12, fill=P["body"],
                     stroke=P["line"], stroke_width=2))
        grp.add(rect(127, -68, 166, 62, rx=4, fill=P["screen"],
                     stroke="#9bbbe0", stroke_width=1))
        screen_anchor = (210, -78)
    else:
        screen_anchor = None

    # shoulder controls on the top edge
    grp.add(rect(45, -12, 44, 14, rx=7, fill=P["dark"], stroke="#222222"))
    grp.add(g(*[line(x, -10, x, 0) for x in (55, 62, 69, 76)],
              stroke="#888888", stroke_width=1))
    grp.add(rect(331, -12, 44, 14, rx=7, fill=P["dark"], stroke="#222222"))
    grp.add(circle(364, -5, 3.5, fill=P["bad"]))

    # body
    grp.add(rect(0, 0, 420, 190, rx=45, fill=P["body"], stroke=P["line"],
                 stroke_width=2))

    # sticks
    for cx in (90, 330):
        grp.add(circle(cx, 92, 32, fill="#b8c0c8", stroke=P["line"],
                       stroke_width=1.5))
        grp.add(circle(cx, 92, 15, fill=P["line"]))
        grp.add(circle(cx, 92, 6, fill="#666666"))

    # return-to-home / pause
    grp.add(circle(210, 45, 12, fill=P["white"], stroke=P["line"],
                   stroke_width=1.5))
    grp.add(text(210, 50, "H", text_anchor="middle", font_size=12,
                 font_weight="bold", fill=P["ink"]))

    # flight mode switch
    grp.add(rect(175, 72, 70, 16, rx=8, fill="#eeeeee", stroke=P["line"],
                 stroke_width=1.5))
    grp.add(circle(210, 80, 6, fill=P["accent"], stroke=P["ink"],
                   stroke_width=1))
    if mode_labels:
        for x, s in ((185, "C"), (210, "N"), (235, "S")):
            grp.add(text(x, 102, s, text_anchor="middle", font_size=9,
                         fill=P["muted"]))

    # power button and battery lights
    grp.add(circle(190, 152, 8, fill=P["white"], stroke=P["line"],
                   stroke_width=1.5))
    grp.add(path("M190 147 v5 M186.5 149.5 a4.5 4.5 0 1 0 7 0",
                 stroke=P["line"], stroke_width=1.5, fill="none",
                 stroke_linecap="round"))
    for i, cx in enumerate((215, 227, 239, 251)):
        grp.add(circle(cx, 152, 3.5, fill=P["ok"] if i < 3 else P["off"],
                       stroke=None if i < 3 else "#999999",
                       stroke_width=None if i < 3 else 0.5))

    # charging / data port
    grp.add(rect(201, 183, 18, 6, rx=3, fill=P["line"]))

    anchors = {
        "left_stick": (58, 92),
        "right_stick": (362, 92),
        "rth": (198, 45),
        "mode_switch": (247, 80),
        "power": (190, 161),
        "battery": (233, 158),
        "port": (210, 190),
        "gimbal_dial": (65, -12),
        "shutter": (353, -12),
        "antenna_left": (2, -75),
        "antenna_right": (418, -75),
        "screen": screen_anchor,
    }
    return grp, anchors


def shift(anchors: dict, dx: float, dy: float) -> dict:
    """Return anchors moved by (dx, dy), skipping None entries."""
    return {k: (v[0] + dx, v[1] + dy) for k, v in anchors.items() if v}


# ---------------------------------------------------------------------------
# Control stick glyph, and small aircraft icons for multi-panel figures
# ---------------------------------------------------------------------------
def stick(dx: float = 0, dy: float = 0, r: float = 30,
          active: bool = True) -> El:
    """One control stick seen from above, knob pushed by (dx, dy) in -1..1.

    Drawn at the local origin. A dashed outline shows the neutral position and
    an arrow shows which way the thumb pushes. An inactive stick is drawn pale,
    so a figure can show both sticks and highlight only the one in use.
    """
    from svgkit import arrow as _arrow

    edge = P["line"] if active else "#c8d0d8"
    knob = P["dark"] if active else "#c8d0d8"

    grp = g(circle(0, 0, r, fill=P["white"], stroke=edge, stroke_width=1.5))
    grp.add(circle(0, 0, r * 0.34, fill="none", stroke="#cccccc",
                   stroke_width=1, stroke_dasharray="3 3"))
    kx, ky = dx * r * 0.52, dy * r * 0.52
    grp.add(circle(kx, ky, r * 0.34, fill=knob, stroke=edge,
                   stroke_width=1.2))
    if active and (dx or dy):
        mag = (dx ** 2 + dy ** 2) ** 0.5
        ux, uy = dx / mag, dy / mag
        grp.add(_arrow(ux * r * 1.02, uy * r * 1.02,
                       ux * (r + 15), uy * (r + 15), width=2.5, head=8))
    return grp


def stick_pair(side: str, dx: float, dy: float, r: float = 20,
               gap: float = 38, body: bool = True) -> El:
    """Both sticks side by side, with only `side` ("left" or "right") active.

    A light rounded outline stands in for the controller, so the pair reads as
    one handset rather than two loose dials. Push arrows deliberately poke a
    little past it.
    """
    left_active = side == "left"
    grp = g()
    if body:
        pad = 12
        w, h = 2 * (gap + r + pad), 2 * (r + pad)
        grp.add(rect(-w / 2, -h / 2, w, h, rx=h * 0.34, fill="#eef1f4",
                     stroke="#c5cdd5", stroke_width=1.5))
    grp.add(
        g(stick(dx, dy, r, True) if left_active else stick(0, 0, r, False),
          transform=f"translate({-gap},0)"),
        g(stick(0, 0, r, False) if left_active else stick(dx, dy, r, True),
          transform=f"translate({gap},0)"),
    )
    return grp


def aircraft_mini_top(r: float = 1.0) -> El:
    """A small quadcopter seen from above, nose up. Roughly 92 x 78 at r=1."""
    grp = g()
    motors = [(-30, -24), (30, -24), (-30, 24), (30, 24)]
    grp.add(g(*[line(mx * 0.28, my * 0.5, mx, my) for mx, my in motors],
              stroke=P["line"], stroke_width=5, stroke_linecap="round"))
    grp.add(g(*[circle(mx, my, 15) for mx, my in motors],
              fill="#e8edf2", stroke="#b6c2cc", stroke_width=1))
    grp.add(g(*[circle(mx, my, 5) for mx, my in motors], fill=P["dark"]))
    grp.add(rect(-11, -20, 22, 40, rx=6, fill=P["body"], stroke=P["line"],
                 stroke_width=1.5))
    # a solid arrowhead marks the nose, so a rotated aircraft is readable
    grp.add(polygon([(0, -37), (-11, -21), (11, -21)], fill=P["dark"],
                    stroke=P["line"], stroke_width=1))
    return g(grp, transform=f"scale({r})") if r != 1.0 else grp


def aircraft_mini_side(r: float = 1.0, nose: bool = True) -> El:
    """A small quadcopter seen from the side, nose to the right.

    Set nose=False for a head-on view, where neither end should look like the
    front (used for the roll panel).
    """
    grp = g()
    grp.add(rect(-22, -8, 44, 18, rx=6, fill=P["body"], stroke=P["line"],
                 stroke_width=1.5))
    if nose:
        grp.add(polygon([(22, -7), (32, 1), (22, 9)], fill=P["dark"],
                        stroke=P["line"], stroke_width=1))
    for mx in (-34, 34):
        grp.add(line(mx, -8, mx, -18, stroke=P["line"], stroke_width=4,
                     stroke_linecap="round"))
        grp.add(line(mx - 17, -20, mx + 17, -20, stroke=P["dark"],
                     stroke_width=4, stroke_linecap="round"))
        grp.add(line(mx * 0.6, -2, mx, -10, stroke=P["line"], stroke_width=4,
                     stroke_linecap="round"))
    for fx in (-14, 14):
        grp.add(line(fx, 10, fx, 20, stroke=P["dark"], stroke_width=4,
                     stroke_linecap="round"))
    grp.add(rect(-6, -4, 10, 9, rx=3, fill=P["dark"]))
    return g(grp, transform=f"scale({r})") if r != 1.0 else grp


# ---------------------------------------------------------------------------
# People and vehicles, for scale and for the rules figures
# ---------------------------------------------------------------------------
def person(x: float, y: float, scale: float = 1.0, fill: str | None = None) -> El:
    """A simple standing figure, drawn with its feet on (x, y)."""
    fill = fill or P["dark"]
    return g(
        g(circle(0, -14, 7, fill=fill),
          path("M-8,3 a8,10 0 0,1 16,0 z", fill=fill),
          transform=f"scale({scale})" if scale != 1 else None),
        transform=f"translate({x},{y})")


def car(x: float, y: float, scale: float = 1.0) -> El:
    """A car seen from the side, drawn about its own centre."""
    return g(
        g(path("M-30,4 l7,-13 h32 l9,13 z", fill="#7a8794", stroke=P["line"],
               stroke_width=1.5),
          rect(-34, 4, 68, 11, rx=4, fill="#8f9aa6", stroke=P["line"],
               stroke_width=1.5),
          circle(-18, 16, 6, fill=P["dark"]),
          circle(18, 16, 6, fill=P["dark"]),
          transform=f"scale({scale})" if scale != 1 else None),
        transform=f"translate({x},{y})")


# ---------------------------------------------------------------------------
# Rotation arrow, used to show which way a propeller turns
# ---------------------------------------------------------------------------
def rotation_arrow(cx: float, cy: float, r: float, clockwise: bool = True,
                   start_deg: float = 150, sweep_deg: float = 210,
                   color: str | None = None, width: float = 2.5) -> El:
    """A circular arrow around (cx, cy). Angles are in screen coordinates,
    where y grows downward, so increasing angle reads as clockwise."""
    color = color or P["accent"]
    a0 = math.radians(start_deg)
    a1 = math.radians(start_deg + (sweep_deg if clockwise else -sweep_deg))
    p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
    p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
    large = 1 if sweep_deg > 180 else 0
    sweep = 1 if clockwise else 0

    # tangent at the end of the arc, then a triangular head on it
    tx, ty = (-math.sin(a1), math.cos(a1)) if clockwise else (math.sin(a1), -math.cos(a1))
    nx, ny = -ty, tx
    tip = (p1[0] + tx * 10, p1[1] + ty * 10)
    left = (p1[0] + nx * 5, p1[1] + ny * 5)
    right = (p1[0] - nx * 5, p1[1] - ny * 5)

    return g(
        path(f"M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 {large},{sweep} "
             f"{p1[0]:.1f},{p1[1]:.1f}",
             fill="none", stroke=color, stroke_width=width,
             stroke_linecap="round"),
        polygon([tip, left, right], fill=color),
    )


# ---------------------------------------------------------------------------
# Aircraft, top view
# ---------------------------------------------------------------------------
def aircraft_top(show_rotation: bool = True, prop_style: str = "blades"):
    """A generic quadcopter seen from above, nose pointing up.

    Origin (0, 0) is the center of the aircraft. Roughly 400 wide by 330 tall
    including the propeller discs.

    prop_style: "blades" draws a disc plus a two-blade propeller
                "disc"   draws the disc only, for small or busy figures
    """
    grp = g(comment("generic quadcopter, top view"))

    motors = {
        "fl": (-130, -100), "fr": (130, -100),
        "rl": (-130, 100), "rr": (130, 100),
    }
    # diagonally opposite motors turn the same way
    spin = {"fl": True, "rr": True, "fr": False, "rl": False}
    blade_angle = {"fl": 30, "fr": -25, "rl": -15, "rr": 35}

    # arms, drawn first so the body and motors sit on top
    arms = g(stroke=P["line"], stroke_width=15, stroke_linecap="round")
    arms_fill = g(stroke=P["body"], stroke_width=11, stroke_linecap="round")
    for key, (mx, my) in motors.items():
        bx = 32 * (1 if mx > 0 else -1)
        by = 46 * (1 if my > 0 else -1)
        arms.add(line(bx, by, mx, my))
        arms_fill.add(line(bx, by, mx, my))
    grp.add(arms, arms_fill)

    # landing feet, under the rear of the body
    for fx in (-35, 35):
        grp.add(rect(fx - 7, 66, 14, 22, rx=5, fill=P["dark"],
                     stroke=P["line"], stroke_width=1.5))

    # propeller discs and blades
    discs = g(fill="#e8edf2", stroke="#b6c2cc", stroke_width=1,
              stroke_dasharray="4 4")
    for mx, my in motors.values():
        discs.add(circle(mx, my, 64))
    grp.add(discs)

    if prop_style == "blades":
        blades = g(fill="#9aa7b2", stroke=P["line"], stroke_width=1.2)
        for key, (mx, my) in motors.items():
            blades.add(El("ellipse", cx=0, cy=0, rx=60, ry=8,
                          transform=f"translate({mx},{my}) rotate({blade_angle[key]})"))
        grp.add(blades)

    # motors
    for mx, my in motors.values():
        grp.add(circle(mx, my, 17, fill=P["dark"], stroke=P["line"],
                       stroke_width=1.5))
        grp.add(circle(mx, my, 6, fill="#888888"))

    # body
    grp.add(rect(-45, -75, 90, 150, rx=18, fill=P["body"], stroke=P["line"],
                 stroke_width=2))

    # satellite receiver and compass, inside the body
    grp.add(rect(-26, -40, 52, 38, rx=5, fill="none", stroke=P["muted"],
                 stroke_width=1.2, stroke_dasharray="4 3"))
    grp.add(text(0, -17, "GNSS", text_anchor="middle", font_size=10,
                 fill=P["muted"]))

    # battery, in the rear half
    grp.add(rect(-30, 8, 60, 52, rx=6, fill="#c2cad2", stroke=P["line"],
                 stroke_width=1.5))
    grp.add(g(*[line(-20 + i * 13, 20, -20 + i * 13, 48) for i in range(4)],
              stroke="#96a1ab", stroke_width=2))

    # camera and gimbal, hanging off the nose
    grp.add(rect(-16, -96, 32, 26, rx=7, fill=P["dark"], stroke=P["line"],
                 stroke_width=1.5))
    grp.add(circle(0, -83, 8, fill="#1b2733", stroke="#6b7c8c",
                   stroke_width=1.5))

    # forward obstacle sensors
    for sx in (-30, 30):
        grp.add(circle(sx, -70, 5, fill="#2b3a47", stroke=P["line"],
                       stroke_width=1))

    # status light at the tail
    grp.add(circle(0, 66, 6, fill=P["bad"], stroke=P["line"], stroke_width=1))

    if show_rotation:
        for key, (mx, my) in motors.items():
            grp.add(rotation_arrow(mx, my, 40, clockwise=spin[key]))

    anchors = {
        "propeller": (-130 - 58, -100 - 26),   # upper-left blade tip
        "motor": (-130, -100),
        "arm": (-80, -74),
        "camera": (0, -96),
        "sensors": (30, -70),
        "gnss": (26, -30),
        "battery": (30, 34),
        "status_light": (0, 72),
        "feet": (35, 88),
        "rotation": (130 + 40, -100 + 30),     # near the front-right arrow
    }
    return grp, anchors
