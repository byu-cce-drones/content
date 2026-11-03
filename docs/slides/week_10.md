---
marp: true
theme: byu
math: mathjax
paginate: true
---

<!-- _class: title -->

# Final Project: You Are the Contractor

## Week 10 — Tuesday Lecture

---

## Today

- What the project is, and what makes it engineering
- Four turn-ins, two flight days, one 50-minute trip
- Permissions: airspace, property, people
- Project ideas, old and new — including a 3D model of your own group
- **Before you leave:** a partner and two candidate sites

<!--
Groups form today; the proposal is due Thursday night. Keep the lecture to about 40 minutes and leave 10 for pairing up and picking sites.
-->

---

## The job

You have been hired to fly a drone mission for a client: a city, a contractor, BYU Physical Facilities.

1. Find a civil or construction use for drone data
2. Plan the project, then the flight
3. Fly it, process it, measure something
4. Present it, and write a one-page memo

**Anyone can produce an orthomosaic.** The engineering is saying who needs the data, why you flew it that way, and what it can and cannot be used for.

---

<!-- _class: prompt -->

# "We flew over a parking lot."

Is that a project? What is missing?

<!--
Pairs 1 min, then take three answers.
Likely answer: "it needs a better site" or "a 3D model". Push toward who and why.
-->

---

<!-- _class: answer -->

## A client, a question, and a product that answers it

| Weak | Strong |
|---|---|
| "We flew over a parking lot." | "How much asphalt would it take to repave this lot, and what would it cost?" |
| No one needs the data | Physical Facilities budgets the work from it |
| A pretty 3D model | An area, a volume, a count, a slope, a map of damage |

The question decides the drone, the altitude, the pattern — and the measurement.

---

![w:1100](../final_project/images/w10_fig01_turn_ins.svg)

<!--
Weights: proposal 2.5 %, flight and processing 5 %, presentation 2.5 %, memo 5 % — 15 % of the course.
Nothing in the project can be turned in late. Learning Suite has the official dates.
-->

---

## Groups and flight days

- **Groups of 2.** Same score for both, except the presentation: a student who does not present gets a zero
- **Thu Nov 12** (5 groups) or **Thu Nov 19** (4 groups), trips at **8:00–8:50** or **9:00–9:50**
- Meet at **EB B122**. The trip leaves on time — a partner who is late is left behind
- Sign up for a **drone on a trip** on the sign-up sheet; first come, first served
- A second flight on another day can be arranged with the TAs, if your project needs one
- No class on a flight day for the groups not flying

---

## Three drones per trip

| Drone | Use it for |
|---|---|
| **Mini** | Regular photos: orthomosaics, 3D models, areas, counts |
| **Thermal** | Regular photos plus heat: roofs, pavement, moisture |
| **Multispectral** | Plant health (NDVI) plus regular photos |

The thermal and multispectral slots go first. **If regular photos answer your question, plan on the Mini** — and name a backup drone in your proposal.

---

<!-- _class: prompt -->

# Your site is a 12-minute walk from EB.

The flight itself is 8 minutes. Does the trip fit in 50?

<!--
Pairs 2 min: make them list every step, not just the flight.
Likely answer: "yes, 12 + 8 + 12 = 32". The missing pieces are checkout, setup, checklists, extra photos, pack-up.
-->

---

<!-- _class: answer -->

![w:1000](../final_project/images/w10_fig03_trip_budget.svg)

<!--
The flight is the small part. Walking both ways and the checklists are most of the trip.
Plan for 40 and keep 10 for wind, a pedestrian, or a battery swap. Time your own walk this week.
-->

---

## Permissions are your job

- **Airspace.** Most of campus is in Provo's **Class D**. Flying there needs **LAANC** authorization — Low Altitude Authorization and Notification Capability. A TA files it with you on Thursday, under their Part 107 certificate
- **Property.** Private property, active construction sites and some campus areas need the owner's OK, in writing. An email is fine
- **People and traffic.** Plan the flight so it never passes over people or moving cars

Every flight has a certified TA or instructor supervising.

---

<!-- _class: prompt -->

# LAANC approved for 200 ft. Can you fly over the Quad at noon?

<!--
Pairs 1 min. Likely answer: "yes, we have authorization".
-->

---

<!-- _class: answer -->

## No — LAANC is airspace only

