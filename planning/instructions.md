# Working Instructions

General conventions for anyone (human or AI) editing this repository.

## Voice and level

- Write for a first-semester student. Define every acronym on first use (UAS, SfM, GSD, AGL, VLOS).
- Prefer short paragraphs and concrete examples from civil engineering or construction sites.
- Tie techniques back to engineering judgment: accuracy needed, effort required, and why it matters.
- Use metric and US customary units together where students will see both in practice.

## Page structure

Each content page should follow the pattern established by the Readings pages
(`gen_reading/flight_basics.md` and `gen_reading/mission_planning_sfm.md` are the models):

1. `# Title` as the first line.
2. A `!!! abstract "Key Takeaways"` admonition with three to five bullets.
3. `---` separators between major sections.
4. `## Section` headings, with `###` for subsections. Avoid going deeper than `###`.
5. Optional closing sections: "Summary", "Check Your Understanding", or "Resources".

Use admonitions consistently: `abstract` for takeaways, `note` for asides, `warning` for safety or
regulatory cautions, `tip` for practical advice, `example` for worked problems.

## Files and naming

`docs/` is organized by what a page **is**, not by when it is used:

| Folder | Holds |
|--------|-------|
| `docs/weeks/` | The fifteen `This Week` index pages, `week_01.md` … `week_15.md`. Short: what the week covers, what to read, the lab, previous/next. Never a due date. |
| `docs/gen_reading/` | The readings. Images in `docs/gen_reading/images/`. |
| `docs/labs/` | The lab sessions. Numbers in the file names are historical; the nav labels labs by week. Images in `docs/labs/images/`. |
| `docs/part_107_license/` | Part 107 pages, practice exams, and keys. Images in `docs/part_107_license/images/`. |
| `docs/software/` | QGIS and Bentley iTwin how-to pages. |
| `docs/final_project/` | The five final project pages. |
| `docs/class_resources/` | Syllabus, grading policy, TA pages. |
| `docs/class_resources/flight_check_list/` | The checklists, grouped under Class Resources in the nav. |

The nav is organized by course week (`Week N — Title`, matching the syllabus schedule), with a
Reference section at the bottom that lists cross-cutting pages a second time. Adding a page means
adding it to its week **and**, if it is something students will look for out of sequence (a
checklist, a software guide, a reference table), to Reference as well. Update the week's `This Week`
page too.

Nav nesting does not change a page's URL in MkDocs, so a page can be regrouped in `nav:` without
moving the file or breaking a link. Moving the file does break links.

- Put a new reading in `docs/gen_reading/`; its images go in `docs/gen_reading/images/`.
- Use lower-case file names with underscores, matching existing pages (for example
  `mission_planning_sfm.md`). Do not leave duplicate or numbered copies such as `file (1).md` or
  `page COPY.md`, and never put a space in a file name.
- Prefer SVG for diagrams and keep raster images under a few hundred kilobytes.
- Any new page must be added to `nav:` in `mkdocs.yml`, or it will build but not appear.

## Figures

- Prefer a figure with a one-sentence caption over a paragraph. Aim for one figure per concept.
- All figures are SVG. Write the SVG directly for one-off drawings, or generate it with a script in
  `fig_tools/` when parts repeat or a numbered homework variant is needed. Scripts write their SVG
  into the owning section's `images/` folder, and both the script and the SVG are committed.
- Style is fixed so every week matches: light gray background with rounded corners, Arial font
  stack, 14 px labels, 17 px bold title at the top of the figure, 12 px subtitle for caveats,
  blue leader lines ending in a dot on the part. Palette and sizes live in `fig_tools/svgkit.py`.
- Drawings are generic. Brand names go in captions or tables, not in the picture. Where hardware
  varies between models, say so in the subtitle or caption.
