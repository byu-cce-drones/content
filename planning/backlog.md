# Backlog

Open items, ideas, and known gaps. Move items to "Done" with the date rather than deleting them.

## Build warnings

`mkdocs build --strict` currently passes with no warnings. Keep it that way.

- [ ] `docs/coming_soon.md` is not in the nav. Decide whether it and
      `docs/images/logo_with_coming_soon.png` are still needed. (Reported as INFO, not a warning.)
- [ ] `docs/week_05/Week_5_60_Question_Exam_Instructor_Key (1).md` is a stray duplicate of the
      instructor key and is not in the nav. Confirm and remove.

## Labs and the final project

Brought across from `byu-cce-drones/content` on 2026-09-03. See `.claude/local/SOURCE_MATERIAL.md`.

- [ ] **Labs 4, 5 and 6 do not exist.** Rock Canyon Park flight, data processing, and Part 107
      studying are empty coming-soon stubs upstream, so there was nothing to bring across. They are
      referenced by Lab 3's "Looking Ahead" and by the syllabus schedule. Write them.
- [ ] **The labs have no figures.** Four labs, one borrowed photo (`holy_stone_controller.jpeg`,
      unreferenced) and one site image. Every lab would carry a figure or two well, and Lab 0's
      homework asks students to label a controller, which `w01_fig07_controller.svg` already draws.
      Convention is set (`labNN_figMM_slug.svg`); the drawings are not.
- [ ] **The final project is scaffolded, not decided.** `final_project/overview.md` ends with ten
      open decisions for the instructor and TAs: team size and formation, individual versus team
      grading, site selection, whether every team flies, all four due dates, minimum ground truth,
      processing software, submission location, presentation length and venue, and the late-work
      policy. Each page carries "Decision needed" admonitions in place. Resolve them, then delete
      the "This page is a draft" blocks.
- [ ] **Rubrics are suggestions.** Every point split in the four project pages is a proposal for the
      instructor to confirm or replace.
- [ ] **No AI-use policy** for the final report. Worth setting before the project is assigned.

## Content gaps

- [ ] Topic 5 `FAA_Exam_Planning_and_Overview.md` has captions for Figures 15, 16, 19, 20, 24, 25,
      and 27, but no matching image files exist. Figure 12 now exists (the three prohibitions);
      Figures 2, 5, 6, 8, 9, 17, 18 and 21 are still unused numbers. Those captions currently sit under nothing.
      Either draw the figures or remove the captions.
- [ ] Neither flight checklist links to drone-specific lists yet. Both pages now say those will be
      added rather than promising links that do not exist. Write them when the fleet is settled.

## Topic 6 images — revisit

Instructor decision, September 2026: keep the current images for now and revisit later.

- [ ] **Licensing on the remaining two Multispectral images.**
      `Screenshot-2019-04-09-14.04.41.webp` is a screenshot and `1_AQtOQh_X4O0JKZg9tGzOmA.webp` is a
      Medium CDN filename. No source, no author, no licence stated, on a public site. Both are NDVI
      map examples, so the fix is a real NDVI product from one of our own flights.
      Half done: the spectrum chart and the leaf reflectance curve were the other two, and Figure 10
      (`fig_tools/fig_spectral.py`) now draws both in one figure. Those two files are deleted.
- [ ] **Attribution on the LiDAR photos.** `A_lidar_view_of_Ferrybridge_Henge_in_West_Yorkshire.jpg`
      and `Lidar_forestry.png` are Wikimedia originals with no link, author, or licence in the
      caption. The Thermal page links each image to its Commons page and is a good pattern to copy,
      though it still needs author and licence in visible text.
- [ ] **The two LiDAR photos still need renaming to `w06_figNN_`.** They are captioned Figure 2 and
      Figure 3 now, but keep their Wikimedia file names because the rename should happen together
      with capturing their author and licence.
- [ ] **The LiDAR examples are off-topic for this course.** Archaeology and forestry, in a civil
      engineering and construction management class. The captions now point at the civil parallel,
      but the right fix is examples from actual project work: an earthwork site, a stockpile, a
      corridor.