- LAANC answers one question: may you be in this controlled airspace, this high, at this time
- It says nothing about **people** under you (§107.39), the **owner** of the ground, or **moving vehicles**
- Fly the Quad at 7 a.m., or pick a site where no one walks under the grid

Three separate checks: airspace, property, people. The proposal names all three.

---

## The proposal — due Thursday 11:59 PM

About one page, plus the flight-plan screenshot and Mission Log:

1. **Project and purpose** — client, problem, decision
2. **Site** — map, why it fits, hazards
3. **Airspace, permissions, safety** — with the LAANC request attached
4. **Time budget** — every minute, 50 or less
5. **Flight plan** — every setting with a reason
6. **Products and roles** — what you will measure, who flies, who watches

---

## Every setting gets a "because"

| Setting | Your value | Why |
|---|---|---|
| Drone, and a backup | | |
| Altitude above ground | | |
| Ground sample distance (GSD) | | |
| Front and side overlap | | |
| Gimbal angle | | |
| Pattern: grid, double grid, orbit, ascending circle | | |
| Flight time and batteries | | |

"110 ft, 80 % front" is a list. "110 ft, because a 0.5 in GSD shows the cracks" is a plan.

---

## Two gates

A proposal whose flight is **not legal**, or **does not fit in 50 minutes**, comes back — whatever else it does well.

Fix it and resubmit before your flight day. **You are not cleared to fly until the TAs approve it.**

---

<!-- _class: title -->

# Project ideas

## Use one, adapt one, or bring your own

---

## Proven ideas from past semesters

<style scoped>
table { font-size: 20px; }
th, td { padding: 3px 10px; }
</style>

| Idea | Product | What went wrong before |
|---|---|---|
| Parking lot resurfacing | Area, stall count, cost | Missed a corner — run the grid past every edge |
| Pavement condition | Map of the worst failures | Trees modeled badly; fly low enough for a 0.5 in GSD |
| Court or park remodel | Orthomosaic, DSM for drainage | Smooth surface left holes — raise the overlap |
| Earthwork volume | Area × depth, or a DSM | Area came out as 100,000 square miles: wrong CRS |
| Room for more parking | Proposed stalls, dimensioned | Measure one real stall first to check the scale |

Full notes on the [Example Projects](../final_project/project_ideas/) page.

---

## New: quick projects near campus

<style scoped>
table { font-size: 20px; }
th, td { padding: 3px 10px; }
</style>

Walkable from EB, one battery, about 30 minutes on site.

| Idea | Drone | Pattern | Check one number |
|---|---|---|---|
| **A 3D model of your group** | Mini | Ascending circle | Tape one person's height |
| **How tall is it?** A light pole, flagpole, building corner | Mini | Ascending circle | Plans, or tape the shadow |
| **Roof heat loss at 8 a.m.** | Thermal | Grid | Thermometer on one surface |
| **Is this ramp accessible?** | Mini | Low grid + oblique line | A level on the ramp |
| **Count the lot by computer** | Mini | Grid, two days | Hand-count one row |

Your proposal names the exact site. These are starting points.

---

![w:1100](../final_project/images/w10_fig02_group_orbit.svg)

<!--
The fun one. DJI's tower-inspection missions fly exactly this: an ascending circle with the camera locked on the centre. A TA sets it up with you.
The measurement: tape one person's height and compare it with the mesh. That one number is the whole engineering point.
Anyone who moves becomes a ghost — that is a real lesson about what photogrammetry assumes (nothing moves between photos).
-->

---

<!-- _class: prompt -->

# The group portrait: is that a flight over people?

The drone circles 25 ft out with the camera pointed in.

<!--
Pairs 1 min. Likely answers split between "yes, they are under it" and "no, they are participating".
-->

---

<!-- _class: answer -->

## Not if the circle stays outside the group

- §107.39: no flight **over** a person who is not directly taking part in the operation
- The drone circles **around** the group; it never passes over a head
- Anyone else who wanders inside the circle: pause the mission
- Pick a spot with no foot traffic — a lawn at 8 a.m., not the Quad at noon

---

<!-- _class: prompt -->

# You want the height of a light pole. Will a nadir grid do it?

A nadir grid: camera straight down, lawnmower lines.

<!--
Pairs 1 min. Likely answer: "yes, the DSM gives the height".
Follow-up: what does a thin pole look like from straight above?
-->

---

<!-- _class: answer -->

## No — straight down, a pole is a dot

