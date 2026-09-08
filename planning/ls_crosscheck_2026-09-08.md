# Site ↔ Learning Suite cross-check — 2026-09-08

Source: the course iCal feed (`learningsuite.byu.edu/iCalFeed/ical.php?courseID=oJ6i_6TFNlfS`,
public, 131 events, read 2026-09-08) against `nav:` in `mkdocs.yml` and the Welcome page's
"semester at a glance" figure. Re-run the check by downloading the feed again; the parse is one
short Python script (sort events by date, bucket by Monday-based week).

**Short answer.** The week structure matches in all three places. Learning Suite's fifteen calendar
weeks (first meeting Thu Sept 3, last Thu Dec 10) line up one-to-one with syllabus Weeks 1–15 and
with the fifteen nav sections; the six areas in the figure sit on the same weeks. What does **not**
match is (1) the URLs Learning Suite links to, which are dead, and (2) several site readings that
Learning Suite never assigns. Nothing here needs the nav or the figure to change.

---

## Week by week

| Wk | Learning Suite (lecture · lab · readings due) | Site nav section | Figure area | Match |
|---|---|---|---|---|
| 1 | Thu only: Introduction and Syllabus · TRUST assignment · syllabus quiz · reading "Surveying With Drones" (links the live Welcome page) | Week 1 — Course Introduction: This Week, Welcome, TRUST Certificate | 1 Fly it | ✔ |
| 2 | Tue: Surveying With Drones · Thu: Intro to Flying Part 1 (TRUST required) · reading due: Surveying With Drones | Week 2 — Drone Applications and Basic Flight: Products, Flight Basics, Lab Intro to Flying | 1 Fly it | ✔ structure; LS assigns no reading for Products or Flight Basics |
| 3 | Tue: Part 107 License · Thu: Intro to Flying Part 2 "Fun Day, no lab work" · reading due: Part 107 Regulations | Week 3 — FAA Rules and Flight Practice: Part 107 Overview, Flight Issues, Lab Flight Practice | 1 Fly it (+ area 5 marker) | ✔ structure; Flight Issues not assigned; lab page has homework, LS says none — **left as is per instructor** |
| 4 | Tue: QGIS · Thu: Flight Checklist lab (EB B122) · reading due: QGIS | Week 4 — GIS and Pre-Flight Procedures: Using QGIS, Flight Checklists, Lab Flight Checklist | 2 Measure it | ✔ |
| 5 | Tue: Measurements (accuracy vs precision, Google Earth, pacing) · Thu: Measurements and Methods lab (EB B122) · reading due: Measurements | Week 5 — Measurements and Field Practice: Measurement Fundamentals, Lab Measurements and Methods | 2 Measure it | ✔ |
| 6 | Tue: Mission Planning · Thu: Rock Canyon Part 1 – Mission Planning · reading due: Mission Planning | Week 6 — Mission Planning: Planning the Flight, Lab Creating Flight Plans | 3 Plan it | ✔ (lab named differently) |
| 7 | Tue: Aerotriangulation Software · Thu: Rock Canyon Part 2 – Flight Mission Day (EB B122) · Create a Bentley account · reading due: Aerotriangulation Software | Week 7 — Photogrammetry and Flight Operations: How Photos Become 3D, Photo Metadata, Bentley iTwin, Lab Rock Canyon Park Flight | 3 Plan it / 4 Process it | ✔ |
| 8 | Tue: Sensors — Lidar, **Radar**, Thermal, Multispectral; agricultural and methane · Thu: Rock Canyon Part 3 – Data Processing ("Computer Lab????") · readings due: Lidar, Thermal, Multispectral | Week 8 — Advanced Sensors and Data Processing: LiDAR, Thermal, Multispectral, Lab Data Processing | 4 Process it | ✔; no radar page; lab room undecided in LS |
| 9 | Tue: Part 107 Exam prep · Thu: Part 107 Test Studying lab · **Part 107 Test** (Thu) · reading due: Part 107 Exam | Week 9 — Part 107 Exam Preparation: Knowledge Review, Study Resources, Mini Exam, Full Exam, Lab Part 107 Studying | 5 Get certified | ✔ |
| 10 | Tue: Final Project Introduction · Thu: Project Proposals lab · Proposal due | Week 10 — Final Project Planning: Overview, Proposal | 6 Prove it | ✔ |
| 11 | Tue: Guest Speaker (TBD) · Thu: Final Project Flight, **Group A** · Flight and Data Processing assignment | Week 11 — Guest Lecture and Project Flights: Flight and Data Processing | 6 Prove it | ✔ (site page now says Group A) |
| 12 | Tue: FE Prep – Survey Questions · Thu: Final Project Flight, **Group B** | Week 12 — Surveying and Project Flights: This Week only | 6 Prove it | ✔ structure; **no FE/survey page exists** (backlog) |
| 13 | Tue: Project Work Day, TA help · no Thu (Thanksgiving) | Week 13 — Project Work | 6 Prove it | ✔ |
| 14 | Tue: Class Recap · Thu: Project Work Day, TA help | Week 14 — Course Review and Project Support | 6 Prove it | ✔ |
| 15 | Mon: Presentation due · Tue: Final Class Review, Show and Tell Day 1 · Thu: Show and Tell Day 2, Final Report due, Part 107 make-up | Week 15 — Final Presentations: Presentation, Report | 6 Prove it | ✔ |

