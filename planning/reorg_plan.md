# Reorganizing the site by week — step-by-step plan

**Executed 2026-09-04.** Steps 0, 1, 3–9 done, committed as `7aaa3b3`, and on `origin/main` (pushed
together with the measurement reading, `b791fb1`). One addition at the instructor's request: the TRUST
certificate became its own page, `gen_reading/trust_certificate.md`, listed as a third Week 1 entry.

**Step 2 — done 2026-09-04.** `docs/labs/flight_practice.md` is written and live, with two `labfp_`
figures. The history: The outline is `planning/week3_lab_outline.md` (moved out of git-ignored `review/` so it
survives a machine change). The instructor read it 2026-09-04 and said it looks good; a Holy Stone
calibration review and a Figures section were added at their request. Still open before the page is
written: the six `> GUS:` questions at the bottom of the outline (TA ownership, timed vs. completion
races, team size and aircraft count, the two proposed figures and the `labfp_` prefix plus which Holy
Stone model the fleet is, overlap with Lab 0 Part 4, induced disorientation as activity or demo).

The six questions were answered the same evening (inline in the outline) and the following happened:
(1) `fig_tools/fig_flight_practice.py` drawing
`labfp_fig01_calibration.svg` and `labfp_fig02_course_layout.svg` into `docs/labs/images/`, PNGs to
`review/` for a look; (2) write the page over the stub, house lab structure, no "precision" as a
flying word; (3) strict build, commit, push. Still open: the instructor's suggested Holy Stone
mini-drone tutorial page shared by the Week 2 and Week 3 labs — proposal at the top of the outline and
in `backlog.md`; when built, the lab's Setup Review shrinks to a link and Figure 1 moves there.

Decided 2026-09-04 with the instructor. The class runs on a weekly Tuesday-lecture / Thursday-lab
rhythm and Learning Suite is a calendar, so the site's nav should be organized by week. The
feasibility analysis behind this is in `review/SITE_REORG_BY_WEEK.md` (git-ignored); the decisions it
produced are recorded here so they survive.

**Decisions made:**

- Nav organized by week, matching the syllabus schedule. Weeks, not Topics.
- **One index page per week** (`docs/weeks/week_NN.md`), listed first under each week, saying what
  the week covers, what to read, what the lab is. Full pages stay where they are.
- A **Reference** section lists the cross-cutting pages a second time (checklists, software,
  products, flight issues) so they can be found without knowing the week.
- **The Week 3 lab does not exist and must be written.** Syllabus: "Mini Drone Lab Part 2 — obstacle
  courses, team flight activities, flight challenges and races." Lab 0's Looking Ahead already
  describes it.
- Labs are labelled by week in the nav, not by number. Existing lab filenames stay as they are
  (renumbering breaks Learning Suite links); the number in the filename becomes historical, the same
  way the `wNN_` figure prefixes already are.

**Why this is cheap:** nav nesting does not change a page's URL in MkDocs. No files move, no URLs
change, no Learning Suite link breaks. A page may appear in the nav more than once — tested,
`--strict` clean.

**Sequencing with the measurement reading:** this reorganization lands **before** the measurement
reading is wired into `docs/`. The reading's draft work continues in `review/` and
`fig_tools/fig_measurement.py` meanwhile; those files do not collide with anything below.

---

## Step 0 — Preflight

- [ ] `git fetch` and confirm `main` matches `origin/main`. Nobody else has committed.
- [ ] `mkdocs build --strict` passes before touching anything. Baseline: one INFO line for the
      orphaned `grading_policy.md`, nothing else.
- [ ] Read `planning/ai_context.md`, `instructions.md`, `backlog.md`, and this file.

## Step 1 — Fix Lab 0's Looking Ahead (wrong today, regardless of the rest)

`docs/labs/0_intro_to_flying.md` "Looking Ahead" currently links to Lab 1 (the checklist lab) while
describing the Week 3 flying lab. Added in Sprint 1 on a fair reading of the file; wrong now that the
schedule is in hand.

