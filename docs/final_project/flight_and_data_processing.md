# Flight and Data Processing

!!! abstract "Key Takeaways"
    - Fly the plan you proposed. If you change it in the field, record what you changed and why.
    - Run the checklist. This is the deliverable where checklist habits are actually graded.
    - Processing is not finished when the software stops. It is finished when you have checked the
      result against something you measured yourself.
    - Worth **5%** of your course grade, the largest single piece.

---

!!! warning "This page is a draft"
    Items marked **Decision needed** are still open. See
    [Open decisions](overview.md#open-decisions).

---

## Part 1 — The flight

### Before you go

- Batteries charged, SD card in and empty, controller and aircraft updated.
- Equipment checklist complete. See the [Pre-Flight Checklist](../class_resources/flight_check_list/pre_flight/pre_general.md).
- Supervising TA or instructor confirmed.
- Weather checked, including wind at altitude rather than at the ground.

### On site

1. Run the site safety check and brief the team.
2. Set up, calibrate, and confirm the mission loads correctly on the controller.
3. Fly the mission. Hold your roles.
4. Fly the ground truth measurements too, or measure them physically while the aircraft is down.
5. Run the [Post-Flight Checklist](../class_resources/flight_check_list/post_flight/post_general.md) before leaving.

!!! warning "Record what actually happened"
    Flight logs are part of the deliverable. If you changed altitude, re-flew a line, aborted for
    wind, or swapped a battery mid-mission, write it down at the time. You will not remember two
    weeks later, and the report needs it.

### Field notes to hand in

- Date, time, and conditions, including wind and cloud.
- Actual parameters flown, against the proposed ones.
- Number of images collected.
- Anything that went wrong, and what you did about it.
- Your ground truth measurements, raw.

---

## Part 2 — Processing

!!! warning "Decision needed — software"
    Which package teams use, and whether licences or seats are limited: _to be set_. Candidates
    already taught in this course are Bentley iTwin and QGIS. [Using QGIS](../software/qgis_measurements.md)
    (Week 4) and [Bentley iTwin](../software/bentley_itwin.md) (Week 7) cover both.

### Expected products

Produce at least:

- An **orthomosaic** of the site.
- A **digital surface model (DSM)**, or a point cloud, depending on your measurement.
- Whatever specific product your question needs — a volume, an area, a profile, a difference map.

The [Week 7](../weeks/week_07.md) reading, [How Photos Become 3D](../gen_reading/sfm_workflow.md), explains what each stage is doing.

### Check the reconstruction before you measure it

Look at the model before you trust it:

- Are there holes over blank asphalt, water, or glass?
- Did anything get matched wrongly — repeating parking stall lines, grass, row crops?
- Does the mesh web across gaps between surfaces that are not connected?
- Does the ortho blur or double anywhere?

Report what you found. A team that spots a bad patch and works around it is doing better engineering
than one that does not look.

---

## Part 3 — The measurement and its check

1. Make your measurement from the drone product.
2. Compare it against your ground truth.
3. Report the difference, as an absolute value **and** as a percentage.
4. Say whether it meets the tolerance you set in your proposal.

| | Drone result | Ground truth | Difference | Within tolerance? |
|---|---|---|---|---|
| Measurement 1 | | | | |
| Measurement 2 | | | | |

!!! tip "A disagreement is a result"
    If your drone measurement is off by 8% and your proposal called for 5%, that is a finding, not a
    failure. Explain where the error most likely came from. Teams lose points for hiding a
    disagreement, not for having one.

---

## Submission

!!! warning "Decision needed — what gets handed in"
    - Do teams submit the **processed products** themselves, or only screenshots and the report?
      Orthomosaics are large. _to be set_
    - **Where:** Learning Suite, Teams, or a shared drive? _to be set_
    - **Raw images:** kept, submitted, or discarded after processing? _to be set_
    - **Due:** _to be set_

---

## Grading

!!! warning "Decision needed — rubric"
    A suggested split, for the instructor to confirm:

    | Element | Points |
    |---|---:|
    | Flight executed safely and by checklist | 20 |
    | Flight matches the proposal, with deviations recorded | 15 |
    | Field notes and logs complete | 10 |
    | Products processed correctly and inspected for defects | 25 |
    | Measurement made and compared against ground truth | 20 |
    | Difference reported honestly and explained | 10 |
