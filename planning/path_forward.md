# Path Forward — 2026-09-04

Written in response to the instructor's inline answers on `review/SITE_REVIEW_2026-09-04.md`. That
review file is git-ignored and will eventually be deleted; this file is the durable version of what
came out of it. Open items are tracked in `backlog.md`; this file holds the *reasoning and the
proposed wording* that the backlog items point at.

**Status, 2026-09-04 (evening).** Sprint 1 (§9) is applied and pushed. Two streams are now in flight
and are meant to run in parallel without touching each other's files:

- **Site reorganization by week** — replaces Sprint 3. **Done and committed 2026-09-04** following
  `planning/reorg_plan.md` (Steps 0–9; Step 2's Week 3 lab page waits on the outline review in
  `review/WEEK3_LAB_OUTLINE.md`, and the page is a coming-soon stub until then). Nav is by week with
  `docs/weeks/` index pages and a Reference section; no URL changed. Once pushed, the measurement
  reading can be wired in: its nav placement is now **Start Here plus Week 5**, and the Week 5 line is
  already in `mkdocs.yml` as a comment.
- **Measurement Fundamentals reading** — **landed 2026-09-04**, committed on top of the reorg. Page,
  seven figures, nav (Start Here and Week 5), Week 5 index link, and the Lab 2 Part 1 standard-deviation
  step are all in. What is left is in `backlog.md` under Content gaps.

Sections 1–3 below still need a sign-off before the syllabus is rewritten.

---

## 1. Outcomes — the two-tier structure

The instructor's framing, in their words:

> "I like these 4 outcomes. They should be the 'base' of the course. To meet them, in this case, we
> use aerial measurements, but the same outcomes could be met in a survey class, an environmental
> measurements class, or other class."

> "The outcomes currently listed specific to this class should not be called learning outcomes, but
> come up with another term, skills, knowledge, etc. Need to consolidate. Perhaps have skills or
> ideas that are gained with each lab or HW and a master list."

That is a real structural change from the review, which proposed one flat list of six. Six is still
too many things at two different altitudes. The two-tier version separates them cleanly.

### Tier 1 — ABET outcomes

Four outcomes. Reworded from the review draft to strip every drone-specific phrase, so the same four
would hold in a surveying or environmental-measurements course. This is the test the instructor set:
if an outcome mentions aircraft, imagery, or flight, it is in the wrong tier.

> **M1. Distinguish accuracy, precision, and resolution,** and identify the principal sources of
> error in a measurement.

> **M2. Select a measurement method appropriate to the accuracy a decision requires,** and justify
> the choice in terms of the time, cost, and effort it consumes.

> **M3. Verify a measurement against independent ground truth,** and report the result together with
> its uncertainty.

> **M4. State what a measurement can and cannot support,** well enough that another engineer could
> act on it or reject it.

M1 → M2 → M3 → M4 is a ladder: know the terms, choose the method, check the answer, defend it. It is
also the arc the semester already follows.

Changes from the review draft: M1 lost "taken from aerial imagery"; M3 lost nothing; M2 and M4 were
already generic. M1 and M3 between them now carry all four measurement terms — see §2.

**How this course meets them.** This table is the argument that CCE 194R is a valid instance of the
four, and is the thing to show at accreditation review. It belongs in the syllabus.

| Outcome | How this course meets it | Evidence |
|---|---|---|
| M1 | Measurement fundamentals reading; Lab 2 pacing vs. Google Maps vs. orthomosaic | Week 5 reading quiz; Lab 2 uncertainty log |
| M2 | Accuracy-vs-effort framing; sensor comparison; flight planning for a target GSD | Lab 2 method comparison; Lab 3 flight-plan justification; project proposal |
| M3 | Ground control and check points; measuring a known dimension in the orthomosaic | Lab 2 results table; project flight and processing deliverable |
| M4 | Final report and presentation: what the data supports and what it does not | Project report and presentation |