- From above you see the top of the pole and almost none of its side
- A thin object gets too few matches; it comes out as a blob, or a web, or not at all
- Circle it with the camera tilted in, climbing as you go — the same plan as the group portrait

![w:620](../gen_reading/images/w04_fig17_orbit.svg)

---

## A class 3D object: the Rock Canyon water tank

![w:900](../final_project/images/w10_class_watertank_mesh.jpg)

<p class="caption">Flown by a class in March 2026: a grid plus one line of oblique photos at −45°. The wall is there because the oblique line saw it.</p>

---

## Roof heat loss at 8 a.m.

- Cold November mornings are the right time: the building has been heating all night and the sun has not warmed the roof yet
- Warm patches on a cold roof mark where heat is leaking — wet insulation, a gap, an unsealed vent
- Fly the thermal drone on a grid over a low roof you are allowed to fly; save the **radiometric** files, not just the colour JPGs
- **Limit to say in the memo:** apparent temperature, not true temperature — shiny metal and glass lie

---

## Is this ramp accessible?

- The ADA limit for a ramp is a slope of **1:12**, about **8.3 %**
- Fly a low grid along the ramp, plus one oblique line; make a DSM; read the rise over the run in QGIS
- Check it with a 2 ft level and a tape at two spots on the ramp
- A useful answer for Physical Facilities: which runs meet 1:12, which do not

---

## Count the lot by computer

Fly a lot, make the orthomosaic, and let a Python image-recognition model count the cars and trucks.

```python
from ultralytics import YOLO             # pip install ultralytics
model = YOLO("yolo11n-obb.pt")           # trained on aerial photos (DOTA)
r = model.predict("lot.jpg", imgsz=1024, conf=0.3)[0]
names = [r.names[int(c)] for c in r.obb.cls]
print({n: names.count(n) for n in set(names)})   # small vehicle, large vehicle
```

- Fly it twice — two days, or 8:05 and 8:40 — and the project becomes an **occupancy study**
- The check: count one row by hand. How many did the model miss, and how many did it invent?

<!--
The DOTA model was trained on aerial photos, so it knows cars from above; a street-view model does not.
It expects coarser pixels than our 1 cm orthomosaics: export a reduced copy, or a crop of the lot, so a car is a few dozen pixels long.
This snippet is a starting point that a TA should run once on the class orthophoto before a group relies on it.
-->

---

## What good work looks like

- The project answers a question someone would actually ask
- The flight plan is made **before** flying, and every setting has a reason
- The flight runs the way a client would expect from a contractor
- The results are clear, and you say plainly what went wrong and what the data cannot support

**Check one number.** Compare one drone measurement with something measured another way: a taped length, a stall count, a dimension from a plan.

---

## The memo: one page, six headings

Scope and purpose · Flight plan · Flight execution · Data summary and results · Limitations · Conclusion

![h:380](../software/images/qgis_15_lot_done.jpg)

<p class="caption">From the Example Technical Memo: the EB east lot traced in QGIS, 28,000 ft², and one stall taped at 19.5 ft against 19.4 ft on the map.</p>

---

<!-- _class: prompt -->

# What can the client *not* decide from your data?

Take the parking-lot memo: area 28,000 ft², cost about $98,000.

<!--
Pairs 2 min. This is the question every presentation will get.
-->

---

<!-- _class: answer -->

## Say it before they ask

- **Parked cars** hid a third of the pavement: no crack map, so no crack-sealing option
- **Shadows and trees** blur one edge: the area could be off by a few hundred ft²
- The **cost per square foot** is a typical value, not a quote: good for a budget, not a bid

Each limitation says what went wrong, how much it matters, and what would fix it.

---

## The presentation: 12 minutes + 5 of questions

- Both partners present. Slides due **Mon Dec 7**; present **Dec 8 or Dec 10**
- **Lead with the answer** in the first minute, then show how you got it
- Show your site, your products, your measurement, and what went wrong
- Skip the history of drones and the software tour

**Questions to expect:** Why that altitude and overlap? What would you change? How sure are you of that number? What can the client not decide?

---

## Thursday: proposal lab

- Bring your partner, your idea and **two** candidate sites
- Build the flight plan in the class planner; fill in the Mission Log
- File the **LAANC** request with a TA; email any property owner **that day**
- Proposal due **Thu Nov 5, 11:59 PM**, one PDF per group, with the KMZ and permissions

---

<!-- _class: title -->

# Before you leave today

## Find a partner · pick two sites · sign up for a drone on a trip
