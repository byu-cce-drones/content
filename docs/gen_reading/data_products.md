# Aerial Measurement Products

!!! abstract "Key Takeaways"
    - **Match the sensor to the question.** A normal camera cannot measure temperature, plant
      health, or gas. Specialized sensors exist because those need different physics, not because
      they are better cameras.
    - **The same product can come from different sensors.** A 3D model can be built from ordinary
      photographs or from LiDAR, and there are good reasons to choose either.
    - Each product answers a **different question**. Picking the wrong one is a common and
      expensive mistake.
    - **DSM keeps the trees and buildings. DTM removes them.** That single distinction decides
      whether your earthwork numbers are right.

This page is a reference. You will come back to it in Topics 2, 3, 4, and 6 as each product turns up.

---

## What comes from what

![How the products derive from one another](images/w01_products_family.svg){ width="100%" }

*Photographs are the only thing a drone actually collects. Every product below is derived from them,
and each step throws some information away in exchange for being easier to use.*

---

## The products

| Product | What it is | What you measure with it | Usual file |
|---------|------------|--------------------------|------------|
| **Photos** | The original overlapping images, straight off the memory card | Nothing directly; they are the input to everything else | `.jpg`, `.dng` |
| **Orthomosaic** | Every photo stitched together and geometrically corrected into one flat, correctly scaled image | Distance, area, position, counting things | `.tif` (GeoTIFF) |
| **Point cloud** | Millions of individual 3D points, each with a position and a color | Shapes, cross sections, clearances | `.las`, `.laz` |
| **DSM** (Digital Surface Model) | The height of the top of everything: ground, trees, roofs, equipment | Building and canopy heights, clearances, stockpile volumes | `.tif` |
| **DTM** (Digital Terrain Model) | The height of the bare ground, with vegetation and structures stripped out | Earthwork volumes, grading, drainage and runoff | `.tif` |
| **3D model** | A solid mesh surface with the photographs draped over it as texture | Visual inspection, presentations, walkthroughs | `.obj`, `.fbx` |
| **Contours** | Lines of equal elevation traced from the DTM | Grading plans and construction drawings | `.shp`, `.dxf` |
| **Thermal mosaic** | The same kind of map, but showing temperature instead of color | Heat loss, trapped moisture, failing equipment | `.tif` |
| **Index map** | A ratio between light bands, such as NDVI | Plant health and stress, bare ground, erosion | `.tif` |

!!! note "DEM, DSM, or DTM?"
    **DEM**, Digital Elevation Model, is the umbrella term, and people use it loosely for either of
    the other two. When it matters, say **DSM** for the surface with everything on it and **DTM**
    for bare ground. If someone hands you a "DEM" for an earthwork calculation, ask which one they
    mean before you use it.

---

## Matching the sensor to the need

Choosing a sensor is the same kind of decision as choosing a measurement method: pay for capability
only when the question needs it.

| Sensor | Measures | Reach for it when |
|--------|----------|-------------------|
| **Standard camera** | Visible light | Almost always. It is already on the aircraft and answers most questions |
| **LiDAR** | Distance, by timing laser pulses | Ground under vegetation, power lines, or when you need geometry at night |
| **Thermal** | Surface temperature | Heat loss, trapped moisture, failing equipment, leak detection |
| **Multispectral** | Light bands beyond visible | Plant health and stress, erosion, bare ground |
| **Dedicated detectors** | One specific thing, such as methane or carbon monoxide | Leak surveys and safety work, where the answer is a concentration |

### Photographs or LiDAR for a 3D model?

Both produce a point cloud and a 3D model. Neither is simply better: the equipment costs more for
LiDAR while the time costs more for photographs, so the answer depends on the site and on which of
the two is short.

| | From photographs | From LiDAR |
|---|---|---|
| **Equipment cost** | Low. The camera is already there | High. A dedicated sensor and a heavier aircraft |
| **Time cost** | Hours of processing to solve the geometry | Much less. The points come out almost directly |
| **Needs** | Daylight and visible texture | Neither. It works at night and over plain surfaces |
| **Vegetation** | Sees the top of the canopy only | Pulses slip between leaves and reach the ground |
| **Result** | Full color, looks like the real thing | Precise geometry, limited or no color |
| **Best for** | Open sites, stockpiles, visual records | Forested ground, power lines, dense structure |

!!! tip "The usual answer is a camera"
    Reach past a standard camera when the question genuinely requires it, and be ready to say what
    the extra sensor bought you. "We flew LiDAR because the stockpile was under tree cover" is an
    engineering justification. "We flew LiDAR because we had it" is not.

---

## Which product answers which question

| If the question is | Reach for |
|--------------------|-----------|
| How big is this parking lot? | Orthomosaic |
| How much dirt is in that stockpile? | DSM or point cloud |
| Where will water collect after a storm? | DTM |
| Will the crane clear that roof? | Point cloud or DSM |
| What did this site look like last month? | Orthomosaic from that date |
| Is heat escaping from that roof? | Thermal mosaic |
| Which part of this slope is not growing back? | Index map |
| What do I show the client? | 3D model or orthomosaic |

---

## DSM or DTM

This is the distinction worth getting right, because both look plausible and only one of them gives
you the correct answer for earthwork.

![Surface model compared with terrain model](images/w01_products_surface_vs_terrain.svg){ width="100%" }

*Use a DSM when you care about what is standing on the ground. Use a DTM when you care about the
ground itself.*

---

## Examples

![Orthomosaic example](images/w01_example_ortho.svg){ width="48%" } ![Point cloud example](images/w01_example_point_cloud.svg){ width="48%" }

![DSM example](images/w01_example_dsm.svg){ width="48%" } ![DTM example](images/w01_example_dtm.svg){ width="48%" }

![3D model example](images/w01_example_model_3d.svg){ width="48%" } ![Contours example](images/w01_example_contours.svg){ width="48%" }

![Thermal example](images/w01_example_thermal.svg){ width="48%" } ![Multispectral example](images/w01_example_multispectral.svg){ width="48%" }

*Real examples from class flights will replace these placeholders.*

---

## What you'll produce in this class

| Topic | What you make |
|------|---------------|
| 2 | An orthomosaic, from photos flown for you |
| 3 | Measurements off that orthomosaic, compared against pacing and Google Maps |
| 4 | A flight plan designed to produce a good orthomosaic and surface model |
| 6 | Thermal and multispectral products, and LiDAR point clouds |

Next: [Flight Basics](flight_basics.md) covers the aircraft itself and how to get it into the air.

---

## Where this is used

- [Lab 2 — Measurements and Methods](../labs/2_measurements_and_methods.md) — you measure off an orthomosaic
- [Lab 5 — Data Processing](../labs/5_data_processing.md) — you produce these products from your own flight
