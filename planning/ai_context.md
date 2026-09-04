# AI Context

Read this before editing any course content.

## Where things stand — 2026-09-04

Start here after any gap. This section is tracked, so it survives a re-clone even when Claude Code's
per-project memory does not.

**Repository.** As of the evening of 2026-09-04, `origin/main` is at `b791fb1` or later: Sprint 1
(`bc1f4c9`), the site-by-week reorganization (`7aaa3b3`), and the Measurement Fundamentals reading
(`b791fb1`) are all pushed. Run `git fetch && git status -sb` first; a Week 3 lab commit may have
landed after this was written. Gus owns `byu-cce-drones/content` outright and pushes to `main`
directly — no fork, no pull request step. `gh` is not installed; use plain `git`.

**Starting on a new machine.** Everything durable is in this folder (`planning/`) and in git. Claude
Code's per-project memory does **not** travel between machines — this block is the recovery point.
Two sessions ran in parallel on 2026-09-04 (one on the reorganization and the Week 3 lab, one on the
measurement reading); that split is over, and a new session can pick up any item below alone. Machine
notes from the original workstation: bare `python` failed there, so scripts were run with the full
Anaconda path (`.../anaconda3/python.exe -m mkdocs build --strict`); Inkscape was installed for
`fig_tools` PNG renders (`--png` flag). Confirm both on the new machine before assuming.

**The working folder was renamed.** It is no longer `G:\GIT_Repo\content`; the clone was recreated
under a folder carrying the org name (expected `G:\GIT_Repo\byu-cce-drones-content`). Confirm the
real path from the session's working directory rather than assuming it. Claude Code keys memory and
history to a slug derived from that path, so if a session starts knowing nothing about this project,
that is why, and this section is the recovery point.

**Four things live only on disk and are not on GitHub.** They were copied across by hand during the
move and any future re-clone must do the same:

