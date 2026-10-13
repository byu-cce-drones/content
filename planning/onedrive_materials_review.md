# Class SharePoint materials review — 2026-10-13

A read-only review of the class SharePoint (synced locally as `CE Drone Class - Documents`) for
material that can improve the existing decks and readings or seed new ones. Three subagents covered
the six iTwin Capture Modeler projects, the raw image sets, and the documents and videos; the
products they missed were previewed afterwards. Nothing on SharePoint was changed.

This file is the durable, public-safe summary. It names no students. The full private notes, the
renders, the parsed data and the reusable scripts are in **`.claude/local/onedrive_review/`**
(git-ignored; see its `README.md`). Paths below starting `OR/` are relative to that folder.

**The DJI Terra quality report was not found.** No file or folder in the local mirror mentions Terra
or a Terra report, and nothing changed on the mirror in the last three weeks. It has probably not
synced to this machine, or it sits in a folder OneDrive is not syncing. Once it is local, review it
against the Week 7 deck: it is the natural companion to the Bentley quality-report slides below.

---

## The best finds

1. **Water tank flight (Rock Canyon, 2026-03-05): the instructor's "capture the sides" rule, flown
   by a class.** Mavic 3M, 95 nadir photos on a seven-line grid plus a dedicated line of ten at −45°.
   About 80 % forward and 60 % side overlap, 0.93 cm GSD at 34.5 m. All 105 photos calibrated,
   43,307 tie points, 0.54 px RMS. Finished products: a 3D mesh and a 1.2 cm orthophoto. Renders:
   camera-position plot, textured, shaded and wireframe mesh views, orthophoto.
2. **Two quality reports side by side.** The water tank is the good case. The tennis-court "3D"
   flight is the failure: only 47 of 89 photos calibrated, lost in alternating runs that look like
   every other flight line, yet its 0.59 px RMS looks fine. One chart shows tie points per photo for
   both (`OR/bentley/per_photo_tiepoints.png`), and Bentley's own acquisition report renders the lost
   photos with red flags (`OR/bentley/tennis3d/tennis3d_acquisition_report.png`).
3. **Our own NDVI.** The Mavic 3M flight over the lawn east of the Engineering Building (EB) has all
   four bands and a calibration-panel shot. A quick NDVI shows the irrigation dry spots cleanly
   (`OR/images/ndvi_EastEBGrass_0035.png`). Once it is reprocessed as calibrated reflectance, it
   replaces the two unlicensed NDVI images on the Multispectral page.
4. **Real thermal with real temperatures.** The Autel `.TIFF` files are radiometric. Renders show
   thermal shadows behind parked cars at the EB lot, reflected cold sky on car roofs (apparent is not
   actual temperature), and a crack network on the Carterville bridge approach slab, at a time of
   day too cold for a proper delamination survey.
5. **A gimbal mistake that ruined two flights.** Two student flights at Rock Canyon had the camera
   80–90° up from straight down, about 200 frames looking across houses at the horizon. The
   resulting orthophoto is all streaks and holes (`OR/products/greenbasin_ortho.png`). A strong
   "check the gimbal before you fly, and the EXIF before you process" lesson, shown without names.
6. **A second Rock Canyon DSM** from the same morning: a clean hillshade showing the tank, sheds and
   trees, with torn, webbed edges where coverage ends (`OR/products/rockcanyon_dsm_hillshade.png`). Its photo
   spacing gives only about 27 % forward overlap against about 80 % side, a lopsided plan that still
   produced a usable surface. That makes it a discussion slide, not a failure slide.
7. **Drone-specific checklists** for the Phantom 4 Multispectral and the Matrice 300 with MicaSense.
   They fill the "will be added" gap on both checklist pages after the research-lab specifics are
   stripped. They carry hard numbers the general list lacks: a 22 mph wind limit and return at 30 %.
8. **Setup and takedown videos** for the Anafi, Matrice, Phantom 4, Autel EVO and the minis, a
   before-during-after video, and two gridded-flight clips. Each is 1–4 GB, so they need Kaltura or
   unlisted YouTube hosting before any page can link them.
