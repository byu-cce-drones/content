# Week 6 — Thermal Imaging Overview

This page outlines thermal (infrared) sensors on drones: how they capture thermal information, typical data products, use cases, and practical flight considerations.

## Key Takeaways
- **Heat, not light:** Thermal sensors measure emitted infrared radiation (heat), not reflected visible light.
- **Surface variation:** Different materials emit heat differently (emissivity), which affects temperature readings.
- **Timing matters:** Early morning or late evening often provides the best thermal contrast for inspections.
- **Applications:** Used widely in building inspections, search and rescue, and precision agriculture.

---

**Key resource:** [DJI — Thermal Drone Basics](https://enterprise-insights.dji.com/blog/thermal-drone-basics){target='_blank'} — A concise, practical overview of thermal sensor types, common payloads, basic flight-planning tips, calibration and emissivity considerations, and typical operational use-cases.

---

## What is thermal imaging?
Thermal sensors measure long-wave infrared radiation emitted by objects, producing images that represent surface temperature differences rather than visible light reflectance.

## How thermal sensors work
- **Infrared Detection:** Sensors detect emitted infrared radiation and convert it to temperature values, either as scaled pixel values or calibrated temperature measurements.
- **Radiometric vs. Non-radiometric:** Some cameras provide relative thermal imagery (for visual inspection), while higher-end units provide radiometrically calibrated images for quantitative temperature analysis.
- **Emissivity:** Surfaces have different emissivities—knowing or estimating emissivity improves temperature accuracy.

## Common data products
- **Radiometric TIFFs:** Temperature-stamped images where each pixel contains a temperature value.
- **Thermal Mosaics:** Stitched orthomosaics showing temperature distribution over a large area.
- **Time-series datasets:** Comparisons of thermal maps over time to monitor changes.
- **File Formats:** Radiometric JPEG/TIFF, FLIR-specific formats.

## Use cases & applications

### 1) Building & Infrastructure Inspection
Thermal images reveal heat loss, missing insulation, HVAC leaks, and rooftop issues.
- **Examples:** Roof heat loss, window/door thermal leaks, HVAC duct defects.

### 2) Electrical & Powerline Inspection
Thermal hotspots on panels, transformers, or circuit breakers can indicate failing components or overloads.
- **Examples:** Transformer hotspots, solar panel cell anomalies, switchgear inspections.

### 3) Search & Rescue / First Responders
Thermal imagery helps detect humans or warm objects in low-light or obscured conditions.
- **Examples:** Drone-assisted searches, night-time perimeter sweeps.

### 4) Agriculture / Vegetation Stress
Thermal contrasts can indicate irrigation stress, soil moisture differences, or animal presence.
- **Examples:** Irrigation effectiveness, livestock detection.

## Flight planning & best practices
- **Overlap:** Ensure high overlap (~80% forward and side) for successful mosaicking, as thermal images often lack distinct features.
- **Altitude & Resolution:** Thermal sensors often have coarser spatial resolution than RGB; flying lower increases ground sampling distance (GSD) but reduces coverage.
- **Time of Day:** Early morning or late evening often yields better thermal contrast for many inspection tasks.
- **Environmental Conditions:** Avoid high winds or recent rain, which can "wash out" thermal signatures.

## Tools & software
- **Processing:** FLIR Tools, QGIS (with plugins), Agisoft Metashape, Pix4D, and UAV-specific inspection tools.

## Example images & student activities

Below are representative thermal images. Use these examples for the suggested activities.

### 1) Lakeshore Geyser — thermal image
<a href="https://commons.wikimedia.org/wiki/File:Thermal_image_of_Lakeshore_Geyser_(early_evening,_1_August_2016).jpg" target="_blank">
  <img src="../images/lakeshore_geyser_thermal.jpg" alt="Thermal image of Lakeshore Geyser" width="720">
</a>

*Description: This image captures the dramatic temperature difference between boiling geothermal water and the cooler surrounding soil. Notice how the steam also carries heat, creating a "soft" glow around the water. In thermal imaging, the bright white areas represent the highest temperatures, while dark purple/black areas are the coolest.*

**Activity:**
- **Emissivity Exploration:** Water and soil have different "emissivity" (how efficiently they emit heat). If the water and the soil were exactly the same temperature, would they look the same in this thermal image? Why or why not?
- **Timing:** This was taken in the early evening. How would the contrast change if it were taken at 2:00 PM on a sunny day?

---

### 2) Coronation Reserve — paired visual + thermal
<a href="https://commons.wikimedia.org/wiki/File:Thermal_image_and_visual_image_of_Coronation_Reserve.png" target="_blank">
  <img src="../images/coronation_reserve_thermal_rgb.png" alt="Thermal and visual image of Coronation Reserve" width="960">
</a>

*Description: This side-by-side view demonstrates why "co-registration" (matching the two images) is so important. A thermal "hotspot" might look like a fire or a leak, but when compared to the RGB image, you might realize it's just a metal roof reflecting the sun. Notice how the paved paths and buildings retain more heat than the grass.*

**Activity:**
- **Thermal Inertia:** Look at the large building in both images. Metals and concrete have high "thermal inertia," meaning they hold onto heat long after the sun goes down. Based on the thermal signatures, which materials in this park seem to be cooling down the fastest?
- **Feature Matching:** Identify three specific objects (e.g., a tree, a path, a building corner) that are clearly visible in both sensors.

---

### 3) Large temperature-differential example
<a href="https://commons.wikimedia.org/wiki/File:Thermal_and_visual_image_showing_29_degree_C._temperature_differential.png" target="_blank">
  <img src="../images/temp_29deg_differential_thermal.png" alt="Thermal and visual image showing 29°C differential" width="1280">
</a>

*Description: This example shows a massive 29°C (84°F) difference within a single scene. Thermal cameras use "palettes" (like Ironbow, Rainbow, or White Hot) to map these temperature ranges to colors. Choosing the right palette can make a subtle leak look obvious or a dangerous hotspot stand out.*

**Activity:**
- **Palette Choice:** The current palette uses "White Hot" for the highest temperatures. If you were searching for a lost hiker in a cold forest, would you prefer "White Hot" or a rainbow-colored palette? Why?
- **Metadata:** To know that the difference is exactly 29°C, we need a "radiometric" sensor. What kind of metadata must the drone record for every pixel to give us an actual temperature instead of just a pretty picture?

---

## Further reading & resources
- [FLIR — How Do Thermal Cameras Work?](https://www.flir.com/discover/otm-ii/how-do-thermal-cameras-work/){target='_blank'}
- [NASA — Infrared Waves](https://science.nasa.gov/ems/07_infraredwaves){target='_blank'}

<!-- End Thermal.md -->
