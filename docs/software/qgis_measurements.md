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
5.  You should see your map appear. if asked about Coordinate Reference Systems (CRS), click "OK" to use the image's default system.

!!! info "CRS Crash Course"
    A **Coordinate Reference System (CRS)** is how the computer "flattens" the round Earth to fit on your screen. If your map looks "squashed" or "stretched," you might be using the wrong CRS. For most labs, we use **WGS 84 / UTM Zone 12N** (Utah's local coordinate system).

    **Before you measure anything, confirm the CRS is *projected*.** A projected CRS has real-world
    units — metres or feet. A geographic CRS such as plain WGS 84 has units of *degrees*, and a
    "distance" measured in degrees is meaningless on a construction site. Check the CRS shown in the
    bottom-right corner of the QGIS window: if it reads `EPSG:4326` you are in degrees, and every
    length and area you read off the screen will be wrong.

    This is the most common reason a student's parking-lot area comes out absurd.

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
    3. Did the number change? (Yes). Did the actual physical size of the parking stall change? (No).
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
    [Lab 2: Measurements and Methods](../labs/2_measurements_and_methods.md).

## 5. Estimating Cut and Fill from a DEM or DSM

Distance and area come off the orthomosaic. **Volume** needs elevation, which means a DEM or DSM
alongside the image.

The idea is a subtraction: two elevation surfaces of the same ground at different times, or one
surface against a design grade. Where the newer surface is higher, material was added — that is fill.
Where it is lower, material was removed — that is cut.

1.  Load both elevation rasters into the same project, in the same projected CRS.
2.  **Raster → Raster Calculator**, and build the expression `"after@1" - "before@1"`. The result is a
    difference surface: positive values are fill, negative values are cut.
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

You will use QGIS in [Lab 2: Measurements and Methods](../labs/2_measurements_and_methods.md), where
you compare a measurement taken from a drone orthomosaic against pacing and against Google Maps. It
is also one of the two processing and analysis tools available for the
[Final Project](../final_project/overview.md).
