# Flight Basics

!!! abstract "Key Takeaways"
    - **A drone is a flying sensor platform.** For engineering work, the camera, the satellite
      receiver, and the gimbal decide the quality of your data. Everything else exists to hold
      them steady in the air.
    - **Four rotors, two spinning each way.** Speeding some up and slowing others produces every
      motion the aircraft can make.
    - **Left stick controls altitude and heading. Right stick moves the aircraft.** Both are
      relative to the nose of the drone, not to where you are standing.
    - **Return to Home is the safety net.** Know what triggers it, and where "home" is, before
      you take off.

!!! note "Not every drone is the same"
    This page describes controls and features that are common across small drones. Inexpensive
    models may have no satellite positioning, no obstacle sensors, and no gimbal. Professional
    aircraft add interchangeable sensors and redundant systems. **Only the two control sticks work
    the same way on nearly every aircraft.** Button names, switch positions, and screens vary from
    model to model, so always check the manual for the drone you are actually flying.
    [Which Features Does Your Drone Have?](#which-features-does-your-drone-have) sets out what to
    expect from each class of aircraft.

---

## Parts of the Aircraft

![Parts of a quadcopter](images/w01_fig01_aircraft_parts.svg){ width="100%" }

*Figure 1: The main parts of a small quadcopter, seen from above. Propellers on opposite corners
spin the same direction, which is what lets the aircraft turn without tipping.*

| Part | What it does | What happens when it fails |
|------|--------------|----------------------------|
| Propellers | Push air downward to create lift | A chipped or bent blade causes vibration, which blurs photos and shortens flight time |
| Motors | Spin the propellers; changing their speeds steers the aircraft | The aircraft cannot hold a level hover |
| Battery | Powers everything, and usually sets the limit on flight time | Sudden power loss, or a forced landing somewhere you did not choose |
| Camera and gimbal | Collect the data; the gimbal holds the camera steady and level | Tilted horizons and motion blur, which make measurements unusable |
| Satellite receiver and compass | Tell the aircraft where it is and which way it is facing | The aircraft drifts, or flies the wrong direction during Return to Home |
| Obstacle sensors | Detect objects in the flight path and stop or steer around them | Collisions with obstacles the pilot did not notice |
| Status light | Reports what the aircraft is doing: ready, waiting, or in an error state | You take off before the drone is actually ready |

!!! tip "Which parts decide your data quality"
    Three parts do most of the work for engineering measurements. The **camera** sets how much
    detail you capture, the **gimbal** keeps that detail sharp and level, and the **satellite
    receiver** records where each photo was taken. Everything else exists to hold those three
    steady in the air.

---

## Cameras, Sensors, and Payloads

For engineering work the sensor **is** the instrument, and the aircraft is the tripod that carries
it. On most small drones the camera is fixed in place and the whole airframe is built around it.
Larger professional aircraft take **interchangeable payloads**, so one aircraft can carry whichever
sensor the job needs.

![Sensors a drone can carry](images/w01_fig03_payloads.svg){ width="100%" }

*Figure 3: Common drone payloads. Which one you need depends entirely on what you are trying to
measure.*

| Payload | Answers the question | Reading |
|---------|----------------------|------------|
| Standard camera | What does the site look like, and what are its dimensions? | [Aerial Measurement Products](data_products.md) and [How Photos Become 3D](sfm_workflow.md) |
| Thermal | Where is heat escaping, or where is moisture trapped? | [Thermal Imaging](thermal.md) |
| Multispectral | How healthy is the vegetation, and where is bare ground? | [Multispectral Imaging](multispectral.md) |
| LiDAR | What is the ground surface underneath the trees? | [LiDAR](lidar.md) |
| Gas detector | Is there a leak, and where is it coming from? | not covered in this course |

Other payloads exist for specific jobs, including speakers, spotlights, and release mechanisms for
delivering small loads.

!!! tip "Choosing a payload is an engineering decision"
    Every step up in capability costs money, weight, flight time, and processing effort. A standard
    camera answers most civil engineering questions perfectly well. Reach for thermal,
    multispectral, or LiDAR when the question genuinely requires it, and be ready to explain why it
    did.

---

## How a Drone Flies

A drone has no wings, no rudder, and nothing that steers. It has four propellers that only spin
faster or slower. Everything the aircraft does comes from that one control.

![Pitch, roll, and yaw](images/w01_fig04_axes.svg){ width="100%" }

*Figure 4: The three rotations. Every flight path is some combination of these, plus climbing and
descending.*

### Staying in the air

Propellers push air downward, and the air pushes back. That upward push is **lift**. Whether the
aircraft rises, holds still, or sinks depends only on how lift compares with the weight of the
aircraft.

![Lift compared with weight](images/w01_fig05_lift_and_weight.svg){ width="100%" }

*Figure 5: Lift greater than weight means climbing, lift equal to weight means hovering, and lift
less than weight means descending.*

### Steering without a rudder

To move in any direction, the flight controller speeds some rotors up and slows others down. You
never do this yourself; you move a stick, and the aircraft works out the rotor speeds hundreds of
times a second.

![Which motors speed up for each movement](images/w01_fig06_differential_thrust.svg){ width="100%" }

*Figure 6: Speeding up the rear pair tips the nose down and the aircraft moves forward. Speeding up
one diagonal pair turns it. Speeding up all four makes it climb.*

!!! note "Why the propellers spin in opposite directions"
    A spinning propeller tries to twist the aircraft the opposite way. Two propellers turn one
    direction and two turn the other, so in a steady hover those twists cancel out. Speeding up one
    diagonal pair unbalances them on purpose, and the aircraft yaws. This is also why a propeller
    fitted in the wrong position will not fly.

!!! warning "Everything costs battery"
    Fighting wind, climbing, and flying fast all mean running the motors harder. A drone in a stiff
    breeze can use its battery far faster than the remaining-time estimate suggests, because that
    estimate assumes calm conditions.

---

## The Controller

![A typical drone controller](images/w01_fig07_controller.svg){ width="100%" }

*Figure 7: A typical controller. The two sticks work the same way on nearly every aircraft. Buttons
and switches are named differently from one manufacturer to the next.*

| Control | What it does | Also called |
|---------|--------------|-------------|
| Left stick | Climbs, descends, and turns the nose left or right | Throttle and yaw |
| Right stick | Moves the aircraft forward, back, left, and right | Pitch and roll |
| Power button | Turns the controller on and shows its battery level | — |
| Return to Home | Pauses the flight, or sends the aircraft back to where it took off | RTH, Home, or the house symbol |
| Flight mode switch | Changes the speed limit and how much the aircraft helps you | Cine / Normal / Sport, or Beginner / Normal |
| Gimbal tilt dial | Tilts the camera up and down during flight | Gimbal wheel, camera dial |
| Shutter and record | Takes a photo, or starts and stops video | — |
| Antennas | Carry the radio link to the aircraft; point the flat face toward the drone | — |

!!! note "Phone or built-in screen"
    Some controllers clamp your phone and run the flight app on it. Others have a screen built in
    and need no phone at all. The sticks and buttons work the same way in both cases; only the
    display is different.

---

## Stick Controls

Nearly every ready-to-fly drone uses the **Mode 2** layout. The left stick handles altitude and
heading, and the right stick moves the aircraft over the ground. Both sticks spring back to center
when you let go, and the aircraft simply holds position.

![What each stick does](images/w01_fig08_stick_controls.svg){ width="100%" }

*Figure 8: The eight stick inputs. In each panel the dark stick is the one you move; the pale one
stays where it is.*

!!! warning "The nose decides left and right, not you"
    Stick directions are relative to the **nose of the aircraft**, not to where you are standing.
    While the drone flies away from you, its left matches your left. Turn it around to face you and
    everything reverses: pushing right sends it to your left. This single fact causes more beginner
    crashes than anything else.

![Flying away from you compared with flying toward you](images/w01_fig09_nose_in.svg){ width="100%" }

*Figure 9: The same stick input gives opposite results depending on which way the nose points.*

!!! tip "Two habits that prevent most crashes"
    Keep the nose pointed away from you while you are learning, and use small stick movements. The
    controls are far more sensitive than they look, and a gentle push is almost always enough.

!!! note "The flight mode changes how the sticks feel"
    Many drones have two or three flight modes, commonly labeled **Cine**, **Normal**, and
    **Sport**, though some manufacturers use names such as Beginner and Normal instead. The same
    stick movement produces a different result in each one:

    - **Cine** slows everything down and softens the response, for smooth video.
    - **Normal** is the everyday setting and what you will use for most measurement flights.
    - **Sport** raises the speed limit and makes the aircraft respond sharply. On many models it
      also **turns obstacle sensing off** and lengthens the braking distance.

    Check which mode the switch is in before you take off. More on this in
    [Automated Flight Functions](#automated-flight-functions) below.

---

## A Basic Flight, Start to Finish

Every flight follows the same nine steps, whether it is a two-minute check or a full survey. Run
them in the same order every time, especially on the flights that feel routine.

![The nine steps of a flight](images/w01_fig10_flight_sequence.svg){ width="100%" }

*Figure 10: A flight from start to finish. The three phases are setting up on the ground, starting
up and checking, then flying and packing away.*

!!! note "Why the power order matters"
    Turn the **controller on first and off last**. If the aircraft is powered while the controller
    is not, it has nothing to listen to. Depending on the model it may sit there refusing to arm,
    or it may start a Return to Home you did not ask for.

If something does not behave the way you expect at any point in that sequence,
[Common Flight Issues](flight_issues.md) lists the usual causes.

The detailed item-by-item lists live on the checklist pages:
[Pre-Flight](../class_resources/flight_check_list/pre_flight/pre_general.md) and
[Post-Flight](../class_resources/flight_check_list/post_flight/post_general.md). Figure 10 is the shape of the
flight; the checklists are what you actually tick off.

### Your first flights

Before flying any real task, get comfortable with the controls somewhere open, well away from
people, cars, buildings, and trees. The box is the standard first exercise.

![The box practice pattern](images/w01_fig11_practice_pattern.svg){ width="100%" }

*Figure 11: Fly one side, stop in a hover at the corner, then fly the next side. Slow and
deliberate beats fast and smooth at this stage.*

Do not treat one lap as finished. Fly the box round several times, until the corners stop needing
thought. Then fly it the other way round, and then again with the nose turned to follow the
direction of travel. The pattern is the same each time; what changes is how much you have to think
about which stick to move. When several laps feel boring, you are ready to fly something useful.

!!! tip "Hover before you go anywhere"
    After take-off, hold a hover at about eye level for a few seconds and try a small input on each
    stick. You are checking that the aircraft responds the way you expect and is not drifting. If
    something feels wrong, land while the drone is still two meters away and at head height, not
    when it is a hundred meters out.

---

## Automated Flight Functions

A modern drone does a great deal for you. It holds position, avoids some obstacles, watches its own
battery, and will fly itself home. This automation is genuinely good, and it is also the most common
source of surprises, because each feature has limits that are not obvious until you meet them.

### Knowing where it is

The aircraft works out its position from satellites, and its heading from an internal compass. When
it powers up and gets a good fix it records a **home point**, the spot it will come back to.

![Holding position with and without satellites](images/w01_fig12_home_point.svg){ width="100%" }

*Figure 12: With satellites, the aircraft sits still on its own. Without them it drifts, and it is
entirely up to you to notice and correct.*

!!! warning "Steel and rebar confuse the compass"
    This matters on a construction site more than almost anywhere. Reinforcing bar, steel decking,
    vehicles, and buried services all distort the magnetic field. A compass calibrated while
    standing on rebar can send the aircraft flying confidently in the wrong direction. Calibrate on
    open ground, away from metal, and always wait for the home point confirmation before you take
    off.

### Seeing obstacles

Obstacle sensors look in fixed directions and are easily fooled. Treat them as a backstop that
occasionally saves you, never as permission to stop looking.

![Where the obstacle sensors look](images/w01_fig13_obstacle_coverage.svg){ width="100%" }

*Figure 13: Sensors watch some directions and not others, and there are things they cannot see even
when pointed straight at them.*

Sport mode turns obstacle sensing off entirely on many models, which is worth remembering before
you reach for it to cover ground faster.

### Watching the battery

As the battery drains, the aircraft takes decisions away from you, one step at a time.

![What happens as the battery drains](images/w01_fig14_battery_states.svg){ width="100%" }

*Figure 14: The thresholds vary by model, and the aircraft raises them the further away you are,
because it has further to fly back.*

### Return to Home

Three things start a Return to Home: **you press the button**, the **battery gets low**, or the
**controller signal is lost**. In all three cases the aircraft does the same thing.

![The Return to Home flight profile](images/w01_fig15_return_to_home.svg){ width="100%" }

*Figure 15: It climbs to a set altitude, flies a straight line home, then descends. It does not
steer around anything on the way.*

!!! warning "Return to Home flies straight, not smart"
    The aircraft will happily fly a straight line through a crane, a building, or a tree line. The
    only thing protecting it is the Return to Home altitude you set before take-off. Set it above
    the tallest obstacle on the site, and reset it when you move to a new site.

!!! tip "Automation is a backup, not a plan"
    Every one of these features can fail or be fooled. Fly so that losing all of them at once would
    be inconvenient rather than dangerous: stay within sight, stay clear of people and obstacles,
    and come back with battery to spare.

When one of them does misbehave, [Common Flight Issues](flight_issues.md) lists the usual causes
and what to do about each.

---

## Which Features Does Your Drone Have?

Almost everything on this page is standard on a mid-range consumer drone, absent from a cheap toy,
and extended on a professional aircraft. Before flying an unfamiliar model, find out which column
it sits in.

| Feature | Toy | Consumer | Professional |
|---------|-----|----------|--------------|
| Satellite positioning | rarely | yes | yes |
| Holds position with no input | no, it drifts constantly | yes | yes |
| Return to Home | no | yes | yes |
| Mechanical gimbal | no, digital stabilization only | usually | yes |
| Obstacle sensors | no | sometimes, often forward and down only | usually all round |
| Flight modes (Cine, Normal, Sport) | no | yes | yes |
| Interchangeable payloads | no | no | yes |
| Remote ID built in | no | yes on current models | yes |
| Redundant motors or batteries | no | no | often |

!!! note "Weight and capability are different questions"
    The sub-250 g aircraft used in this class are **consumer** drones despite their size. They have
    satellite positioning, a gimbal, and Return to Home. Being under 250 g changes what you must
    register, not what the aircraft can do. Do not assume a small drone is a toy, or that a heavy
    one is capable.

---

## Rules in One Screen

Flying is regulated, and the rules exist because a two-pound object falling from 300 feet is
dangerous. Three of them are easy to break without noticing.

![The rules that apply on every flight](images/w01_fig16_rules.svg){ width="100%" }

*Figure 16: Keep the aircraft in sight and below the altitude limit, and know the three things you
must never fly over or into.*

**The three you must never do**

- **Never over people** who are not part of your operation. Not a crowd, not a single bystander,
  not the rest of your crew standing across the site.
- **Never over moving traffic.** Roads, rail, and waterways in use are all excluded, and a stalled
  line of traffic can start moving while you are above it.
- **Never in airspace you are not authorized for.** Controlled airspace around airports, restricted
  areas, and temporary flight restrictions all exclude you unless you hold a specific
  authorization. Check before every flight, not once per site.

**The rest, in short**

- Keep the aircraft **within your own unaided sight** at all times. Binoculars and the camera view
  do not count.
- Stay at or below **400 ft (120 m) above the ground**.
- **Daylight only**, one aircraft at a time, and never from a moving vehicle.
- **Register the aircraft** if it weighs 250 g or more, and comply with **Remote ID**.
- Any flight connected to work, study, or business needs a **Part 107 Remote Pilot Certificate**.

!!! warning "Course work counts as a business purpose"
    Flying for a class project, research, or anything a client might pay for falls under Part 107,
    not the recreational rules, even when nobody is paying you. [Week 3](../weeks/week_03.md) covers
    the certificate and the exam in full.

[The FAA Part 107 Overview page covers all of this in detail](../part_107_license/faa_exam_planning_and_overview.md),
including airspace, weather, and the Part 107 exam itself.

---

## Check Your Understanding

**1. Name each numbered control.**

![Controller with numbered controls](images/w01_fig07b_controller_numbered.svg){ width="100%" }

??? note "Answers"
    1. Left stick
    2. Right stick
    3. Power button
    4. Battery level lights
    5. Return to Home and flight pause
    6. Flight mode switch
    7. Gimbal tilt dial
    8. Shutter and record button
    9. Antennas
    10. Phone holder or built-in screen
    11. Charging and data port

**2.** The drone is hovering with its nose pointed back at you. You push the right stick to the
right. Which way does the aircraft move, from where you are standing?

??? note "Answer"
    To **your left**. Stick directions are relative to the nose of the aircraft, and the nose is
    facing you, so the aircraft's right is your left.

**3.** To turn the aircraft to the right, which motors speed up, and why does it not tip over?

??? note "Answer"
    One **diagonal pair** speeds up, the pair that spins counter-clockwise. Because they are on
    opposite corners, the extra lift is balanced across the aircraft, so it stays level. What
    changes is the twisting force, and the aircraft rotates.

**4.** You lose the controller signal at 90 m altitude. There is a 100 m tree line between you and
the aircraft. What does the aircraft do, and what single setting decides whether it gets home?

??? note "Answer"
    Losing signal triggers **Return to Home**. The aircraft climbs to its Return to Home altitude,
    flies a straight line back, and descends. The setting that matters is that **Return to Home
    altitude**: if it is below the height of the tree line, the aircraft flies straight into it.

**5.** Why does it matter where you stand when the drone calibrates its compass on a construction
site?

??? note "Answer"
    Rebar, steel decking, vehicles, and buried services distort the magnetic field. A compass
    calibrated over them gives the aircraft a wrong idea of which way it is facing, which can send
    it flying the wrong direction, including during Return to Home.

**6.** Which parts of the aircraft matter most to the quality of an engineering measurement, and
why?

??? note "Answer"
    The **camera** sets how much detail each photo holds, the **gimbal** keeps that detail sharp
    and level, and the **satellite receiver** records where each photo was taken. Without all
    three, the images may look fine but cannot be turned into a defensible measurement.

---

## Resources

### Watch before class

<iframe width="560" height="315" src="https://www.youtube.com/embed/ccep1cKgb2M" title="Drone flight basics" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/euDo4vXLvkY" title="Flying a small drone" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/6_ucCKFJUCU?start=275" title="Safe drone flying zones" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Watch the third video until 14:32.

### Manuals and references

Every drone is different, and the manual is the only place with the right answer for the aircraft in
your hands.

- [DJI remote controller button functions](https://support.dji.com/help/content?customId=en-us03400006567&spaceId=34&re=US&lang=en){target="_blank"} — what each control does on the DJI controllers
- [Holy Stone manuals](https://www.firstquadcopter.com/drone-manuals/free-holy-stone-drone-manuals-pdf-download-guides-for-all-models/){target="_blank"} — PDFs for the Holy Stone models
- [FAA Remote Pilot Study Guide](https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/media/remote_pilot_study_guide.pdf){target="_blank"} — the official study guide behind the Part 107 pages (Weeks 3 and 9)

### Next steps

- [Pre-Flight Checklist](../class_resources/flight_check_list/pre_flight/pre_general.md) and
  [Post-Flight Checklist](../class_resources/flight_check_list/post_flight/post_general.md) — what to run through
  on site
- [FAA Part 107 Overview](../part_107_license/faa_exam_planning_and_overview.md) (Week 3) — the rules in full, and the
  certificate you will need
- [LiDAR](lidar.md), [Thermal Imaging](thermal.md) and [Multispectral Imaging](multispectral.md) (Week 8) — thermal, multispectral, and LiDAR payloads in detail

---

## Where this is used

[Week 2 lab — Intro to Flying](../labs/0_intro_to_flying.md) is where you fly for the first time, using
the controller and the orientation skills described above.