- [ ] **4.4 MB of byte-identical duplicates.** Three thermal images exist twice under different
      names; the Wikimedia-named copies are never displayed. Also unused:
      `Effigy_mounds_lidar.jpg`, `Infrared_thermal_imaging_during_a_yacht_survey.jpg`,
      `LIDAR_field_yield.jpg`, `Tank-DSM-filled.webp`, and both files in `week_06/media/`.
- [ ] **Raw `<img>` tags** remain on the Thermal and Multispectral pages, which work only because
      clean URLs are on. Convert to Markdown with `attr_list`. Two fewer on Multispectral now that
      the spectrum and leaf images are gone.

## Housekeeping

- [ ] `docs/week_03/` now holds only `metadata.md`. The measurement lab moved to
      `docs/labs/2_measurements_and_methods.md` (the TA version, which supersedes the older, shorter
      copy that was here). Decide whether Topic 3 should absorb another page or be folded elsewhere.
- [ ] Upstream has `docs/software/qgis_measurements COPY.md`, a stray duplicate with a space in the
      filename, published live as `software/qgis_measurements%20COPY/`. Not brought across. Flag it
      to the TAs.


- [ ] Topic 6 uses raw `<img src="../images/...">` tags in seven places. MkDocs does not rewrite
      paths inside raw HTML, so these work only because clean URLs are on. Convert them to Markdown
      images with `attr_list` for sizing, matching the other weeks.
- [ ] `test_image.jpg` and `mkdocs_thermal_page.html` sit at the repository root. Move them into
      `docs/` if they are used, otherwise remove them.
- [ ] `docs/requirements.txt` is published to the site root, because MkDocs copies every file in
      `docs/`. Harmless, but worth knowing before putting anything else in `docs/`.

## Figure naming rollout

Figures are named `wNN_figMM_short_name.svg`, numbered as one sequence per week in nav order. See
`instructions.md`. Topics 1 and 5 are converted. The rest are deferred to each week's content
revision, because they have no figure numbers today and inventing numbers now would only be redone
when the captions are rewritten.

- [ ] **Topic 3** — three images, one referenced, no figure numbers anywhere. Assign numbers and
      rename during the Topic 3 revision. `EB_Parking_Lot.png` and `EB_Parking_Lot_digital.png` are
      unreferenced; decide whether they are wanted before renaming them.
- [x] **Topic 4** — done. Both pages rewritten with nine numbered figures, `w04_figNN_`, running
      through the week in nav order.
- [ ] **Topic 6** — seventeen images across three pages, none numbered, captions written as
      "Description:" rather than "Figure N". Several are Wikimedia originals whose file names carry
      the provenance, so record each source and licence in its caption before renaming. Seven
      references are raw HTML `<img>` tags that also need converting to Markdown (see Housekeeping).
      Unreferenced: `Effigy_mounds_lidar.jpg`, `Infrared_thermal_imaging_during_a_yacht_survey.jpg`,
      `LIDAR_field_yield.jpg`, `Tank-DSM-filled.webp`, and both files in `week_06/media/`.

## Topic 1 follow-ups

- [ ] Replace the eight `w01_example_*.svg` placeholders on `week_01/data_products.md` with real
      products from class flights: orthomosaic, point cloud, DSM, DTM, 3D model, contours, thermal,
      and an index map. Each is a separate file, so they can be swapped one at a time as data
      becomes available.
- [ ] Replace `w01_overview_photo_placeholder.svg` on the overview page with a real photo of
      students flying. Worth having: pilot, controller, and aircraft all in one frame; someone at a
      laptop with a finished map on screen. Check whether consent is needed for recognizable faces.
- [ ] The old overview defined DEM as including vegetation and structures, which is really a DSM.
      The rewrite uses DSM and DTM, matching Topics 4 and 6, and treats DEM as the umbrella term.
      Worth a glance to confirm that is how you want the three used across the course.

- [ ] Confirm the three pre-class videos in `week_01/flight_basics.md`. They were restored from
      `DJI_Mini_Resources.md`, which commit `d173bd4` deleted during the Topic 1 reorganization, so
      they may have been dropped on purpose.
