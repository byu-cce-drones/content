# Final Report

!!! abstract "Key Takeaways"
    - The report is the record. If it is not written down, it did not happen.
    - Its central job is to answer one question: **is this data appropriate, reliable, and
      defensible for the decision at hand?**
    - Report your disagreement with ground truth honestly. That paragraph is worth more than a
      polished 3D model.
    - Worth **5%** of your course grade.

---

!!! warning "This page is a draft"
    Items marked **Decision needed** are still open. See
    [Open decisions](overview.md#open-decisions).

---

## Required sections

### 1. Introduction

The question, the site, and who would use the answer. Half a page.

### 2. Methods

What you planned and what you did.

- Flight parameters as flown, with the proposed values beside them.
- Conditions on the day.
- Equipment used.
- Processing software and the settings that mattered.
- How you made your ground truth measurements.

Someone should be able to repeat your work from this section alone.

### 3. Results

- The products you generated, shown as figures.
- Your measurement.
- Your ground truth measurements.
- The comparison table.

Every figure needs a number and a caption, and every figure must be referred to in the text. A
figure nobody mentions does not belong in the report.

### 4. Accuracy and uncertainty

The section the whole course points at. Address:

- How large is the difference between your result and your check, absolutely and as a percentage?
- Does it meet the tolerance you set in the proposal?
- Where did the error most likely come from? Candidates: GSD, overlap, ground control, surface
  texture, the reconstruction itself, or the ground truth measurement being wrong.
- How confident are you, and in what range does the true value probably sit?

!!! tip "Name the weakest link"
    Every measurement chain has one step that dominates the error. Identifying yours, and saying so,
    is the single clearest sign that you understood this course.

### 5. Discussion and recommendation

- What decision could be made from this data, and at what level of confidence?
- What could **not** be decided from it, and what would you need to collect instead?
- If you flew it again, what would you change, and what would that buy you?

### 6. Conclusion

Short. The answer, its uncertainty, and whether it is fit for purpose.

---

## Format

!!! warning "Decision needed — format and length"
    - **Length:** _to be set_ (suggested: 4 to 6 pages including figures, for a 1-credit course).
    - **File type:** _to be set_.
    - **Submitted where:** _to be set_.
    - **Due:** _to be set_.
    - **Is a report template provided?** _to be set_.

### Writing conventions

- Define every acronym on first use: UAS, SfM, GSD, AGL, VLOS, DSM, DTM.
- Give units every time, in metric and US customary where both are used in practice.
- Do not report more digits than your accuracy justifies. A stockpile volume is not known to the
  cubic centimeter.
- Credit the source of anything you did not collect yourself.

---

## Grading

!!! warning "Decision needed — rubric"
    A suggested split, for the instructor to confirm:

    | Element | Points |
    |---|---:|
    | Question and site clearly framed | 10 |
    | Methods reproducible | 20 |
    | Results presented clearly, figures numbered and referenced | 20 |
    | Accuracy and uncertainty analyzed, not just reported | 30 |
    | Recommendation is supported by the data | 15 |
    | Writing, units, and conventions | 5 |

!!! warning "Decision needed — academic honesty and AI use"
    The course has no stated policy yet on the use of AI writing tools in the report. Worth setting
    one before the project is assigned. _to be set_
