---
marp: true
theme: cce
math: mathjax
paginate: true
---

<!-- _class: title -->

# Using QGIS

## Week 4 — Tuesday Lecture

---

## Today

- What a GIS is, and why an orthomosaic is a measuring instrument
- Installing QGIS — before Thursday
- Loading an orthomosaic and checking the coordinate reference system
- Two ways to measure: the quick one, and the one you can hand in

---

<!-- _class: prompt -->

# A picture, or a measurement?

An aerial photo shows you a parking lot. An orthomosaic in a GIS tells you it is **27,856 ft²**.

What has to be true of the image for that number to mean anything?

---

## GIS is a database with a map on the front

- Every pixel of an **orthomosaic** has a real-world coordinate
- So a click on the screen is a **position**, two clicks are a **distance**, and a closed shape is an **area**
- **QGIS** is the free, open-source GIS we use to take those measurements

The number is only as good as the image under it and the coordinate system it is drawn in.

---

## Install QGIS

![w:880](../software/images/qgis_01_download_ltr.jpg)

<p class="caption">qgis.org → Download → <strong>Long Term Release (LTR)</strong>. Windows: run the .msi and keep the defaults.</p>

---

## It will ask for a donation first

![w:820](../software/images/qgis_02_download_donate.jpg)

<p class="caption">Not required. Click <strong>Skip it and go to download</strong>.</p>

---

## Load the orthomosaic

![w:900](../software/images/qgis_03_window.jpg)

<p class="caption">New empty project, then drag the .tif onto the map. Layers panel on the left; the CRS in the bottom-right corner.</p>

---

## Zoom in

![w:900](../software/images/qgis_04_zoom_stall.jpg)

<p class="caption">One-centimetre pixels. You can see the stripe, the curb, and the bumper — and that matters for where you click.</p>

---

## Same lot, two images

<div style="display:flex; gap:18px; align-items:flex-start;">
<div style="flex:1;">

![w:530](../software/images/qgis_05_google_maps_lot.jpg)

<p class="caption">Google Maps satellite imagery (© Google)</p>
</div>
<div style="flex:1;">

![w:530](../software/images/qgis_06_ortho_lot.jpg)

<p class="caption">Drone orthomosaic, January 2026, 1 cm pixels</p>
</div>
</div>

---

<!-- _class: prompt -->

# Where does the pavement end?

Zoom in on both. Which one lets you put the cursor on the curb with confidence — and how much area is one metre of doubt around the whole lot?

---

## The coordinate reference system

- A **CRS** is how the round Earth is flattened onto your screen
- **Geographic** CRS (plain WGS 84, `EPSG:4326`): units are **degrees**
- **Projected** CRS (WGS 84 / UTM zone 12N, `EPSG:32612`): units are **metres**

Measure in degrees and every number you write down is meaningless. Check the corner **before** you measure.

---

## The corner tells you

![w:780](../software/images/qgis_07_statusbar_4326.png)

![w:780](../software/images/qgis_08_statusbar_32612.png)

<p class="caption">Same project, two settings. Top: degrees — do not measure. Bottom: metres — go ahead.</p>

---

## Set the project CRS

![h:500](../software/images/qgis_09_crs_dialog.png)

<p class="caption">Click the corner (or Project → Properties → CRS), type <strong>32612</strong>, pick WGS 84 / UTM zone 12N.</p>

---

## Set the units you will report in

![w:860](../software/images/qgis_10_project_units.png)

<p class="caption">Project → Properties → General → Measurements: <strong>feet</strong> and <strong>square feet</strong> for the lab worksheet.</p>

---

<!-- _class: prompt -->

# A parking lot of 0.00002

That is what a student's area comes out as, every semester. What happened, and what is the unit?

---

## Measure a distance

![w:900](../software/images/qgis_11_measure_line.jpg)

<p class="caption">Ruler icon or Ctrl+Shift+M. Click, click, <strong>right-click</strong> to finish. One stall: 19.4 ft.</p>

---

## Measure an area

![w:900](../software/images/qgis_12_measure_area.jpg)

<p class="caption">Measure Area from the ruler's drop-down. Click each corner, right-click to close. One stall: 167.5 ft².</p>

---

<!-- _class: prompt -->

# The ruler challenge

Measure the stall in **metres**. Switch the units to **feet** and measure it again.

Did the number change? Did the stall?

---

## The Measure tool forgets

The number is on screen, and then it is gone.

For anything you have to **defend** — a lab result, a quantity in a report — draw the shape instead:

1. Create a polygon layer
2. Trace the feature
3. Let the Field Calculator compute the area

The shape is saved with the project. Reopen it, fix one edge, hand it in.

---

## Create a polygon layer

![w:860](../software/images/qgis_13_new_layer.png)

<p class="caption">Layer → Create Layer → New Shapefile Layer. Geometry <strong>Polygon</strong>, CRS <strong>EPSG:32612</strong>, a file name you can find again.</p>

---

## Trace the feature

![w:900](../software/images/qgis_14_trace_lot.jpg)

<p class="caption">Toggle Editing (pencil), Add Polygon Feature, click along the asphalt edge, right-click to close. Asphalt only — no sidewalk, no grass.</p>

---

## Save it

![w:900](../software/images/qgis_15_lot_done.jpg)

<p class="caption">Toggle Editing off and save. Two shapes on record: the stall and the lot.</p>

---

## Compute the area

![h:470](../software/images/qgis_16_field_calc.png)

<p class="caption">Open the Attribute Table, then the Field Calculator (abacus). New field <strong>area_ft2</strong>, decimal, expression <strong>$area</strong>.</p>

---

## Read it off

![w:700](../software/images/qgis_17_attribute_table.png)

<p class="caption">Stall 167.1 ft², lot 27,856 ft². These are the numbers that go on the worksheet.</p>

---

## Two methods, one feature

| Method | Stall area |
|---|---|
| Measure tool | 167.5 ft² |
| Digitized polygon + `$area` | 167.1 ft² |

They agree to a quarter of a percent. If yours differ by a factor of thousands, **check the CRS first** — nothing else produces a mistake that large.

---

## Thursday

- **Install QGIS before lab** — the download is large and the lab Wi-Fi is not
- Bring a laptop; the orthomosaic download is on the lab page
- You will pace the lot, measure it in Google Maps, then measure it in QGIS — and compare all three

[Measurements and Methods](../labs/2_measurements_and_methods.md) · [Using QGIS](../software/qgis_measurements.md)