### Tier 2 — the course-specific list

**Proposed name: "Course Skills."** Plain enough for a freshman, and unmistakably not the ABET word.
Alternatives if you prefer: "Skills and Knowledge" (accurate, covers the C1/C6 knowledge items but
clumsier), or "What You Will Be Able To Do" (friendliest, least formal). I would use Course Skills.

Thirteen skills, absorbing all thirteen old ABET items plus the review's S1 and S2. Every one names
where it is built and which Tier 1 outcome it serves, which is exactly the "master list" the
instructor asked for.

| # | Skill | Built in | Serves |
|---|---|---|---|
| C1 | Describe how aerial measurement is used on civil and construction projects | Class Overview reading | context |
| C2 | Describe the Part 107 rules that govern a flight, and say when a certificate is required | Part 107 readings; practice exams | M4 |
| C3 | Operate a small unmanned aircraft under control in a confined space | Lab 0 | — |
| C4 | Complete a flight from a written checklist, pre-flight through post-flight | Lab 1; Lab 4 | M3 |
| C5 | Recognize common flight problems and take the right corrective action | Common Flight Issues reading; Labs 0 and 4 | — |
| C6 | Explain how overlapping photos become a 3D model, and what the process needs to succeed | How Photos Become 3D | M1 |
| C7 | Plan a mapping mission: altitude, overlap, ground sample distance, and ground control | Planning the Flight; Lab 3 | M2 |
| C8 | Compare RGB, LiDAR, thermal and multispectral sensors and say which suits a given question | Sensor readings | M2 |
| C9 | Load, measure and export from a geographic information system | QGIS page; Lab 2 | M3 |
| C10 | Process an image set into an orthomosaic and a 3D product | Bentley iTwin page; Lab 5 | M3 |
| C11 | Work as a team through plan → fly → process → report | Final project | M4 |
| C12 | Present measurement results in writing, visually, and orally | Final project | M4 |
| C13 | Apply fundamental surveying and trigonometry concepts to a field measurement | Week 12 (page does not exist yet — see §8) | M1, M3 |

Notes on what happened to the old thirteen:

- Old #4 ("operate mini drones indoors") and old #5 ("prepare and use checklists") were lab
  activities pretending to be outcomes. As Tier 2 skills they are fine, and become C3 and C4.
- Old #7 named Google Earth and QGIS. C9 drops the tool names; naming a tool in a list you have to
  defend for years dates it the moment the tool changes. The tools stay named on the page.
- Old #10's radar is dropped, per the instructor.
- Old #13 was a bare noun phrase. C13 gives it a verb, and flags that nothing on the site teaches it.
- Old #6 (accuracy vs. precision) is not here — it was promoted to M1, where it belongs.

### Where each list lives

- **Tier 1** goes in `class_resources/syllabus.md`, under "Course Learning Outcomes", with the
  meets-them table above and a note that this is the ABET-recorded wording. It replaces **both**
  existing lists.
- **Tier 2** goes on a new page, `class_resources/course_skills.md`, linked from the syllabus.
- Each lab and reading gains a short "Skills built here" line naming its C-numbers. That is one
  line per page and it makes the master list verifiable rather than aspirational.
- `gen_reading/class_overview.md` loses its collapsed four-bullet block and links to the syllabus.
  Three lists on one site is a defect regardless of what they say.

---

## 2. Does precision need to be on the ABET list?

**Yes — and it already is, inside M1. It does not need an outcome of its own.**

The instructor's two comments frame this:

> "we need to add precision to the course, but precision in hovering is not the concept. The concept
> is precision in measurements — a general concept, not specific to drones, but to any measurement."

> (on accuracy/precision/resolution vs. accuracy/resolution/uncertainty) "need all of these"

All four terms are wanted. The thing to avoid is treating them as four parallel items and giving
each one an outcome, which is how the list got to thirteen the first time. They are not parallel:

| Term | What it actually is | Where it belongs |
|---|---|---|
| **Accuracy** | How close a measurement is to the true value — systematic error | M1 |
| **Precision** | How closely repeated measurements agree with each other — random error | M1 |
| **Resolution** | The smallest difference the instrument or the data can show — a property of the tool, not of the result | M1 |
| **Uncertainty** | The range you attach to the number you report; it combines the three above | M3 |

Accuracy and precision are a matched pair — the two halves of error — and teaching either without
the other is what makes students conflate them. Resolution is the instrument property that limits
both, and on this course it has a concrete face in ground sample distance. Those three are one
assessable idea: *tell these apart and know where error comes from.* That is M1, one verb.

Uncertainty is different in kind. It is not a concept to distinguish; it is something you are
required to **do** — report a number with a range on it. So it sits in M3, where the verb is
"report", and it is assessed by whether the student actually did it.

So the ABET list carries all four terms across two outcomes, and stays at four outcomes. A fifth
outcome for precision would be a vocabulary item promoted to accreditation evidence, which is what
made old #13 ("Fundamental surveying concepts") indefensible.

**The real problem with old #6 was never its wording.** It said "explain the difference between
accuracy and precision" and nothing on the site taught it — precision appears only as a flying
adjective in Lab 0 and as marketing copy elsewhere. Keeping precision in M1 is only honest once §3
exists. The two items travel together.

**Also required, and cheap:** rename "precision hovering" and "precision landing" in
`labs/0_intro_to_flying.md` — three occurrences — to "controlled hovering" and "controlled landing".
A freshman meets the word in week 2 attached to holding a hover steady, and is asked in week 5 to
use it in a metrology sense. Nothing currently tells them these are different words.

---

## 3. The measurement fundamentals reading

Agreed by the instructor, tied to the ABET fundamentals. The instructor also raised placement:

> "as this is the base of the course, maybe it should be first or at a higher level as it is an
> overriding concept, not a specific activity."

### Proposed placement

Keep the file at `docs/gen_reading/measurement_fundamentals.md` — it is a reading, and `gen_reading/`
is where readings live — but give it a **top-level nav entry directly under Home**, not a slot inside
Readings:

```yaml
nav:
  - Home: index.md
  - Measurement Fundamentals: gen_reading/measurement_fundamentals.md
  - Class Resources:
      ...
  - Readings:
      ...
```

Nav nesting does not change a page's URL in MkDocs, so this costs nothing and breaks no Learning
Suite link. It puts the spine of the course second in the left-hand nav, above everything else,
which is what "higher level, an overriding concept" means in a sidebar. If the Topic relabelling in
§4 goes ahead, this entry sits above Topic 1 and is deliberately not numbered — it is not a week.

### Outline

Sized for one pre-class reading with a quiz behind it. Follows the house page structure: `# Title`,
`!!! abstract "Key Takeaways"`, `---` separators, `##` sections.

1. **What a measurement is** — a number, a unit, and a range. Why the range is not optional.
2. **Accuracy, precision, resolution** — the three-panel target figure, then the same three ideas on
   a parking-lot dimension so it is not only an abstraction. Explicitly: accuracy is systematic,
   precision is random, resolution is the instrument.
3. **Where the error comes from** — the instrument, the method, the operator, the reference.
4. **Uncertainty: the number you actually report** — combining the above into a range, and why
   "42.7 m ± 0.3 m" is a stronger answer than "42.7 m".
5. **How much accuracy does this decision need?** — a table from "is there a boulder in this field"
   (metres) to "has this beam settled" (millimetres).
6. **What it costs to buy more** — pacing, tape, Google Maps, drone, drone with ground control,
   total station. Home for the existing `w01_overview_accuracy_effort.svg`.
7. **Reporting a number honestly** — significant figures; never quote more digits than you can
   defend.