- [ ] Change the forward link to the Week 3 lab created in Step 2. Until that page exists, the link
      target is the new file's path; the strict build will hold you to creating it.
- [ ] Rename the three flying uses of "precision" while in the file: line 346 "Precision hovering" →
      "Controlled hovering", line 352 "Precision landing" → "Controlled landing", line 188 "more
      precise maneuvers" → "more demanding maneuvers". Approved by the instructor; the measurement
      reading needs the word to mean one thing.

## Step 2 — Write the Week 3 lab

New file: **`docs/labs/flight_practice.md`**. Unnumbered on purpose — see decisions above.

- [ ] Outline first, in `review/`, before the page. Source material: the syllabus Week 3 bullets
      (obstacle courses, team flight activities, flight challenges and races) and Lab 0's Looking
      Ahead list (controlled hovering, maintaining altitude, directional control, orientation,
      controlled patterns, combining inputs, controlled landing, recovering from mistakes). Lab 0 is
      the voice and structure to match.
- [ ] House lab structure: Key Takeaways, Background, Objectives, Required Materials, Lab Overview,
      Activity Instructions, In Lab Reflection, Homework, Looking Ahead. Open with a "Before this lab,
      read" block (Flight Basics, Common Flight Issues) and close with a forward link to the Week 4
      checklist lab.
- [ ] Instructor reviews the outline, then the page. TAs may own the activity content — ask.
- [ ] Add it to the nav in Step 4.

## Step 3 — Write the fifteen week pages

New folder **`docs/weeks/`**, files `week_01.md` … `week_15.md`. Generate the first draft of all
fifteen from the syllabus schedule and the week mapping in `review/SITE_REORG_BY_WEEK.md`; hand-edit
after.

Template, one page:

```markdown
# Week 5 — Measurements and Field Practice

!!! abstract "This week"
    - **Tuesday lecture:** accuracy vs. precision; measurement methods and applications
    - **Thursday lab:** measurement lab and first larger-drone flights

## Before Thursday, read

- [Measurement Fundamentals](../gen_reading/measurement_fundamentals.md) — the vocabulary the lab
  assumes: accuracy, precision, resolution, uncertainty

## Thursday's lab

- [Measurements and Methods](../labs/2_measurements_and_methods.md)

## Looking ahead

Next: [Week 6 — Mission Planning](week_06.md)
```

- [ ] Weeks 10–15 are project weeks; their pages point at the final project pages and at each other.
- [ ] Weeks 13 and 14 (work days) get a page each so the sequence is unbroken, kept to a few lines.
- [ ] **Do not put due dates on these pages.** Dates live in Learning Suite and change; a stale date
      on the site is worse than none. Say "see Learning Suite for due dates" once, on Week 1.
- [ ] Every week page links to the previous and next week.
- [ ] Week 1's page is also the place for the "how this site is organized" note the backlog asks
      for on `index.md`.

## Step 4 — Rewrite the nav

Replace the `nav:` block of `mkdocs.yml` with the structure below. Section headings say "Week N —
Topic", matching the syllabus headings exactly.

