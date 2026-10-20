"""Part 107 regulation figures for the Part 107 overview reading and the
Week 3 and Week 9 lecture decks.

    w05_fig07_exam_topics.svg        what the knowledge test covers (2025 weights)
    w05_fig15_waivable.svg           which rules a certificate of waiver can relax
    w05_fig15b_ops_over_people.svg   the four categories for flying over people
    w05_fig25_currency.svg           staying current: training every 24 months
    w05_fig27_remote_id.svg          three ways to comply with Remote ID

Every rule drawn here was checked against the eCFR text of 14 CFR Parts 89
and 107 (2026-10-15 issue) and the PSI UAG Applicant Information Bulletin
effective 2025-09-29. Figure 7 replaces an older hand-made drawing of the
same name that showed the superseded ACS ranges. 15b is a lettered variant
so it sits beside Figure 15 without moving any number after it.

Usage:
    python fig_tools/fig_part107_rules.py --out review --png
    python fig_tools/fig_part107_rules.py --out docs/part_107_license/images
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parts import aircraft_mini_top, person  # noqa: E402
from svgkit import PALETTE as P  # noqa: E402
from svgkit import (Callouts, El, Figure, arrow, circle, figure_name,  # noqa: E402
                    g, line, path, rect, render_png, text, translate)

W = 900
CARD = dict(rx=10, fill=P["white"], stroke="#dde3e9", stroke_width=1.5)
BLUE = P["accent"]
GREEN = "#2f8f4e"
ORANGE = P["warn"]
RED = P["bad"]
BLUE_FILL = "#e8f1fb"
ORANGE_FILL = "#fdf3e6"
RED_FILL = "#fdecea"
GREEN_FILL = "#e6f4ea"


def _t(fig, x, y, s, size=12, bold=False, fill=None, anchor="middle",
       italic=False):
    fig.add(text(x, y, s, text_anchor=anchor, font_size=size,
                 font_weight="bold" if bold else None,
                 font_style="italic" if italic else None,
                 fill=fill or P["ink"]))


def _lines(fig, x, y, lines, size=11.5, pitch=16, fill=None, anchor="start",
           italic=False):
    """Several short lines of text, one under the other. Returns the y of the
    next free line."""
    for i, s in enumerate(lines):
        _t(fig, x, y + i * pitch, s, size=size, fill=fill or P["muted"],
           anchor=anchor, italic=italic)
    return y + len(lines) * pitch


def _chip(fig, x, y, w, name, section, fill, stroke, h=30):
    """A rounded label: plain-English name on the left, CFR section on the
    right."""
    fig.add(rect(x, y, w, h, rx=h / 2, fill=fill, stroke=stroke,
                 stroke_width=1.2))
    _t(fig, x + 16, y + h / 2 + 4.5, name, size=13, anchor="start")
    _t(fig, x + w - 16, y + h / 2 + 4.5, section, size=11.5, fill=P["muted"],
       anchor="end")


# ---------------------------------------------------------------------------
# 7. What the knowledge test covers
# ---------------------------------------------------------------------------
# PSI UAG Applicant Information Bulletin, effective 2025-09-29: per cent of
# the 60 scored items, with the approximate question count that implies.
TOPICS = [
    ("Regulations", 48, 29,
     "operating rules, certification, waivers, flying over people, Remote ID"),
    ("Operations", 25, 15,
     "radio and airports, emergencies, decision-making, physiology, maintenance"),
    ("Airspace", 20, 12,
     "airspace classes, authorization, reading sectional charts"),
    ("Weather", 5, 3,
     "weather sources and effects, METAR and TAF"),
    ("Loading and Performance", 2, 1,
     "weight and balance, density altitude, load factor"),
]


def build_exam_topics() -> Figure:
    fig = Figure(W, 462, "Figure 7: What the knowledge test covers",
                 "60 scored questions. Weights from the PSI applicant bulletin, "
                 "effective 29 Sept 2025; older study guides show different "
                 "ranges.")
    x0, scale, bar_h = 262, 9.0, 22
    y = 104
    # a recessive baseline the bars grow from
    fig.add(line(x0, y - 24, x0, y + 4 * 66 + 12, stroke="#b6c2cc",
                 stroke_width=1))
    for name, pct, n, example in TOPICS:
        w = pct * scale
        _t(fig, x0 - 16, y, name, size=14, bold=True, anchor="end")
        fig.add(rect(x0, y - 16, w, bar_h, rx=4, fill=BLUE))
        label = El("text", El("tspan", f"{pct} %", font_weight="bold"),
                   El("tspan", f"about {n} question{'s' if n > 1 else ''}",
                      fill=P["muted"], font_size=12, dx=8),
                   x=x0 + w + 10, y=y, font_size=14, fill=P["ink"])
        if pct == 2:
            label.add(El("tspan", "small but tested", font_weight="bold",
                         font_size=12.5, fill=ORANGE, dx=14))
        fig.add(label)
        _t(fig, x0, y + 24, example, size=12, fill=P["muted"], anchor="start")
        y += 66
    _t(fig, W / 2, 438,
       "Regulations alone are nearly half the test. Five unscored trial "
       "questions are mixed in, so the screen shows 65.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 15. Which rules can be waived
# ---------------------------------------------------------------------------
# The ten sections listed in 14 CFR 107.205, in the order the rule lists them.
WAIVABLE = [
    ("Flying from a moving vehicle or aircraft", "§107.25"),
    ("Lights at night and civil twilight", "§107.29(a)(2), (b)"),
    ("Visual line of sight", "§107.31"),
    ("Visual observer", "§107.33"),
    ("One pilot flying several aircraft", "§107.35"),
    ("Yielding the right of way", "§107.37(a)"),
    ("Flying over people", "§107.39"),
    ("Flying in controlled airspace", "§107.41"),
    ("Altitude, speed, visibility, cloud clearance", "§107.51"),
    ("Flying over moving vehicles", "§107.145"),
]
# Rules students ask about that are not on that list, so no waiver exists.
NOT_WAIVABLE = [
    ("Careless or reckless flying; dropping things", "§107.23"),
    ("Alcohol or drugs", "§107.27"),
    ("Carrying hazardous material", "§107.36"),
    ("Transponder or ADS-B Out switched on", "§107.52, .53"),
    ("Registering the aircraft", "§107.13"),
]


def build_waivable() -> Figure:
    fig = Figure(W, 572, "Figure 15: Which rules can be waived?",
                 "A certificate of waiver (§107.200) can relax only the ten "
                 "rules listed in §107.205. Everything else in Part 107 stands "
                 "as written.")
    # left: the ten
    lx, lw = 30, 440
    fig.add(rect(lx, 84, lw, 432, **CARD))
    _t(fig, lx + lw / 2, 110, "Can be waived (§107.205)", size=14, bold=True,
       fill=BLUE)
    for i, (name, sec) in enumerate(WAIVABLE):
        _chip(fig, lx + 16, 128 + i * 38, lw - 32, name, sec, BLUE_FILL, BLUE)
    # right: short and absolute
    rx, rw = 495, 375
    fig.add(rect(rx, 84, rw, 432, **CARD))
    _t(fig, rx + rw / 2, 110, "Cannot be waived", size=14, bold=True, fill=RED)
    for i, (name, sec) in enumerate(NOT_WAIVABLE):
        _chip(fig, rx + 16, 128 + i * 38, rw - 32, name, sec, RED_FILL, RED)
    _lines(fig, rx + rw / 2, 352, [
        "…and every other section that is not",
        "on the left. The FAA has no form for",
        "those, so there is nothing to apply for.",
    ], size=12, pitch=17, anchor="middle")
    _lines(fig, rx + rw / 2, 428, [
        "Even a waiver never allows carrying",
        "someone else's property for hire beyond",
        "line of sight or from a moving vehicle",
        "(§107.25, §107.31).",
    ], size=11.5, pitch=16, anchor="middle", italic=True)
    _t(fig, W / 2, 540,
       "Night flying needs no waiver since April 2021: anti-collision lights "
       "visible 3 statute miles and current training (§107.29).",
       size=12, fill=P["muted"], italic=True)
    _t(fig, W / 2, 558,
       "Apply for a waiver through FAA DroneZone with a safety case; the "
       "Part 107 waiver is the exam's name for that paperwork.",
       size=12, fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 15b. Flying over people: the four categories
# ---------------------------------------------------------------------------
# (header, key figure, what the key figure is, body lines)
CATEGORIES = [
    ("Category 1", "0.55 lb or less", "takeoff weight, everything on board",
     ["No Declaration of Compliance",
      "needed. No exposed rotating",
      "parts that could cut skin.",
      "",
      "Weigh it with everything attached:",
      "lights, guards, payload."],
     "§107.110"),
    ("Category 2", "under 11 ft·lb", "impact energy on a person",
     ["FAA-accepted Declaration of",
      "Compliance from the maker,",
      "and a category label on the",
      "aircraft. No exposed parts",
      "that could cut skin."],
     "§107.115, §107.120"),
    ("Category 3", "under 25 ft·lb", "impact energy on a person",
     ["Declaration and label, plus:",
      "only over a closed or restricted",
      "site with people on notice, or",
      "no sustained flight over anyone",
      "not under cover.",
      "Never over open-air assemblies."],
     "§107.125, §107.130"),
    ("Category 4", "Airworthiness certificate", "issued under Part 21",
     ["Certified like a manned",
      "aircraft: flown to its Flight",
      "Manual limits, maintained",
      "and inspected to its manual,",
      "records kept."],
     "§107.140"),
]


def _crowd(fig, cx, y, n=3, gap=22):
    for i in range(n):
        fig.add(person(cx + (i - (n - 1) / 2) * gap, y, 0.9,
                       fill="#7a8794"))


def build_ops_over_people() -> Figure:
    fig = Figure(W, 504, "Figure 15b: Flying over people, the four categories",
                 "§107.39 and Subpart D. No category is needed over people "
                 "taking part, under a covered structure, or inside a "
                 "stationary vehicle.")
    cw, gap, x0 = 207, 10, 24
    for i, (head, key, key_sub, body, sec) in enumerate(CATEGORIES):
        x = x0 + i * (cw + gap)
        cx = x + cw / 2
        fig.add(rect(x, 84, cw, 280, **CARD))
        fig.add(rect(cx - 56, 94, 112, 26, rx=13, fill=BLUE))
        _t(fig, cx, 112, head, size=13, bold=True, fill=P["white"])
        # the scene: an aircraft over three people
        fig.add(translate(cx, 150, aircraft_mini_top(0.42)))
        _crowd(fig, cx, 186)
        _t(fig, cx, 212, key, size=16 if i < 3 else 14.5, bold=True,
           fill=BLUE)
        _t(fig, cx, 229, key_sub, size=11, fill=P["muted"])
        _lines(fig, x + 14, 252, body, size=11.5, pitch=16)
        _t(fig, cx, 354, sec, size=10.5, fill=P["muted"])
    # the declaration of compliance, the most-missed exam item
    fig.add(rect(24, 380, 858, 62, rx=10, fill=ORANGE_FILL, stroke=ORANGE,
                 stroke_width=1.5))
    _t(fig, W / 2, 404,
       "Declaration of Compliance: the manufacturer declares it, the FAA "
       "accepts it, the label on the aircraft shows the category.",
       size=13, bold=True)
    _t(fig, W / 2, 426,
       "The pilot's job is to check the label. This is the most-missed item "
       "on the knowledge test (FAA statistics, 2023 to 2025).",
       size=12, fill=P["muted"])
    _t(fig, W / 2, 466,
       "Sustained flight over an open-air assembly (a crowd): Categories 1, "
       "2 and 4 only with Remote ID (§89.110 or §89.115(a));",
       size=12, fill=P["muted"], italic=True)
    _t(fig, W / 2, 484, "Category 3 never (§107.125).", size=12,
       fill=P["muted"], italic=True)
    return fig


# ---------------------------------------------------------------------------
# 25. Staying current
# ---------------------------------------------------------------------------
def build_currency() -> Figure:
    fig = Figure(W, 444, "Figure 25: Staying current",
                 "The certificate never expires. The right to use it does: "
                 "recurrent training every 24 calendar months (§107.65).")
    fig.add(rect(30, 84, 840, 266, **CARD))
    ay = 200
    n0, n1, n2, end = 150, 420, 690, 850          # 270 px per 24 months
    fig.add(line(70, ay, end - 14, ay, stroke="#9aa7b2", stroke_width=2))
    fig.add(arrow(end - 30, ay, end, ay, color="#9aa7b2", width=2, head=10))
    for x, lab in ((n0, "month 0"), (n1, "24 calendar months"),
                   (n2, "48 months")):
        fig.add(line(x, ay - 6, x, ay + 6, stroke="#9aa7b2", stroke_width=2))
    # the certificate: one bar along the whole line, it never ends
    # "current" bands between the training events
    for xa, xb in ((n0, n1), (n1, n2)):
        fig.add(rect(xa, ay + 12, xb - xa, 12, fill=GREEN_FILL, stroke=GREEN,
                     stroke_width=1.2))
        _t(fig, (xa + xb) / 2, ay + 22, "current", size=11, bold=True,
           fill=GREEN)
    fig.add(rect(n2, ay + 12, end - 30 - n2, 12, fill=GREEN_FILL, stroke=GREEN,
                 stroke_width=1.2, stroke_dasharray="4 3"))
    _t(fig, (n2 + end - 30) / 2, ay + 22, "and on", size=11, bold=True,
       fill=GREEN)
    # events
    for x, head, subs in (
        (n0, "Pass the knowledge test",
         ["certificate issued;", "it does not expire"]),
        (n1, "Recurrent training",
         ["free online course, FAA Safety Team", "ALC-677; no retest since April 2021"]),
        (n2, "Recurrent training again",
         ["every 24 calendar months", "for as long as you fly"]),
    ):
        fig.add(circle(x, ay, 11, fill=BLUE, stroke=P["white"],
                       stroke_width=2))
        _t(fig, x, 142, head, size=13.5, bold=True)
        _lines(fig, x, 160, subs, size=11.5, pitch=15, anchor="middle")
    _t(fig, n0, ay + 48, "month 0", size=11, fill=P["muted"])
    _t(fig, n1, ay + 48, "24 calendar months", size=11, fill=P["muted"])
    _t(fig, n2, ay + 48, "48 months", size=11, fill=P["muted"])
    # the lapse: training missed at month 24
    ly = ay + 74
    fig.add(rect(n1, ly, 150, 12, fill=RED_FILL, stroke=RED, stroke_width=1.2,
                 stroke_dasharray="4 3"))
    _t(fig, n1 + 75, ly + 10, "not current", size=11, bold=True, fill=RED)
    fig.add(circle(n1 + 150, ly + 6, 7, fill=GREEN, stroke=P["white"],
                   stroke_width=1.5))
    fig.add(path(f"M{n1 + 150},{ly - 2} V{ay + 26}", fill="none",
                 stroke=GREEN, stroke_width=1.5, stroke_dasharray="3 3"))
    _lines(fig, n1 + 166, ly + 10, [
        "finish the course and you are current again",
    ], size=11, fill=GREEN)
    _lines(fig, 60, ly + 14, [
        "Missed the training at month 24? Then you are",
        "not current: you may not act as remote pilot in",
        "command until you finish the course. The",
        "certificate itself is still valid; nothing is reissued.",
    ], size=11.5, pitch=15)
    # carry it
    fig.add(rect(30, 366, 840, 60, rx=10, fill=BLUE_FILL, stroke=BLUE,
                 stroke_width=1.5))
    _t(fig, W / 2, 390, "Carry the certificate and a photo ID whenever you "
       "fly (§107.7).", size=13, bold=True)
    _t(fig, W / 2, 412, "Show them on request to the FAA, the NTSB, the TSA "
       "or any federal, state or local law enforcement officer.", size=12,
       fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
# 27. Three ways to comply with Remote ID
# ---------------------------------------------------------------------------
def build_remote_id() -> Figure:
    fig = Figure(W, 552, "Figure 27: Three ways to comply with Remote ID "
                 "(Part 89)",
                 "Required since 16 September 2023 for any drone that has to "
                 "be registered. §89.110 built in; §89.115(a) add-on module; "
                 "§89.115(b) FRIA.")
    # 1. standard remote ID aircraft, with the eight message elements
    fig.add(rect(30, 84, 540, 384, **CARD))
    _t(fig, 300, 110, "1. Standard Remote ID, built into the aircraft (§89.110)",
       size=13.5, bold=True)
    _t(fig, 300, 128, "broadcasts these message elements from takeoff to "
       "shutdown (§89.305)", size=11.5, fill=P["muted"])
    ax, ay = 300, 268
    # broadcast arcs off the nose
    for r in (58, 74, 90):
        fig.add(path(f"M{ax - r * 0.5:.1f},{ay - r * 0.87:.1f} "
                     f"A{r},{r} 0 0 1 {ax + r * 0.5:.1f},{ay - r * 0.87:.1f}",
                     fill="none", stroke=BLUE, stroke_width=2,
                     opacity="0.55"))
    fig.add(translate(ax, ay, aircraft_mini_top(1.3)))
    co = Callouts()
    # left labels end at x=196, right labels start at x=404
    L, R = 196, 404
    co.add("Aircraft ID", (L, 172), "end", (L + 6, 168), (ax - 39, ay - 31),
           sub="serial number or session ID")
    co.add("Time stamp", (R, 172), "start", (R - 6, 168), (ax + 39, ay - 31),
           sub="UTC, for each position")
    co.add("Aircraft position", (L, 252), "end", (L + 6, 248), (ax - 14, ay - 8),
           sub="latitude and longitude")
    co.add("Aircraft altitude", (R, 252), "start", (R - 6, 248),
           (ax + 14, ay - 8), sub="geometric, not barometric")
    co.add("Velocity", (L, 332), "end", (L + 6, 328), (ax - 39, ay + 31),
           sub="speed and direction")
    co.add("Emergency status", (R, 332), "start", (R - 6, 328),
           (ax + 39, ay + 31), sub="if the aircraft declares one")
    # the control station: the pilot, linked to the aircraft
    px, py = 300, 418
    fig.add(line(ax, ay + 50, px, py - 34, stroke="#9aa7b2", stroke_width=1.2,
                 stroke_dasharray="3 3"))
    fig.add(person(px, py, 1.3))
    co.add("Control station position and altitude", (px + 22, py - 4),
           "start", (px + 16, py - 8), (px + 7, py - 10),
           sub="where the pilot stands, broadcast too")
    fig.add(co.leaders())
    fig.add(co.names())

    # 2. broadcast module
    mx, mw = 590, 280
    fig.add(rect(mx, 84, mw, 174, **CARD))
    _t(fig, mx + mw / 2, 110, "2. Broadcast module (§89.115(a))", size=13.5,
       bold=True)
    _lines(fig, mx + 16, 136, [
        "An add-on for a drone without built-in",
        "Remote ID. It broadcasts the aircraft's",
        "ID, position, altitude and velocity, but",
        "the takeoff location instead of the",
        "control station (§89.315).",
        "Keep the aircraft in sight at all times;",
        "check the module before takeoff.",
    ])
    # 3. FRIA
    fy = 276
    fig.add(rect(mx, fy, mw, 192, **CARD))
    _t(fig, mx + mw / 2, fy + 26, "3. Fly inside a FRIA (§89.115(b))",
       size=13.5, bold=True)
    _lines(fig, mx + 16, fy + 52, [
        "An FAA-Recognized Identification Area,",
        "usually a model-club or school field.",
        "No Remote ID equipment is needed, but",
        "the aircraft and the pilot both stay",
        "inside the area, and the aircraft stays",
        "in sight.",
    ])
    _lines(fig, mx + 16, fy + 160, [
        "Not an option on a job site: a FRIA is",
        "that one field.",
    ], italic=True)

    fig.add(rect(30, 484, 840, 56, rx=10, fill=ORANGE_FILL, stroke=ORANGE,
                 stroke_width=1.5))
    _t(fig, W / 2, 508,
       "If the broadcast stops in flight, land as soon as practicable "
       "(§89.110(a)(2), §89.115(a)(4)).", size=13, bold=True)
    _t(fig, W / 2, 528,
       "The serial number of the aircraft or the module goes on the "
       "Certificate of Aircraft Registration (§89.110(b)(4), §89.115(a)(1)).",
       size=12, fill=P["muted"])
    return fig


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="review")
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()

    # (builder, number, variant, slug): a lettered variant sits beside the
    # figure it extends without moving any number after it
    for builder, number, variant, slug in (
        (build_exam_topics, 7, "", "exam_topics"),
        (build_waivable, 15, "", "waivable"),
        (build_ops_over_people, 15, "b", "ops_over_people"),
        (build_currency, 25, "", "currency"),
        (build_remote_id, 27, "", "remote_id"),
    ):
        fname = os.path.join(args.out, figure_name(5, number, slug, variant))
        builder().save(fname)
        print("wrote", fname)
        if args.png:
            png = render_png(fname)
            if png:
                print("wrote", png)


if __name__ == "__main__":
    main()
