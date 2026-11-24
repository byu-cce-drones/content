# Winter 2027 Course Redesign — Plan

Drafted 2026-11-24 from the instructor and TA planning meeting the same morning. Companion to
`planning/winter_2027_schedule.md`, which holds the calendar and the due-date rules.

**Scope.** Everything except the final project. The final project pages (`docs/final_project/`) and
the project weeks (11–14) keep their content, deliverables and dates as already set. Where a meeting
idea touches the project (moving the proposal earlier, requiring a checklist in the project), it is
listed under "Parked: touches the final project" and not planned.

**This file is in a public repository.** It names roles, not people, and holds no room codes,
student names or certification status. Keep it that way.

---

## 1. The two structural changes

1. **Much more hands-on flying.** By the final project most students had flown a real drone about
   once. Every lab from Week 4 on runs as **two rotating stations**: half the lab time flies with
   TAs while the other half works with the instructor (talk, checklist, technique), then they swap.
   With 12 students per lab time that is 6 flying in 3 pairs, which needs 3 TA pilots plus the
   instructor at the talking station.
2. **Part 107 woven through every lecture,** instead of one prep week at the end. Each pre-class
   reading includes a short Part 107 topic; the lecture opens with a Part 107 attendance quiz on it.

A third thread came out of the meeting and needs the same treatment: **more surveying**, tied to
the ABET outcome that prepares students for the surveying part of the FE exam.

### The lecture pattern ("Sunday school" format)

| Minutes | What happens |
|---|---|
| 0–5 | Part 107 attendance quiz (one question from the pre-class reading), then discuss the answer |
| 5–40 | The week's topic |
| 40–50 | A surveying note that ends in a problem; the same kind of problem goes in the homework |

### The lab pattern

| Minutes | Group 1 | Group 2 |
|---|---|---|
| 0–5 | Everyone: the instructor's stand-up | |
| 5–25 | Flying with TAs | Instructor station |
| 25–45 | Instructor station | Flying with TAs |
| 45–50 | Pack up, batteries | |

Weather rule for every outdoor lab: dress for the cold; if it is only cold, we fly. If it is
snowing or unsafe, the flying half flies Holy Stones indoors, and any data the lab needs comes from
a prior-semester dataset so the lab work still happens.

---

## 2. Week by week

Weeks and dates follow `docs/class_resources/schedule_winter_2027.md`. "P107" is the Part 107
topic for the opening quiz; "Surveying" is the closing note and homework problem. The topic
assignments are a first proposal for the team to rearrange.