- Keep text as text in the SVG. Do not convert labels to paths.
- File names: `wNN_figMM_short_name.svg` inside the owning section's `images/` folder, for example
  `w01_fig07_controller.svg` in `docs/gen_reading/images/`. The `wNN_` prefix is historical — it
  records which topic a figure belongs to and does **not** match a folder name any more. See the
  prefix table in `ai_context.md`. Lab figures use `labNN_figMM_short_name.svg` in `docs/labs/images/`,
  for example `lab00_fig01_controller.svg`, numbered as one sequence per lab. The prefix says which
  lab a figure came from once it is out of the repository, the same way `wNN_` does for a Topic. The week prefix means an exported figure still says where it came
  from once it is out of the repository. Scripts build the name with `svgkit.figure_name()`, so the
  number in the file name cannot drift away from the number printed inside the drawing.
- `MM` runs as **one sequence across a whole topic**, following the nav order of that topic's pages.
  A three-page topic numbers straight through rather than restarting at each page, so no two figures
  sharing a `wNN_` prefix have the same number. Note that several topics now share one `images/`
  folder, so it is the prefix plus the number that must be unique, not the number alone.
- A borrowed image's original file name is part of its provenance. Before renaming one, make sure
  the caption already records the source and the licence, or the trail back to it is lost. This
  matters most on the LiDAR and Thermal pages, where several images come from Wikimedia.
- The Markdown caption is an italic line under the image: `*Figure NN: ...*` The number there, the
  number in the file name, and the number in the drawing's own title must all agree.
- A figure used in more than one week is generated once per week with a `--number` flag, because the
  same drawing may be Figure 16 on one page and Figure 12 on another.
- Do not leave a `*Figure NN: ...*` caption on the page without the image above it. Seven such
  captions currently sit under nothing on the Part 107 overview page.
- Check every figure by rendering it to PNG (Inkscape command line, or `--png` on the script)
  and looking at it before committing.

## Before committing

- Build locally to catch broken links and nav errors:

  ```
  pip install mkdocs pymdown-extensions python-markdown-math
  mkdocs build --strict
  mkdocs serve
  ```

- Do not commit `site/`, large PDFs, or anything under `.claude/local/`.
- Write commit messages that say which week and which page changed, matching the existing history
  (for example, "Standardize Topic 4 SfM and Mission Planning materials").

- Check that internal links still resolve. `mkdocs build --strict` catches broken Markdown links but
  **not** paths inside raw HTML `<img>` tags, and not a caption whose image is missing.

## Working with Claude Code

- Project-wide context lives in this folder and is loaded through the root `CLAUDE.md`.
- Session notes, drafts, experiments, and anything you would not want a collaborator to read go in
  `.claude/local/` (git-ignored). Promote anything durable into `planning/` when it is ready.
- Draft figures, renders, and page drafts that are ready for Gus to look at go in `review/`
  (git-ignored). Files there are temporary: once approved they are moved to their real home
  (the section's `images/` folder, `docs/<section>/`, or `fig_tools/`) and added to git there; once rejected
  they are deleted. Clean `review/` out after each approved batch. See `review/README.md`.
- When asked to create or reorganize a topic, update `mkdocs.yml`, the page itself, and
  `planning/backlog.md` if the work leaves anything unfinished.

## Cross-referencing

- A lab should link to the reading a student was meant to have done, and a reading should link
  forward to the lab that uses it. Every lab opens with a "Before this lab, read" block and every
  reading with a lab has a "Where this is used" section (added 2026-09-04). Keep both current.
- Cross-links to labs read by week and name: `[Week 4 lab — Flight Checklist](../labs/1_flight_checklist.md)`.
  Not "Lab 1" (the file number is historical) and not a bare "Week 4" (a week number alone goes
  stale when the schedule moves).
- Link to a page, not to a topic or week number alone. `[Planning the Flight](../gen_reading/mission_planning_sfm.md)`
  always works; "Topic 4 covers this" was what the 2026-09-04 conversion had to clean up.
