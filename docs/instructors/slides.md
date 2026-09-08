# Lecture Slides

!!! abstract "Key Takeaways"
    - Lecture decks are written in Markdown and built with **Marp**, a slide toolchain separate from
      MkDocs. Sources live in `docs/slides/week_NN.md`; built HTML and PDF are committed alongside
      them and served as static files.
    - `mkdocs.yml` excludes the slide sources from the site build, so a deck's Markdown never
      becomes a page of its own — only the exported HTML/PDF is reachable.
    - A deck reuses the same figures as the reading, at the same relative path, and is a subset of
      the reading, not a copy of it.
    - Build with `python fig_tools/build_slides.py`, then link the result from the week page and
      commit the source and the export together.

---

## One-time setup

Each machine that builds slides needs:

- **Node.js LTS**, then `npm install -g @marp-team/marp-cli` to install the Marp command line tool.
- **A Chromium-based browser** for PDF and PPTX export — on Windows, Microsoft Edge is enough; Marp
  finds it automatically.
- **The "Marp for VS Code" extension**, for a live preview pane while you edit a deck.

## Where decks live

Deck sources are Markdown files at `docs/slides/week_NN.md`, one per lecture, sharing a house theme
at `docs/slides/theme.css`. `mkdocs.yml` excludes the sources from the MkDocs build:

```yaml
exclude_docs: |
  slides/*.md
```

That means a deck's `.md` source is never turned into a course page — only the **exported** `.html`
and `.pdf` files that Marp writes into `docs/slides/` are served, as static files MkDocs copies
through unchanged. Committing the source alongside its export is deliberate: Read the Docs builds
the site with plain MkDocs and never runs Node, so the export has to already exist in the
repository.

## Figure paths match the reading

A deck reaches into the same `images/` folders the readings use, with the same relative path a
page under `docs/gen_reading/` would use — for example:

```
../gen_reading/images/w00_fig01_accuracy_precision.svg
```

There is no separate copy of a figure for slides. If a figure changes on the reading, rebuild the
deck and the slide picks up the same file.

## Deck front matter and slide syntax

Every deck starts with:

```yaml
---
marp: true
theme: cce
math: mathjax
paginate: true
---
```

- A line containing only `---` marks a slide break (after the front matter block, which is also
  delimited by `---`).
- `![w:900](path)` sizes an image to 900 px wide; adjust the number to fit the slide.
- `$$ ... $$` writes math the same way the readings do, rendered through MathJax.

## Building a deck

The easy way, which builds every deck in `docs/slides/` at once:

```
python fig_tools/build_slides.py
```

This produces HTML and PDF for each deck. Add `--pptx` to also export PowerPoint:

```
python fig_tools/build_slides.py --pptx
```

The equivalent raw Marp commands, useful if you are debugging one deck on its own:

```
marp docs/slides/week_05.md --theme-set docs/slides/theme.css --allow-local-files -o docs/slides/week_05.html
marp docs/slides/week_05.md --theme-set docs/slides/theme.css --allow-local-files --pdf -o docs/slides/week_05.pdf
marp docs/slides/week_05.md --theme-set docs/slides/theme.css --allow-local-files --pptx -o docs/slides/week_05.pptx
```

`--allow-local-files` is required whenever a deck references a local image, which is every deck
that uses a course figure.

!!! warning "PowerPoint export is a picture of the deck, not editable text"
    The default `--pptx` export renders each slide as an image inside the `.pptx` file. It presents
    perfectly well, but the text on each slide cannot be edited in PowerPoint afterward. An
    experimental `--pptx-editable` flag produces real editable text boxes, but it requires
    LibreOffice installed on the machine doing the export and is not the default for that reason.

## Process for one lecture

1. Edit `docs/slides/week_NN.md` with the Marp VS Code preview open, so you can see each slide as
   you write it.
2. Build the deck with `python fig_tools/build_slides.py`.
3. Link it from that week's page (`docs/weeks/week_NN.md`), under the Tuesday lecture entry:

   ```markdown
   [Slides](../slides/week_05.html) · [PDF](../slides/week_05.pdf)
   ```

4. Run `mkdocs build --strict` to confirm the week page's links resolve.
5. Commit the deck's Markdown source **and** its exported `.html`/`.pdf` together, in the same
   commit. Committing the export is what lets Read the Docs serve it without running Node.
6. Push.

## Design rule: a deck is not the reading

A lecture deck is a **subset** of the reading it accompanies, built for fifty minutes in a room, not
a second copy of the page for someone to read alone. One deck per lecture, roughly 15 to 25 slides
for a 50-minute session, built from the reading's own figures plus a few prompt slides to drive
discussion. Do not restate the reading's prose on slides — if a slide needs a paragraph of text to
make sense, that content belongs on the page, not in the deck.

Week 5's deck is the template to copy structurally when starting a new one.

## Where to go next

- [Editing the Site](editing.md) for how a week page links out to its reading, lab, and now its
  slides.
- [Making Figures](figures.md) for how the figures a deck reuses are built and named.
- [For Instructors and TAs](index.md) for how the repository as a whole is organized.
