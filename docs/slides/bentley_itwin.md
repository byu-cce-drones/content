---
marp: true
theme: cce
math: mathjax
paginate: true

---

<!-- _class: title -->

# Bentley iTwin Capture Modeler

## Processing Lab — step by step

---

## Today

- Photos in, orthophoto and 3D model out
- Steps: project, import, aerotriangulation, reconstruction, production
- Then open the orthophoto in QGIS
- What to check along the way
- What to turn in

---

![w:900](../gen_reading/images/w04_fig01_pipeline_overview.svg)

<p class="caption">Six stages, four buttons. Import, Aerotriangulation, Reconstruction and Production map onto the pipeline you saw Tuesday.</p>

---

## Step 1 — Create a Project

- Open **iTwin Capture Modeler**
- Create a **new project**; name it and choose the project folder
- **New Capture**, then **New Block**: the set of photos
- Engine must be running, or jobs stay **pending**

---

![w:1000](../software/images/itwin_01_project_tree.jpg)

<p class="caption">One project: a block of photos, its aerotriangulated copy, a reconstruction and a production. iTwin Capture Modeler, Bentley Systems.</p>

---

## Step 2 — Import Photos

- Open the block's **Photos** tab
- Add all the photos of a directory
- GPS positions are read from the photo metadata
- Check the block **3D view**: do the cameras match your flight?

---

![w:1000](../software/images/itwin_02_block_photos.jpg)

<p class="caption">The block's Photos tab, with the buttons for adding photos. iTwin Capture Modeler, Bentley Systems.</p>

---

## The Bad Photo Hunt

Before the next step, scan your photos. **Delete** any that are:

- Blurry
- Pointed at the ground during takeoff
- Far from the study area

Garbage in, garbage out.

---

## Step 3 — Aerotriangulation

- Click **Submit Aerotriangulation**, then choose the **Engine**
- Keep the **default settings** (Adjust, Normal, Default)
- Click **Submit**, then wait
- Result: a new block with a **sparse point cloud**

---

![w:1000](../software/images/itwin_11_at_wizard.jpg)

<p class="caption">The Aerotriangulation Definition wizard. iTwin Capture Modeler, Bentley Systems.</p>

---

## Reading the AT result

- **Photos calibrated:** all, or nearly all
- **View quality report:** reprojection error under 1 px is good
- Sparse cloud, **3D view**: most points on brick and grass
- **Holes:** shiny surfaces, windows, fresh asphalt

---

![w:1000](../software/images/itwin_04_at_dashboard.jpg)

<p class="caption">The output block's dashboard: how many photos were calibrated. iTwin Capture Modeler, Bentley Systems.</p>

---

![w:1000](../software/images/itwin_05_at_sparse.jpg)

<p class="caption">The sparse cloud and the camera positions in the output block's 3D View. iTwin Capture Modeler, Bentley Systems.</p>

---

## Step 5 — Reconstruction

- (Step 4, ground control, is skipped in this lab)
- **New Reconstruction**: **Orthophoto/DSM** for the map, **3D reconstruction** for mesh and points
- **Spatial Framework:** set `EPSG:32612`, check the region of interest
- **Geometric precision:** Medium for the map

---

![w:1000](../software/images/itwin_07_reconstruction_spatial.jpg)

<p class="caption">The Spatial Framework tab: reference system, resolution and region of interest. iTwin Capture Modeler, Bentley Systems.</p>

---

## Step 6 — Production

Click **Submit Production**, pick the purpose:

- **Export Orthomosaic/DSM** — **TIFF/GeoTIFF**, `EPSG:32612`, **Resolution** in meters
- **Export 3D mesh** — **iTwin Ready** or **OBJ wavefront**
- **Export 3D point cloud** — **LAS**

QGIS needs the orthophoto GeoTIFF.

---

![w:1000](../software/images/itwin_12c_production_format.jpg)

<p class="caption">The production's Format/Options page. iTwin Capture Modeler, Bentley Systems.</p>

---

## While it runs

- **Aerotriangulation is the brain.** If it fails, the model fails
- **Sparse** cloud comes first: points only
- **Dense** reconstruction, the actual model, comes after
- Look at the sparse cloud now: where are the holes?

---

<!-- _class: prompt -->

# The sparse cloud has a hole over the parking lot.

What happened on the flight?

---

## What to turn in

The lab page has the deliverables: [Data Processing](../labs/5_data_processing.md).

Full written steps: [Bentley iTwin](../software/bentley_itwin.md).