8. **Checking against ground truth.**
9. **Check Your Understanding**, collapsible answers, matching `flight_basics.md`.

Sections 5 and 6 are the "when do you need more precision, when is less fine" question. Sections 2
and 3 are M1; sections 4, 7 and 8 are M3; sections 5 and 6 are M2. The page will say so, so the
outcome-to-evidence trail is visible rather than asserted.

Figures needed (all new, `fig_tools/`, prefix to be decided with the Topic numbering in §4):

- Three-panel target: accurate/imprecise, precise/inaccurate, both, plus a fourth panel showing
  resolution as grid coarseness.
- The error-source diagram for section 3.
- The accuracy-need ladder for section 5 — a table may be enough; a figure is better.

---

## 4. Topic labels in the nav

**Superseded 2026-09-04.** The instructor later chose to organize the nav by week rather than restore
Topic labels; `planning/reorg_plan.md` is the plan that was executed. Every "Topic N" reference
became a week reference and the two SVGs were regenerated. The Learning Suite screenshots are no
longer needed. The text below is kept for the record.

The instructor chose option (a): restore Topic labels rather than strip "Topic N" from prose, and
will supply screenshots of the Learning Suite schedule and assignment pages.

**This is blocked until those screenshots arrive**, and deliberately so — the whole point of option
(a) is that the nav matches what Learning Suite tells students, and I cannot guess that.

Sequence once they do:

1. Build a Topic ↔ nav-section mapping table from the Learning Suite schedule, and put it in this
   file so it does not live only in a screenshot.
2. Relabel the nav sections as `Topic N — Name`. Labels only; no file moves, so no URL changes and
   no broken Learning Suite links.
3. Walk the thirteen prose references and confirm each now resolves. They are enumerated in the
   review file §B2.
