# Week 6 — LiDAR Overview

This page introduces LiDAR sensors on drones: how they work, the primary data products, common use cases, and practical guidance for planning LiDAR flights.

## Key Takeaways
- **Direct Measurement:** LiDAR measures distance directly using laser pulses, unlike SfM which estimates it from photos.
- **Vegetation Penetration:** LiDAR can see through gaps in leaves to map the ground (DTM) even in dense forests.
- **Point Clouds:** The primary output is a 3D point cloud, where each point has an X, Y, Z coordinate and often an "intensity" value.
- **Classification:** Processing involves labeling points as "ground," "vegetation," or "building" to create terrain models.

---

## What is LiDAR?
LiDAR (Light Detection and Ranging) uses rapid pulses of laser light to measure distances to surfaces. A LiDAR sensor records time-of-flight measurements and returns a dense set of 3D points (a point cloud) representing the scanned surfaces.

## How LiDAR works
- **Laser Pulses:** The sensor emits thousands of laser pulses per second and measures the time until the reflected light returns.
- **Georeferencing:** Each point is positioned in space using high-precision GNSS (GPS) and an IMU (Inertial Measurement Unit) that tracks the drone's tilt and rotation.
- **Multiple Returns:** A single laser pulse can hit a leaf, pass through, and then hit the ground. This results in "multiple returns," allowing us to map both the tree canopy and the floor beneath.

### Multimedia: LiDAR in action
Below are links to several LiDAR visualizations. Notice the platform motion and how the laser "paints" the 3D scene.

- [50 Kilometers of Brazilian Forest Canopy](https://en.wikipedia.org/wiki/File:50_Kilometers_of_Brazilian_Forest_Canopy.webm){target='_blank'}
- [Flying Through LIDAR Canopy Data](https://en.wikipedia.org/wiki/File:Flying_Through_LIDAR_Canopy_Data.webm){target='_blank'}
- [Amazon Canopy Comes to Life](https://en.wikipedia.org/wiki/File:Amazon_Canopy_Comes_to_Life_through_Laser_Data.webm){target='_blank'}

## Common data products
- **Point Cloud (LAS/LAZ):** The raw 3D data.
- **Digital Terrain Model (DTM):** A map of the bare ground surface (vegetation removed).
- **Digital Surface Model (DSM):** A map of the top surfaces, including trees and buildings.
- **Canopy Height Model (CHM):** The difference between DSM and DTM, showing actual tree heights.
- **Intensity Imagery:** A raster showing how strongly different materials reflected the laser.

## Use cases & applications
- **Archaeology:** Finding ruins hidden under dense jungle canopies.
- **Forestry:** Measuring tree height, density, and biomass.
- **Infrastructure:** Mapping powerlines and road corridors with high precision.
- **Floodplain Modeling:** Creating accurate ground models for water flow analysis.

## Flight planning & best practices
- **Point Density:** This is the number of points per square meter. Flying lower or slower increases density, allowing you to see smaller details (like thin powerlines).
- **Overlap & Swath:** Ensure laser swaths overlap sufficiently to avoid "gaps" in the point cloud.
- **Georeferencing:** Use RTK (Real-Time Kinematic) or PPK to ensure the point cloud is accurately positioned on the Earth's surface.
- **Sensor Settings:** Adjust the Pulse Repetition Frequency (PRF) based on the required range and density.

## Tools & software
- **Processing:** PDAL, LAStools, CloudCompare.
- **Visualization:** Bentley iTwin, QGIS.
- **Format:** LAS is the industry standard; LAZ is the compressed version.

## Example outputs & images

### 1) Point Cloud vs. Terrain Model
This diagram shows how LiDAR returns are used to separate the "ground" from "vegetation."

![Stylized LiDAR point cloud and terrain model](images/lidar_pointcloud.svg)

*Description: Ground returns (last returns) form the DTM, while first returns contribute to the DSM. This filtering process is what allows LiDAR to "see" the ground under trees.*

**Activity:**
- If you were looking for an old stone wall buried under a forest, which data product would you use: the DSM or the DTM? Why?

---

### 2) Archaeology — Ferrybridge Henge
![Ferrybridge Henge LiDAR hillshade](images/A_lidar_view_of_Ferrybridge_Henge_in_West_Yorkshire.jpg)

*Description: A "hillshade" rendering of a DTM. By removing the trees and buildings and simulating sunlight from the side, archaeologists can find subtle earthworks that are invisible from the ground.*

**Activity:**
- Examine the circular features in the image. How might these be different if we were looking at a standard aerial photograph instead of a LiDAR hillshade?

---

### 3) Forestry — Canopy Heights
![LiDAR forestry canopy heights](images/Lidar_forestry.png)

*Description: Points colored by height. This visualization is a powerful tool for foresters to estimate timber volume and monitor forest health.*

**Activity:**
- Explain the calculation for a Canopy Height Model (CHM). If the DSM value at a point is 45 meters and the DTM value is 32 meters, how tall is the tree?

---

## Further reading & resources
- [Wikipedia — Lidar](https://en.wikipedia.org/wiki/Lidar){target='_blank'}
- [USGS — What is Lidar?](https://www.usgs.gov/faqs/what-lidar){target='_blank'}

<!-- End LiDAR.md -->