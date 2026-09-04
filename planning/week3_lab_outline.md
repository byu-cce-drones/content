# Outline — Flight Practice Lab (Week 3)

**Status, 2026-09-04 (evening).** Instructor read the outline and said it looks good, and asked for two
additions, both now in: a short review of calibrating the Holy Stone drone (Setup Review below) and
an answer to "do we need figures?" (Figures below). The six questions at the bottom are still open;
Q4 now also asks which Holy Stone model the fleet is. `docs/labs/flight_practice.md` exists only as a
titled "coming soon" stub (same pattern as Labs 4–6) so the nav line and Lab 0's forward link
resolve; the real page replaces the stub once the questions are answered.

This file moved from `review/` (git-ignored) to `planning/` so it travels with the repository.

**Instructor suggestion, 2026-09-04:** a separate mini-instruction / tutorial page for the Holy Stone
drone, shared by both labs that use it (Week 2 Intro to Flying and this one). Proposal, not yet
built: `docs/class_resources/holy_stone_mini_drone.md`, listed under Reference in the nav and in the
"Before this lab, read" block of both labs. Contents: parts of the aircraft, controller layout
(reuse `w01_fig07_controller.svg`), power-on and pairing order, gyro calibration, trim, speed modes,
why headless mode stays off, emergency stop, what the lights and beeps mean, battery care and flight
time. The Setup Review section below then shrinks to a link plus the "calibrate after every crash"
rule, and the calibration figure proposed under Figures lives on the tutorial page instead of here.
Source: the Holy Stone HS210 manual (`holystone.com/docs/HS210_EN_Manual.pdf`); confirm the fleet's
model first, because the calibration stick corner differs between models.

This document proposes the structure and content of a new lab page. It is an outline, not a draft of
the page. Once the questions at the bottom are answered, the page is written to
`docs/labs/flight_practice.md` (title: **Flight Practice Lab**). It is already in `nav:` under Week 3.

- **Week:** 3. Syllabus entry: *"Mini Drone Lab Part 2: obstacle courses, team flight activities,
  flight challenges and races."*
- **Follows** Lab 0 — Introduction to Flying (Week 2), whose Looking Ahead already promises this lab
  and already links to `flight_practice.md`. **Leads into** Lab 1 — Flight Checklist (Week 4).
- **Aircraft:** Holy Stone mini drones, indoors, same as Lab 0.
- **File name:** unnumbered on purpose. Existing lab files keep their numbers so their URLs and any
  Learning Suite links stay stable; inserting a `3_` here would renumber four files.
- **Wording constraint:** "precision" never appears as a flying adjective on this page. Every
  instance is "controlled". The word is reserved for its measurement sense in Week 5.

---

## Before this lab, read

Abstract admonition at the very top, matching Lab 0 and Lab 1. Both were already assigned for Lab 0,
so the framing is *re-read the orientation section*, not *read something new*.

- [Flight Basics](../gen_reading/flight_basics.md) — stick controls, and why the nose decides left
  and right (Figure 9, "The nose decides left and right, not you")
- [Common Flight Issues](../gen_reading/flight_issues.md) — the "In the air" table and
  "When to stop flying"

---

## Key Takeaways

Proposed bullets (5):

1. Deliberate, repeatable control is a skill built by practice, not by reading about it.
2. Stick inputs are relative to the nose of the aircraft, so a pilot has to track orientation
   continuously — not only once it has already become a problem.
3. Small corrections, made one at a time, recover an unsteady aircraft faster than large ones.
4. Most real flight tasks combine several inputs at once; smooth flight comes from blending them,
   not from doing one thing at a time.
5. Every mapping flight later in the course is a pattern flown accurately enough to trust the data
   that comes out of it.

---

## Background

Roughly three short paragraphs:

- Lab 0 established that the drone can be made to move. This lab is about making it move *where you
  intended*, repeatably, while something else is also demanding attention — a course, a clock, or a
  teammate.
- The measurement tie-in: later in the semester a larger aircraft flies a planned grid at a set
  altitude with set overlap. A pilot who cannot hold altitude or heading by hand cannot judge
  whether an automated flight is going wrong, or take over when it does. Deliberate control is the
  foundation under every measurement the course produces.
- New relative to Lab 0: sustained flight instead of isolated maneuvers, combined inputs, working
  with a partner, and recovering from a mistake on purpose rather than by accident.

Safety warning admonition (required), at the end of Background:

> **!!! warning "Challenges and races do not change the rules"**
>
> - Never fly toward a person, including teammates and spectators.
> - Land immediately when an instructor or TA calls a stop, whatever the clock says.
> - No deliberate contact with obstacles, walls, or another aircraft. Contact ends the run.
> - A fast run that leaves the flight area is not a run. Staying inside the boundary is part of
>   every task on this page.
> - Speed is never the tiebreaker over control. Where a task is timed, control errors carry a
>   penalty larger than any time a rushed run could save.