| Wk | Lecture changes | P107 topic | Surveying topic | Lab changes |
|---|---|---|---|---|
| 1 | Thu Jan 7, two hours: syllabus, then lab-time groups rotate through stations: CTB 250 (drones on display), EB B122 (where labs meet), CB 308 (computer lab; create a CAEDM account there), and Part 107 introduced as a semester-long thread, plus "you may take it any time" | What Part 107 is and who needs it | — | No lab |
| 2 | **Retitle and refocus:** "What is surveying?" How measurement was done (chains, tapes, total station, GNSS) and where drones fit; the deliverables (orthomosaic, DEM). Flight basics (controls) move to the lab | Recreational (TRUST) vs. Part 107: the "grandma's house" and "paid in cookies" cases | Traditional surveying vs. drones; ground truth when there is no RTK or PPK | Holy Stone 1: safety, controls, box drills, troubleshooting. Absorbs the controls part of Flight Basics |
| 3 | Part 107 lecture stays (the regulations: who, where, how high, over people) | (the whole lecture) | Distances and error | Holy Stone 2: open flying and obstacles, more stick time, less structure |
| 4 | QGIS: **pre-class** is install QGIS or name the lab computer you will use, and open the class TIFF. **Lecture** sets the coordinate system and starts measuring (doubles as the homework start). Add coordinate systems | Sectional chart basics, airspace classes | Coordinate systems: lat/long, UTM, state plane; a USGS topo map exercise (find the feature at a coordinate) | Flight Checklist with Minis: station A assemble, pre- and post-flight checklists; station B fly: takeoff, climb, manual photo, speed modes (moved here from Lab 2). **Homework:** more varied QGIS measurements |
| 5 | Measurements: add the FE concepts (error, accuracy, precision) | Controlled airspace B, C, D and LAANC | Error and accuracy, FE-style | Measurements and Methods: pacing, manual photos, more flying; Minis' follow-me and hero-shot modes. Bad weather: pace the hallway, walk the lot later in the week |
| 6 | Mission planning shortened to about 25 minutes (GSD, overlap, course angle), the rest surveying | METAR | Angles, bearings, azimuths | Creating Flight Plans: all planning in the class web planner, flown on Minis; show the Mavic and Autel controllers by screenshot or on the TV. Note RC2 works, the older RC does not |
| 7 | No lecture (Monday schedule) | — | — | Thu Feb 18 free fly day (done): Mavic, Matrice, Inspire; also a make-up day |
| 8 | Aerotriangulation: add a troubleshooting toolkit (why a model fails and what to check) | TAF, weather effects | Ground control and targets; traverse and closure | Rock Canyon flight. Cancelled: hand out a prior dataset and stay on schedule |
| 9 | Sensors: unchanged apart from the quiz and the surveying close | Density altitude, performance | Leveling, elevations, geoid vs. ellipsoid | Data Processing: a **small, fast** dataset; every student processes their own; first stage in lab, the rest as homework; a TA records a step-by-step screen video on the lab PCs; SD-card adapters; shared class drive |
| 10 | Second Part 107 lecture (exam prep). Keep or replace: **decision** | (the whole lecture) | Area by coordinates | **Part 107 lab dropped.** Becomes a flying lab, and the weather backup for anything cancelled earlier |
| 11–14 | Final project: unchanged. The Week 12 and 13 lectures can still open with a P107 quiz | Operations: night, over people, Remote ID | Earthwork volumes; curves; staking (pending the surveying-instructor meeting) | Final project: unchanged |
| 15 | Class recap | Review | Review | No lab |

---

## 3. Site content work

Ordered so students get the early weeks first; the semester starts Wed Jan 6.

### Before Jan 6

1. **Syllabus.** *Done 2026-11-24:* course info, a "How the Course Runs" section (three threads,
   lecture pattern, winter weather), attendance and lab wording, the checklist link, and the topic
   list rewritten to the winter weeks; schedule page Weeks 2, 4 and 10 updated to match. No grace
   day (decision 6 dropped). Originally: add: the Part 107 quiz in every lecture, expanded flying, the surveying thread,
   winter weather and "dress for it", and why missed labs mostly cannot be made up (no flying
   without a TA). Grade breakdown unchanged. Replace "Learning Suite" with Canvas throughout. The
   Week 1–15 topic list at the bottom must match Section 2.
2. **Week 1 and Week 2.** A new Week 2 lecture reading, "What is surveying?", or a rewrite of
   `data_products.md`'s opening. Move the controls content of `flight_basics.md` into the Week 2 lab.
3. *Done 2026-11-24:* `docs/part_107_license/weekly/`, an index and ten pages (Weeks 2, 4, 5, 6,
   8, 9, 11, 12, 13, 14), each with Key Takeaways, figures from the existing set, three practice
   questions with collapsible answers, and a link back to the Week 3 reading; in the nav as
   "Part 107 Every Week" and linked from each lecture on the schedule page. Weeks 3 and 10 are the
   two full Part 107 lectures; Week 15 points at Common Traps. **Still to do:** the Canvas
   attendance questions. The practice answers are public, so write the attendance question bank
   separately (one or two per week, on the same topic, not copied from the page). Originally:
   **Part 107 weekly snippets.** One short page or section per week (about 5 minutes of reading,
   one figure from the FAA supplement where it fits), each with 2–3 quiz questions. Most of the text
   already exists in `part_107_license/` and the Week 3 and Week 9 decks; this is cutting it into
   weekly pieces. A new folder, `docs/part_107_license/weekly/`, keeps them together.
4. **Surveying notes.** One short section or page per week with a worked problem, plus 1–2 homework
   problems. Source: the Week 12 FE Surveying Review deck and `fe_surveying_review.md`, which already
   have the figures and worked numbers. This is also the existing backlog item "turn
   `fe_surveying_review.md` into a full reading"; the weekly pieces can be that reading's sections.
