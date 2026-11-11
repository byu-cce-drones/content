# FE Surveying Review

!!! abstract "Key Takeaways"
    - This page collects the review materials for the **surveying** portion of the **FE** (Fundamentals of Engineering) exam.
    - The slide deck is the lecture outline; the homework lets you practice the same topics.
    - Try each problem first. Open a hint only when you are stuck, and open them one at a time.

---

## Downloads

- [FE Surveying Review slides (PowerPoint)](../slides/fe_surveying_review.pptx)
- [FE Surveying Homework (Word)](fe_surveying_homework.docx)

---

## Hints

Hints point you to the right method and the right Handbook section. They do not give final answers.
Keep the NCEES FE Reference Handbook open while you work.

??? question "Problem 1 — Bearings, azimuths, and an oblique triangle"
    - **(a)** A bearing in the northeast quadrant needs no conversion beyond reading the angle from north.
    - **(b)** You are given the angle turned *to the right* at B, measured from line BA, not line AB.
      Start from the back azimuth of AB, then add the angle. Subtract 360° if you pass it.
      To write a bearing, find the quadrant first, then the acute angle to the north or south line.
    - **(c)** Which two sides and which angle do you know? When the known angle is *between* the
      two known sides, use the law of cosines.
    - **(d)** Now that you know AC, the law of sines is fastest. Check your answer by finding the
      third angle and confirming that all three add to 180°.

??? question "Problem 2 — Differential leveling"
    - **(a)** Compute the height of instrument (HI) as elevation + BS. Then elevation = HI − FS.
      Repeat at each setup. A turning point is both a foresight and the next backsight.
    - **(b)** The sum of the backsights minus the sum of the foresights must equal the last
      elevation minus the first.
    - **(c)** Misclosure is the difference between what you computed and what is published. Watch
      the sign convention and state which way you subtracted.
    - **(d)** Grade is rise over run. Use the elevation change (with its sign) over the horizontal distance.

??? question "Problem 3 — Earthwork by average end area"
    - **(a)** Treat each 100 ft interval as its own segment: average the two end areas, then multiply by 100 ft.
      Add the segments, then convert ft³ to yd³ (27 ft³ = 1 yd³).
    - **(b)** The prismoidal formula uses *three* areas: both ends and the middle section. Look it up
      in the Handbook, and note that the middle area is the measured section, not an average.
      Convert to yd³ the same way and subtract. Pay attention to which method gives the larger value.

??? question "Problem 4 — Closed traverse"
    - **(a)** The interior angles of an n-sided polygon should sum to (n − 2) × 180°. The difference
      is the angular misclosure. Spread it equally and check that the adjusted angles sum correctly.
    - **(b)** Move from one leg to the next with: new azimuth = previous azimuth ± 180° + angle to the
      right at that vertex. The check is to carry the last azimuth back around to line AB.
    - **(c)** Latitude = distance × cos(azimuth); departure = distance × sin(azimuth). Sum each
      column. For a perfect traverse both sums would be zero. The linear misclosure is the
      hypotenuse of the two sums, and precision is the perimeter divided by that misclosure.
    - **(d)** Each leg's correction is proportional to its length over the perimeter. The sign is
      opposite to the misclosure. Check that the corrected columns sum to zero.
    - **(e)** Start at A and add each leg's *adjusted* latitude and departure in turn.
    - **(f)** Use the coordinate (cross-multiplication) formula from the Handbook. Subtracting a
      constant from all the coordinates first keeps the numbers small without changing the area.
      Remember to divide by 2, and then by 43,560 for acres.

??? question "Problem 5 — Horizontal and vertical curves"
    - **(a)** Every horizontal curve element comes from R and Δ. Start with Δ/2, since most of the
      formulas use it. Keep your angle in decimal degrees when you use a calculator.
    - **(b)** Station arithmetic is easier in feet: write 118+42.50 as 11,842.50, work, and convert
      back. The PC is a tangent length before the PI. The PT is a *curve length* after the PC.
    - **(c)** Compare "PI + T" with your PT from (b). Think about which path the stationing follows
      along the alignment, and what it does at the PI.
    - **(d)** The PVC and PVT are each half the curve length from the PVI. Use the grade of the
      tangent on that side to find their elevations.
    - **(e)** A is the difference in grades in percent (later grade minus earlier grade). K is the
      curve length divided by A. The sign of A tells you whether it is a crest or a sag.
    - **(f)** The low point is where the slope of the curve is zero. Find its distance from the PVC
      with the Handbook formula, confirm it falls within the curve, then plug that distance into
      the curve elevation equation.
    - **(g)** First find how far Station 118+00 is from the PVC. Then use the same elevation
      equation as in (f).
