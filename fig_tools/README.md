# Figure tools

Python scripts that generate SVG figures for the course pages. This folder holds the **tools**, not
the pictures. Generated SVGs live with the page that uses them, in the owning section's `images/` folder (for example `docs/gen_reading/images/`), and are
committed there, so Read the Docs never runs these scripts.

Re-run a script when a figure needs to change, then commit both the script and the regenerated SVG.

Nothing in this folder may move under `docs/`. MkDocs copies every file in `docs/` to the published
site, including scripts.

## Layout

| File | Purpose |
|------|---------|
| `svgkit.py` | Tiny SVG builder, shared palette and type sizes, arrows, callout helper, optional PNG render through Inkscape |
| `parts.py` | Reusable drawings: controller, quadcopter (top view), mini aircraft icons, control sticks, rotation arrows |
| `fig_aircraft.py` | Figure 1, parts of a quadcopter, labeled and numbered |
| `fig_controller.py` | Figure 7, the controller, labeled and numbered |
| `fig_sticks.py` | Figures 8 and 9, stick controls and nose-in reversal |
| `fig_flight.py` | Figures 4, 5 and 6, rotation axes, lift against weight, differential thrust |
| `fig_payloads.py` | Figure 3, the sensors a drone can carry |
| `fig_sequence.py` | Figures 10 and 11, the flight sequence and the box practice pattern |
| `fig_automation.py` | Figures 12 to 15, position hold, sensor coverage, battery states, Return to Home |
| `fig_rules.py` | Flight Basics Figure 16 (Week 2) and Part 107 Figure 12 (Week 3), from one drawing |

Each `fig_*.py` writes to `review/` by default and to a docs images folder with `--out`.

Anything drawn more than once belongs in `parts.py`, so the same aircraft and the same controller
appear in every figure. Change a part there and every figure that uses it updates on the next run.

## File names

Figures are named `wNN_figMM_short_name.svg`, week first, then the figure number in page order.
Scripts never spell the name out; they call `svgkit.figure_name(week, number, slug)`, so the
number in the file name always matches the number printed inside the drawing.

A figure used in more than one week is generated once per week, with `--number` setting the number
in its title. `fig_rules.py` works this way: Flight Basics (Week 2) gets the full drawing, Part 107 (Week 3) gets `--no-scene`
because it already covers line of sight and altitude in its own figures.

```
python fig_tools/fig_rules.py --out docs/gen_reading/images
python fig_tools/fig_rules.py --no-scene --week 5 --number 12     --slug prohibitions --out docs/part_107_license/images
```

No third-party packages are required. Any Python 3.8 or newer works.

## Running

```
python fig_tools/fig_controller.py --png
python fig_tools/fig_controller.py --out docs/gen_reading/images
```

`--png` renders a PNG next to each SVG using Inkscape if it is installed, which is the quickest
way to check a figure. The PNG is for checking only; the site uses the SVG.

If a script reports that Inkscape was not found, point it at the executable:

```
set INKSCAPE=C:\Program Files\Inkscape\bin\inkscape.com
```

## Conventions

- Draw in a fixed `viewBox` between 700 and 900 units wide. Height as needed.
- Title at the top inside the figure, subtitle when a caveat belongs with the picture.
- Labels are real text, never paths, so they stay searchable and editable.
- Colors and fonts come from `svgkit.PALETTE` and `svgkit.FONT`. Do not hard-code new colors.
- Generic drawings. Brand names appear only in captions or tables, never in the figure.
- Figures that need a numbered variant for homework build both from one script.