---

## Objectives

By completing this lab, students will:

1. Maintain a controlled hover at an assigned altitude for a sustained period.
2. Hold altitude while moving the aircraft horizontally.
3. Fly a defined course in both directions without changing the aircraft's heading.
4. Fly the same course while rotating the aircraft to follow the direction of travel.
5. Combine throttle, pitch, roll, and yaw inputs in a single continuous movement.
6. Re-establish control of the aircraft after becoming disoriented.
7. Perform a controlled landing on a marked target.
8. Communicate clearly with a partner acting as a spotter or caller.
9. Explain how deliberate aircraft control affects the quality of data collected on a mapping flight.

---

## Required Materials

Lab 0's list, plus what the courses need:

1. Holy Stone mini drone and controller
2. Charged batteries — **at least three or four per aircraft**, plus a charging station running during the lab; see the battery note under Setup Review
3. Designated flight area with marked boundaries
4. Obstacle course materials: cones, gates or hoops, tape targets, boxes, marked landing pads
5. Stopwatch or phone timer, one per group
6. Score sheet / lab worksheet
7. Eye protection, if the instructor requires it
8. The manual for the fleet's Holy Stone model, one copy at the TA table

---

## Lab Overview

Short section — Lab 0 has no equivalent, but the house structure calls for it. It carries the table
below, whether groups rotate through stations or all fly the same part at once (depends on aircraft
count, see Q3), and the scoring philosophy stated once: control errors cost more than time.

**Time budget — 110 minute lab**

| Segment | Minutes |
|---|---|
| Setup, safety briefing, pairing and gyro calibration | 10 |
| Part 1 — Warm-Up: Hover and Altitude Hold | 15 |
| Part 2 — Obstacle Course | 25 |
| Part 3 — Team Flight: Caller and Pilot | 15 |
| Part 4 — Lost Orientation Recovery | 15 |
| Part 5 — Flight Challenges | 15 |
| Part 6 — The Race | 15 |
| Wrap-up, reflection, put away | 10 |
| **Total** | **110** |

Parts 5 and 6 are the compressible ones if the room runs long.

---

## Setup Review: Pairing, Calibration and Trim

New section, placed where Lab 0 has "Basic Drone Controls" — a short review before the activities,
because this lab flies four times as much as Lab 0 and a drifting aircraft ruins every course below.
Lab 0 never covered calibration; this is where it enters the course, and it is the same habit the
larger aircraft demand in Week 4 ("batteries, controllers, and calibration procedures" is on the
Week 4 syllabus line, so this is the warm-up for that).

Written from the Holy Stone HS210 manual. **The stick combination is model-specific** — the HS210
calibrates with both sticks to the *lower-left* corner, the HS420 with both sticks to the
*lower-right* — so the page states the HS210 procedure as the example and carries a Lab-0-style note:
"the exact combination depends on the model in your hands; your TA will demonstrate, and the manual
is at the TA table."

Proposed content (numbered steps on the page, one figure — see Figures below):

1. **Power on in the right order, on a level surface.** Battery into the drone; set it on a flat,
   level surface with the nose pointing away from you and the tail toward you; turn on the
   transmitter; push the left stick up, then down, to pair. Solid lights on the drone mean paired.
2. **Calibrate the gyro.** Both sticks to the lower-left corner together and hold. The drone's lights
   blink fast, then go solid; one long beep from the transmitter means done. The drone must be still
   and level while this happens — a calibration on a tilted table teaches the gyro that tilted is
   level, and the drone will drift toward the low side for the rest of the flight.
3. **When to recalibrate.** Every time after pairing, after **any** crash or hard landing, and any
   time the drone drifts with the sticks centred. Land first; never calibrate in the air.
4. **Trim, only if calibration does not fix a drift.** With the drone hovering, press the throttle
   stick in and hold, and push the direction stick *against* the drift (drifts left → push right,
   drifts forward → push back). Release when it holds. One long beep confirms the adjustment.
   Trim in small steps.
5. **Speed switch on Low.** Three speeds; the beeps count them (one beep Low, two Medium, three
   High). Everything in this lab is flown on Low except the race, where the TA decides.
6. **Headless mode stays off.** It makes the drone move relative to the pilot instead of its own
   nose, which is exactly the orientation skill this lab is built to teach. If a drone's lights are
   blinking after pairing, headless mode is on; press the button again to turn it off.
7. **Know the emergency stop before you take off.** Upper-left and upper-right buttons together kill
   the motors instantly. Use it for a fly-away toward people or a hand, never as a normal landing.

