# Part 107 Studying Lab — Answers

**Try the lab first.** These are the answers for Parts 1–3 of the
[Part 107 Studying Lab](6_part_107_studying.md), with the source for each and a short explanation.
Part 4 has no fixed answer because the weather changes; the section below says how to judge your
decode. Part 5 is your own plan.

Everything here was checked against the source named in October 2026. If a link or page number has
moved, the source is still the thing to find.

---

## Part 1 — Resource Scavenger Hunt

| # | Resource | Answer | Where it is |
|---|---|---|---|
| 1 | Testing supplement (course PDF) | **PDF page 13** | Appendix 1, "Legend 1 — Sectional Aeronautical Chart". Pages 14–31 are the Chart Supplement legends, not the sectional legend |
| 2 | Supplement Figure 26, area 2 | **Cooperstown (S32)** | PDF page 59; the airport data block reads "COOPERSTOWN (S32) AWOS-3 118.75 1424 \*L 35 122.9" |
| 3 | Supplement Figure 12 | **KMDW** (Chicago Midway) | PDF page 46. Its line begins `SPECI KMDW 121856Z` and carries `RA` (rain). KJFK is also a SPECI, but with `FG` (fog), not rain |
| 4 | AC 107-2A | **Chapter 8**, Small Unmanned Aircraft Over People | §8.9 "Declarations of Compliance" (printed page 8-20); the term is defined in §4.2.4 and appears throughout chapter 8 |
| 5 | 14 CFR §107.51 | **87 knots** (100 mph) groundspeed | §107.51(a) |
| 6 | 14 CFR §107.9 | **10 calendar days** | §107.9, "Safety event reporting": serious injury, loss of consciousness, or property damage over $500 |
| 7 | PHAK chapter 15 | **Class A** | Chapter 15 PDF, page 15-2: "Class A airspace is generally the airspace from 18,000 feet mean sea level (MSL) up to and including flight level (FL) 600" |
| 8 | FAA LAANC page | Any of the providers listed as offering public service — in October 2026: **Airspace Link, Aloft, AstraUTM, AutoPylot, Avision, Flightloop, UASidekick, Wing** | faa.gov/uas/getting_started/laanc, "UAS Service Suppliers". The list changes; what matters is that the student found it |
| 9 | PSI site | **Exam Resources → Unmanned Aircraft Systems → UAG** (Sample Test) | faa.psiexams.com; "Exam Resources" is in the top menu of the landing page and does not need a login |
| 10 | FAA UAG sample-question PDF | **46 questions; no answer key** | The PDF is eleven pages, numbered 1–46, with an ACS code after each question and no key anywhere. The Week 9 slides work ten of them; this lab works four more |

---

## Part 2 — Reading a Figure Question

Each answer is followed by the reasoning the student's "why" sentence should contain.

**FAA sample question 9 (TA demonstration) — C. Unmarked balloon on a cable up to 3,008 feet MSL.**
Figure 20, area 3, is Elizabeth City Regional (ECG) in the lower centre of the chart. Just southeast
of the airport, exactly where the question puts you, is a boxed caution: "CAUTION: UNMARKED BALLOON
ON CABLE TO 3008′ MSL. CHECK NOTAMS." The box says MSL, so B is the units trap (step 5 of the
method). A is wrong because the "high density military operations" caution on this chart is the
one by Oceana and Fentress, up near area 6, not here. A tethered balloon on a cable to 3,000 ft is a
real hazard for any aircraft below it, which is why the chart tells you to check NOTAMs before
flying there.

**FAA sample question 24 — C. Garrison Airport.** Figure 21. The **48°** latitude line runs across
the middle of the chart and the **101°** longitude line runs down its centre. 47°40′N is 20 minutes
*south* of the 48° line (count twenty small ticks down the 101° line, or use the scale: 20 nautical
miles). 101°26′W is 26 minutes *west* of the 101° line, to the left. That point lands on the
magenta airport with the brown ring, labelled GARRISON (D05), beside Audubon Lake. Mercer County
Regional is much further south, near the bottom-left corner (about 47°20′N), and Semchenko is
northeast of Garrison, east of the 101° line.

**FAA sample question 26 — A. 180° true at 4 knots.** Figure 12, the last line: `SPECI KJFK
121853Z 18004KT ...`. The wind group `18004KT` is the direction the wind blows *from* (180°) and the
speed (04 knots). Wind in a METAR or TAF is always a **true** direction, which rules out B; winds
given by a tower or ATIS over the radio are magnetic. C reads the group backwards.

**FAA sample question 31 — B. The degrees of latitude north and south of the equator.** Figure 26,
area 4, sits on the thick line labelled **47°** that runs east–west across the chart just above
Jamestown. A line of latitude measures how far north or south of the equator you are. A and C
describe *longitude*, which is measured east and west of the Prime Meridian — the line through
Greenwich, England (A and C are the same wrong answer worded twice). This question is pure
definition, but it is on the test, and it is the kind of question a student loses by not reading
all three choices.

---

## Part 3 — Look-It-Up Race

A right answer with no source scores half. The source column is what the race is for.

