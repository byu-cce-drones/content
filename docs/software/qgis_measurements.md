# Using QGIS for Drone Measurement Analysis

!!! abstract "Key Takeaways"
    - **GIS is more than a map**: It is a database for spatial data that lets you take real-world measurements off an aerial image.
    - **LTR is for Stability**: Always choose the **Long Term Release (LTR)** version of QGIS for the most stable experience.
    - **Check your CRS first**: If the layer is in degrees rather than metres or feet, every distance and area you measure will be wrong. This is the single most common mistake.
    - **Measure Twice, Fly Once**: Accuracy in QGIS depends on the resolution of your drone image. The higher the flight, the larger the error margin.

---

**QGIS** is a free and open-source Geographic Information System (GIS). We use it to load the maps
(orthomosaics) we created and take measurements off them.

Because an orthomosaic is georeferenced, every pixel corresponds to a real-world coordinate. That is
what turns an aerial photograph into a measurement: distances for pipeline runs or drainage paths,
areas for earthwork pads, stockpiles, or impervious surfaces. Paired with a DEM or DSM, the same
image can give you a cut/fill volume estimate for a grading check or an as-built comparison.

## 1. Installing QGIS
1.  Go to the [QGIS Download Page](https://qgis.org/en/site/forusers/download.html).
2.  Download the **Long Term Release (LTR)** version (most stable).
3.  Install it on your computer.

!!! tip "Installer notes"
    The download page will ask you to donate. It is not required.

    - **Windows:** open the `.msi` file and follow the setup wizard — accept the licence, keep the default install options, click Install.
    - **Mac:** open the `.dmg` file and drag the QGIS icon into your Applications folder. If the first launch is blocked by security settings, control-click the QGIS icon, choose **Open**, then confirm in the dialog.

## 2. Loading Your Orthomosaic
1.  Open QGIS Desktop.
2.  Start a **New Empty Project**.
3.  Locate your orthomosaic file (usually a `.tif` file created in Bentley iTwin or other software).
4.  Drag and drop the `.tif` file into the main QGIS window.
5.  You should see your map appear. If asked about Coordinate Reference Systems (CRS), click **OK** to use the image's default system, then follow **Setting the CRS** below to confirm it is one you can measure in.

!!! info "CRS Crash Course"
    A **Coordinate Reference System (CRS)** is how the computer "flattens" the round Earth to fit on your screen. If your map looks "squashed" or "stretched," you might be using the wrong CRS. For most labs, we use **WGS 84 / UTM Zone 12N** (Utah's local coordinate system).

    **Before you measure anything, confirm the CRS is *projected*.** A projected CRS has real-world
    units — metres or feet. A geographic CRS such as plain WGS 84 has units of *degrees*, and a
    "distance" measured in degrees is meaningless on a construction site. Check the CRS shown in the
    bottom-right corner of the QGIS window: if it reads `EPSG:4326` you are in degrees, and every
    length and area you read off the screen will be wrong.

    This is the most common reason a student's parking-lot area comes out absurd.

### Setting the CRS

Use **WGS 84 / UTM Zone 12N** (EPSG:32612) for everything in this course. It is a projected CRS with
units of metres, and it covers all of Utah.

QGIS has two CRS settings, and they are not the same thing:

- **Project CRS** — how the map is displayed and measured on screen. This is the one that controls
  the Measure tool.
- **Layer CRS** — what the file itself was saved in. QGIS reprojects layers on the fly to match the
  project, so you can leave the orthomosaic as it is.

**Change the project CRS:**

1.  Click the CRS code in the **bottom-right corner** of the QGIS window (it will say something like
    `EPSG:4326`). Or go to **Project → Properties → CRS**.
2.  In the **Filter** box, type `32612`.
3.  Select **WGS 84 / UTM zone 12N** from the list.
4.  Click **OK**. The bottom-right corner should now read `EPSG:32612`.

**Set the measurement units** (so the numbers come out in the units the lab worksheet asks for):

1.  **Project → Properties → General**.
2.  Under **Measurements**, set **Distance units** to *feet* and **Area units** to *square feet*.
    Use metres and square metres instead if that is what you are recording.
3.  Click **OK**.

**When you create a new vector layer** (section 4), set its CRS to `EPSG:32612` in the New Shapefile
Layer dialog so the saved shapes and the `$area` calculation are in metres, not degrees.

!!! warning "Check, do not assume"
    Changing the project CRS fixes the Measure tool. It does **not** change what is stored in a layer
    that was already saved in degrees. If a `$area` value looks absurdly small (a parking lot of
    `0.00002`), the layer is in EPSG:4326 — create a new layer in 32612 and redraw, or right-click
    the layer → **Export → Save Features As** and choose 32612.

## 3. Performing Measurements

There are two ways to get a number out of QGIS, and they are for different jobs:

| Method | Use it when | Section |
|---|---|---|
| **Measure tool** | You want a quick answer on screen and do not need to keep it | 3 |
| **Digitize to a vector layer** | You need a result you can save, re-open, check, or hand in | 4 |

Both should give you the same number on the same feature. If they do not, something is wrong — start
with the CRS.

### Measure Line (Distance)
1.  Look for the icon that looks like a ruler 📏 in the top toolbar (or press `Ctrl+Shift+M`).
2.  A window called "Measure" will pop up.
3.  Click on your map to start a line.
4.  Click again to add a segment.
5.  **Right-click** to finish the measurement.
6.  Read the "Total" length in the window (ensure units are set to meters or feet as needed).

### Measure Area
1.  In the "Measure" window, click the drop-down arrow next to the title (or the specific Area icon in the toolbar).
2.  Select **Measure Area**.
3.  Click around the perimeter of the object you want to measure (e.g., a building roof or a parking lot).
4.  **Right-click** to close the polygon.
5.  Read the area in square meters or square feet.

!!! question "Activity: The Ruler Challenge"
    1. Measure the length of a parking stall in **Meters**.
    2. Change the units to **Feet** and measure the same stall again.
    3. Did the number change? Did the actual physical size of the parking stall change?

??? note "Answer"
    The number changed (Yes) — meters and feet are different units. The actual physical size of the
    parking stall did not change (No).

*Always check your units before recording data on your lab worksheet!*

## 4. Digitizing Features to a Vector Layer

The Measure tool gives you a number and then forgets it. When the measurement is something you have
to defend — a lab result, a quantity in a report — draw the feature instead, so it is saved with the
project and can be checked later.

1.  **Layer → Create Layer → New Shapefile Layer**. Set the geometry type to **Polygon** (or
    **LineString** for a distance), and set the CRS to match your orthomosaic.
2.  Select the new layer, then click **Toggle Editing** (the pencil icon).
3.  Click **Add Polygon Feature** and trace the feature on the orthomosaic. **Right-click** to close
    the shape.
4.  Click **Toggle Editing** again and save.
5.  Open the layer's **Attribute Table**, then open the **Field Calculator** (the abacus icon).
6.  Create a new field — call it `area_ft2` — and set the expression to `$area`. QGIS fills in the
    area of every feature in the layer's units.

!!! tip "Why bother"
    A digitized feature is a record. You can re-open it next week, correct one edge without redrawing
    everything, measure fifty stockpiles in one pass instead of one at a time, and export the result
    to a report or to CAD. This is the workflow you will use in
    [Week 5 lab — Measurements and Methods](../labs/2_measurements_and_methods.md).

## 5. Estimating Cut and Fill from a DEM or DSM

Distance and area come off the orthomosaic. **Volume** needs elevation, which means a DEM or DSM
alongside the image.

The idea is a subtraction: two elevation surfaces of the same ground at different times, or one
surface against a design grade. Where the newer surface is higher, material was added — that is fill.
Where it is lower, material was removed — that is cut.

1.  Load both elevation rasters into the same project, in the same projected CRS.
2.  **Raster → Raster Calculator**. In the **Raster Bands** list at the top left, double-click the
    newer surface, type ` - `, then double-click the older surface. The expression will look like
    `"after@1" - "before@1"`. The result is a difference surface: positive values are fill,
    negative values are cut.

    !!! note "Your layer names will be different"
        `after` and `before` are just the names of the two layers as they appear in the Layers panel
        — QGIS takes the name from the file name unless you rename the layer. `@1` means band 1 of
        that layer. If your files are `rock_canyon_march.tif` and `rock_canyon_june.tif`, the
        expression is `"rock_canyon_june@1" - "rock_canyon_march@1"`. Double-clicking in the Raster
        Bands list inserts the exact name, so use that rather than typing it.
3.  To get a volume over a specific area, clip the difference raster to the polygon you digitized in
    section 4, then use **Raster → Analysis → Zonal Statistics** to get the mean difference and the
    cell count.
4.  Volume is the mean difference multiplied by the area — check your units before you report it.

!!! warning "Know what your surface includes"
    A **DSM** includes whatever is standing on the ground: vegetation, vehicles, equipment, stockpile
    tarps. A **DTM** is the bare earth with that removed. Differencing two DSMs over a site where a
    truck moved between flights will report the truck as a cut. For earthwork quantities you want
    DTMs, and you want to know how the bare-earth surface was produced.

    Treat any volume from this workflow as an estimate. Say so when you report it, and say what you
    checked it against.

---

## Where this is used

You will use QGIS in [Week 5 lab — Measurements and Methods](../labs/2_measurements_and_methods.md), where
you compare a measurement taken from a drone orthomosaic against pacing and against Google Maps. It
is also one of the two processing and analysis tools available for the
[Final Project](../final_project/overview.md).