!!! tip "The engineering version of this habit"
    Calibration is telling the instrument what "level" and "still" mean before you trust anything it
    reports. It is the same thing a surveyor does levelling a total station, and the same thing you
    will do with the mapping aircraft in Week 4. An uncalibrated instrument gives confident wrong
    answers.

Battery note for Required Materials: the HS210 flies about **7 minutes** per battery and charges in
about 40, and the drone lands itself about a minute after the low-battery lights start blinking. Six
parts of flying means at least three or four charged batteries per aircraft, and a charging station
running through the lab.

---

## Figures

Answering the "do we need figures?" question directly: **two new figures, and one reused by link.**
House style is figures over prose, and both of these are things a TA or a student otherwise has to
picture from text.

| # | Figure | Why | Drawn from |
|---|---|---|---|
| 1 | **Calibration and trim on the controller.** Three small panels: pairing (left stick up, then down), gyro calibration (both sticks lower-left), trim (throttle stick pressed in, direction stick pushed against the drift, with arrows). Subtitle: "Stick positions shown for the HS210; other models differ — check the manual." | Students do this every flight from now on; a picture removes the "which corner?" confusion, and the panel is generic enough to reuse in Week 4 | `parts.controller()` and `parts.stick()` already exist in `fig_tools/parts.py` |
| 2 | **Obstacle course layout, plan view.** The room from above: start pad, gates or hoops in sequence, a cone slalom, an altitude change over a box, the landing pad, and the boundary. Generic shapes, no room dimensions, station letters matching the Part 2 text | TAs set the room up the same way each section; students can study the route before flying it; the same drawing with a different route serves Part 6 | new, simple shapes plus `parts.aircraft_mini_top()` |
| — | **Nose-in reversal** — the drone facing the pilot with left and right swapped | Part 4 depends on it | already Figure 9 on Flight Basics; link to it, do not redraw |

Not worth drawing: caller-and-pilot (two people and a drone, prose says it), the race (Figure 2 with
a different route), hover box (a sentence).

Naming: this lab has no number, so the `labNN_` convention does not apply directly. Recommendation
is `labfp_fig01_calibration.svg` and `labfp_fig02_course_layout.svg` in `docs/labs/images/` — `fp` for
flight practice, so an exported figure still says where it came from, which is all the prefix is
for. Using `lab03_` would collide with the flight-plans lab, whose file is `3_creating_flight_plans.md`.
Generated by a new `fig_tools/fig_flight_practice.py`, rendered to PNG in `review/` for a look
before they land.

---

## Activity Instructions

### Part 1 — Warm-Up: Hover and Altitude Hold (15 min)

**Purpose:** re-establish Lab 0 skills and confirm every aircraft flies properly before it is asked
to do anything demanding.

Students take off, hold a hover at roughly chest height for 30 seconds, then hold that same altitude
while translating slowly left, right, forward, and back. A partner watches from 90° to the side and
calls out altitude drift, which the pilot cannot see well from behind. Finish with a controlled
landing on a marked pad, repeated three times.

**Judged:** not scored. A TA confirms each aircraft holds altitude and each student can land on the
pad before the group moves on.

### Part 2 — Obstacle Course (25 min)

**Purpose:** the syllabus's "obstacle courses" — combined inputs and sustained control over a route
with defined tolerances.

Five to seven elements: a gate to fly through, a slalom between cones, a climb over a barrier, a
descent under a bar, a hover held inside a marked box, a landing on a target pad. Each student flies
the course twice with the nose held in one direction, then twice more rotating the nose to follow
the direction of travel — the contrast Lab 0 Part 4 sets up, now with real obstacles.

**Judged:** completion-based, untimed. Each element passed cleanly counts; a missed gate, touched
cone, or landing off the pad is a retry of that element, not a failed run.

### Part 3 — Team Flight: Caller and Pilot (15 min)

**Purpose:** the syllabus's "team flight activities", and the habit that matters later — a pilot
flying while someone else watches what the pilot cannot.

Pairs. The pilot flies a short route toward a target only the caller can see; the caller gives
directional commands out loud. Roles swap. A second round adds a constraint: commands must be in
*aircraft* terms ("nose left") rather than *room* terms ("toward the window"), and the class
compares which was easier to follow.

**Judged:** completion-based, both roles performed. Optional light scoring on commands needed.

### Part 4 — Lost Orientation Recovery (15 min)

**Purpose:** deliberately practicing recovery from a mistake, which every other activity is designed
to avoid. No equivalent in Lab 0.

A TA directs the pilot to yaw the aircraft 180° so the nose points back at them, then to navigate it
to a landing pad behind their own position. Second exercise: the TA calls "stop" mid-course; the
pilot brings the aircraft to a stable hover, states out loud which way the nose is pointing, then
continues. Debrief ties it to the readings — stop making aggressive inputs, stabilize, re-orient.