9. **Final project precedents from Winter 2026:** a client-memo report to Provo City about the Rock
   Canyon road (five headings), four teams of about three, and 10-minute presentations in the last
   Tuesday lecture.
10. **Our own LiDAR before and after vegetation removal** (CloudCompare cloth filter, from the 2023
    CE 594R sensors document). It is a civil-relevant DSM-versus-DTM example to replace the
    off-topic archaeology and forestry images on the LiDAR page.

---

## By week: what to add where

### Weeks 1–2: Welcome, Aerial Measurement Products

- **Replace the `w01_example_*` placeholders** on `gen_reading/data_products.md` with class
  products:

  | Placeholder | Real product available |
  |---|---|
  | Orthomosaic | Parking-lot orthophoto (UTM 12N, 1 cm) or the water-tank orthophoto |
  | DSM | Rock Canyon DSM hillshade and colour relief; Grass field DSM hillshade |
  | 3D model | Water-tank mesh, textured and wireframe |
  | Thermal | EB lot thermal (cars and thermal shadows) |
  | Index map | Mavic 3M NDVI, once calibrated |
  | DTM | LiDAR cloth-filter screenshots from the CE 594R document (permission needed) |
  | Point cloud, contours | Not on SharePoint. Contours can be generated from the Rock Canyon DSM with `gdal_contour` |

- **Welcome-page photo.** Three Mini 4 Pro photos from 2026-09-24 show the class outside the EB
  and the instructor beside a drone case. They fit the backlog item for
  `w01_overview_photo_placeholder.svg`, but every face is identifiable: consent first, EXIF stripped.
- **Application hooks.** A small reservoir dam and outlet (Box Lake), a road bridge (Carterville),
  and the Rock Canyon road memo give the applications lecture local civil examples.

### Weeks 2–4: labs and checklists

- Link the minis setup video and the "how to fly minis" video from the Week 2 and Week 3 labs once
  hosted. Confirm whether "minis" means DJI Minis or the Holy Stone HS210 first.
- Link the before-during-after video from the checklist index and the Week 4 checklist lab.
- Start `class_resources/flight_check_list/pre_flight/<aircraft>.md` pages from the P4M and M300
  checklists. Add their "pilot's check" block (rested, no hurry, no alcohol within 8 h, airframe
  inspected, LAANC, TFRs) to `pre_general.md`.

### Week 4: QGIS

- The parking-lot orthophoto in the SharePoint `General` folder is the same file as the Lab 2
  orthophoto. That partly answers "where should the Lab 2 orthophoto live": it already sits on the
  class SharePoint. A class-wide share link to that file would replace the personal one.

### Week 5: Measurement Fundamentals

- **Repeatable is not accurate.** The parking lot was aerotriangulated twice from the same 251
  photos: 101,142 and 101,147 tie points, both 0.61 px RMS. Very repeatable, and neither run has a
  single check point.
- **Precise with no scale at all.** The Grass field project used 26 screen grabs with no GPS. It
  solved to 0.57 px RMS in arbitrary units. Reprojection error measures agreement between photos,
  not the size of the model.
- **No project on SharePoint has ground control or check points,** so none has an absolute
  accuracy. That is itself the teaching point, and a reason to add check points to the final project.
- **Resolution.** A Phantom 4 Pro frame at 50 m beside one at 103 m: 1.4 cm against 2.8 cm GSD
  (`OR/images/gsd_Phantom_50m_vs_103m.png`). The crops need matching before it goes on a slide.
- **Ground truth candidate.** A taped diameter of the water tank, or its published dimensions,
  would turn the mesh into a real accuracy check.
- **PPK.** Four Autel flights carry raw RINEX and timestamp logs. In the field every photo was a
  standalone fix, about 1 m horizontal and 3 m vertical. With one base-station download from a Utah
  CORS station they could be corrected to a few centimetres: a real "what more accuracy costs"
  example.

### Week 6: Planning the Flight

