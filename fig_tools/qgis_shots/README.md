# QGIS screenshots for the Week 4 deck

The seventeen `docs/software/images/qgis_NN_*.{jpg,png}` screenshots are generated, not taken by
hand, so a QGIS upgrade or a re-crop is a rerun rather than a photo session.

1. Put the Lab 2 orthophoto, `EB-Parking-1-22-26-orthophoto.tif` (EPSG:32612, 1 cm pixels), in
   `.claude/local/` — it is git-ignored and lives behind the BYU SharePoint link on the lab page.
2. Run `fig_tools\qgis_shots\run_qgis.bat` from the repository root. It launches the OSGeo4W QGIS at
   `C:\OSGeo4W` with a throwaway `capture` profile and runs `capture.py` inside it, which loads the
   orthophoto, walks through Lab 2 Part 4 (zoom, CRS in degrees and metres, CRS dialog, project
   units, Measure line and area, New Shapefile Layer, digitizing, Field Calculator, attribute
   table) and writes raw grabs to `.claude/local/scratch/qgis/shots/`. Modal dialogs are grabbed by
   a QTimer that fires while the dialog blocks; the floating Measure dialog is composited onto the
   window grab. Expect QGIS to open on screen for about a minute.
3. The two download-page images come from headless Chrome:
   `chrome.exe --headless --screenshot=... --window-size=1600,1000 "https://qgis.org/download/?skip_donate=true"`
   (and the same URL without the parameter for the donate interstitial).
4. Run `process_shots.py` with the Anaconda python to crop, resize and convert into
   `docs/software/images/`. Map-heavy grabs become JPEG; dialogs and status-bar strips stay PNG.
5. Rebuild the deck: `python fig_tools/build_slides.py --only week_04 --pptx`.

Stall and lot outlines are hard-coded in `capture.py` as orthophoto pixel coordinates.
