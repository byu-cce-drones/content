# How Photos Become 3D

!!! abstract "Key Takeaways"
    - **Structure from Motion (SfM)** turns ordinary overlapping photos into a 3D model by finding
      the same point in several of them.
    - A point photographed **once** is useless. The same point photographed from several positions
      becomes a measurement.
    - The software solves for **where the camera was** and **what the scene looks like** at the same
      time.
    - Knowing roughly where the drone was, from GPS, makes that solve faster and puts the answer in
      the right place on Earth.

This page is about why you fly the way you do in the next section. You do not need the algorithms;
you need to know what the software is trying to do, so that you give it what it needs.

---

## Where 3D comes from

A single photo is flat. Two photos of the same thing, taken from different places, are not.

![One pole photographed from two positions](images/w04_fig01_parallax.svg){ width="100%" }

*Figure 1: The same pole looks short from almost overhead and long from off to the side. That
difference is the measurement.*

If you already know where the drone was for each photo, the only unknowns left are the height and
position of the pole, and two photos are enough to solve for them. Two known camera positions, two
measured angles, one unknown height: that is a triangle.

### What if you do not know where the drone was?

In practice you rarely know the camera positions exactly. Then you are solving a bigger problem:
**where each photo was taken from, and where everything in the scene is, at the same time.**

That is still solvable, but it needs more to work with. The same point has to appear in several
photos, and each pair of photos needs several points in common, not just one. Given enough shared
points across enough photos, there is only one arrangement of cameras and 3D points that explains
every photo at once, and the software searches for it.

This is what Structure from Motion does, and it is why the name mentions structure *and* motion: it
recovers the shape of the scene and the path of the camera together. Robotics calls the same problem
**SLAM**, simultaneous localization and mapping.

!!! warning "Shape is not size"
    With no known positions at all, the software recovers the **shape** of everything and the
    relative arrangement of the cameras, but not the **size**, and not where any of it sits on
    Earth. A model of a building can come out perfectly proportioned and twice life size.

    Something has to supply the missing scale and position. Usually that is the drone's GPS. It does
    not have to be perfect: a rough position for each photo gives the software a starting point near
    the answer, so it solves faster and drifts less. With **RTK GPS**, where each photo's position is
    known to a few centimeters, the camera positions are close to known before processing begins.

---

## Why overlap is the whole game

Everything above depends on one thing: the same point appearing in many photos. That is what overlap
buys you, and it is the single most important number you set before a flight.

![What overlap means](images/w04_fig02_overlap.svg){ width="100%" }

*Figure 2: Overlap is not wasted effort. It is what puts every ground point into five to nine
different photos.*

A **tie point** is a feature the software recognizes in more than one photo. More overlap means more
tie points, and more tie points means a better solve. Too little overlap and the reconstruction
develops holes that no amount of processing will fill.

### What makes a good tie point

The software is not looking for *texture*. It is looking for a point it can identify **uniquely** and
then find again in another photo. Those are not the same thing, and the difference is where most
reconstructions go wrong.

| Kind of surface | Examples | What the software does |
|-----------------|----------|------------------------|
| **Uniquely identifiable** | A manhole cover, a rock, a building corner, a crack, a painted arrow or number | Matches it correctly. This is what you want. |
| **Nothing to identify** | Blank asphalt, fresh snow, still water, plain roofs, glass | Finds nothing. You get holes. |
| **Identifiable but repeated** | Parking stall lines, lane dashes, grass, row crops, tiled roofs | Matches confidently and **wrongly**. |

!!! warning "A repeating pattern is worse than a blank one"
    A blank surface fails honestly. The software finds nothing, and you get a hole you can see and
    deal with.

    A repeating pattern fails quietly. Every dash in a lane line looks like every other dash, so a
    segment in one photo gets matched to the wrong segment in the next. Parking lot stall lines do
    this constantly. So does grass: one clump looks distinctive on its own, but the field is full of
    clumps that are equally distinctive and look just like it. Row crops are the same problem planted
    in neat rows.

    The result is not a gap. It is a model that is confidently wrong, sometimes with a whole section
    shifted or warped, and nothing on screen tells you. Only a checkpoint catches it.

    **What helps:** more overlap, so a bad match is outvoted by good ones; a cross-hatch pass, so the
    pattern is seen from a second direction; and ground control, so the error has something to show
    up against.

!!! tip "This is why overcast days are good for mapping"
    Flat light means a feature looks the same in every photo. Bright sun creates hard shadows that
    move as you fly, and a shadow edge is exactly the kind of false feature that fools the matcher.

---

## From points to products