5. **Labs 0 and Flight Practice (Weeks 2–3).** Cut to 50 minutes; move the controls content in.
6. **Lab pages to the two-station 50-minute format.** `1_flight_checklist.md` and
   `2_measurements_and_methods.md` first (Weeks 4–5), then `3_creating_flight_plans.md` (Week 6).
   Each gets a "Bad weather" box.
7. **QGIS page and Week 4.** Pre-class install or access instructions, the TIFF to open, the
   coordinate systems mini-lesson, an expanded measurement homework.
8. **Flight checklist page** printable, one copy in every drone box, and usable on a phone.

### Before Week 8 (Feb 23)

9. **Rock Canyon lab** (`4_rock_canyon_flight.md`, still a stub) and its backup dataset.
10. **Data Processing lab** (`5_data_processing.md`, still a stub): pick the small dataset, link the
    screen recording, SD adapters, the shared drive.
11. **Aerotriangulation troubleshooting** section in `sfm_workflow.md` and the Week 7 deck.

### Before Week 10 (Mar 9)

12. **Retire `6_part_107_studying.md` from Week 10** (keep the page; it is a good study resource)
    and write the Week 10 flying lab page.
13. **Lecture decks:** add the opening quiz slide and closing surveying slide to each existing deck.

### Throughout

14. **Week pages and nav.** The nav and `docs/weeks/` follow fall numbering (Week 7 = Rock Canyon,
    and so on). Either renumber them to the winter weeks or drop the week pages and let the Winter
    2027 schedule page plus Canvas modules carry the order. **Decision.**
15. **Planning docs.** `ai_context.md` and `instructions.md` still say "no due dates on the site;
    dates live in Learning Suite". Update for Canvas and the site as the source of truth.

---

## 4. Canvas setup (outside this repository)

- One **module per week**, each linking the site pages for that week (the site stays the source of
  truth; Canvas holds quizzes, submissions and grades).
- The **recurring attendance quiz** format: one question, opens at 8:00, closes a few minutes in.
- **Pre-assigned lab-time groups** and pairs, plus the swap process already on the schedule page.
- Rebuild the Part 107 practice test; carry over the question-bank fixes from 2026-10-20.
- The Part 107 incentive (take the real test during the semester for 5 points) moves from Learning
  Suite to Canvas.

---

## 5. Logistics and staffing (not site work, listed so nothing is lost)

- **TA pilots:** 3 per lab time for the flying station. Email the class: licensed students who want
  to TA should reach out. The instructor attends every lab for the talking station.
- **EB B122:** mobile TV stand, large TV, long extension cord; test which outlets work. Test
  mirroring the Autel controller to the TV.
- **Batteries:** enough for every lab time; reserve half for the later lab times; two fast chargers.
- **Thermal drone:** about 10 minutes of warm-up before useful images; brief the TAs.
- **Checklists** printed into every drone box.
- **Meet with the UVU surveying instructor and the surveying TAs** to settle staking, a total
  station demo, and the FE surveying topics.
- **Backup datasets** from fall for every outdoor lab.

---

## 6. Decisions needed

1. ~~**Rooms for the Holy Stone labs.**~~ Decided 2026-11-24: the Week 2 and Week 3 labs (both
   Holy Stone labs) meet in CTB 250; schedule page updated.
2. **Minis earlier?** Swap the second Holy Stone lab for Minis, or keep two Holy Stone labs?
3. **Week 10 lecture:** keep a second Part 107 lecture, or use it for surveying or another topic?
4. **Total station:** a demo station in which lab (Week 2 or Week 5), or none?
5. **Staking:** in the course, and where? After the surveying meeting.
6. ~~**Grace day for lectures.**~~ Dropped for now (instructor, 2026-11-24). The syllabus keeps
   "no absences are automatically dropped".
7. **QGIS pre-class:** required on a personal laptop, or "your laptop or a named lab computer"?
8. **Week pages and nav:** renumber for winter, or retire them in favor of the schedule page and
   Canvas modules?

## Parked: touches the final project

- Moving the proposal earlier to give a week of feedback before flights.
- Requiring a printed or digital checklist in the project flight.
- Using the Week 10 lab as a project flight backup.