- **The sides rule:** the water-tank camera plot, an oblique frame showing the wall, and the mesh
  wall. Overlap and GSD numbers from the same flight make a worked example. The tank roof sits about
  9 m closer to the camera, so its GSD is about 0.68 cm, not 0.93: GSD depends on distance to the
  surface, not on the altitude setting.
- **Spot the problem:** the tennis-court flight that lost every other line; the gimbal-at-the-
  horizon flights; the lopsided-overlap Rock Canyon flight; the example memo's 20 % side overlap for
  a 3D model.
- **Patterns:** Big East Lake flown by two aircraft within 20 minutes, one on a grid and one in
  shoreline loops; Carterville as a single-line corridor flight with a return oblique leg.
- **Gridded-flight video clips** from the Fall 2025 lab, once hosted.

### Week 7: How Photos Become 3D, Photo Metadata, Bentley

- **Reading a quality report:** the water tank (good) against the tennis 3D flight (bad), with the
  per-photo chart. Bentley's own acquisition report render is our output from licensed software;
  crop the logo as with the other iTwin screenshots.
- **Mesh:** the water-tank wireframe shows large triangles on the flat roof and wall and small ones
  in vegetation, plus a roof vent as a spike. It can sit beside or replace the generic meshing
  figure.
- **DSM:** the Rock Canyon and Grass field hillshades, both with drooping, webbed edges where overlap
  runs out.
- **Water does not reconstruct:** Big East Lake, mostly open water.
- **Metadata examples to sit beside the Parrot Anafi:** a DJI nadir frame and a −45° frame from the
  water-tank flight (`GimbalPitchDegree`, `RelativeAltitude`); the Autel clock stamped in UTC in 2024
  and local time in 2025; the 26 Grass field PNGs with no EXIF at all; the gimbal-at-the-horizon
  flights caught by reading the pitch tag.
- **Bentley guide (`software/bentley_itwin.md`):**
    - A TA handout's screenshots confirm the Start-menu names "iTwin Capture Modeler Engine" and
      "iTwin Capture Modeler Master" and the New Capture menu, clearing two of the five unverified
      labels.
    - Add to troubleshooting: a job stuck "pending" while the Engine runs means the job-queue folder
      in Modeler Settings does not match the project's.
    - Add: tiling when "Large reconstruction detected" warns about memory.
    - Mention: "Check Image Files" before aerotriangulation, and measuring in the Desktop Viewer.
- **Caution:** five of the seven productions in the iTwin project folders failed, and their logs
  are encrypted. The finished products are the water-tank mesh, the Grass field orthophoto and DSM,
  the parking-lot orthophoto and the three Rock Canyon GeoTIFFs.

### Week 8: Sensors and data processing

- **Thermal:** EB lot thermal shadows; parking-lot reflected sky (emissivity); Carterville bridge
  cracks plus the timing lesson (ASTM D4788 wants hours of sun or a clear night, a dry deck, low
  wind); Big East Lake water against forest at dawn. The Rock Canyon thermal folders hold colour
  JPGs only, which makes a second lesson: a picture is not a measurement.
- **Multispectral:** the NDVI, the four-band contact sheet showing that each band is its own camera,
  and the calibration-panel rules from the CE 594R document (within 2.5 h of solar noon, panel about
  a third of the frame, avoid partly cloudy days).
- **LiDAR:** the cloth-filter before and after, redrawn or re-rendered.

### Weeks 3 and 9: Part 107

- An instructor deck on SharePoint is text only and probably machine-generated. It is a usable
  outline for a Part 107 Marp deck, but four errors need fixing first: it says the certificate is
  valid 24 months (recurrent training is due every 24 calendar months; the certificate does not
  expire), leaves out night operations, lists B4UFLY as a LAANC app, and gives Class E as starting at
  700 ft only.
- Its decoded KATL METAR is a ready base for the missing Part 107 Figure 16.
- A TA guide adds local logistics: testing at the Provo airport through UVU, what to bring, retake
  rules, and how to read "Refer to FAA-CT-8080-2H, Figure 22, area 2". Good for a tip box on the
  overview page.