```yaml
nav:
  - Home: index.md

  - Start Here:
      - Syllabus: class_resources/syllabus.md
      - Teaching Assistants:
          - About the TAs: class_resources/ta/tas.md
          - Office Hours: class_resources/ta/ta_hours.md

  - Week 1 — Course Introduction:
      - This Week: weeks/week_01.md
      - Welcome to the Course: gen_reading/class_overview.md

  - Week 2 — Drone Applications and Basic Flight:
      - This Week: weeks/week_02.md
      - Reading — Aerial Measurement Products: gen_reading/data_products.md
      - Reading — Flight Basics: gen_reading/flight_basics.md
      - Lab — Intro to Flying: labs/0_intro_to_flying.md

  - Week 3 — FAA Rules and Flight Practice:
      - This Week: weeks/week_03.md
      - Reading — FAA Part 107 Overview: part_107_license/faa_exam_planning_and_overview.md
      - Reading — Common Flight Issues: gen_reading/flight_issues.md
      - Lab — Flight Practice: labs/flight_practice.md

  - Week 4 — GIS and Pre-Flight Procedures:
      - This Week: weeks/week_04.md
      - Reading — Using QGIS: software/qgis_measurements.md
      - Reading — Flight Checklists: class_resources/flight_check_list/index.md
      - Lab — Flight Checklist: labs/1_flight_checklist.md

  - Week 5 — Measurements and Field Practice:
      - This Week: weeks/week_05.md
      # - Reading — Measurement Fundamentals: gen_reading/measurement_fundamentals.md   <- Sprint 2
      - Lab — Measurements and Methods: labs/2_measurements_and_methods.md

  - Week 6 — Mission Planning:
      - This Week: weeks/week_06.md
      - Reading — Planning the Flight: gen_reading/mission_planning_sfm.md
      - Lab — Creating Flight Plans: labs/3_creating_flight_plans.md

  - Week 7 — Photogrammetry and Flight Operations:
      - This Week: weeks/week_07.md
      - Reading — How Photos Become 3D: gen_reading/sfm_workflow.md
      - Reading — Photo Metadata: gen_reading/metadata.md
      - Reading — Bentley iTwin: software/bentley_itwin.md
      - Lab — Rock Canyon Park Flight: labs/4_rock_canyon_flight.md

  - Week 8 — Advanced Sensors and Data Processing:
      - This Week: weeks/week_08.md
      - Reading — LiDAR Imaging: gen_reading/lidar.md
      - Reading — Thermal Imaging: gen_reading/thermal.md
      - Reading — Multispectral Imaging: gen_reading/multispectral.md
      - Lab — Data Processing: labs/5_data_processing.md

  - Week 9 — Part 107 Exam Preparation:
      - This Week: weeks/week_09.md
      - Knowledge Review: part_107_license/part_107_knowledge_review.md
      - Study Resources: part_107_license/part_107_resources.md
      - Mini Practice Exam: part_107_license/mini_exam.md
      - Full Practice Exam (60 Q): part_107_license/60_question_exam.md
      - Lab — Part 107 Studying: labs/6_part_107_studying.md

  - Week 10 — Final Project Planning:
      - This Week: weeks/week_10.md
      - Project Overview: final_project/overview.md
      - Project Proposal: final_project/proposal.md

  - Week 11 — Guest Lecture and Project Flights:
      - This Week: weeks/week_11.md
      - Flight and Data Processing: final_project/flight_and_data_processing.md

  - Week 12 — Surveying and Project Flights:
      - This Week: weeks/week_12.md

  - Week 13 — Project Work:
      - This Week: weeks/week_13.md

  - Week 14 — Course Review and Project Support:
      - This Week: weeks/week_14.md

  - Week 15 — Final Presentations:
      - This Week: weeks/week_15.md
      - Project Presentation: final_project/presentation.md
      - Final Report: final_project/report.md

  - Reference:
      - Flight Checklists:
          - Overview: class_resources/flight_check_list/index.md
          - Pre-Flight: class_resources/flight_check_list/pre_flight/pre_general.md
          - Post-Flight: class_resources/flight_check_list/post_flight/post_general.md
      - Using QGIS: software/qgis_measurements.md
      - Bentley iTwin: software/bentley_itwin.md
      - Photo Metadata: gen_reading/metadata.md
      - Aerial Measurement Products: gen_reading/data_products.md
      - Common Flight Issues: gen_reading/flight_issues.md
```

- [ ] The two instructor answer-key pages and `coming_soon.md` are **not** in this nav. The keys are
      a deferred decision (`backlog.md`); leaving them out of the nav is the least the reorganization
      can do without pre-empting it. They still build and are still reachable by URL. If the
      instructor wants them listed, add them under Week 9. `coming_soon.md` was "leave for now" —
      leaving it out of the nav produces an orphan INFO line, which is acceptable; ask.