4. Regenerate the two SVGs that have "Topic N" baked into their text —
   `w01_fig16_rules.svg` ("Topic 5 covers the full set.") and `w01_products_family.svg` ("covered in
   Topic 6"). These are `fig_tools/` regenerations, not text edits.
5. Re-run `mkdocs build --strict`.

**If the screenshots show Learning Suite speaks in weeks rather than topics**, the same procedure
applies with week labels, and the prose references become "Week N". Worth knowing before step 1
rather than after step 4.

---

## 5. The seven Part 107 figures

The instructor prefers all seven drawn rather than the five weaker captions deleted. All go in
`docs/part_107_license/images/` with the `w05_` prefix, generated from `fig_tools/`, in house style.

| Fig | Caption on the page | Proposed drawing |
|---|---|---|
| 15 | Waiverable vs. non-waiverable Part 107 provisions | Two columns, waiverable on the left and non-waiverable on the right, each rule as a labelled chip. The visual point is that the right column is short and absolute. |
| 16 | Annotated METAR example | **The most valuable of the seven.** One real METAR string across the top, each group leader-lined down to a plain-English label: station, time, wind, visibility, sky, temp/dewpoint, altimeter. |
| 19 | Density altitude effects | Two aircraft side by side at the same pressure altitude, one cold day, one hot-and-high, with rotor performance and takeoff roll called out. The exam tests the *consequence*, so the drawing should show the consequence. |
| 20 | CG envelope | A load envelope box with a correctly loaded point inside and two failure points outside — nose-heavy and tail-heavy — annotated with what the aircraft does in each case. |
| 24 | Hazardous attitudes and antidotes | Five paired cards: attitude on the left, antidote on the right. This is pure recall on the exam and pairs are exactly what a figure does better than prose. |
| 25 | 24-month currency cycle | A horizontal timeline: certificate issued → 24-month recurrent training → repeat, with what lapses and what does not marked on it. |
| 27 | Remote ID broadcast contents | The aircraft at the centre with the broadcast fields radiating out: ID, position, altitude, velocity, control-station position, timestamp, emergency status. Standard vs. broadcast-module differences in the subtitle. |

**On the numbering gaps.** Figures 2, 5, 6, 8, 9, 17, 18 and 21 are unused on that page, so the
sequence will still have holes after these seven land. Recommendation: **leave the gaps.** Closing
them means renumbering every caption, every file name and every number drawn inside every figure on
the page, for a cosmetic gain a student will never notice. If you would rather close them, it is one
pass and worth doing in the same sitting as the Topic relabel, not separately.

---

## 6. Duplicates, placeholders, and dead pages

All instructor-approved; none of these needs further input. This is the cheapest phase and the one
that stops the site showing students something broken.

**`software/qgis_measurements COPY.md`** — fold its three unique items into
`software/qgis_measurements.md`, then delete the file and its nav line:

1. Confirming the CRS is *projected* — real-world units, not degrees. This is the single most common
   reason a student's area comes out wrong, and it belongs in the existing "CRS Crash Course" note.
2. Digitizing features to a vector layer, for work that gets reused.
3. Cut/fill volume estimation from a DEM/DSM.

**`labs/example.md`** — merge into `labs/1_flight_checklist.md`, then delete the file and its nav
line. What is worth keeping: the emergency checklist, and the "weak checklist items" critique
exercise, which Lab 1 has no equivalent of and which is the better teaching of the two pages. The
numbered `## 1.` headings do not survive the merge; Lab 1's house structure wins.

**`class_resources/grading_policy.md`** — flip line 34 of `mkdocs.yml` back to a comment. The
instructor's note was "revert it out, this was meant as an example". The syllabus stays the single
source for grading; if anything on the page is worth keeping, it goes into the syllabus, not back
into the nav.

**The three placeholder labs** — `labs/4_rock_canyon_flight.md`, `labs/5_data_processing.md`,
`labs/6_part_107_studying.md`. Each is one line referencing `../images/logo_with_coming_soon.png`.
That path is **not** broken — an earlier note in this file said it was, wrongly; MkDocs rewrites it
correctly and the strict build always passed. What the pages actually render as is an untitled
1.8 MB logo with no heading and no indication of what the lab is for. The instructor wants a
coming-soon marker rather than removal from the nav, so each gets:

```markdown
# Lab N: <Title>

!!! note "Coming soon"
    This lab is being written. It covers <one sentence from the syllabus schedule>.

![Coming soon](../images/logo_with_coming_soon.png)
```

with the image path corrected. A titled page with an honest note is a very different thing from a
broken image, and it costs three small edits. TAs are writing the real content.

**`coming_soon.md`** — leave, per the instructor.

---

## 7. The Lab 2 orthophoto link

`labs/2_measurements_and_methods.md` sends students to a SharePoint download for the orthophoto the
whole lab depends on. The instructor asked for mitigations. Three failure modes, in the order they
actually bite:

1. **The share expires or was never set class-wide.** A link shared to named people works for the
   person who tested it and nobody else — the classic version of this failure, and it surfaces
   twenty minutes into lab.
2. **It lives in a personal OneDrive.** That share dies with the account. Every TA turnover is a
   chance to lose it.
3. **BYU sign-in friction** for a student on a personal laptop mid-lab.

Recommended, in order:

- **Mirror the file into the Learning Suite content area and make Learning Suite the link the lab
  page points at.** The class already lives there, authentication is already solved, and it does not
  depend on one person's storage. This is the real fix.
- **Move the SharePoint copy off personal OneDrive** into a class- or department-owned Team, shared
  to the whole class with no expiry, and keep it as the fallback.
- **Name the file on the lab page**, not just the link, so a TA can re-share it when a link rots.
- **Have a TA open the link from a student account** before the lab each semester. One minute,
  catches every one of the three failures above.

Committing a copy into the repository is the one option I would not take: an orthomosaic at a
resolution students can actually measure on is far too large for the repo, and a version reduced
enough to commit would undercut the point of the lab.

---

## 8. Deferred by the instructor

Recorded so they are not silently dropped. All are in `backlog.md`; none is being worked.

| Item | Instructor's note |
|---|---|
| Published answer keys (review C3) | Leave for now |
| Final project draft banners and 19 "decision needed" boxes (C5) | Leave for now; project still in progress |
| Lab 3's missing back half (C2) | In progress elsewhere |
| Labs 4, 5, 6 (C1) | TAs are writing them |
| TA bios and grading table (C8) | Leave for now |
| Image attribution, raw `<img>` conversion, placeholder replacement | Leave for now |
| `coming_soon.md`, `mkdocs_thermal_page.html`, C8 smalls | Leave for now |
| FE-style surveying and basic trig review | Needed, but where it fits in the semester is undecided |
| AI-use policy for the final report | Collect suggestions with the rest of the project decisions |

---

## 9. Suggested order of work

Reordered from the review's phases to reflect what the instructor deferred and what is blocked.

**Sprint 1 — complete, 2026-09-04.** All nine steps done; see the Done section of `backlog.md` for
what changed. Strict build clean.

1. ~~Fix `site_url` in `mkdocs.yml`.~~
2. ~~Fix the three placeholder lab pages.~~ (§6)
3. ~~Revert `grading_policy.md` out of the nav.~~ (§6)
4. ~~Merge and delete `qgis_measurements COPY.md`.~~ (§6)
5. ~~Merge and delete `labs/example.md`.~~ (§6)
6. ~~Add "Before this lab, read" blocks to all seven labs and "Where this is used" sections to the
   readings.~~ (review §B1)
7. ~~Link Lab 2 to the QGIS page and reconcile the measure-tool discrepancy.~~
8. ~~Move `metadata.md` under Software in the nav.~~
9. ~~`mkdocs build --strict`.~~

**What Sprint 1 turned up.** Filling in the lab-to-reading table found the gap the instructor
expected it to: `lidar.md`, `thermal.md` and `multispectral.md` are the only three readings with no
lab and no assignment behind them. They are the only readings that got no "Where this is used"
section, because there was nothing true to put in one. Tracked in `backlog.md`.

**Sprint 2 — needs sign-off on §1–§3, then it is mine.**

10. Write the Tier 1 and Tier 2 lists into the syllabus and a new `course_skills.md`; point
    `class_overview.md` at the syllabus.
11. Write `gen_reading/measurement_fundamentals.md` and its figures; place it top-level in the nav.
12. Wire it into Lab 2, and add the "Skills built here" lines across labs and readings.
13. ~~Rename "precision hovering/landing" in Lab 0.~~ Done 2026-09-04 as part of the reorganization.

**Sprint 3 — superseded by the site reorganization by week, done 2026-09-04.** See
`planning/reorg_plan.md`.

14. ~~Topic labels in the nav; verify the thirteen prose references; regenerate the two SVGs.~~
    Converted to week references instead.
15. ~~Reorder the nav to match class progression.~~ The nav is now the class progression.

**Sprint 4 — figures.**

16. The seven Part 107 drawings. (§5)

---

## 10. What I need from you

1. ~~**The Learning Suite screenshots.**~~ No longer needed; the nav follows the syllabus schedule.
   Instead: **review `review/WEEK3_LAB_OUTLINE.md`** so the Week 3 lab can be written.
2. **A name for Tier 2.** Recommendation: "Course Skills". (§1)
3. **Sign-off on M1–M4 as reworded** and on the thirteen Tier 2 skills. (§1)
4. **Sign-off on the measurement reading sitting top-level in the nav,** directly under Home. (§3)
   Under the week nav this means Start Here **plus** Week 5; the Week 5 line is already commented in.
5. **Where the Lab 2 orthophoto should live** — is mirroring it into Learning Suite workable? (§7)

Sprint 1 does not wait on any of these and can start immediately.
