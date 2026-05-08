# Measurement Lab

!!! abstract "Key Takeaways"
    - Accuracy depends on both the tool and the human operating it.
    - Calibrating your pace is a foundational skill for field estimation.
    - GIS software (like QGIS) allows for higher precision by leveraging high-resolution aerial imagery.
    - Understanding uncertainty is as important as the measurement itself.

---

## 1. Background

In engineering and construction, accurate measurement of distance and area is essential for site planning, cost estimation, drainage design, and infrastructure layout. Traditional field techniques such as pacing and taping provide quick approximations but are limited in accuracy. Modern surveying increasingly relies on aerial imagery and Geographic Information Systems (GIS) to obtain precise measurements efficiently.

In this lab, you will compare multiple methods for estimating area:

- **Human Pacing** (Traditional field method)
- **Google Maps** (Web-based remote sensing)
- **GIS (QGIS)** (Professional-grade orthomosaic measurement)

!!! question "Activity: Prediction Challenge"
    Before you start, rank the three methods from **Most Accurate** to **Least Accurate**. 
    1. [ ] 
    2. [ ] 
    3. [ ] 
    How much of a difference (in square feet) do you think there will be between your pacing estimate and the GIS measurement?

---

## 2. Objectives

By completing this lab, students will:

1. Calibrate their walking pace (feet per step). 
2. Estimate the area of a single parking stall using pacing. 
3. Compare accuracy, uncertainty, and sources of error between methods. 
4. Understand the advantages of aerial and GIS-based surveying techniques.

---

## 3. Required Materials

- **EB-Parking-1-22-26-orthophoto.tif** (provided below)
- Google Maps (web browser)
- QGIS software
- Measuring tape or known-distance reference (provided by TA)
- Lab Worksheet

---

## 4. Procedure

### Part 1 – Pace Calibration

For the first part of the lab you will be finding your pace length in feet per step. This will be used later to convert your pacing measurements into feet. 

1. The TAs will already measure a straight 100‑ft distance on the ground using a tape or known reference.
2. Walk the distance at a normal pace and count your steps. Try to be as consistent as possible with your stride.
3. Repeat at least **three (3)** times and compute the average number of steps per 100 ft.
4. Compute your pace length using:

$$
\text{Feet per step} = \frac{100}{\text{average steps}}
$$

5. Record this value for use in later calculations.

---

### Part 2 – Finding the Area by Pacing

The parking lot we will be measuring (just east of the Engineering Building) is not a perfect rectangle. For the pacing activity, you will pace out the top and left side of the lot.

![EB_Parking_Lot_Pacing.png](images/EB_Parking_Lot_Pacing.png)

1. Using your calibrated pace length from Part 1, pace the **length** and **width** of the entire parking lot.
2. Convert your paced steps to feet.
3. Estimate the parking lot area assuming a rectangular shape:

$$
A_{\text{lot,pacing}} = (\text{length in ft})\,(\text{width in ft})
$$

4. **Stall Measurement:** Measure the length and width of a single parking stall and calculate its area. 
5. **Lane Measurement:** Measure the width of the driving lane between rows of parking stalls. 

!!! note "The Uncertainty Log"
    As you pace, identify at least two things that might make your measurement inaccurate (e.g., walking around a parked car, a slight slope in the pavement). Record these on your worksheet.

---

### Part 3 – Google Maps Measurement 

1. Open **Google Maps** in satellite view.
2. Right‑click on the map and select **Measure distance**.
3. Trace the outline of a single parking stall and record the area (ft²).
4. Trace the full parking lot boundary (asphalt only). Zoom in to ensure you are not including sidewalks or grassy areas.
5. Record the total area (ft²).

---

### Part 4 – Orthomosaic Measurement (QGIS)

Professional GIS software allows for much higher precision because you can zoom in closely on high-resolution drone imagery.

!!! success "Download the Lab Image"
    [**Download EB-Parking-1-22-26-orthophoto.tif**](https://byu.sharepoint.com/:i:/s/CEDroneClass/IQBihTemBdyeQoa21AmGFfznAev9rZIMYF_WNmvkp7KsD3s?download=1){target="_blank"}

1. Open QGIS and load the orthophoto.
2. Using the **Polygon tool**, trace the outline of a single parking stall.
3. Use the **Field Calculator** to compute the area in square feet.
4. Repeat the process for the entire parking lot boundary.

---

## 5. Lab Reflection & Discussion

- **The Winner:** Which method produced the largest value? Which produced the smallest?
- **Accuracy vs. Effort:** Pacing is "free" but tiring. Google Maps is fast but relies on someone else's data. QGIS is precise but requires a drone flight. In what scenario would you choose each?
- **Resolution Impact:** How much easier was it to see the "edge" of the parking lot in the drone imagery compared to Google Maps?
- **The "Ground Truth":** If the measurements don't match, which one do you trust most? Why?