**Judged:** not scored. Success is a stable hover and a correct call of the heading, not a fast fix.

### Part 5 — Flight Challenges (15 min)

**Purpose:** the syllabus's "flight challenges" — short, discrete, skill-isolating tasks.

Three or four stations, each one task with a clear pass condition. Candidates: hold a hover inside a
1 m box for 30 seconds; land on a target the size of a sheet of paper; fly a figure-eight around two
cones; carry a paper cup through a gate without dropping it; hold a marked altitude while a TA calls
headings to yaw to.

**Judged:** pass / retry per station, recorded on the worksheet. Students choose which to attempt if
time is short.

### Part 6 — The Race (15 min)

**Purpose:** the syllabus's "races", and a controlled demonstration of the lab's central point —
speed without control loses.

Teams run a short subset of the Part 2 course against the clock, one pilot at a time, as a relay or
head-to-head depending on room and aircraft count. Scoring is time **plus penalties**: a touched
obstacle, missed gate, landing off the pad, or leaving the flight area each add a fixed penalty
large enough that a clean slow run beats a fast messy one. Everyone flies at least one leg.

**Judged:** timed with penalties — but see Q2; completion-only is a live alternative.

---

## In Lab Reflection

Answered in the Learning Suite quiz, same as Lab 0. Proposed six:

1. Which was harder: flying the course with the nose fixed, or rotating the nose at each turn? Why?
2. What did you actually do first when you lost track of which way the drone was facing?
3. What did your partner see from the side that you could not see from behind the aircraft?
4. Where did you find yourself overcorrecting, and what fixed it?
5. During the race, did the clock change how you flew? Did it make your flying better or worse?
6. A mapping flight has to hold a set altitude and a set path to produce usable data. Which part of
   today's lab would be hardest to do accurately for ten minutes straight?

---

## Homework

Two short parts, submitted in the Learning Suite quiz, due before the next lab.

**Part 1 — Course sketch and control plan.** Sketch the obstacle course as flown. For three of its
elements, name the control input or combination of inputs each one required, and note where the nose
was pointing. One or two sentences per element.

**Part 2 — Connect it to the reading.** Choose one situation from
[Common Flight Issues](../gen_reading/flight_issues.md) — drift, lost orientation, an aircraft not
responding as expected — or one idea from
[Flight Basics](../gen_reading/flight_basics.md#stick-controls). Describe a moment in the lab where
it applied, what you did, and what the reading says a pilot should do. If those differ, say which
you would do next time and why.

---

## Looking Ahead

Next: [Week 4 lab — Flight Checklist](1_flight_checklist.md).

Content to cover: today was flying by feel with a TA watching. The next lab formalizes the procedure
*around* the flight into written pre-flight, during-flight, and post-flight checklists, and
introduces the larger aircraft those procedures exist for. Close on the thread running through the
course — control first, procedure next, then measurement.

---

## Questions for the instructor

**Q1. Do the TAs own the activity content?** This outline proposes specific courses, challenges, and
a race format. If the TAs design the actual stations, the page should instead describe the *type* of
activity and the rules that govern it, and leave the layouts to them.

> GUS:

**Q2. Timed and competitive, or completion-only?** Part 6 is written as timed with penalties.
Completion-only is safer with freshmen and mini drones; timed is more engaging and is what "races"
in the syllabus implies. Which?

> GUS:

**Q3. Team size, and do groups rotate through stations?** Lab 0 says "work with your group" without
a number. Pairs work best for Part 3 (pilot and caller); Parts 5 and 6 want teams of three or four.
Also: how many aircraft are available, which decides whether the class runs one part at a time or
rotates?

> GUS:

**Q4. Figures — agree with the two proposed under Figures above, and the `labfp_` prefix?** The
calibration-and-trim panel and the course plan view are the two I would draw; nose-in reversal is
reused from Flight Basics. Also: which Holy Stone model is the fleet, so the calibration figure and
text show the right stick corner?

> GUS:

**Q5. Does any of this duplicate Lab 0 Part 4?** Lab 0's A-B-C-D box pattern already teaches
nose-fixed versus nose-rotating flight, and Part 2 here repeats that contrast with obstacles added.
Keep both as written, drop the repeat from Part 2, or trim Lab 0 Part 4 to a single pass now that
this lab exists?

> GUS:

**Q6. Is Part 4 (induced disorientation) acceptable indoors?** It deliberately puts a freshman into
the situation the readings warn about, with a TA standing by. It is the only place in the course
that practices recovery rather than avoidance, and also the part most likely to produce a crash.
Keep it as a student activity, or demote it to a TA demonstration the class watches?

> GUS:
