# Editing the Site

!!! abstract "Key Takeaways"
    - Clone the repo, install three Python packages, and `mkdocs serve` gives you a live preview at
      `localhost:8000` that updates as you save.
    - Run `mkdocs build --strict` before every commit. It fails the build on a broken link, which is
      exactly what you want it to do before a student sees it.
    - Every page follows the same structure: a title, a "Key Takeaways" box, `##` sections separated
      by `---`, admonitions used consistently, and a short closing section.
    - A new page has to be added to `mkdocs.yml` or it will build but never appear in the nav.

---

## Getting set up

Clone the repository from GitHub (`byu-cce-drones/content`), then install the packages MkDocs
needs:

```
pip install mkdocs pymdown-extensions python-markdown-math
```

!!! tip "If `python` or `pip` is not found"
    On some Windows machines the bare `python` command is not on the path, usually because Python
    was installed through Anaconda. If commands fail with "not recognized", use the full path to
    the Anaconda install instead, for example
    `C:\Users\<you>\anaconda3\python.exe -m pip install mkdocs pymdown-extensions python-markdown-math`.
    Ask a returning TA if you are not sure where Anaconda put itself on a given lab machine.

## Previewing your changes

From the repository root:

```
mkdocs serve
```

This starts a local server, usually at `http://127.0.0.1:8000`, and rebuilds the page you are
looking at every time you save a file. Leave it running in a terminal while you edit; it is the
fastest way to see whether a figure, a link, or an admonition rendered the way you expected.

## Before every commit

```
mkdocs build --strict
```

`--strict` turns warnings into build failures — a broken internal link, a page missing from the
nav, or a malformed reference all stop the build instead of quietly shipping a dead link. Run it
before you commit, not just before you push; it is fast, and it catches most mistakes in seconds.

**What `--strict` does not catch:**

- A path inside a raw HTML `<img>` tag. Prefer Markdown image syntax (`![alt](path)`) so broken
  paths are caught; raw HTML is invisible to the link checker.
- A `*Figure N: ...*` caption sitting under an image that failed to load or was never added.
- A page that exists, builds cleanly, and is simply empty.

Check those three by eye — load the page in `mkdocs serve` and look at it.

## Page structure

Every content page follows the same shape. `docs/gen_reading/flight_basics.md` is the model to
copy from.

1. `# Title` as the first line of the file.
2. A `!!! abstract "Key Takeaways"` admonition, three to five bullets, right after the title.
3. `---` on its own line between major sections.
4. `## Section` headings, `###` for subsections. Do not nest deeper than `###`.
5. An optional closing section: "Summary", "Check Your Understanding", or "Resources".

Write for a first-semester student with no prior drone, GIS, or surveying background. Define every
acronym on first use (UAS, SfM, GSD, AGL, VLOS, and so on), keep paragraphs short, and use concrete
civil engineering or construction examples. Give metric and US customary units together where a
student will encounter both in practice.

## Admonitions

Enabled types and when to reach for each:

| Type | Use for |
|------|---------|
| `abstract` | The "Key Takeaways" box at the top of every page |
| `note` | An aside — useful context that is not required to keep reading |
| `warning` | Safety or regulatory cautions, and anything a student could get badly wrong |
| `tip` | Practical advice — a habit, a shortcut, a way to avoid a common mistake |
| `example` | A worked problem |

Collapsible answer blocks (`??? note "Answers"`) are used for "Check Your Understanding" sections,
via `pymdownx.details`. Keep the question visible and the answer collapsed by default.

## File naming

- Lower-case file names with underscores, matching the existing pages — `mission_planning_sfm.md`,
  not `MissionPlanningSfM.md` or `mission-planning-sfm.md`.
- No spaces in a file name, ever. No numbered duplicates (`page (1).md`) and no `COPY` suffixes —
  if you are keeping an old version around, put it in `review/`, not in `docs/`.
- Put a new reading in `docs/gen_reading/` with its images in `docs/gen_reading/images/`; a new lab
  in `docs/labs/` with images in `docs/labs/images/`; and so on down the folder table in
  `planning/instructions.md`. The folder says what a page **is**, not which week it is used in.

## Adding a page to the nav

A new file is invisible until it is listed in `mkdocs.yml`. Add it in two places if it applies:

1. **Its week**, under the matching `Week N —` block, so a student following the schedule finds it.
2. **Reference**, near the bottom of `nav:`, if the page is cross-cutting — a checklist, a software
   guide, or anything a student might need to find outside the week it was assigned in.

The same file can be listed at two nav entries with no duplication problem; MkDocs serves it once,
at one URL, regardless of how many places link to it.

## Commit messages

Say which week and which page changed, in the style of the existing history — for example
"Standardize Week 6 SfM and Mission Planning materials" or "Fix a broken link on the Week 3 lab
page." A commit that touches the nav should say so.

## What never gets committed

- `site/` — the built output. It is regenerated by Read the Docs and should never be tracked.
- Large PDFs. The full FAA knowledge testing supplement, in particular, stays off the repository;
  a reduced copy already lives under `docs/part_107_license/images/`.
- Anything under `.claude/local/` — session notes and scratch files, git-ignored on purpose.
- Anything still under `review/` that has not been approved. Move it to its real home first.

## Where to go next

- [Making Figures](figures.md) for the SVG toolchain and figure naming.
- [Lecture Slides](slides.md) for building and linking a Marp deck.
- [For Instructors and TAs](index.md) for how the repository as a whole is organized.