- [ ] Measurement Fundamentals is commented out under Week 5 until Sprint 2 lands the page. Its
      "Start Here" placement is still an open decision; put it in **both** places once it exists.

## Step 5 — "Topic N" becomes "Week N"

Thirteen prose references and two SVGs say "Topic N". Under a week nav they must say "Week N" and
link to the week page. Old-topic-to-week mapping, to be confirmed against each reference as it is
edited:

| Old Topic | Covered | Weeks |
|---|---|---|
| 1 | Welcome, products, flight basics, flight issues | 1–2 |
| 2 | QGIS and Bentley | 4 (QGIS), 7 (Bentley) |
| 3 | Metadata | 7 |
| 4 | How Photos Become 3D, Planning the Flight | 6–7 |
| 5 | Part 107 | 3 (intro), 9 (exam prep) |
| 6 | Sensors | 8 |

- [ ] Prose, thirteen places: `final_project/flight_and_data_processing.md:54,64`,
      `final_project/proposal.md:71`, `gen_reading/class_overview.md:61`,
      `gen_reading/flight_basics.md:65-67,364,367,450,457,459`,
      `part_107_license/60_question_exam.md:2`,
      `part_107_license/60_question_exam_instructor_key.md:2`. Most already carry a page link, so
      the edit is usually replacing the words and adding a week link.
- [ ] SVGs, two: `w01_fig16_rules.svg` ("Topic 5 covers the full set.") and
      `w01_products_family.svg` ("(covered in Topic 6)"). Regenerate from `fig_tools/fig_rules.py`
      and `fig_tools/fig_products.py`; render to PNG and look at them.

## Step 6 — Relabel the Sprint 1 cross-links

Sprint 1 added "Lab N —" labels in Looking Ahead links and "Where this is used" sections. Under
week-labelled labs these should read by week and name.

- [ ] `grep -rn "Lab [0-6] " docs/` and change each to the form "Week 4 lab — Flight Checklist".
- [ ] "Before this lab, read" blocks are unaffected; leave them.

## Step 7 — Verify

- [ ] `mkdocs build --strict`. Expected: clean, or INFO lines only for `grading_policy.md`,
      `coming_soon.md`, and the two answer-key pages if omitted.
- [ ] `mkdocs serve`, then click **every** nav entry. Confirm each week page's links resolve, each
      "This Week" lands on the right page, and the Reference duplicates open the same page as their
      week copy.
- [ ] Spot-check three URLs that Learning Suite is likely to link — a lab, a reading, the syllabus —
      and confirm they are unchanged from before the reorganization.

## Step 8 — Commit and push

- [ ] One commit for the reorganization, message in the style of the history (say what moved in the
      nav and that no URL changed). Second commit for the Week 3 lab if it lands separately.
- [ ] Push to `main`. Watch the Read the Docs build.

## Step 9 — Bookkeeping

- [ ] `planning/ai_context.md`: the "How `docs/` is organized" section and the nav description are
      now wrong. Rewrite them: nav is by week, `docs/weeks/` exists, labs are labelled by week, lab
      filenames are historical. Update the "Where things stand" block at the top.
- [ ] `planning/instructions.md`: add `docs/weeks/` to the folder table; note that adding a page
      means adding it to its week **and**, if cross-cutting, to Reference.
- [ ] `planning/backlog.md`: close the "Restore Topic labels" item (superseded — weeks instead),
      the "Reorder the nav to match class progression" item, the "Topic N references" item, and the
      "three sensor readings have no lab" item (they are Week 8 lecture material). Add: Week 12 page
      still missing; radar still in the Week 8 syllabus line.
- [ ] `planning/path_forward.md`: mark Sprint 3 done; note that Sprint 2's nav placement decision
      is now "Start Here plus Week 5".

---

## Not in scope

- Renumbering lab files. Breaks links; decided against.
- Rewriting the syllabus. Sprint 2.
- Writing the Week 12 FE/trig page. Backlog.
- Anything under `review/` or `fig_tools/fig_measurement.py` — those belong to the measurement
  reading work and are being handled separately.
