# Creating Flight Plans Lab

!!! tip "Rock Canyon flight sign-up"
    Sign up with your teammate for next week's Rock Canyon Park flight on the [**Rock Canyon Flights sign-up sheet**](https://docs.google.com/spreadsheets/d/1PY6UmZ-bPXODonB8KVhoySvfqFCsi2Hi9SblSYZBIEE/edit?usp=sharing){target="_blank"}. See [Part 5](#part-5-mission-4-rock-canyon-park-team).

## Key Takeaways

1. A good flight plan begins with a clear mission objective.
2. Mission constraints influence how a drone flight should be designed.
3. Flight altitude, camera angle, image overlap, and flight speed all affect the quality and efficiency of a mapping mission.
4. Mission planning requires balancing data quality, flight time, battery usage, and operational limitations.
5. A flight plan should be reviewed before flying to confirm that it can be completed safely and within the available time and equipment limits.

---

## Background

Drone mapping missions should be planned before the aircraft ever leaves the ground.

A pilot or mission planner must determine what data needs to be collected, what area needs to be covered, and how the aircraft should fly in order to accomplish the mission safely and efficiently.

For aerial mapping, several flight parameters can directly affect the final data product. These may include:

* Flight altitude
* Camera angle
* Front overlap
* Side overlap
* Flight speed
* Flight path
* Total mission time
* Battery requirements

Changing one parameter can affect several others.

For example, flying at a lower altitude may provide more detailed imagery, but it may also require more flight lines, more photographs, and a longer mission. Increasing image overlap may improve the ability to reconstruct a site, but it can also increase the number of images collected and the amount of data that must be processed.

Mission planning therefore involves making decisions and evaluating tradeoffs rather than simply choosing the highest-quality settings.

In this lab, you will plan **four** aerial mapping missions:

* **Three personal missions**, planned on your own. These are practice missions at sites around Provo, each with a different set of constraints. You will plan them but not fly them.
* **One team mission** at **Rock Canyon Park** in Provo, planned with a teammate. This is a real mission, and its constraints depend on the drone and controller your team will use.

Your goal for each mission is a flight plan that satisfies the mission requirements while also considering the quality of the imagery that will be collected.

---

## Objectives

By completing this lab, students will:

1. Define an objective for an aerial mapping mission.
2. Interpret and apply mission constraints.
3. Select an appropriate flight altitude.
4. Select an appropriate camera angle.
5. Choose front and side image overlap.
6. Select an appropriate flight speed.
7. Estimate the duration of a planned flight.
8. Evaluate tradeoffs between image quality, flight time, battery usage, and data quantity.
9. Create flight plans that satisfy several different sets of mission requirements.
10. Document and justify the major decisions used in each flight plan.
11. Work with a teammate to plan and check a mission for a real flight.

---

## Required Materials

