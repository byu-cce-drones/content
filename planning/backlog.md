# Backlog

Open items, ideas, and known gaps. Move items to "Done" with the date rather than deleting them.

Last reconciled against the repository: **2026-09-04**, after the topic-material merge into `main`
(`1542bae`). A full site review from that date is in `review/SITE_REVIEW_2026-09-04.md`
(git-ignored); this file is the durable summary of what came out of it.

The instructor answered that review inline on 2026-09-04. Those answers are recorded against the
items below and worked into a sequenced plan in `planning/path_forward.md`. Where an item says
"instructor, 2026-09-04", the decision is made and does not need re-litigating.

## Waiting on the instructor

- **Review of `review/WEEK3_LAB_OUTLINE.md`**, the outline for the Week 3 Flight Practice lab. Six
  questions with `> GUS:` lines (TA ownership, timed vs. completion races, team size, figure prefix,
  overlap with Lab 0 Part 4, induced disorientation). The page is written only after this.
- A name for the Tier 2 list ("skills", "knowledge", "competencies"). Recommendation is in
  `path_forward.md` §1.
- Sign-off on the reworded Tier 1 outcomes M1-M4 and on where the measurement reading sits in the
  nav.
- Where the Lab 2 orthophoto should live long term.

## Build state

`mkdocs build --strict` passes with no warnings. Expected INFO lines for pages deliberately out of
the nav: `coming_soon.md`, `grading_policy.md`, and the two instructor answer-key pages. Anything
else is a regression.

Note what strict mode does **not** catch: paths inside raw HTML `<img>` tags, a `*Figure NN:*`
caption whose image is missing, and a page that is in the nav but empty.

---

## Blocking, student-visible

- [ ] **Lab 3 stops mid-page.** `labs/3_creating_flight_plans.md` ends after "Understanding Mission
      Constraints". It has no Activity Instructions, no Homework, no In Lab Reflection, and no
      Looking Ahead — the sections every other lab ends with.
- [ ] **Answer keys are published to students.** `mini_exam.md` and `60_question_exam.md` each carry
      a complete answer key inline at the bottom of the student page, and both instructor key pages
      are separate nav entries. The Part 107 practice test is 10% of the course grade. Instructor
      2026-09-04: leave for now. Revisit before the graded practice exam opens.
- [ ] **Decide whether to delete `class_resources/grading_policy.md`.** It is out of the nav as of
      2026-09-04 and no longer reachable from the site, but the file is still in the repository and
      shows up as the one orphan-page INFO line on a strict build. If nothing in it is worth folding
      into the syllabus, delete it and the commented nav line together.
- [ ] **`coming_soon.md`** is a bare image with no heading and a top-level nav entry. Instructor
      2026-09-04: leave for now.

---

## Learning outcomes

**Structure decided 2026-09-04 (instructor).** Two tiers, not one flat list:

- **Tier 1 — ABET outcomes.** Four measurement outcomes, worded generically enough that a surveying
  or environmental-measurements course could meet the same four. Drones are the vehicle, not the
  outcome. Short enough to assess and to defend at review time.
- **Tier 2 — course skills.** Everything drone-specific and course-specific, including the old
  thirteen. Deliberately *not* called learning outcomes. Each is attached to the lab, reading or
  homework that builds it, and collected on one master page.

Proposed wording for both tiers is in `planning/path_forward.md` §1.

- [ ] **Write the two-tier list and rewrite the syllabus around it.** The syllabus carries two
      parallel lists today — eight prose "Learning Outcomes" and thirteen "ABET Course Outcomes",
      said to cover the same material when they do not — and a third list matching neither is
      collapsed at the bottom of `gen_reading/class_overview.md`. End state: one Tier 1 list in the
      syllabus, one Tier 2 skills page, and `class_overview.md` pointing at the syllabus rather than
      carrying its own list.
- [ ] **Name the Tier 2 list.** Instructor to choose the term; `path_forward.md` §1 recommends
      "Course Skills".
- [ ] **Attach Tier 2 skills to the labs and homework that build them,** with a master list on one
      page.