| # | Question | Answer | Source |
|---|---|---|---|
| 1 | Minimum flight visibility | **3 statute miles**, as seen from the control station | 14 CFR §107.51(c) |
| 2 | Distance from clouds | **500 ft below** and **2,000 ft horizontally** | 14 CFR §107.51(d) |
| 3 | Hours after alcohol | **8 hours**; also no flying under the influence or at 0.04 or more | 14 CFR §107.27, which applies §91.17(a) to remote pilots; AC 107-2A §5.16 |
| 4 | Declaration of Compliance | The **applicant** — whoever designs, produces or modifies the aircraft, in practice the **manufacturer**; it makes an aircraft eligible for **Category 2 or 3** operations over people. The remote pilot checks the label | AC 107-2A chapter 8, §8.9 (page 8-20) and §4.2.4; 14 CFR §107.155 and following |
| 5 | Standard Remote ID stops broadcasting | **Land as soon as practicable** | 14 CFR §89.110(a)(2) (broadcast module: §89.115(a)); AC 107-2A §5.17 |
| 6 | Airspace needing prior ATC authorization | **Class B, C, D, and the surface area of Class E designated for an airport.** Obtained through LAANC or FAA DroneZone | 14 CFR §107.41; AC 107-2A §5.10 |
| 7 | Recurrent training | Within the **previous 24 calendar months** (initial test or recurrent training) | 14 CFR §107.65; AC 107-2A chapter 6 |
| 8 | Waiver for flight over people | **Yes.** §107.39 (operation over people) is on the list of waivable sections | 14 CFR §107.205(g); the full list is §107.205(a)–(j) |
| 9 | Registration exemption under 0.55 lb | Only when the aircraft is flown **exclusively as a recreational aircraft** (49 U.S.C. 44809) and weighs 0.55 lb or less. **Every Part 107 aircraft is registered**, whatever it weighs | 14 CFR §48.15(b); §107.13 |
| 10 | Stadium on game day | No drones within **3 nautical miles** and up to **3,000 ft AGL** of the stadium from **one hour before** to **one hour after** the game (stadiums seating 30,000 or more; NCAA Division I football counts, and LaVell Edwards Stadium qualifies) | FAA stadium page, faa.gov/uas/getting_started/where_can_i_fly/airspace_restrictions/sports_stadiums (3 NM and the one-hour window are stated there); the standing NOTAM **FDC 0/0367** as cited in [The Part 107 Exam §IV.E](../part_107_license/faa_exam_planning_and_overview.md#e-temporary-flight-restrictions-stadiums-and-game-day); 14 CFR §107.47 |

A note on question 10: the FAA page gives the rule but not the NOTAM number in its visible text.
Either citation earns full credit; what does not is "I heard you can't fly near the stadium."

---

## Part 4 — Today's Real Weather

There is no fixed answer; the METAR is different every hour. Judge a pair's decode on these points.

**The decode.** Each group must be read as the code means it, not as a guess. Using the morning
sample from the lab page, `METAR KPVU 271356Z 12003KT 10SM CLR 05/02 A3008 RMK AO2 SLP173 T00500022`:

| Group | Meaning |
|---|---|
| `METAR KPVU` | Routine report (not a SPECI) for Provo Municipal |
| `271356Z` | 27th of the month, 13:56 UTC — 07:56 MDT (UTC−6) or 06:56 MST (UTC−7). The common error is to forget the conversion, or to use the wrong one for the season |
| `12003KT` | Wind from 120° **true** at 3 knots |
| `10SM` | Visibility 10 statute miles (the station reports "10+" as 10) |
| *(no present weather group)* | Nothing falling or obscuring |
| `CLR` | No clouds below 12,000 ft (automated station); no ceiling |
| `05/02` | Temperature 5 °C, dew point 2 °C. Close together means fog is possible if it cools |
| `A3008` | Altimeter 30.08 inches of mercury |
| `RMK AO2 SLP173 T00500022` | Remarks: automated station with a precipitation sensor; sea-level pressure 1017.3 mb; temperature 5.0 °C and dew point 2.2 °C to a tenth |

**The go / no-go.** The decision itself is not graded; the reasoning is. A sound answer checks all
of these and gives the number that decided it:

- **Visibility ≥ 3 SM** (§107.51(c)). Ten miles passes; `1 1/2SM` does not.
- **Ceiling and cloud clearance** (§107.51(d)). The ceiling is the lowest BKN or OVC layer. A 400 ft
  flight needs it at or above 900 ft AGL; a lower ceiling is not a no-go by itself, it caps the
  altitude at ceiling minus 500 ft. `CLR`, `FEW` and `SCT` are not ceilings. A pair that writes
  "OVC007, so no-go" has it right; a pair that writes "SCT015, so no-go" has treated a scattered layer
  as a ceiling.
- **Wind** against the aircraft limit the TA gave, remembering knots and that gusts (`G`) count.
- **TFRs** at tfr.faa.gov. Usually none over Provo; on a home football game day the stadium
  restriction applies for about five hours.
- **Airspace.** KPVU is Class D, so a real flight anywhere on campus needs a LAANC authorization
  (§107.41) — a legal weather report is necessary but not sufficient. The best answers say "GO on
  weather, pending LAANC."

The reflection question asks what single change would flip the decision. Good answers are specific:
"a BKN008 layer would cap us at 300 ft," "a gust over N knots," "a TFR."

---

## Part 5 — My Study Plan

No answer. The check is whether every day names a resource the student could open right now
(a chapter, a figure range, a named video), with real dates, and whether the two weakest areas got
the extra days.
