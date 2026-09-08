---
marp: true
theme: cce
math: mathjax
paginate: true
---

<!-- _class: title -->

# Measurement Fundamentals

## Week 5 — Tuesday Lecture

---

## Today

- Accuracy, precision, and resolution — three different things
- Where measurement error actually comes from
- How much accuracy a decision needs
- Reporting a number you can defend

---

## The question this course asks

**"The lot is 210 feet long"** — an assertion.

**"210 ± 6 feet"** — a measurement.

Every method in this course, from pacing to a drone, is judged by the same test.

---

<!-- _class: prompt -->

# How good is this number?

You will not know until you can answer that with a range, not a single value.

---

![w:920](../gen_reading/images/w00_fig01_accuracy_precision.svg)

<p class="caption">Accurate means close to the true value. Precise means the repeats agree.</p>

---

## Three different things

- **Accuracy** — how close to the true value. Errors are usually **systematic**.
- **Precision** — how closely repeats agree with each other. Errors are usually **random**.
- **Resolution** — the smallest difference the instrument can show you.

Averaging fixes scatter. It does not fix a result that is consistently off.

---

<!-- _class: prompt -->

# Which walker would you trust for a single walk?

Walker A: 38, 39, 38 steps &nbsp;&nbsp;&nbsp; Walker B: 35, 42, 39 steps

---

![w:920](../gen_reading/images/w00_fig02_pacing_spread.svg)

<p class="caption">Same average, very different spread — only one walker is precise.</p>

---

## Walker A's standard deviation

$$
\bar{x} = \frac{38+39+38}{3} = 38.33
$$

$$
\sigma = \sqrt{\frac{(-0.33)^2+(0.67)^2+(-0.33)^2}{3-1}} = \sqrt{0.33} \approx 0.6 \text{ steps}
$$

A tight $\sigma$ on an average near 38 — Walker A is precise. This says nothing yet about accuracy.

---

![w:900](../gen_reading/images/w00_fig03_error_sources.svg)

<p class="caption">Instrument, method, operator, reference — repeating a measurement only exposes one.</p>

---

## Turning a percent into a range

A calibrated pace is good to about **3%**.

$$
3\% \times 210\text{ ft} \approx 6\text{ ft}
$$

Report **210 ± 6 ft** — not a bare 210.

---

<!-- _class: prompt -->

# Boulder, or beam?

"Is there a boulder in this field?" and "has this beam settled?" do not need the same accuracy.

---

![w:900](../gen_reading/images/w00_fig04_accuracy_ladder.svg)

<p class="caption">The decision sets the accuracy needed — meters down to millimeters.</p>

---

![w:900](../gen_reading/images/w00_fig05_accuracy_effort.svg)

<p class="caption">Accuracy rises with effort, but not smoothly — pick the method the decision needs.</p>

---

<!-- _class: prompt -->

# Pace it off, or fly it?

A pair of boots and a drone both answer some question correctly, and both answer some question wastefully.

---

![w:900](../gen_reading/images/w00_fig06_significant_figures.svg)

<p class="caption">Your calculator does not know how good your input was.</p>

---

## 106.26, or 106 ± 3?

42 paces at a calibrated 2.53 ft/pace:

$$
42 \times 2.53\text{ ft} = 106.26\text{ ft}
$$

Pace is good to about 3% $\Rightarrow$ about ±3 ft.

**Report 106 ± 3 ft.** The extra digits are decoration, not confidence.

---

![w:900](../gen_reading/images/w00_fig07_ground_truth.svg)

<p class="caption">The largest residual against an independent check — that is the honest claim.</p>

---

## What to do Thursday

- Pace your calibration distance **three times** — record every count
- Compute your own $\bar{x}$ and $\sigma$ before lab
- Bring both to [Measurements and Methods](../labs/2_measurements_and_methods.md)

You will check your pace against a tape, then against a parking lot.
