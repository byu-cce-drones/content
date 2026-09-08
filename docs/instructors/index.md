# For Instructors and TAs

!!! abstract "Key Takeaways"
    - This section is for the people who build the site, not the students who read it. It is still
      public — write nothing here you would not want a student to see.
    - The site is organized by week, matching the Learning Suite schedule. Each week has a "This
      Week" index page, plus the readings and lab for that week.
    - A page's URL never changes even when the navigation around it does, because Learning Suite
      links directly to pages. Moving a file breaks links; reorganizing the nav does not.
    - Planning documents, the backlog, and session notes live in `planning/` on GitHub, not on the
      published site.

---

## What this section is

The rest of the site is course content: readings, labs, the Part 107 material, the final project.
This section is documentation for whoever maintains that content — a new TA, a returning
instructor, anyone who needs to edit a page, add a figure, or build a lecture deck. It assumes you
can write Markdown but have not necessarily used MkDocs, git, or this repository before.

Three pages follow this one:

| Page | Covers |
|------|--------|
| [Editing the Site](editing.md) | Cloning the repo, previewing changes, page structure, admonitions, file naming, commit style |
| [Making Figures](figures.md) | The SVG figure toolchain, house style, naming, and how to place a new figure on a page |
| [Lecture Slides](slides.md) | The Marp slide toolchain: setup, building, and linking a deck from a week page |

## How the site is organized

The nav is grouped by course week (`docs/weeks/week_01.md` through `week_15.md`), matching the
Tuesday-lecture / Thursday-lab rhythm on the syllabus. Each week has a **"This Week" page** listed
first — it says what the week covers, what to read before Tuesday, and what the lab is, then links
to the full pages. The full readings and labs live in their own folders
(`docs/gen_reading/`, `docs/labs/`, `docs/part_107_license/`, `docs/software/`,
`docs/final_project/`) and are organized by what a page **is**, not by which week uses it.

A **Reference** section near the bottom of the nav lists the cross-cutting pages a second time —
checklists, software guides, aerial measurement products, common flight issues — so they can be
found without knowing which week they belong to. The same page appears at two nav entries; it is
still one file with one URL.

!!! warning "URLs do not follow the nav"
    Nav nesting in MkDocs does not change a page's URL. `docs/labs/2_measurements_and_methods.md`
    is served at the same address whether it is filed under Week 5 or listed twice under Reference.
    **Moving or renaming the file is what breaks a link.** Learning Suite's schedule links straight
    to these pages, so reorganize the `nav:` block freely, but treat a file path as fixed once it is
    published.

## What lives where in the repository

| Path | Holds |
|------|-------|
| `docs/` | Every published page and image. Everything here is student-facing. |
| `docs/weeks/` | The fifteen "This Week" index pages. |
| `mkdocs.yml` | The `nav:` block — the authoritative page order and grouping. |
| `fig_tools/` | Python scripts that generate the SVG figures. Not published; MkDocs never sees this folder. |
| `planning/` | Working documents for people building the course: writing conventions, background, and the backlog. Tracked in git, not published to the site. |
| `review/` | Scratch space for drafts and figure renders waiting on a look before they are committed. Git-ignored and temporary — nothing here is backed up. |

The planning documents are on GitHub at
[github.com/byu-cce-drones/content/tree/main/planning](https://github.com/byu-cce-drones/content/tree/main/planning).
`planning/backlog.md` there is the running to-do list: open gaps, decisions waiting on the
instructor, and known issues. Check it before starting new work, and add to it if you leave
something unfinished.

## Before you edit anything

- Read `planning/instructions.md` on GitHub. It is the house style guide for this repository —
  page structure, admonition usage, file naming, and figure conventions — and the source this
  section is condensed from.
- Build with `mkdocs build --strict` before you commit. It catches broken Markdown links and nav
  errors that a quick look in the browser will not.
- **Treat every edit under `docs/` as visible to students immediately after it is pushed.** There is
  no staging site and no review queue; `main` is what Read the Docs builds.
- Put drafts, work in progress, and anything you are not ready for a student to see in `review/`
  (git-ignored) until it is finished, then move the finished file into its real home under `docs/`.

## Getting help

If something in this section is out of date, or a step does not match what actually happens on
your machine, say so — fix the page if you can, or flag it to the instructor if you cannot. This
section describes the repository as it stands; the repository, not this section, is the source of
truth when the two disagree.

## Where to go next

Start with [Editing the Site](editing.md) if you are about to change a page for the first time.
