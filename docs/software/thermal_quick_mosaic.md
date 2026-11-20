# Thermal Quick Mosaic

!!! abstract "Key Takeaways"
    - **The quick mosaic is the route for the Autel thermal drone this semester.** It turns the whole flight into a temperature map in °C in a few minutes, it works even when the photos barely overlap, and the instructor can make it for your group.
    - **It lays every photo flat on the ground.** Positions and sizes are good to a few metres on flat ground; a raised roof comes out too large unless you tell the tool how high it is.
    - **Temperatures are only as good as the camera's warm-up.** Power on 10 minutes before the first photo and run the shutter calibration by hand, or the photos carry an error of many degrees.
    - **iTwin needs a flight planned for the thermal camera.** A test flight connected only 13 of its 68 photos in iTwin, because it was planned for the visible camera; this page explains why and how to plan the next one.
    - **Check one number** against an infrared thermometer before you believe the map.

---

This page is for final-project groups who flew the **Autel EVO II Dual 640T** thermal drone. It makes a **thermal mosaic**: one map, in °C, of the whole area you flew, that opens in QGIS. It uses the class's own Python tool, **autel-thermal**, and its command `autel-ortho`.

There are two ways to make a thermal map from this drone:

| Route | How it works | Needs | Use it |
|---|---|---|---|
| **Quick mosaic** (this page) | Each photo is placed on the map from the drone's GPS position and camera angles, then the photos are stitched together | Nothing beyond a normal flight; overlap does not matter | **This semester, for every thermal group** |
| [Thermal Mosaic in iTwin](thermal_itwin.md) | Photogrammetry: iTwin matches the photos to each other, as in the Week 7 lab | A flight **planned for the thermal camera**, with about 80 % overlap, and a warmed-up camera | Only with a flight planned as in [Planning a thermal flight that works](#planning-a-thermal-flight-that-works) |

!!! tip "The instructor can make your mosaic"
    This semester the instructor is offering to make the quick mosaic for thermal groups. Reply in the class **Teams** thread with:

    - your **group number**;
    - **where your flight is** on the class SharePoint (the folder's location);
    - the **roof's height above the takeoff point**, if you flew a roof (see `--ground-below-takeoff` under [Options you may need](#options-you-may-need)).

    You get back `mosaic.tif` and the other files listed under [What it writes](#what-it-writes); carry on from [Step 2](#step-2-open-it-in-qgis). What You Need and Step 1 are for groups who want to run the tool themselves.

---

## What You Need

| # | What | Where it comes from | Time |
|---|---|---|---|
| 1 | Your whole flight folder | The drone's SD card | A few minutes to copy |
| 2 | Miniforge and a `thermal` environment | conda-forge's website | About 5 minutes |
| 3 | The autel-thermal tool | `autel-thermal.zip` on the class SharePoint | About 3 minutes |
| 4 | QGIS | Already on the lab computers | — |

Items 2 and 3 are the same as on the iTwin page: follow [2. Miniforge and a Python environment](thermal_itwin.md#2-miniforge-and-a-python-environment) and [3. The autel-thermal tool](thermal_itwin.md#3-the-autel-thermal-tool) there, then come back. You install them **once per computer and per user**; a lab computer you use on Tuesday and your laptop on Thursday each need their own install.

### Your flight folder

Copy the flight's whole folder off the SD card to the computer's own drive (not a network or OneDrive folder; it is faster and nothing gets lost while syncing), and keep it together:

- `IRX_nnnn.irg` and `IRX_nnnn.TIFF`: **the temperatures**. Without them there is no °C.
- `IRX_nnnn.jpg`: a coloured picture of each frame, and the GPS position and camera angles. It holds no temperatures.
- `MAX_nnnn.jpg`: the photos from the drone's **visible** (ordinary) camera, taken at the same moments.
- the `.mrk` file: the drone's GPS log.

Rename no files. You may rename the folder itself, and a short name with no spaces or commas, such as `C:\thermal\roof_flight`, makes the commands below easier to type.

If the folder has only `IRX_nnnn.jpg` files, the camera was not set to **JPG + TIFF**: the photos hold no temperatures, and no software can recover them. Talk to a TA.

---

## Step 1: Make the Mosaic

Skip this step if the instructor is making the mosaic for your group.

1. Open a command window: on Windows, **Miniforge Prompt** from the Start menu; on a Mac, Terminal.
2. Switch to the environment. The start of each line then reads `(thermal)`:

        conda activate thermal

3. Run the tool. The first path is your flight folder, the second a **new** folder for the results (never inside the flight folder):

        autel-ortho C:\thermal\roof_flight C:\thermal\roof_quick --mosaic

    On a Mac the paths look like `~/thermal/roof_flight`. If a path has spaces, put it in quotation marks. A flight of 100 photos takes about a minute.

4. **Read what it prints.** One line per photo, starting `[OK]`, `[SKIP]` or `[LOW]`, then a summary. Watch for photos it skipped:

    | Message | What it means | What to do |
    |---|---|---|
    | `[SKIP] IRX_nnnn: stale-NUC ramp (skipped)` | The camera had not finished warming up, so that photo's temperatures are wrong: a smooth error runs from its top to its bottom | If only the first few photos say it, carry on. If most of the flight says it, the temperatures cannot be trusted: see [The camera was not warmed up](#1-the-camera-was-not-warmed-up) |
    | `[LOW]  IRX_nnnn: below minimum height ...` | Taken on or near the ground at takeoff or landing | Nothing; these are converted to °C but not placed |

    Photos taken at an angle are placed too, but the part of each that looks toward the horizon is left out.

### Options you may need

Add these to the end of the `autel-ortho` line.

| Option | What it does | When to use it |
|---|---|---|
| `--ground-below-takeoff -6` | Places the photos on a surface **6 m above** the takeoff point instead of at the takeoff height. The number is the height *below* takeoff, so a roof above takeoff is a negative number | **Roofs.** Use the roof's height above where you took off (from the building plans, or the drone's height display while hovering at the roof edge). Without it, a 6 m roof flown at 40 m comes out about 40 % too large in area |
| `--dem` | Places each photo on the real ground height under it, from the USGS 3DEP elevation model (needs the internet; US only) | Sloping ground, such as a hillside or a canyon |
| `--mosaic-gsd 0.10` | Makes the mosaic with 10 cm pixels instead of the photos' own (about 3 to 6 cm) | Big flights, or if the tool says the mosaic would need too much memory |
| `--shift 1.5 -0.8` | Moves the whole result 1.5 m east and 0.8 m south | After you have measured an offset against a better map (see [Can the visible photos help?](#can-the-visible-photos-help)) |
| `--keep-suspect` | Also places the photos flagged `stale-NUC ramp` | Only to *see* the area. Their temperatures are wrong: never measure them |

`--dem` and `--ground-below-takeoff` cannot be used together.

### What it writes

| File | What it is |
|---|---|
| `mosaic.tif` | **The temperature map.** Every pixel is °C (a decimal number). Empty areas have no value. Coordinates are UTM zone 12N (EPSG:32612), in metres |
| `IRX_nnnn_ortho.tif` | Each photo on its own, placed on the map, also in °C |
| `mosaic_frame.tif` | Which photo each pixel of the mosaic came from. Where photos overlap, the one looking most nearly straight down at that spot is used |
| `footprints.geojson` | The outline of every photo on the ground |
| `frames.geojson` | The camera positions |
| `ortho_report.csv` | One row per photo: position, height, camera angle, temperature summary, and why it was skipped, if it was |

---

## Step 2: Open It in QGIS

1. Start QGIS and set the project to `EPSG:32612` (bottom-right corner), as in [Using QGIS](qgis_measurements.md).
2. Drag `mosaic.tif` from the results folder onto the map. Optionally add a basemap first (see the QGIS page) to see where you are.
3. **Colour it by temperature:** right-click the layer → **Properties → Symbology**. Render type **Singleband pseudocolor**, colour ramp **Inferno** or **Turbo**, and set **Min** and **Max** to the range you care about (for a roof in the morning, something like 0 and 20). Click **OK**.
4. **Read a temperature:** choose the **Identify Features** tool (the arrow with an *i*) and click the map. The value shown is °C.
5. Add `footprints.geojson` to see where each photo landed; set its fill to **No brush** so the mosaic shows through.

### Measure the area of a warm patch

1. **Raster → Raster Calculator.** Enter, with your own threshold in °C:

        "mosaic@1" > 12

    and save the result as `warm.tif`. Pixels warmer than 12 °C become 1, the rest 0.
2. **Raster → Conversion → Polygonize (Raster to Vector)**, input `warm.tif`. This makes a polygon layer.
3. Open the new layer's **attribute table**, select the polygons whose value (the `DN` field) is 1, and use the **Field Calculator** to add a field `area_m2` with the expression `$area`. Each polygon's area is now in square metres.

Choose the threshold from the map itself: look at the temperatures of the surrounding roof first, and say in your memo which threshold you used and why.

### Reading a relative map

If your camera was not warmed up, the instructor may also send you a **relative map**, `mosaic_relative.tif`, with a Word document that explains it. It is made from the same photos with one extra step: in each photo, the smooth change from the top edge to the bottom edge (the warm-up error described in [The camera was not warmed up](#1-the-camera-was-not-warmed-up)) was estimated from the middle value of every row of pixels and subtracted. What is left shows each spot **compared with its surroundings in the same photo**. It is not an option of the tool; only the instructor makes it.

- **Its values are differences in °C, not temperatures.** **+3** means that spot is about 3 °C warmer than what is typical around it in its photo; **−2** means about 2 °C colder; **0** means the same as its surroundings.
- **Colour it** with a ramp that has a neutral middle: Singleband pseudocolor, colour ramp **RdBu** with **Invert Color Ramp** chosen from the same menu (red warm, blue cold), Min **−5** and Max **5**.
- **Measure warm patches** as above, with a difference as the threshold: `"mosaic_relative@1" > 2`.

Know its limits before you use it:

- **It is a patchwork.** Each photo has its own zero, so values can jump where two photos meet. Compare spots that are close together, not opposite ends of the site.
- **Real smooth changes are removed too.** If one end of a roof really is warmer than the other, gradually, the relative map hides it. Only local warm and cold features survive: a vent, a roof unit, a wet patch.
- **It is not a temperature.** Do not compare it with an infrared thermometer or report its values as temperatures. In your memo, write "about 3 °C warmer than the roof around it", not "3 °C".

---

## Step 3: Check One Number, and Know the Limits

- **Check one number.** Read a surface you can reach (a roof edge, a wall, a pavement patch) with an infrared thermometer as close in time to the flight as you can, and compare it with `mosaic.tif` at the same spot. Report both numbers in your memo, as the [Measurement Fundamentals](../gen_reading/measurement_fundamentals.md) reading asks.
- **Flat-ground placement.** Every photo is laid on one flat surface. Roof edges and walls shift between neighbouring photos, so seams run through them, and anything at a different height from that surface is placed a little off. Expect positions good to a few metres, not centimetres.
- **Shiny surfaces lie.** Metal flashing, glass and wet surfaces reflect the cold sky and read far too cold. Do not report their temperatures.
- **The camera's own accuracy** is about ±3 °C. Differences between two spots in the same flight are more reliable than any single absolute number.

---

## Why the Test Flight Did Not Work in iTwin

The [iTwin route](thermal_itwin.md) was tested on 2026-11-19 with iTwin Capture Modeler 2024.1.7, on a final-project flight (task folder `100FTASK`: 68 thermal photos, 31 m above takeoff). iTwin loaded every photo and read its GPS position, the camera's size and the camera angles, but it could connect only **13 of the 68 photos**. The reasons are worth knowing before you plan your own flight.

### 1. The camera was not warmed up

On this flight the first photo was taken **75 seconds** after the drone was switched on, and the last about four minutes after. The thermal camera recalibrates itself (its non-uniformity correction, NUC) during its first minutes; until then each photo carries a smooth error from top to bottom, here 20 to 58 °C between the top and the bottom of one photo. The tool flagged 55 of the 68 photos, and photos that passed its check can carry the same error, hidden under a warm roof. **No software can recover the true temperatures afterwards.** (A [relative map](#reading-a-relative-map) removes the smooth error, but the true temperatures go with it.) The fix is a habit: switch on 10 minutes before the first photo and run the shutter calibration (FFC) by hand in the app just before takeoff.

### 2. The flight was planned for the wrong camera

The drone has two cameras that take photos at the same moment, and they see very different amounts of ground. The flight was planned with the mapping app using the **visible** camera, so the overlap was right for the visible photos and far too small for the thermal ones:

| At 31 m above takeoff | Thermal camera (640 × 512 pixels, 13 mm lens) | Visible camera (4096 × 3072 pixels, 6.67 mm lens) |
|---|---|---|
| Ground seen by one photo (across × along the flight line) | 18 × 15 m | 46 × 35 m |
| Distance between photos | 6.3 m | 6.3 m |
| **Forward overlap** (one photo with the next) | **about 57 %** | about 82 % |
| Distance between flight lines | 13 to 15 m | 13 to 15 m |
| **Side overlap** (one line with the next) | **about 23 %** | about 70 % |

Photogrammetry needs every spot on the ground in **at least three photos**, and thermal photos have little texture to match, so thermal flights need about **80 % forward and side overlap**, planned with the thermal camera's footprint. With 23 % side overlap, neighbouring flight lines shared almost nothing, and iTwin could tie only 13 of the 68 thermal photos together.

### 3. iTwin's own temperature tools do not read this camera

iTwin offers a **Temperature Map** and a **Thermal** colour source, but, according to Bentley, only for radiometric JPEGs from the cameras it supports (FLIR, some DJI models, Skydio). The Autel's JPEG holds no temperatures, so those options are greyed out. That is why the iTwin route turns the temperatures into grey levels and back again in QGIS.

### What the test showed that does work

- iTwin reads the tool's TIFFs (from the `autel-thermal.zip` of 2026-11-19 or later), their GPS positions, the camera size and the camera angles, with no typing.
- The 13 photos that did connect fit each other to under half a pixel.
- The orthophoto came out in UTM, within a few metres of the quick mosaic, with grey levels on the tool's temperature scale, **as long as Color correction mode is None**: with colour correction on, the whole map shifted by about 10 °C. Because of the warm-up error, this flight could not show how closely iTwin's temperatures match the quick mosaic's.

---

## Planning a Thermal Flight That Works

Do this if you want the iTwin route, or simply a better quick mosaic.

1. **Warm up:** switch the drone on 10 minutes before the first photo; run the FFC (shutter calibration) by hand just before takeoff.
2. **Photo format:** JPG + TIFF.
3. **Plan with the thermal camera.** If the mapping app lets you choose which camera the plan is for, choose the **thermal (640T)** camera. If it does not, plan by hand from this table, which assumes 80 % forward and 80 % side overlap: <!-- verify in Autel Explorer whether the mission planner offers a thermal camera choice -->

    | Height above takeoff | Thermal photo covers | Pixel on the ground | Photos at most this far apart | Flight lines at most this far apart | Top speed with a photo every 2 s |
    |---|---|---|---|---|---|
    | 30 m (100 ft) | 18 × 14 m | 2.8 cm | 2.8 m | 3.5 m | 1.4 m/s |
    | 40 m (130 ft) | 24 × 19 m | 3.7 cm | 3.8 m | 4.7 m | 1.9 m/s |
    | 60 m (200 ft) | 35 × 28 m | 5.5 cm | 5.7 m | 7.1 m | 2.8 m/s |
    | 80 m (260 ft) | 47 × 38 m | 7.4 cm | 7.6 m | 9.5 m | 3.8 m/s |

    The camera needs about 2 seconds between photos, which sets the top speed. Flying **higher** covers more ground per photo, so you need fewer lines and can fly faster, at the cost of coarser pixels. For a building roof, 40 to 60 m is a good compromise. Compare the test flight: at 31 m its lines were 13 to 15 m apart, where this table allows about 3.7 m.

4. **Fly the grid past the edges** of what you care about by at least half a photo width, as for any mapping flight (see [Planning the Flight](../gen_reading/mission_planning_sfm.md)).
5. **Check the time budget.** Covering 100 m × 100 m at 60 m takes about 15 flight lines, roughly 9 minutes of flying at 2.8 m/s, plus turns.

---

## Can the Visible Photos Help?

Yes, in two ways today, and possibly a third later.

1. **A sharp base map.** The visible `MAX_nnnn.jpg` photos usually *do* have enough overlap, because the flight was planned for them. Process them in iTwin exactly as in the [Week 8 lab — Data Processing](../labs/5_data_processing.md) (and the [Bentley iTwin](bentley_itwin.md) page) to get a normal colour orthophoto and a DSM (Digital Surface Model). Add the colour orthophoto under your thermal `mosaic.tif` in QGIS: the roof edges and vents in the colour map show where the warm patches really are. Use only the `MAX_` files for this, not the `IRX_` files.
2. **Lining the two maps up.** If the thermal mosaic sits a metre or two off the colour orthophoto, measure the offset on a clear corner (photogrammetry usually places the colour map better) and run `autel-ortho` again with `--shift E N` (metres east and north) to move the whole thermal mosaic onto it. The roof's height above takeoff for `--ground-below-takeoff` can also be read off the DSM: the roof's height minus the ground's height where you took off.
3. **Later: thermal on the photogrammetry model.** Because both cameras fire at the same moment, the positions iTwin computes for the visible photos could help place the thermal photos. Bentley describes a way to tie thermal photos to a visible model, and the autel-thermal tool may support it later; neither has been tried with this drone, so it is **not ready** for this semester.

---

## When Something Goes Wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `autel-ortho` is "not recognized" or "command not found" | The `thermal` environment is not active, or the tool is not installed in it | Run `conda activate thermal`; if it still fails, install the tool as in [3. The autel-thermal tool](thermal_itwin.md#3-the-autel-thermal-tool) |
| The install asks you to **sign in to GitHub** | The repository is still private | Use the SharePoint zip |
| Nothing is placed, or the tool finds no photos | Wrong folder, or a JPG-only flight | Point the command at the folder that holds the `IRX_` files (it may be a `Thermal` subfolder) |
| Most photos say `stale-NUC ramp` | The camera was not warmed up | The temperatures are not usable; ask the instructor about a [relative map](#reading-a-relative-map), and plan a new flight with the warm-up |
| `mosaic.tif` is missing | `--mosaic` was left off, or the mosaic would need too much memory | Add `--mosaic`; add `--mosaic-gsd 0.10` for big flights |
| The mosaic is in the wrong place by tens of metres | The `.mrk` file is from another flight | Keep only the flight's own `.mrk` in the folder |
| A roof looks too big, or its edges double | Flat-ground placement at the takeoff height | Add `--ground-below-takeoff` with the roof's height (negative number) |
| QGIS shows the mosaic in grey with no temperatures | Default style | Set **Singleband pseudocolor** (Step 2); the values are already °C |

---

## Resources

- **autel-thermal**: the class's Python tool, from `autel-thermal.zip` on the class SharePoint. Its repository is private for now. Inside the zip, `examples/README.md` has the tool's own install notes, and the `examples` notebooks 01 to 04 go further: one photo in °C, a whole flight as a table, placing photos, and hot spots with their area.
- [Thermal Mosaic in iTwin](thermal_itwin.md): the photogrammetry route, for a flight planned as above.
- [Thermal Imaging](../gen_reading/thermal.md): what a thermal camera measures, and when to fly.
- [Using QGIS](qgis_measurements.md): opening maps, measuring, and the Raster Calculator.

---

## Where this is used

- [Flight and Data Processing](../final_project/flight_and_data_processing.md): Part 2, for groups that flew the thermal drone.
- [Example Projects — Roof heat loss at 8 a.m.](../final_project/project_ideas.md#roof-heat-loss-at-8-am)