Once the cameras and the tie points agree, the rest is mechanical. Each step trades some information away for something easier to use.

![The reconstruction pipeline](images/w04_fig03_pipeline.svg){ width="100%" }

*Figure 3: The same building at four stages. A sparse cloud of tie points is thickened into a dense
cloud, meshed into a surface, and covered with the original photographs.*

### What actually happens at each step

**Sparse to dense.** The sparse cloud only has points where the software found something
distinctive, so it is mostly corners and edges. Now that it knows where every camera was, it goes
back to the photos and works on *every* pixel. The trick is that once the camera positions are
known, a pixel's match in another photo must lie along a single known line, so a search of the whole
image becomes a search along one line. That is what makes matching millions of points possible at
all. Thousands of points become millions.

**Dense to mesh.** A point cloud is samples, not surfaces. Meshing stretches a continuous skin of
triangles over the points, bridging small gaps and deciding what is solid. Noise gets smoothed here,
and thin things such as railings, wires, and fence posts often vanish, because too few points landed
on them to define a surface.

It also errs the other way. Where two things are near each other but not actually joined, such as a
tree beside a wall, the gap between two buildings, or the space under a railing, the mesher can
bridge straight across and invent a surface that is not there. Models like this look shrink-wrapped
or webbed, and it is obvious once you know to look for it.

!!! tip "If the mesh looks webbed, change the tolerance"
    Processing software exposes settings for how far it is willing to reach when joining points.
    Tighten them and the mesh follows the points more strictly, which removes the false webbing at
    the cost of leaving more genuine holes. Loosen them and you get a smoother, more complete
    surface that may be partly invented. Neither setting is correct in general; it depends on
    whether you would rather have gaps you can see or surfaces you cannot trust.

**Mesh to textured model.** Each triangle is colored using whichever photo saw it best: most
face-on, least blurred, least shadowed. This adds no geometry at all. It is what makes the model
recognizable rather than what makes it accurate.

**Surface to orthophoto.** Every photo is a perspective view, so buildings lean outward from the
center of the frame and the scale changes across it. Orthorectification projects each pixel onto the
surface the software just built, then re-renders the scene as if photographed from directly
overhead, everywhere at once. Every part of the result is at the same scale, and that is precisely
what makes it something you can measure on.

**Surface to DSM and DTM.** The surface is sampled onto a regular grid, storing one height per cell
instead of a picture. Keep everything and you have a **DSM**. Classify the cells, remove the ones
that are vegetation or structures, and interpolate the ground underneath, and you have a **DTM**.

![From the surface to the deliverables](images/w04_fig03b_to_products.svg){ width="100%" }

*Figure 3b: The orthophoto and the DSM are the same surface read two different ways, one as a
picture and one as a grid of heights.*

!!! note "Georeferencing runs through all of it"
    None of the above puts the model anywhere in particular. GPS positions and ground control points
    are what tie the whole reconstruction to real coordinates, and that happens during the solve
    rather than at the end.

See [Aerial Measurement Products](data_products.md) for what each of those outputs is
used for.

---

!!! question "Activity: think like the software"
    Look at two overlapping photos from a flight, or at the site outside your classroom.

    1. **Find three easy features.** Points a computer could identify and find again: a manhole
       cover, a corner of a sidewalk, a painted arrow or number.
    2. **Find three hard ones.** Two kinds count here. Areas with nothing to match at all, such as
       blank asphalt or a puddle, and areas full of things that look identical to each other, such
       as stall lines or mown grass. Which kind worries you more, and why?
    3. **Then decide.** You are asked to map a rocky canyon and a snowfield on the same day. Which
       one worries you, and what would you change about the flight to compensate?

---

??? note "Optional: what the algorithms are called"
    You will meet these names in software documentation. You do not need them for this course.

    - **Feature detectors:** SIFT, ORB, AKAZE. These find and describe distinctive keypoints.
    - **Outlier rejection:** RANSAC. Throws out matches that do not fit the emerging geometry.
    - **Bundle adjustment solvers:** Ceres Solver, g2o. These minimize reprojection error, the gap
      between where a point should appear in a photo and where it actually does.
    - **Surface reconstruction:** Poisson reconstruction, Delaunay triangulation. These turn a cloud
      of points into a continuous surface.
    - **Open-source pipeline:** COLMAP, if you want to see the whole process end to end.

---

## Where this is used

- [Lab 3 — Creating Flight Plans](../labs/3_creating_flight_plans.md) — the overlap you plan for is driven by what this process needs
- [Lab 5 — Data Processing](../labs/5_data_processing.md) — you run this process on your own photographs
