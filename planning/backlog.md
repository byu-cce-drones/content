# Backlog

Open items, ideas, and known gaps. Move items to "Done" with the date rather than deleting them.

Last reconciled against the repository: **2026-09-04**, after the topic-material merge into `main`
(`1542bae`). A full site review from that date is in `review/SITE_REVIEW_2026-09-04.md`
(git-ignored); this file is the durable summary of what came out of it.

## Build state

`mkdocs build --strict` passes with no warnings and no orphan-page INFO lines. Keep it that way.

Note what strict mode does **not** catch: paths inside raw HTML `<img>` tags, a `*Figure NN:*`
caption whose image is missing, and a page that is in the nav but empty.

---

## Blocking, student-visible

- [ ] **Three lab pages are empty files in the nav.** `labs/4_rock_canyon_flight.md`,
      `labs/5_data_processing.md` and `labs/6_part_107_studying.md` are zero bytes and publish as
      blank pages. Either write them or take them out of `nav:` until they exist.
- [ ] **Lab 3 stops mid-page.** `labs/3_creating_flight_plans.md` ends after "Understanding Mission
      Constraints". It has no Activity Instructions, no Homework, no In Lab Reflection, and no
      Looking Ahead — the sections every other lab ends with.
- [ ] **Answer keys are published to students.** `mini_exam.md` and `60_question_exam.md` each carry
      a complete answer key inline at the bottom of the student page, and both instructor key pages
      are separate nav entries. The Part 107 practice test is 10% of the course grade. Decide what
      stays public.
- [ ] **`class_resources/grading_policy.md` describes a different course.** Raw HTML from Learning
      Suite: midterms and a final, Colab notebooks and spreadsheet formulas, three units, groups of
      three, a 10%-per-week late penalty. The syllabus says none of that. Added to the nav
      2026-09-04 at the instructor's request; rewrite it against the syllabus or drop it.
- [ ] **`software/qgis_measurements COPY.md` is a duplicate.** Raw HTML, no `# Title`, space in the
      filename. It does hold three things the real QGIS page lacks: projected CRS vs. degrees,
      digitizing to a vector layer, and cut/fill from a DEM/DSM. Merge those into
      `software/qgis_measurements.md`, then delete the copy.
- [ ] **`labs/example.md` is a second checklist lab.** "Drone Operations Checklist Lab", 635 lines,
      overlaps `labs/1_flight_checklist.md` and is more detailed than it. It also uses numbered `##`
      headings where the real labs do not. Merge the good parts into Lab 1 and delete it, or promote
      it and retire Lab 1.
- [ ] **`coming_soon.md`** is a bare image with no heading. Now in the nav. Remove it, or give it a
      title and a purpose.

---

## Learning outcomes

- [ ] **The syllabus carries two parallel outcome lists.** Eight "Learning Outcomes" and thirteen
      "ABET Course Outcomes", said to "cover the same material" — they do not. The ABET list is a
      topic inventory, not outcomes: #13 is the bare fragment "Fundamental surveying concepts", #10
      lists radar which the course never teaches, and #4 and #5 are lab activities rather than
      outcomes. For a one-credit freshman measurements course this should be **three or four**
      measurement outcomes. Draft wording is in the review file.
- [ ] **A third outcome list is hidden on the Welcome page.** `gen_reading/class_overview.md` ends
      with a collapsed "Course learning objectives" block of four bullets that match neither
      syllabus list. Point it at the syllabus instead.
- [ ] **ABET outcome 6 has nothing behind it.** "Explain the difference between accuracy and
      precision" — precision is never defined anywhere on the site in the measurement sense. The
      only occurrences are "precision hovering" and "precision landing" in Lab 0, which is the
      flying sense and will actively confuse a freshman.

---

## Cross-referencing

- [ ] **No lab links to any reading, and no reading links to any lab.** Zero edges in either
      direction across 41 pages. Each lab ends with a "Looking Ahead" that describes the next lab in
      prose without linking to it or to the reading behind it.
- [ ] **"Topic N" references do not resolve.** Thirteen in prose plus two baked into SVG text
      (`w01_fig16_rules.svg`, `w01_products_family.svg`). The nav has no Topic labels. Either
      restore Topic labels in `nav:` or replace each reference with a page link.
- [ ] **The software pages are unreachable from anywhere.** Lab 2 runs on QGIS and never links to
      `software/qgis_measurements.md`; the final project names Bentley iTwin and QGIS as "Topic 2"
      without linking either.
- [ ] **`gen_reading/metadata.md` has no inbound link.** It is in the nav and nothing points at it.
      The Bentley iTwin workflow depends on EXIF and would be the natural place to link from.

---

## Content gaps

- [ ] **There is no measurement reading.** The course is called Aerial Measurement, the syllabus
      schedules "Accuracy vs. precision" in Week 5, and the Readings section has no page on
      measurement fundamentals. Accuracy vs. precision, uncertainty, error sources, ground truth and
      significant figures appear only inside Lab 2's activity instructions, where they cannot be
      assigned as pre-class reading or quizzed. Section V of `mission_planning_sfm.md` ("How will
      you know it worked?") is the one good treatment on the site and is the model to build from.
- [ ] **Seven figure captions sit under no image** on
      `part_107_license/faa_exam_planning_and_overview.md`: Figures 15, 16, 19, 20, 24, 25, 27.
      Either draw them or remove the captions.
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
      site across the five pages, plus five "This page is a draft" banners.
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
- [ ] A short "how this site is organized" note on `index.md`, which is currently three sentences of
      boilerplate and does not link to anything.

---

## Deferred

- [ ] **Flight Basics Phase 4** — deferred by the instructor, September 2026. Keep, do not drop.
      Optional animation on two or three figures, a full read-through of both Topic 1 pages for
      length and consistency, and a backlog tidy. Pick this up once the other topics are revised.

---

## Done

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