- [ ] **Precision belongs in the ABET list, inside M1 — not as its own outcome.** M1 carries
      accuracy, precision and resolution; uncertainty is carried by M3, which requires reporting a
      result with it. All four terms are therefore in Tier 1 without adding a fifth outcome.
      Reasoning in `path_forward.md` §2.
- [ ] **Drop radar** from the outcome wording (instructor, 2026-09-04). It appears in old ABET #10
      and nowhere else on the site.
- [ ] **Old ABET #13, "Fundamental surveying concepts",** becomes a Tier 2 skill, not an outcome.
      Tied to the FE trig review item under Content gaps.

---

## Cross-referencing

- [ ] **The three sensor readings still have no "Where this is used" section.** Resolved as
      structure — they are Week 8 lecture material and the Week 8 page says so — but the pages
      themselves could still say they feed the final project's method-selection decision.
- [ ] **`gen_reading/metadata.md` still does not follow the house page structure.** It uses numbered
      `## 1.` headings unlike every other reading. Moved under Software in the nav 2026-09-04; the
      structure was left alone.
- [ ] **Week 12 has no page.** The syllabus schedules FE-style surveying review and basic
      trigonometry; `weeks/week_12.md` says the material will be posted and links nothing for it.
      Same gap as the FE/trig item under Content gaps, now visible in the nav.
