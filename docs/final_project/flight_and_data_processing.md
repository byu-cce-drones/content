# Flight and Data Processing

!!! abstract "Key Takeaways"
    - Turn-in point 2 of 4, due **one week after your group flies**: Group A Thu Nov 19, Group B
      Thu Nov 26. Worth **5%** of your course grade, the largest piece of the project.
    - Fly the plan you proposed. If you change something in the field, write down what and why.
    - Run the checklists. This is where checklist habits are graded.
    - Processing is done when you have **looked at** the result, not when the software stops.

---

## Part 1 — The flight

Group A flies Thu Nov 12 and Group B flies Thu Nov 19, starting in EB B122. Coordinate the details
with the TAs.

### Before you go

- Proposal approved, and the flight plan loaded on the controller.
- Batteries charged, SD card in and empty.
- Supervising TA confirmed.
- Weather checked, including the wind forecast.

### On site

1. Brief your partner and the TA on the site and its hazards.
2. Run the [Pre-Flight Checklist](../class_resources/flight_check_list/pre_flight/pre_general.md).
3. Fly the mission. Hold your roles.
4. Take any extra photos or ground measurements you planned.
5. Run the [Post-Flight Checklist](../class_resources/flight_check_list/post_flight/post_general.md)
   before you leave.

!!! warning "Write it down at the time"
    If you changed altitude, re-flew a line, waited out wind, or swapped a battery mid-mission, note
    it on site. You will not remember it by the time you write the memo.

### Flight record to hand in

- Date, time, and weather (wind and cloud).
- Settings actually flown, beside the ones you proposed.
- Number of photos collected.
- Anything that went wrong, and what you did about it.

---

## Part 2 — Processing

Process your photos in [Bentley iTwin Capture Modeler](../software/bentley_itwin.md), as in the
[Week 8 lab — Data Processing](../labs/5_data_processing.md). Start the same week you fly; processing
can take hours and the lab machines are shared.

### Products

Produce at least **two** of the following, chosen to fit your purpose:

- An **orthomosaic** of the site.
- A **3D model** (mesh).
- A **digital surface model (DSM)** or **point cloud**.

Then make the measurement or observation your project needs: a length, an area, a count of stalls,
the extent of cracked pavement. Use [QGIS](../software/qgis_measurements.md) for measurements on the
orthomosaic.

### Check the result before you use it

[How Photos Become 3D](../gen_reading/sfm_workflow.md) explains why these happen:

- Holes over blank asphalt, water, or glass?
- Trees or poles that came out as blobs or webs?
- Blurry or doubled areas in the orthomosaic?
- Did the aerotriangulation report use most of your photos?

Note what you find. These go in the Limitations section of your memo.

---

## Turning it in

Upload to Learning Suite, **one submission per group**:

1. Your flight record (Part 1), as a PDF.
2. Screenshots of each product, with the whole site in view.
3. One screenshot of your measurement or observation.
4. A sentence or two on any problems you found in the products.

Keep your processed files on the lab machine or your own drive. You will need them for the slides
and memo, and you do not need to upload them.

---

## Grading

Scored on three criteria, 10 points each, **30 points total**. Both partners get the same score.

| Criterion | Exceeds (10) | Meets (8) | Below (5) |
|---|---|---|---|
| **Mission execution** | Flight matches the proposed plan, checklists used, and the mission ran smoothly, to the standard a client would expect from a contractor | Flight completed in the time given with a few hiccups, or changes from the plan not explained | Flight poorly executed, or it does not match the project |
| **Flight record** | Complete: conditions, settings flown against settings planned, photo count, problems and fixes | Mostly complete; one or two items missing | Little or no record kept |
| **Processed products** | At least two products that fit the purpose, a measurement made, and problems in the products noted | Products made, but no measurement or no check of their quality | One product or less, or products unusable |

A part that is missing entirely scores **0**.