- [ ] Decide whether the Check Your Understanding answers should stay visible on the public site.
      They are collapsed behind a toggle, not hidden.

## Ideas

- [ ] Add a course-wide glossary page for acronyms (UAS, SfM, GSD, AGL, VLOS, GCP, RTK).
- [ ] Add "Check Your Understanding" questions to Topics 1 through 4 to match the Topic 5 practice exams.
- [ ] Decide whether instructor answer keys should stay on the public site or move to a private
      location.

## In progress: Topic 1 Flight Basics

Plan agreed September 2026. Generic, figure-led page in Topic 1, with detail moved to linked pages.

- [x] Phase 0 — figure style approved; `fig_tools/` toolkit and generic controller figure built.
- [x] Phase 1 — page skeleton, flight checklist landing page, post-flight list, nav fix,
      clean strict build. Awaiting instructor review of the checklist overview prose.
- [x] Phase 2 — all sections written, sixteen figures. Figure 2 (an underside view of the
      aircraft) was planned but not needed; add it only if the parts table proves thin in class.
- [x] Phase 3 — `week_01/flight_issues.md` added with Figures 17 to 19 and linked from Flight
      Basics and the pre-flight checklist; feature-availability matrix added as a section of Flight
      Basics rather than its own page, since it is one table.
- [ ] Phase 4 — **deferred by the instructor, September 2026. Keep, do not drop.** Optional
      animation on two or three figures, a full read-through of both Topic 1 pages for length
      and consistency, and a backlog tidy. Pick this up once the other weeks are revised.

## Done

- 2026-09-03 — Topic 6 thermal page reoriented to civil work: roof moisture, concrete
  delamination and concealed services replace search-and-rescue and agriculture. Added three
  figures (what the camera reads, emissivity and false hotspots, when to fly) and a timing
  table with real windows rather than "early morning or late evening".
- 2026-09-03 — Redrew the LiDAR returns figure as Topic 6 Figure 1: one pulse with four
  returns beside a classified cross-section, with a legend and a note that the two surfaces
  coincide over open ground. Numbered the LiDAR page's three figures.

- 2026-09-03 — Added tracked `planning/` folder, root `CLAUDE.md`, git-ignored `.claude/local/`
  and `review/` folders.
- 2026-09-03 — Built `fig_tools/` (SVG toolkit, reusable parts, controller figure script) and
  recorded the figure style rules in `instructions.md`. Folder named `fig_tools`, not `figures`,
  so it is not mistaken for a folder of images.
- 2026-09-03 — Topic 1 Flight Basics finished: all sections written with sixteen generated
  figures, plus Check Your Understanding with collapsible answers and a Resources section.
  Automated Flight Functions sits below A Basic Flight so students meet manual flying first.
  Added `pymdownx.details` to `mkdocs.yml` for the collapsible answer blocks.
- 2026-09-03 — Redrew Topic 4 Figure 3 around one building at four stages, and added Figure 3b
  for where the orthophoto and DSM come from.
- 2026-09-03 — Rewrote both Topic 4 pages around the decisions a student actually makes, with nine
  figures. Six are new (parallax, overlap, overlap cost, GSD, nadir/oblique, accuracy) and three
  replaced older drawings. Algorithm names moved into a collapsed appendix.
- 2026-09-03 — Added `week_01/flight_issues.md` (symptom, cause, action tables plus a fly-away
  warning) and a feature-availability matrix inside Flight Basics.
- 2026-09-03 — Adopted `wNN_figMM_short_name.svg` for figure files and converted Topics 1 and 5.
  `svgkit.figure_name()` is now the only place a generated figure's name is built.
- 2026-09-03 — Fixed the Topic 1 nav entry (`DJI_Mini_Basics.md` never existed) by adding
  `week_01/flight_basics.md`. Added `flight_check_list/index.md`, filled the empty post-flight
  checklist, and removed the dangling "links below" promise from both checklist pages. The strict
  build is now clean.