- [ ] **Radar is still in the Week 8 syllabus line** ("LiDAR, radar, thermal, and multispectral
      sensors") although it was dropped from the outcomes and no page teaches it. Dropping it from
      the schedule line makes the three sensor readings match the week exactly.

---

## Content gaps

- [ ] **Write `gen_reading/measurement_fundamentals.md`** — the largest content gap on the site,
      agreed by the instructor 2026-09-04. The course is called Aerial Measurement, the syllabus
      schedules "Accuracy vs. precision" in Week 5, and no page covers measurement. Accuracy,
      uncertainty, error sources, ground truth and significant figures appear only inside Lab 2's
      activity instructions, where they cannot be assigned as pre-class reading or quizzed. It must
      cover accuracy, precision, resolution **and** uncertainty — instructor: "need all of these" —
      and tie explicitly to the Tier 1 outcomes. Section V of `mission_planning_sfm.md` ("How will
      you know it worked?") is the model to build from. Outline in `path_forward.md` §3.
- [ ] **Give the measurement reading top-level nav placement.** Instructor 2026-09-04: it is the base
      of the course, "an overriding concept, not a specific activity", so it should sit first or at a
      higher level rather than as one reading among ten. Proposal in `path_forward.md` §3.
- [ ] **Write the Week 3 lab, `labs/flight_practice.md`.** Currently a titled coming-soon stub in the
      nav (same pattern as Labs 4–6). Syllabus: Mini Drone Lab Part 2 — obstacle courses, team
      flight activities, flight challenges and races. Outline awaiting review, see top of this file.
- [ ] **FE-style surveying and basic trigonometry review.** Instructor 2026-09-04: the course may
      need a basic trig review for the FE exam, and where it fits in the semester is undecided. The
      syllabus schedules "FE-style surveying review" and "basic trigonometry" in Week 12; no page
      covers either.
- [ ] **The Lab 2 orthophoto is a SharePoint link.** `labs/2_measurements_and_methods.md` sends
      students to a SharePoint download that can expire or lose class-wide sharing, and that dies
      with the account if it sits in a personal OneDrive. Mitigations in `path_forward.md` §7.
- [ ] **Draw the seven missing Part 107 figures.** Seven italic captions on
      `part_107_license/faa_exam_planning_and_overview.md` render under nothing: Figures 15, 16, 19,
      20, 24, 25, 27. Instructor 2026-09-04 prefers all seven drawn over deleting the weaker five.
      Per-figure specs in `path_forward.md` §5. Figures 2, 5, 6, 8, 9, 17, 18 and 21 are unused
      numbers, so the sequence has gaps as well; recommendation is to leave the gaps rather than
      renumber every caption.
- [ ] **The labs have no figures.** The convention is set (`labNN_figMM_slug.svg` in
      `docs/labs/images/`); the drawings do not exist. Lab 0's homework asks students to label a
      controller, which `w01_fig07_controller.svg` already draws.
- [ ] **Lab 2's printable worksheet says "Coming Soon".**
- [ ] Neither flight checklist links to drone-specific lists yet. Both pages say those will be added
      rather than promising links that do not exist. Write them when the fleet is settled.
- [ ] `class_resources/ta/tas.md` has three TAs with empty bios and an empty "Grading
      Responsibilities" section, which both the syllabus and the TA page point students to.

---

## Final project

- [ ] **Ten open decisions**, listed at the bottom of `final_project/overview.md`: team size and
      formation, individual versus team grading, site selection, whether every team flies, all four
      due dates, minimum ground truth, processing software, submission location, presentation length
      and venue, and the late-work policy. Nineteen "Decision needed" admonitions are live on the
      site across the five pages, plus five "This page is a draft" banners. Instructor 2026-09-04:
      the project is still being worked on — leave the pages as they are and collect suggestions and
      open questions here rather than editing the pages.
- [ ] **Rubrics are suggestions.** Every point split in the four project pages is a proposal for the
      instructor to confirm or replace.
- [ ] **No AI-use policy** for the final report. Worth setting before the project is assigned.

---

## Images and attribution

- [ ] **Licensing on two Multispectral images.** `Screenshot-2019-04-09-14.04.41.webp` is a
      screenshot and `1_AQtOQh_X4O0JKZg9tGzOmA.webp` is a Medium CDN filename. No source, no author,
      no licence stated, on a public site. Both are NDVI map examples, so the fix is a real NDVI
      product from one of our own flights.
- [ ] **Attribution on the LiDAR photos.** `A_lidar_view_of_Ferrybridge_Henge_in_West_Yorkshire.jpg`
      and `Lidar_forestry.png` are Wikimedia originals with no link, author, or licence in the
      caption. The Thermal page links each image to its Commons page and is a good pattern to copy,
      though it still needs author and licence in visible text.
- [ ] **The two LiDAR photos still need renaming to `w06_figNN_`.** They are captioned Figure 2 and
      Figure 3 now, but keep their Wikimedia names until author and licence are captured.
- [ ] **The LiDAR examples are off-topic.** Archaeology and forestry, in a civil engineering and
      construction management class. The captions point at the civil parallel; the right fix is
      examples from actual project work — an earthwork site, a stockpile, a corridor.
- [ ] **Raw `<img>` tags** remain in five places on the Thermal and Multispectral pages. They work
      only because clean URLs are on, and `--strict` cannot check them. Convert to Markdown with
      `attr_list`.
- [ ] Replace the eight `w01_example_*.svg` placeholders on `gen_reading/data_products.md` with real
      products from class flights: orthomosaic, point cloud, DSM, DTM, 3D model, contours, thermal,
      and an index map. Each is a separate file, so they can be swapped one at a time.
- [ ] Replace `w01_overview_photo_placeholder.svg` on the Welcome page with a real photo of students
      flying. Worth having: pilot, controller, and aircraft in one frame; someone at a laptop with a
      finished map on screen. Check whether consent is needed for recognizable faces.
- [ ] Byte-identical duplicate images and unreferenced files remain in `gen_reading/images/`. Audit
      and remove.

---

## Housekeeping

- [ ] `mkdocs_thermal_page.html` sits at the repository root. Move it into `docs/` if it is used,
      otherwise remove it.
- [ ] `docs/requirements.txt` is published to the site root, because MkDocs copies every file in
      `docs/`. Harmless, but worth knowing before putting anything else in `docs/`.
- [ ] The DEM / DSM / DTM distinction: the readings now use DSM and DTM with DEM as the umbrella
      term. Worth an instructor glance to confirm that is how the three should be used course-wide.
- [ ] Decide whether the "Check Your Understanding" answers on `flight_basics.md` should stay
      visible on the public site. They are collapsed behind a toggle, not hidden.
- [ ] Confirm the three pre-class videos in `gen_reading/flight_basics.md`. They were restored from
      a deleted page and may have been dropped on purpose.

---

## Figure naming rollout

Figures are named `wNN_figMM_short_name.svg`, numbered as one sequence per topic in nav order. See
`instructions.md`. The `w01_`, `w04_` and `w05_` sets are converted.

- [ ] **Metadata page** — three images, one referenced, no figure numbers. `EB_Parking_Lot.png` and
      `EB_Parking_Lot_digital.png` are unreferenced; decide whether they are wanted before renaming.
- [ ] **LiDAR / Thermal / Multispectral** — seventeen images across three pages, none numbered on
      LiDAR and Multispectral, captions written as "Description:" rather than "Figure N". Several are
      Wikimedia originals whose file names carry the provenance, so record each source and licence in
      its caption before renaming.

---

## Ideas

- [ ] Add a course-wide glossary page for acronyms (UAS, SfM, GSD, AGL, VLOS, GCP, RTK, DSM, DTM,
      EXIF, CRS, NDVI). Several are defined more than once and at least one is never defined.
- [ ] Add "Check Your Understanding" questions to the readings that lack them, to match
      `flight_basics.md`.

---

## Deferred

- [ ] **Flight Basics Phase 4** — deferred by the instructor, September 2026. Keep, do not drop.
      Optional animation on two or three figures, a full read-through of both Topic 1 pages for
      length and consistency, and a backlog tidy. Pick this up once the other topics are revised.

---

## Done

- 2026-09-04 — **Site reorganized by week**, following `planning/reorg_plan.md`. Nav is now Home,
  Start Here, `Week 1` … `Week 15` (headings match the syllabus schedule), Reference. Fifteen
  `docs/weeks/week_NN.md` index pages, each with the week's lecture/lab summary, readings, lab, and
  previous/next links; Week 1 carries the TRUST-certificate requirement as its own section, the
  "how this site is organized" note, and the only mention of due dates. At the instructor's request
  the TRUST certificate was also lifted out of the Welcome page into its own reading,
  `gen_reading/trust_certificate.md`, listed as a third Week 1 nav entry. No file moved and no URL
  changed. Closed by this work:
    - "Restore Topic labels in the nav" — superseded; the site speaks in weeks. All thirteen
      "Topic N" prose references converted, plus "Topics 2 to 4" and "Topics 2, 3, 4, and 6" that
      the count had missed; `w01_fig16_rules.svg` and `w01_products_family.svg` regenerated from
      `fig_tools/` with "Week 3" / "Week 8" text and checked by eye.
    - "Reorder the nav to match class progression" — it now is the class progression.
    - "The final project does not link to the software pages" — `flight_and_data_processing.md`
      links Using QGIS (Week 4) and Bentley iTwin (Week 7).
    - "Three sensor readings have no lab" — they are Week 8 lecture material; downgraded above.
    - "Rename precision hovering / landing in Lab 0" — three occurrences now "controlled" /
      "more demanding maneuvers".
    - "How this site is organized note on `index.md`" — on Week 1's page, with a sentence and a
      Week 1 link on `index.md`.
    - Lab 0's Looking Ahead pointed at the Week 4 checklist lab while describing the Week 3 flying
      lab; it now points at `labs/flight_practice.md`. Sprint 1 cross-links relabelled from
      "Lab N — Name" to "Week N lab — Name" (16 places including two on the QGIS page).
    - `fig_tools/README.md` paths updated from the long-gone `docs/week_NN/images/`.
- 2026-09-04 — **Sprint 1 of `path_forward.md`.** Strict build clean; the only remaining orphan-page
  INFO line is `grading_policy.md`, which is deliberate.
    - Gave `labs/4_rock_canyon_flight.md`, `5_data_processing.md` and `6_part_107_studying.md` a
      title, a "coming soon" note naming what the lab will cover, and a "Before this lab, read" block.
      Correction to an earlier note in this file: the image path in those pages was **not** broken.
      MkDocs rewrites `../images/` correctly and the strict build always passed; the pages rendered
      as an untitled 1.8 MB logo, which is a different problem from a broken image.
    - Reverted `grading_policy.md` out of the nav.
    - Merged the three unique sections of `qgis_measurements COPY.md` into
      `software/qgis_measurements.md` — projected CRS vs. degrees (into the CRS Crash Course
      admonition), digitizing to a vector layer, and cut/fill from a DEM/DSM — and deleted the copy.
    - Merged the emergency checklist and the weak/strong checklist-item exercise from
      `labs/example.md` into `labs/1_flight_checklist.md` as a new `### Emergency` subsection and a
      new `## Writing a Checklist That Works` section, added two objectives, and deleted
      `example.md`.
    - Added "Before this lab, read" blocks to all seven labs, "Where this is used" sections to the
      seven readings that have a lab, and forward links in the Looking Ahead sections of Labs 0-2.
      Lab 3 has no Looking Ahead to link from; that is part of finishing Lab 3.
    - Linked Lab 2 to the QGIS page and reconciled the measure-tool discrepancy: the Measure tool is
      the quick answer, digitizing plus the Field Calculator is the recorded one, both should agree,
      and if they do not the CRS is the first thing to check. Added a units warning to Lab 2 Part 4.
    - Moved `metadata.md` under Software in the nav as "Photo Metadata". The file did not move, so
      no URL changed.
- 2026-09-04 — Fixed `site_url` in `mkdocs.yml`. It read
  `https://byu-cce_aerial_measurements.readthedocs.io/en/latest/` with underscores; the live site is
  `https://byu-cce-aerial-measurements.readthedocs.io/en/latest/` with hyphens, confirmed by the
  instructor. A wrong `site_url` breaks the canonical link on every page and every sitemap entry.
  Closes review question 16.
- 2026-09-04 — Recorded the instructor's answers to the site review against the items in this file
  and worked them into `planning/path_forward.md`. Review question 15 (push access) is also closed:
  `gus-p-williams` owns the repository and `main` tracks `origin/main` with nothing outstanding.
- 2026-09-04 — Added the four orphan pages to `nav:` (`grading_policy.md`,
  `qgis_measurements COPY.md`, `labs/example.md`, `coming_soon.md`) at the instructor's request.
  Strict build clean and the orphan INFO block is gone. All four are flagged above as still needing
  a real resolution.
- 2026-09-04 — Reconciled `ai_context.md`, `instructions.md` and this file against the merged
  repository. The old text described `docs/week_NN/` folders and a separate upstream repository;
  neither exists here. Recorded that `origin` is the published repository and that `gus-p-williams`
  currently has no push access to it.
- 2026-09-03 — Merged the topic material into `main`: rewritten readings and 56 figures, the
  `fig_tools/` toolkit, the Part 107 figure-naming pass and prohibitions figure, the final project
  scaffold, and the syllabus outcome rewrite. Five commits, 122 files, +13,603 / -745.
- 2026-09-03 — Thermal page reoriented to civil work: roof moisture, concrete delamination and
  concealed services replace search-and-rescue and agriculture. Added three figures and a timing
  table with real windows.
- 2026-09-03 — Redrew the LiDAR returns figure: one pulse with four returns beside a classified
  cross-section, with a legend and a note that the two surfaces coincide over open ground.
- 2026-09-03 — Added tracked `planning/` folder, root `CLAUDE.md`, git-ignored `.claude/local/`
  and `review/` folders.
- 2026-09-03 — Built `fig_tools/` (SVG toolkit, reusable parts, controller figure script) and
  recorded the figure style rules in `instructions.md`.
- 2026-09-03 — Flight Basics finished: all sections written with sixteen generated figures, plus
  Check Your Understanding with collapsible answers and a Resources section. Added
  `pymdownx.details` to `mkdocs.yml`.
- 2026-09-03 — Rewrote both mission-planning pages around the decisions a student actually makes,
  with nine figures. Algorithm names moved into a collapsed appendix.
- 2026-09-03 — Added `gen_reading/flight_issues.md` (symptom, cause, action tables plus a fly-away
  warning) and a feature-availability matrix inside Flight Basics.
- 2026-09-03 — Adopted `wNN_figMM_short_name.svg` for figure files. `svgkit.figure_name()` is now
  the only place a generated figure's name is built.
- 2026-09-03 — Added `flight_check_list/index.md`, filled the empty post-flight checklist, and
  removed the dangling "links below" promise from both checklist pages.