1. Computer or tablet with a web browser
2. The class flight planner: [**cce-byu-flight-planner.streamlit.app**](https://cce-byu-flight-planner.streamlit.app/){target="_blank"}
3. Mission constraints for the personal missions (on this page) and the team mission (on the board)
4. Google Maps, for measuring the size of a mission area
5. Calculator, if needed
6. A way to take screenshots of your finished plans

---

## Lab Overview

This lab will focus on creating flight plans for aerial mapping missions.

You will plan four missions in total:

| Mission | Who | Location | Constraints |
|---|---|---|---|
| Mission 1 – Stadium Turf Check | You, on your own | LaVell Edwards Stadium, BYU | On this page |
| Mission 2 – Inspecting the Y | You, on your own | Y Mountain, Provo | On this page |
| Mission 3 – Racing the Sunset | You, on your own | Utah Lake State Park, Provo | On this page |
| Mission 4 – Team Mission | You and a teammate | Rock Canyon Park, Provo | On the board; depends on your team's drone |

For each mission you will:

1. Review the mission area.
2. Review the constraints.
3. Define the objective of the mission.
4. Select appropriate flight parameters.
5. Create a proposed mapping flight path.
6. Calculate the estimated flight time.
7. Adjust the flight plan as needed.
8. Compare your plan with the mission requirements.
9. Record and justify your final decisions in the [Mission Log](#mission-log).

The goal is not to create one single "correct" flight plan.

Different students may develop different solutions while still satisfying the same mission requirements. Because each of your personal missions uses different constraints, your three plans should also look different from each other. Comparing them is a large part of what this lab teaches.

!!! note "Mission Constraints"
    The constraints for the three personal missions are on this page, in each mission's section below.

    The constraints for the team mission will be listed on the board during the lab, because they depend on which drone and controller your team is using.

!!! warning "Personal missions are planned, not flown"
    Missions 1–3 are practice plans only. Flying any of these sites for real would need permission from the property owner, and some would need FAA airspace authorization. Plan them as if you had both, but do not fly them.

### How the Lab Runs

The personal missions and the team mission happen at the same time.

* Everyone works on **Missions 1–3** at their own computer.
* Meanwhile, teams **rotate through the controller station**, where a TA helps each team build its Rock Canyon Park plan on the actual controller for its drone.
* When a TA calls your team, note where you are in your personal mission and go to the station with your teammate. When your team's turn is over, return to your personal missions and pick up where you left off.

### Suggested Time

| Segment | Minutes |
|---|---|
| Part 1 – Getting Started with the flight planner | 15 |
| Parts 2–4 – Missions 1–3, with each team taking a turn at the controller station (Part 5) | 75 |
| Compare your missions and reflection | 20 |
| **Total** | **110** |

Plan on about 25 minutes for each personal mission, less the time your team spends at the controller station. If you finish a personal mission early, check it once more against its constraints before starting the next one.

---

## Understanding Mission Constraints

Before creating a flight plan, you must first understand the conditions and limitations of the mission.

Mission constraints may include:

* Area that must be mapped
* Maximum or minimum flight altitude
* Maximum flight time
* Available battery capacity
* Required image overlap
* Required camera angle
* Areas that should not be flown over
* Takeoff and landing locations
* Terrain or elevation changes
* Other aircraft operating nearby
* Time available at the site
* Mission-specific data requirements

These constraints help define what is possible and what tradeoffs may be necessary.

### Example Mission Constraints

The following is an example only:

* The total time available to travel to the site, prepare the aircraft, complete the mission, and return may be limited.
* Only a portion of that time may be available for actual flight operations.
* Each group's flight plan may need to remain within a specific flight-time range.
* Multiple groups may be operating at the same location.
* Flight areas may need to be separated so that simultaneous missions do not overlap.
* A qualified pilot or TA may be required to supervise the flight.

!!! warning "Use the Lab Constraints"
    Do not assume the example constraints above apply to your mission.

    Use the constraints written for each personal mission below, and the team mission constraints the TAs list on the board.

### Two Kinds of Constraints

As you read each constraint set, sort each item into one of two kinds:

* **Hard constraints** must be met or the plan fails. Examples: a maximum altitude, a no-fly area, a photo limit, a required camera angle.
* **Goals** are things to do as well as you can within the hard constraints. Examples: the most detail you can get, the shortest flight you can plan.

A plan that meets every hard constraint and does reasonably on the goals is a good plan. A plan with beautiful imagery that breaks one hard constraint is not a plan that can be flown.

!!! tip "Start from the constraint that limits you most"
    In most constraint sets, one item decides the plan and the rest are easy to meet. Find it first.

    If the detail you need sets your altitude, set the altitude and then see whether the flight time still fits. If a short flight time is the tight limit, start there and see what detail you can afford. The [Planning the Flight](../gen_reading/mission_planning_sfm.md) reading works through both cases.

---

## Activity Instructions

### Part 1 – Getting Started with the Flight Planner

All four missions are built in the class flight planner, a website made for planning mapping missions for the class's DJI drones.

!!! success "Open the Flight Planner"
    [**cce-byu-flight-planner.streamlit.app**](https://cce-byu-flight-planner.streamlit.app/){target="_blank"}

    If the page says the app has gone to sleep, click **Yes, get this app back up!** and wait about a minute for it to start.

Set up a practice mission before you begin Mission 1:

1. Open the **Creator** tab.
2. At the top of the sidebar on the left, check **Change to a mapping mission**. This lets you draw an area to map instead of a single flight line.
3. Under **1. Hardware & Payload**, look at the **Drone Platform** choices:
    * **DJI Fly** – the smaller consumer drones. A DJI Fly mission is limited to **99 photos**.
    * **DJI Pilot 2** – the larger enterprise mapping drone. There is no photo limit; the battery is the limit.

    For the personal missions, Mission 1 uses **DJI Fly** and Missions 2 and 3 use **DJI Pilot 2**. Each mission's constraints say which to pick.
4. Use **Jump to Address** below the map to go to the mission area.
5. Use the polygon or rectangle tool on the map to draw the area you want to map.
6. Find each of these settings in the sidebar:
    * **Relative Altitude (ft)** – height above the takeoff point
    * **Elevation Source** – which elevation data the planner uses for the ground under your flight
    * **Gimbal Pitch (°)** – the camera angle. **−90°** points straight down (nadir).
    * **Est. Ground GSD** – the ground sample distance (GSD) at your altitude, shown in cm per pixel
    * **Frontal Overlap (%)** and **Side Overlap (%)**
    * **Flight Speed (mph)**
    * **Set flight line direction** – leave this off to let the planner choose the direction with the fewest flight lines
    * **Show FAA Airspace Restrictions** – shows the altitude ceilings in controlled airspace
7. Above the map, find **Total Path Distance**, **Estimated Photos**, and **Passes** (the number of flight lines).
8. Change the altitude up and down once and watch how the GSD, passes, path distance, and photo count respond.

!!! note "Parameters to Review"
    Ground sample distance (GSD), front and side overlap, and grid and crossing patterns are all explained in [Planning the Flight](../gen_reading/mission_planning_sfm.md). Keep it open during the lab.

!!! note "Naming and saving a plan"
    Before saving, type a name in the **Filename** box under **2. Global Config**. Use your last name and the mission, for example `Smith_M1_Stadium`. The planner adds the platform and your altitude, camera angle, and overlap to the end of the name, so the file comes out looking like `Smith_M1_Stadium_Fly_H150A90OL85SO80`.

    **Save & Generate KMZ** creates the KMZ mission file a drone can fly, and a **Download KMZ** button then saves it to your computer. You will turn in the KMZ file for every mission. See [What to Turn In](#what-to-turn-in).

#### Calculating the Flight Time

The flight planner reports the total path distance, but **not the flight time**. You calculate it. Because 1 mph is exactly 88 feet per minute:

$$
\text{Flight time (min)} = \frac{\text{Total path distance (ft)}}{(\text{flight speed in mph})(88)}
$$

!!! example "Example (illustrative numbers)"
    A plan has a total path distance of 5,280 ft (one mile) and is flown at 10 mph.

    Flight time = 5,280 ft / (10 × 88 ft/min) = **6 minutes** of mapping.

    Takeoff, the climb to the first waypoint, and the return home all add time on top of this, usually a couple of minutes on a small site.

You can also check the planner's path distance. A mapping grid is mostly straight lines, so:

$$
\text{Path distance} \approx (\text{number of passes})(\text{length of the area along the lines})
$$

Measure the length of the area in Google Maps, the same way you did in the [Measurement Lab](2_measurements_and_methods.md). If your rough check and the planner disagree by a lot, something is set incorrectly.

---

### Part 2 – Mission 1: Stadium Turf Check (Personal)

!!! example "Mission 1 constraints"
    **Location:** the playing field at LaVell Edwards Stadium, BYU, including both end zones (about 360 ft × 160 ft, or 110 m × 49 m). Map the grass only, not the stands.

    **Objective:** before the season opener, the grounds crew wants a map of damaged turf. The smallest divots they care about are about 3 in (7.5 cm) across.

    * **Aircraft:** a small consumer drone. Plan it as **DJI Fly**.
    * **Detail:** GSD no coarser than **1.5 cm/px (0.6 in/px)**, so each divot is several pixels across.
    * **Camera:** straight down, **−90°**.
    * **Overlap:** your choice, from the table in [Planning the Flight](../gen_reading/mission_planning_sfm.md#ii-how-much-overlap). Look at which row describes a football field.
    * **Photo limit:** no more than **99 photos**. Do not use the override.

Plan this mission on your own:

1. Copy the constraints into the Mission 1 column of the [Mission Log](#mission-log).
2. Mark which constraints are **hard constraints** and which are **goals**.
3. Write the mission objective in one sentence in your own words.
4. Choose the altitude, overlap, speed, and camera angle, and draw the area in the flight planner.
5. Record the GSD, passes, total path distance, and estimated photos.
6. Calculate the flight time.
7. Check every hard constraint. If any is not met, change the plan and check again.
8. Name the mission (for example `Smith_M1_Stadium`), click **Save & Generate KMZ**, then **Download KMZ**.
9. Take a screenshot of the finished plan showing the flight path and the planner's numbers.
10. Write a short justification of your two most important decisions.

!!! question "Learning Suite Question"
    For Mission 1, which constraint limited your plan the most? What did you change to meet it?

---

### Part 3 – Mission 2: Inspecting the Y (Personal)

!!! example "Mission 2 constraints"
    **Location:** the block **Y** on Y Mountain, above the BYU campus, plus about 50 ft (15 m) of hillside around it. The Y is roughly 380 ft (115 m) tall and sits on a steep, west-facing slope.

    **Objective:** before the Y is repainted, the crew wants to find cracked or worn concrete, down to features about 1.5 in (4 cm) across.

    * **Aircraft:** the enterprise mapping drone. Plan it as **DJI Pilot 2**.
    * **Detail:** GSD no coarser than **2 cm/px (0.8 in/px)**.
    * **Camera:** tilted, **between −70° and −45°**, so the camera looks more squarely at the slope. Explain the angle you chose.
    * **Terrain:** the ground climbs steeply. Set **Elevation Source** to **USGS 3DEP (US High-Res)** so the plan follows the slope.
    * **Takeoff:** from beside the first waypoint. The planner measures altitude from the takeoff point, so a takeoff far below the first waypoint changes the height of the whole flight.
    * **Height above the ground:** never more than **400 ft (122 m)**.

Plan this mission on your own, following the same steps as Mission 1 and recording your work in the Mission 2 column of the [Mission Log](#mission-log).

Before you start, compare these constraints with Mission 1. Predict which of your parameters will need to change, and in which direction, before you touch the flight planner.

!!! tip "Check the slope"
    After saving, open the plan in the **Viewer** tab. It shows the elevation change between waypoints. On this mission, look for any leg where the plan climbs or drops more than you expected.

!!! question "Prediction Check"
    After finishing Mission 2, compare your prediction with the plan you actually built.

    Which parameter changed the most from Mission 1? Did it change the way you expected?

---

### Part 4 – Mission 3: Racing the Sunset (Personal)

!!! example "Mission 3 constraints"
    **Location:** the harbor at Utah Lake State Park, west of Provo: the boat ramps, docks, parking area, and beach along the harbor.

    **Objective:** park staff want a map of the shoreline and the parking area to plan repairs after a season of high water. The sun is setting and the light will be gone soon.

    * **Aircraft:** the enterprise mapping drone. Plan it as **DJI Pilot 2**.
    * **Time:** no more than **12 minutes** of mapping flight, by your calculation.
    * **Detail:** GSD no coarser than **3 cm/px (1.2 in/px)**.
    * **Airspace:** the park is close to Provo Municipal Airport. Turn on **Show FAA Airspace Restrictions**, and fly no higher than the ceiling shown over the site. Record that ceiling.
    * **Height:** never more than **400 ft (122 m)** above the ground.
    * **Water:** keep the flight over land. Photos of open water are nearly featureless and will not match together.

Plan this mission on your own, following the same steps as the first two and recording your work in the Mission 3 column of the [Mission Log](#mission-log).

!!! warning "Some constraint sets cannot all be met"
    A constraint set may ask for more than a single flight can deliver, such as more area than an airspace ceiling and a time limit allow together.

    If you cannot meet every requirement, do not quietly drop one. Decide what you would do instead: split the flight across two batteries, map only the part of the site that matters most, or ask for a change to the constraints. Write down which requirement could not be met and why.

!!! question "Learning Suite Question"
    Put your three personal plans side by side. Which one would you be most confident flying tomorrow, and why?

---

### Part 5 – Mission 4: Rock Canyon Park (Team)

The team mission is planned for **Rock Canyon Park** in Provo. **The plan you make in this part will be flown during next week's lab.**

!!! tip "Sign up for a Rock Canyon flight"
    With your teammate, sign up on the [**Rock Canyon Flights sign-up sheet**](https://docs.google.com/spreadsheets/d/1PY6UmZ-bPXODonB8KVhoySvfqFCsi2Hi9SblSYZBIEE/edit?usp=sharing){target="_blank"}. Choose one row: a trip time, a mission area, and a drone. Put both names in it. Your row is the flight you plan in this part and fly next week.

Its constraints will be listed on the board, and they depend on the drone and controller your team signed up for. Some teams will fly a mission built in the class flight planner; others will use a drone whose controller has its own mission planning app.

You do not work on this mission as a separate block at the end of the lab. While everyone works on their personal missions, teams take turns at the **controller station**, where a TA helps each team build its plan on the actual controller for its drone. See [How the Lab Runs](#how-the-lab-runs).

The team mission is planned the way a real flight crew plans: one person builds the plan, and the other checks it.

#### Before your turn

Do these with your teammate at your desks, in between your personal missions:

1. Find your teammate and sign up together on the [Rock Canyon Flights sign-up sheet](https://docs.google.com/spreadsheets/d/1PY6UmZ-bPXODonB8KVhoySvfqFCsi2Hi9SblSYZBIEE/edit?usp=sharing){target="_blank"}, if you have not already.
2. Record the **drone and controller** from your sign-up row in the Mission 4 column of the [Mission Log](#mission-log).
3. Read the team constraints on the board together, and agree on the hard constraints, the goals, and a one-sentence mission objective.
4. Each of you briefly explains how you approached one of your personal missions. Decide together which approach fits this mission best, and sketch the altitude, overlap, speed, and camera angle you plan to use.
5. If your drone flies missions made in the class flight planner, build the plan there now (set **Drone Platform** to match your drone; if it is a DJI Fly drone, the 99-photo limit applies). Name it with both last names and the site, for example `Smith_Jones_RockCanyon`, click **Save & Generate KMZ**, then **Download KMZ**, and bring the file to the station.

#### At the controller station

6. With the TA, build your plan on the controller, or load and review the plan you made in the class flight planner.
7. One teammate works the controller while the other records the settings and the controller's estimates in the Mission Log.
8. Switch roles for the check. The teammate who did not build the plan goes through every hard constraint and confirms it is met, using the controller's numbers and your own flight-time calculation.
9. Fix anything the check finds, then check it again.
10. Name the mission on the controller the same way, for example `Smith_Jones_RockCanyon`.
11. Take a photo or screenshot of the finished plan on the controller screen.

#### After your turn

12. Return to your personal missions.
13. **Both teammates** record the team plan in their own Mission Log and turn it in. See [What to Turn In](#what-to-turn-in).

!!! tip "Rock Canyon Park is not flat"
    The park climbs toward the mouth of the canyon. In the class flight planner, set **Elevation Source** to **USGS 3DEP (US High-Res)**, and take off as close as you can to the first waypoint.

!!! note "Coordinating with Other Teams"
    Several teams will fly at Rock Canyon Park. Your flight area and takeoff location may need to stay clear of other teams' missions. Check with the teams around you before you finalize the plan.

!!! question "Learning Suite Question"
    What did your teammate catch during the check, or what did you catch in theirs? If nothing needed fixing, what did you check to be sure?

---

## Mission Log

Record your results in the Mission Log spreadsheet. You will use these values to compare your missions, complete the Learning Suite quiz, and turn it in with your mission files.

!!! success "Download the Mission Log"
    [**Download lab03_mission_log.xlsx**](files/lab03_mission_log.xlsx)

    Opens in Excel or Google Sheets. Fill in one column per mission, and upload the finished file to the Learning Suite assignment. The last row checks your flight-time calculation from the path distance and speed you enter.

The spreadsheet has the same rows as the table below:

| | Mission 1 – Stadium | Mission 2 – The Y | Mission 3 – Utah Lake | Mission 4 – Rock Canyon (Team) |
|---|---|---|---|---|
| Mission name (file name) | | | | |
| Drone and planning tool | | | | |
| Hard constraints | | | | |
| Mission objective | | | | |
| Relative altitude (ft) | | | | |
| Est. ground GSD (cm/px) | | | | |
| Frontal overlap (%) | | | | |
| Side overlap (%) | | | | |
| Flight speed (mph) | | | | |
| Gimbal pitch (°) | | | | |
| Passes | | | | |
| Total path distance (ft) | | | | |
| Estimated photos | | | | |
| Flight time (min, your calculation) | | | | |
| Batteries needed | | | | |
| All hard constraints met? (Y/N) | | | | |
| Most important decision, and why | | | | |

!!! tip "Units"
    The flight planner works in feet and miles per hour, but reports GSD in centimetres per pixel. Record each value in the units shown in the table. If your team's controller app uses metres, write down which units it used so the two can be compared.

---

## Compare Your Missions

After finishing all four missions, compare them using your Mission Log.

Consider:

* Which mission had the lowest altitude? Which had the highest? What set each one?
* Which mission had the longest flight time? What caused it?
* Which mission needed the most photographs? How would that affect processing time?
* Did any two missions end up with nearly the same plan even though their constraints were different? Why?
* Which constraint changed your plan the most across all four missions?
* How did planning with a teammate differ from planning on your own?

!!! question "Tradeoffs Across Missions"
    Pick two of your missions. Explain how a difference in their constraints led to a difference in altitude, overlap, or flight time, and what that difference would mean for the imagery collected.

---

## In Lab Reflection

Before leaving the lab, consider the following questions:

* **Limiting Constraint**: Across your three personal missions, what kind of constraint limited you most often: detail, time, photo count, airspace, or terrain?
* **Altitude and Detail**: How did changing the altitude change the GSD, the number of passes, the flight time, and the number of photographs in your plans?
* **Overlap Cost**: When you increased the overlap, which increase cost more flight time: frontal overlap or side overlap? Did that match the [Planning the Flight](../gen_reading/mission_planning_sfm.md#ii-how-much-overlap) reading?
* **The 99-Photo Limit**: On Mission 1, how close did you come to the DJI Fly photo limit? What would you have changed if you had gone over it?
* **Terrain**: On Mission 2, what would have happened to your plan if the drone had taken off at the bottom of the hill instead of beside the first waypoint?
* **Unmet Requirements**: Was there a mission where you could not meet every constraint? What did you decide to do instead?
* **Team Planning**: What was different about planning with a teammate? Did the check find anything?
* **Data Quality**: Which of your four plans would produce the most useful data for an engineer, and what makes it the most useful?

You will be asked to answer these questions in the Learning Suite quiz associated with this lab.

---

## Homework

Complete the questions associated with this lab in Learning Suite, and turn in your mission files.

### What to Turn In

Upload these to the **Learning Suite assignment** for this lab:

| For each mission | Mission 1 | Mission 2 | Mission 3 | Mission 4 (Team) |
|---|:---:|:---:|:---:|:---:|
| The **KMZ file**, named for the mission | ✔ | ✔ | ✔ | ✔ |
| A **screenshot** of the finished plan | ✔ | ✔ | ✔ | ✔ (photo of the controller screen) |

And once for the whole lab:

* Your completed **Mission Log**, as the downloaded spreadsheet from the [Mission Log](#mission-log) section.

Name each file so it can be matched to its mission, for example `Smith_M1_Stadium`. For the team mission, **both teammates** turn in the files, named with both last names, for example `Smith_Jones_RockCanyon`. If your team built its plan on the controller and has no KMZ file, ask the TA how to export it; if it cannot be exported, the photo of the controller screen is enough.

The Learning Suite quiz will also ask for:

1. Your flight-time calculation for each mission.
2. A short justification for the most important decision in each mission.
3. Your answers to the In Lab Reflection questions.

Be prepared to discuss:

* How each set of constraints shaped your plan
* The tradeoffs between detail, flight time, photo count, and battery use
* How you checked that each plan met its constraints
* What you learned from planning with a teammate

---

## Looking Ahead

Next: [Week 7 lab — Rock Canyon Park Flight](4_rock_canyon_flight.md).

In the next lab, the plans move from the screen to the field at **Rock Canyon Park**. Keep your team mission plan, its KMZ file if you made one, and your Mission Log. The decisions you made today are the ones that will be tested.

The flight planner can tell you how far a flight will go and how many photographs it should take. Only flying the mission shows whether the plan was a good one: whether it fit in the time available, whether the batteries lasted, and whether the imagery has the detail and overlap the processing needs.

!!! question "From Plan to Flight"
    Look at your team mission. What could happen at Rock Canyon Park that would make the plan harder to fly than it looked on the screen?

    How would you change the plan if it happened?