- Two more study videos for `part_107_resources.md`, link only.
- The UNM study guide (2019) is by an outside author with no licence. Do not republish it.
- **On the live site:** `faa_exam_planning_and_overview.md` lists DJI FlySafe as a LAANC-approved
  app. DJI's FlySafe is geofencing, not an FAA LAANC provider; check the FAA's current provider list
  and correct the sentence.

### Week 12: Surveying (no page yet)

- The CE 594R document has step-by-step Topcon HiPer VR rover checkout and survey instructions
  (reservation through the CCE reservations site, BYU cellular RTK network). With the TA schedules'
  "RTK day / surveying day / accurate mapping day" ideas, that is the core of a check-point lab and
  the missing Week 12 page.

### Final project

- **Report format:** the Winter 2026 example is a client memo with five headings (Scope, Flight Plan,
  Data Collection and Results, Limitations, Conclusion). It has no accuracy, GSD or ground-truth
  section, which makes it a good "what would you add?" exercise. Publish it only with the author's
  consent, or write a course example in the same format.
- **Decisions it informs:** team size about three (decision 1), Rock Canyon road and park as proven
  sites (decision 3), 10-minute presentations in the last Tuesday lecture (decision 9), and check
  points with the Topcon rover (decision 6).
- **Volume exercise ideas** from the TA schedules: paint for the Y, the Rock Canyon retention basin,
  stockpiles.

---

## Do not use as is

- **Misleading names.** "Water Tower" is a ground-level reservoir tank. "Tennis Court 3D" was an
  orthophoto job. "Parking Lot DEM" was a failed 3D mesh. Carterville "050" and "100" hold no bridge
  data, so there is no three-height set.
- **Grass field** has no scale; do not measure on it.
- **No coordinate system** on the water-tank orthophoto, the Green Basin orthophoto or the second
  Rock Canyon DSM: they were exported in local coordinates, unlike the parking-lot orthophoto. The
  Bentley guide's EPSG:32612 step exists for exactly this reason.
- **Privacy.** Student names are in several folder names. Two sets show identifiable students, and
  the horizon-pointing flights show private homes and yards. Every frame's EXIF carries GPS and the
  aircraft serial number. Strip EXIF and names before anything goes on the site.
- **Third-party material:** DJI manual pages and a YouTube screenshot inside the documents, and the
  UNM guide.

---

## Questions for the instructor

1. Where is the DJI Terra quality report on SharePoint? It has not synced to this machine.
2. May the 2024 how-to videos go on Kaltura or unlisted YouTube and be linked? Do the "minis" videos
   show DJI Minis or the Holy Stone?
3. May the student flights (water tank, the lopsided-overlap flight, the two gimbal flights) appear
   in slides with names removed? May the example memo be published, or should a course example be
   written instead?
4. Consent for the 2026-09-24 class photos on the Welcome page?
5. Were the Carterville 50 ft and 100 ft flights flown? Only 200 ft is on SharePoint.
6. Should the five failed productions be rerun for slides (parking-lot orthophoto/DSM and mesh,
   tennis courts)? Is there a known Engine or licence problem from those dates?
7. Is anyone downloading base-station data to finish PPK on the four Autel flights?
8. Should the NDVI be reprocessed as calibrated reflectance (DJI Terra or Pix4D) before it replaces
   the unlicensed images, or is a labelled quick-look acceptable?
9. May the CE 594R LiDAR screenshots and BYU hardware photos be reused on the public site?
10. Is the Winter 2026 project format (teams of about three, client memo, 10-minute talks) the plan
    for this semester? If so, decisions 1, 3 and 9 can be written into the project pages.
11. Which planning app does the class use with the larger aircraft now? The sample checklists assume
    DJI GS Pro.
12. Is the Topcon rover available to freshmen, or to TAs only?

Two security and privacy items found in the SharePoint folders were reported to the instructor
directly and are not recorded here.