**Figure vs nav.** Fly it = Weeks 1–3, Measure it = 4–5, Plan it = 6–7, Process it = 7–8, Get
certified = 9 (marker at 3), Prove it = 10–15. Every nav page falls inside its area. The Part 107
Overview reading in Week 3 is the "rules introduced" marker.

---

## Where Learning Suite needs editing

### 1. Dead links (highest priority)

Every pre-class reading item from Week 2 on, and the lab links in Weeks 5–7, point at
`https://byu-cce-drone-measurements.readthedocs.io/en/latest/…`, which returns **404**. The live site is
`https://byu-cce-aerial-measurements.readthedocs.io/en/latest/`. The Week 5 lab link also uses the
pre-reorganization path `week_03/`, which never existed on the live site. Only the Week 1
"Surveying With Drones" item links correctly.

Correct URLs, one per Learning Suite item (all under `https://byu-cce-aerial-measurements.readthedocs.io/en/latest/`):

| Learning Suite item | Link to |
|---|---|
| Pre-Class Reading: Surveying With Drones | `gen_reading/class_overview/` |
| Trust Certificate (assignment) | FAA page as now; optionally also `gen_reading/trust_certificate/` |
| Pre-Class Reading: Part 107 Regulations | `part_107_license/faa_exam_planning_and_overview/` |
| Pre-Class Reading: QGIS | `software/qgis_measurements/` |
| Pre-Class Reading: Measurements | `gen_reading/measurement_fundamentals/` |
| Pre-Class Reading: Mission Planning | `gen_reading/mission_planning_sfm/` |
| Pre-Class Reading: Aerotriangulation Software | `software/bentley_itwin/` (and `gen_reading/sfm_workflow/` for the concept) |
| Pre-Class Reading: Lidar / Thermal / Multispectral | `gen_reading/lidar/`, `gen_reading/thermal/`, `gen_reading/multispectral/` |
| Pre-Class Reading: Part 107 Exam | `part_107_license/part_107_knowledge_review/` |
| Intro to Flying Lab Instructions | `labs/0_intro_to_flying/` |
| Intro to Flying Part 2 (Week 3) | `labs/flight_practice/` |
| Flight Checklist Lab Instructions | `labs/1_flight_checklist/` |
| Measurement Lab Instructions | `labs/2_measurements_and_methods/` |
| Lab – Creating Flight Plans | `labs/3_creating_flight_plans/` |
| Rock Canyon Lab Instructions | `labs/4_rock_canyon_flight/` |
| Lab – Data Processing | `labs/5_data_processing/` |
| Lab Instructions: Part 107 Test Studying | `labs/6_part_107_studying/` |
| Final Project items | `final_project/overview/`, `final_project/proposal/`, `final_project/flight_and_data_processing/`, `final_project/presentation/`, `final_project/report/` |
| Any week's schedule entry | `weeks/week_NN/` (e.g. `weeks/week_05/`) — the "This Week" page |

### 2. Site readings that Learning Suite never assigns

These pages exist under their week on the site but have no pre-class reading item in Learning
Suite. They are read only if a student follows the "Before this lab, read" block. Decide whether each
gets a reading quiz or stays lab support:

| Week | Page | Used by |
|---|---|---|
| 2 | Aerial Measurement Products | Lab 2, final project |
| 2 | Flight Basics | Intro to Flying lab; the controller homework |
| 3 | Common Flight Issues | both flying labs, Rock Canyon flight |
| 4 | Flight Checklists (and the pre/post lists) | Flight Checklist lab, every field flight |
| 7 | How Photos Become 3D, Photo Metadata | Data Processing lab |

### 3. Names that differ (cosmetic)

Learning Suite and the site name the same thing differently. Neither is wrong; consistency helps a
freshman find the page.

| Week | Learning Suite | Site |
|---|---|---|
| 2 | Lecture: Surveying With Drones | Week 2 — Drone Applications and Basic Flight |
| 6 | Lab: Rock Canyon Part 1 – Mission Planning | Lab — Creating Flight Plans |
| 7 | Lecture: Aerotriangulation Software; Lab: Rock Canyon Part 2 | Week 7 — Photogrammetry and Flight Operations; Lab — Rock Canyon Park Flight |
| 8 | Lab: Rock Canyon Part 3 – Data Processing | Lab — Data Processing |
| 9 | Part 107 Test | Full Practice Exam (60 Q) |

### 4. Loose ends visible in the calendar

- Week 8 lab location is "Computer Lab????".
- Week 8 lecture title still lists radar; no page teaches it (backlog).
- Week 12 Tuesday "FE Prep – Survey Questions" has no site page (backlog).
- Week 1's "Surveying With Drones" reading is due Wed Sept 2, the day before the first class meeting.
- Week 3 lab: "no instructions or lab work" in Learning Suite; the site page has a reflection and
  homework. Instructor 2026-09-08: leave as is for now.

---

## Where the site was changed to match (done 2026-09-08, `2ff29f3`)

Week 1 meets only on Thursday; Week 7 asks for the Bentley account; Weeks 11 and 12 name Groups A
and B; Week 13 has no Thursday class; Week 14 is recap then work day; Week 15 is two show-and-tell
days plus the report and the Part 107 make-up. No dates on any page.