| Path | Holds |
|---|---|
| `review/` | `SITE_REVIEW_2026-09-04.md` (the site review, with Gus's answers), `WEEK3_LAB_OUTLINE.md` (awaiting instructor review), `MEASUREMENT_READING_PLAN.md` and `SITE_REORG_BY_WEEK.md` (reasoning behind work now landed; decisions are duplicated in `planning/`), `measurement_fundamentals_DRAFT.md` (superseded by the live page), and PNG renders of figures |
| `.claude/local/` | `SOURCE_MATERIAL.md`, `notes.md`, `rtd_snapshot/`, `instructor_bundle/`, `drafts/`, `scratch/` |
| `.claude/settings.local.json` | per-machine permission allowlist, untracked in `51bff7f` |
| `fig_tools/__pycache__/` | disposable |

**There is an open site review.** `review/SITE_REVIEW_2026-09-04.md` is a full read-through of all 41
published pages: findings, a proposed set of ABET outcomes, a suggested order of work, and 16
questions for the instructor. Gus answers inline with `> GUS:` prefixes — never delete or rewrite
those. Read it before proposing content work. Its durable summary is `backlog.md` in this folder.

**What was last done.** Sprint 1 of `path_forward.md` (`bc1f4c9`), then the **site reorganization by
week** following `planning/reorg_plan.md`: the nav is now fifteen `Week N — Title` sections matching
the syllabus schedule, each led by a `This Week` page in `docs/weeks/`, plus a Reference section.
Every "Topic N" reference in prose and in two SVGs became a week reference, Lab 0's Looking Ahead
now points at the Week 3 lab, and the three flying uses of "precision" in Lab 0 became "controlled".
The TRUST certificate got its own page, `gen_reading/trust_certificate.md`, listed under Week 1.
`docs/labs/flight_practice.md` (the Week 3 lab) is a titled coming-soon stub; its outline is in
`review/WEEK3_LAB_OUTLINE.md` waiting for instructor review. No URL changed.

Then the **Measurement Fundamentals reading** (`b791fb1`): `gen_reading/measurement_fundamentals.md`,
general engineering measurement with drones confined to one table, seven `w00_` figures from
`fig_tools/fig_measurement.py`, in the nav under Start Here and Week 5, linked from the Week 5 page,
and a standard-deviation step added to Lab 2 Part 1. The reasoning and the instructor's answers that
shaped it are in `review/MEASUREMENT_READING_PLAN.md`; `path_forward.md` §2–§3 holds the durable
version.

**What is waiting on Gus.** The Week 3 lab outline (`review/WEEK3_LAB_OUTLINE.md`, six questions with
`> GUS:` lines); sign-off on `path_forward.md` §1 (the two-tier outcomes: M1–M4 wording, the
thirteen "Course Skills", and the name for that list) before the syllabus is rewritten; where the
Lab 2 orthophoto should live; real accuracy numbers for the aerial table in the measurement reading,
if wanted; and the ten final-project decisions. The Learning Suite screenshots are no longer needed.

**What is next, in order.** (1) Finish the Week 3 lab once the outline is approved. (2) The syllabus
and outcomes rewrite — `path_forward.md` §1 has the proposed wording; it replaces both existing
lists, adds `class_resources/course_skills.md`, and points `class_overview.md` at the syllabus.
(3) The seven missing Part 107 figures, specced in `path_forward.md` §5. Everything else is in
`backlog.md`.

## What this repository is

- Source for a Read the Docs site built with **MkDocs** (`readthedocs` theme). Config lives in
  `mkdocs.yml`; the build environment is in `.readthedocs.yaml` and `docs/requirements.txt`.
- All published content is Markdown under `docs/`.
- Figures are SVG. Many are generated by scripts in `fig_tools/` (outside `docs/`, so MkDocs never
  publishes the scripts) and committed as SVG under the owning section's `images/` folder. See
  `instructions.md` for the style rules.
- The site is the homework and exercise companion to the class. The BYU Learning Suite schedule
  links into these pages.

## This is the published repository

`origin` is `https://github.com/byu-cce-drones/content` and **this is the repository the student
site builds from**. Work merged here is visible to students. There is no longer a separate
"upstream" repo to port from: the topic-organized material that used to live in a personal
`week_NN/` repository was merged into `main` on 2026-09-03.

Practical consequence: treat every edit under `docs/` as student-facing. Draft work belongs in
`review/` or `.claude/local/` until it is ready.

**Push access.** `gus-p-williams` owns the repository and can push to `main` directly as of
2026-09-04. Work on `main`, tracking `origin/main`; there is no fork-and-pull-request step. An
earlier personal fork (`github.com/gus-p-williams/content`) was deleted once ownership was granted.
`gh` CLI is not installed on the working machine, so use plain `git` for everything.

## The course

- **Title:** CCE 194R — Aerial Measurement (site title: BYU CCE Drone Measurements).
- **Audience:** freshman Civil Engineering and Construction Management students. Assume no prior
  drone, GIS, or surveying experience.
- **Format:** one-credit introductory course. One 50-minute lecture (Tue) plus a 110-minute lab
  (Thu) per week, over a 14-15 week semester. Lecture content must fit in about one hour.
- **Central theme:** drones are *measurement instruments* for engineers. Every page should connect
  back to the question "is this data appropriate, reliable, and defensible for the decision at
  hand?" Accuracy versus effort (pacing vs. Google Maps vs. drone) is the recurring idea.

## How `docs/` is organized

Folders are named by what a page **is**, not by when it is used. The one exception is `docs/weeks/`,
which holds the fifteen short `This Week` index pages; the full readings and labs stay in their
section folders. There are no `week_NN/` content folders.

| Folder | Holds |
|--------|-------|
| `docs/weeks/` | `week_01.md` … `week_15.md`: one index page per week — what the week covers, what to read, what the lab is, previous/next links. Week 1 also carries the TRUST-certificate requirement and the "how this site is organized" note. No due dates; those live in Learning Suite. |
| `docs/gen_reading/` | The readings, including `trust_certificate.md`. Images in `docs/gen_reading/images/`. |
| `docs/labs/` | The lab sessions. File names carry historical numbers (`0_` … `6_`) plus the unnumbered `flight_practice.md`; the nav labels labs by week, not number. Images in `docs/labs/images/`. |
| `docs/part_107_license/` | Part 107 overview, knowledge review, resources, practice exams and keys. Images in `docs/part_107_license/images/`. |
| `docs/software/` | QGIS and Bentley iTwin how-to pages. |
| `docs/final_project/` | The five final project pages. |
| `docs/class_resources/` | Syllabus, grading policy, TA pages, and the flight checklists. |

The authoritative nav is the `nav:` block in `mkdocs.yml`, **organized by course week** since
2026-09-04 (`planning/reorg_plan.md`): Home, Start Here (syllabus, TAs), then `Week 1 — Course
Introduction` through `Week 15 — Final Presentations` with headings matching the syllabus schedule
exactly, then Reference. Each week section leads with its `This Week` page, then `Reading — Name`
entries, then `Lab — Name`. Reference lists the cross-cutting pages (checklists, QGIS, Bentley,
metadata, products, flight issues) a second time so they can be found without knowing the week; a
page may appear in the nav more than once and `--strict` accepts it.

When a page is added, put it under its week **and**, if it is cross-cutting, under Reference. Nav
nesting does not change a page's URL, so a page can be regrouped without moving the file; moving or
renaming the file does break Learning Suite links, which is why lab files keep their old numbers.

Deliberately **not** in the nav: the two instructor answer-key pages, `coming_soon.md`, and
`grading_policy.md`. They build, are reachable by URL, and show up as four INFO lines on a strict
build. The Measurement Fundamentals line under Week 5 is commented out until that page lands.

### Figure prefixes do not match folder names

Figure files still carry `wNN_` prefixes (`w01_`, `w04_`, `w05_`, `w06_`) from the earlier
week-numbered organization, even though the folders are now named by section. That is deliberate:
renaming would churn every reference for no student-visible benefit. The prefix records which topic
a figure came from once it is out of the repository. Roughly:

| Prefix | Lives in | Covers |
|--------|----------|--------|
| `w01_` | `docs/gen_reading/images/` | Welcome, Aerial Measurement Products, Flight Basics, Common Flight Issues |
| `w04_` | `docs/gen_reading/images/` | How Photos Become 3D, Planning the Flight |
| `w05_` | `docs/part_107_license/images/` | Part 107 material |
| `w06_` | `docs/gen_reading/images/` | LiDAR, Thermal, Multispectral |

### Weeks, not Topics

The material was once organized in six Topics; the site now speaks in weeks. Every "Topic N" in
prose and in the two SVGs that carried it was converted on 2026-09-04, and cross-links to labs read
"Week 4 lab — Flight Checklist". If an old commit, figure prefix, or note says "Topic N", this is
what it meant:

| Old Topic | Covered | Now |
|---|---|---|
| 1 | Welcome, products, flight basics, flight issues | Weeks 1–3 |
| 2 | QGIS and Bentley | Week 4 (QGIS), Week 7 (Bentley) |
| 3 | Metadata | Week 7 |
| 4 | How Photos Become 3D, Planning the Flight | Weeks 6–7 |
| 5 | Part 107 | Week 3 (overview), Week 9 (exam prep) |
| 6 | Sensors | Week 8 |

## Hardware and software referenced

- **Aircraft:** Holy Stone mini drones for the indoor labs; larger mapping aircraft for fieldwork.
- **Software:** Bentley iTwin Capture Modeler, QGIS, Google Maps/Earth.
- **Regulatory:** TRUST for the in-class recreational flying, FAA Part 107 for the certificate the
  course prepares students for. Part 107 material tracks the FAA Airman Knowledge Testing Supplement
  (FAA-CT-8080-2H). The full PDF is git-ignored; a reduced copy lives in
  `docs/part_107_license/images/`.

## Markdown features in use

Enabled in `mkdocs.yml`: `admonition` (used heavily for "Key Takeaways" blocks), `attr_list`,
`md_in_html`, `sane_lists`, `pymdownx.arithmatex` (MathJax), `pymdownx.details`,
`pymdownx.tasklist`, `pymdownx.emoji`. Custom styling is in `docs/css/custom.css`; MathJax config is
in `docs/js/mathjax-config.js`.

## People

- Repository owner, instructor, and primary author: Gus Williams (`gus-p-williams` on GitHub).
  Refer to review by Gus as "instructor review".
- TAs also commit content. Past contributors in the history: `Brandan-W`, `norar24`.
- Content goes through a review pass before landing. Call it "TA review" or "instructor review"
  depending on who did it.

## Things to be careful about

- **Answer keys are public.** Two instructor key pages are in the nav, and `mini_exam.md` and
  `60_question_exam.md` each carry a full answer key inline at the bottom of the *student* page.
  The Part 107 practice test is worth 10% of the course grade. Do not add or move exam answers
  without checking with the instructor.
- `docs/class_resources/grading_policy.md` is raw HTML pasted from Learning Suite and describes a
  **different course** (midterms, Colab notebooks, three units, groups of three). It contradicts the
  syllabus. It was briefly in the nav on 2026-09-04 and reverted the same day; the file is still in
  the repository and should be deleted or folded into the syllabus.
- `docs/labs/4_rock_canyon_flight.md`, `5_data_processing.md`, `6_part_107_studying.md` and
  `flight_practice.md` are **titled coming-soon stubs in the nav**. TAs own the first three; the
  fourth is the Week 3 lab whose outline is under instructor review.
- Keep external links and figures attributable. Several LiDAR and Thermal images come from Wikimedia
  and need their captions and credits preserved.
- Do not commit the full FAA supplement PDF or other large binaries.
