# Example Projects

!!! abstract "Key Takeaways"
    - A good project has a **client**, a **question**, and a **product** that answers it.
    - Pick a site you can reach, fly, and leave in **50 minutes**, starting and ending at EB B122.
    - The ideas below come from past semesters. Use one, adapt one, or bring your own.
    - Read the "what went wrong" notes. Past groups hit these problems so you don't have to.

---

## What makes a good project

| Good | Weak |
|---|---|
| "How much asphalt would it take to repave Lot 45, and what would it cost?" | "We flew over a parking lot." |
| A client who would actually use the answer: a city, BYU Physical Facilities, a contractor | No one who needs the data |
| A product that answers the question: an area, a volume, a count, a map of damage | A pretty 3D model with no measurement |
| A site close to campus with open sky | A site 20 minutes away under trees and power lines |

---

## Ideas from past semesters

### Parking lot resurfacing estimate

Measure the paved area of a campus lot in QGIS, count the stalls, and estimate the cost to repave and
restripe.

- **Products:** orthomosaic; area polygon; stall count.
- **What went wrong before:** one group missed a corner of the lot and had to fill it in from
  Google satellite imagery. Plan your grid to extend past every edge. Another could not map cracks
  because parked cars covered the pavement.

### Pavement condition survey

Map a road or lot and locate the worst failures: alligator cracking, potholes, washouts. Recommend
where to patch and where to fully reconstruct.

- **Products:** orthomosaic or 3D model; marked-up figures of the worst areas.
- **What went wrong before:** trees along the road modeled poorly. Fly low enough to see cracks
  (a GSD around 0.5 in, or 1 cm) and keep the road, not the trees, in the middle of the grid.

### Sports court or park remodel

Document existing conditions of tennis courts, a playground, or a walkway, and propose a remodel:
resurfacing, new striping, better access to parking.

- **Products:** orthomosaic; DSM to check drainage; before-and-after figures.
- **What went wrong before:** a smooth, even court surface left holes in the model. Use higher
  overlap over low-texture surfaces.

### Earthwork volume

On a field or site that has been regraded, measure the area and estimate the soil moved, then compare
against the contractor's number.

- **Products:** orthomosaic; area; volume from area × depth, or from a DSM.
- **What went wrong before:** the area first came out at about 100,000 square miles because the
  coordinate reference system (CRS) was wrong. Set the project to **EPSG:32612** before you measure
  anything. Repetitive dirt texture also gave a poor orthomosaic. The group's final estimate was within
  about 11% of the contractor's, a good result worth reporting.

### Room for more parking

Map an area beside a trailhead or park and measure how many stalls would fit.

- **Products:** orthomosaic or 3D model; a figure of the proposed stalls with dimensions.
- **Tip:** a standard stall is about 9 ft wide and 18 to 20 ft long. Measure an existing stall on
  the orthomosaic first to check your scale.

### Other ideas

- Roof area of a campus building, for a re-roofing or solar estimate.
- Stockpile volume at a construction site (ask the site manager first).
- Impervious area of a block, for a stormwater runoff estimate.
- Vegetation health on a lawn or detention basin, with the multispectral drone.
- Construction progress on a campus project, compared against a site plan.

---

## Before you pick a site

- **Can you do it in 50 minutes?** Walk or drive from EB B122, set up, fly, pack up, and get back.
  See the time budget on the [Project Proposal](proposal.md#4-time-budget) page.
- **Is it legal?** Check the airspace and whether you need LAANC authorization. Most of campus is in
  Provo's Class D airspace.
- **Do you need permission?** Private property, active construction sites, and some campus areas
  need the owner's OK. Getting it is your job.
- **Will the drone see what you need?** Trees, shadows, parked cars, and water all cause trouble.

Then write it up in your [Project Proposal](proposal.md).
