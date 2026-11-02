# Flight and Data Processing

!!! abstract "Key Takeaways"
    - Turn-in point 2 of 4, due **one week after your group flies**: Thu Nov 19 if you fly Nov 12,
      Thu Nov 26 if you fly Nov 19. Worth **5%** of your course grade, the largest piece of the
      project.
    - Most of the points are for **output**: processed products uploaded and raw data shared.
    - Be at **EB B122** by the start of your trip. The trip leaves on time, with or without you.
    - Have your permissions in hand before flight day. If you need LAANC, work it out with a TA
      ahead of time.

---

## Part 1 — Flight day

Each lab runs **two trips**: 8:00–8:50 and 9:00–9:50. Sign up for one on the [flight sign-up sheet](https://docs.google.com/spreadsheets/d/1-hEvm97lUHL3hY51JkCKc-cPAqJRwi-Ihlb1KQrEZ54/edit?usp=sharing). You have
**50 minutes** to leave EB B122, fly, and get back.

### Before flight day

- Proposal approved, and the flight plan built in the planner.
- **Permissions secured:** LAANC authorization through a TA if your site needs it, and the
  property owner's OK if the site is private or an active construction site.
- Weather forecast checked, including wind.

### On flight day

1. **Be at EB B122 by the start of your trip.** The TA checks you in and you pick up the drone. The
   trip leaves on time: a partner who is not there is left behind and gets 0 for attendance. If
   **neither** partner is there, the group gets 0 for attendance and has to find a new time to fly
   with a TA.
2. Travel to the site.
3. Brief your partner and the TA on the site and its hazards, then run the
   [Pre-Flight Checklist](../class_resources/flight_check_list/pre_flight/pre_general.md).
4. Fly the mission. Hold your roles.
5. Take any extra photos or ground measurements you planned.
6. Run the [Post-Flight Checklist](../class_resources/flight_check_list/post_flight/post_general.md)
   and head back. The next trip needs the drone.

!!! warning "Write it down at the time"
    If you changed altitude, re-flew a line, waited out wind, or swapped a battery mid-mission, note
    it on site. You will need it for the memo.

### Flight record

- Date, trip time, and weather (wind and cloud).
- Settings actually flown, beside the ones you proposed.
- Number of photos collected.
- Anything that went wrong, and what you did about it.

---

## Part 2 — Processing

Process your photos in [Bentley iTwin Capture Modeler](../software/bentley_itwin.md), as in the
[Week 8 lab — Data Processing](../labs/5_data_processing.md). Start the same week you fly; processing
can take hours and the lab machines are shared.

### Products

Produce at least **two** of the following, chosen to fit your project:

- An **orthomosaic** of the site.
- A **3D model** (mesh).
- A **digital surface model (DSM)** or **point cloud**.

Then make the measurement or observation your project needs: a length, an area, a count of stalls,
the extent of cracked pavement. Use [QGIS](../software/qgis_measurements.md) for measurements on the
orthomosaic, and set the project CRS to EPSG:32612 first.

### Check the result before you use it

[How Photos Become 3D](../gen_reading/sfm_workflow.md) explains why these happen:

- Holes over blank asphalt, water, or glass?
- Trees or poles that came out as blobs or webs?
- Blurry or doubled areas in the orthomosaic?
- Did aerotriangulation use most of your photos?

Note what you find. These go in the Limitations section of your memo.

---

## Turning it in

**Learning Suite**, one submission per group:

1. Your **flight record**, as a PDF.
2. Your **proof of permission**: a screenshot of the LAANC approval, an email from the property
   owner, or one sentence saying why none was needed.
3. **Processed images:** a screenshot of each product with the whole site in view, a screenshot of
   your measurement or observation, and a sentence or two on any problems you found.

**Raw data**, in the class shared folder (the TAs post the link on Teams):

- A folder named for your project, holding **all the original photos** from the flight, unedited.

---

## Grading

**50 points total.** Both partners get the same score, except attendance, which is scored per
student.

| Criterion | Points | Full credit | Partial credit | No credit |
|---|---:|---|---|---|
| **Mission plan and permissions** | 10 | Flight matches the approved plan, changes recorded with reasons, permission shown, flight record complete | Flown, but changes unexplained, flight record thin, or permission proof missing (5) | Required permission not obtained, or no record (0) |
| **Flight attendance** *(per student)* | 5 | At EB B122 by the trip's start time and on site for the flight | — | Not at B122 when the trip leaves (0). If neither partner is there, the group must reschedule with a TA |
| **Processed products** | 25 | At least two products that fit the project, a measurement or observation made, and problems in the products noted | One product, or products with no measurement (15) | No processed products uploaded (0) |
| **Raw data shared** | 10 | Every original photo in the shared folder, in a folder named for the project | Some photos missing or folder hard to identify (5) | Not shared (0) |
