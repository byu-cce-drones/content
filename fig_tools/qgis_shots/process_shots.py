"""Turn the raw QGIS captures into the slide images under docs/software/images/.

Map-heavy window grabs become JPEG (photo content compresses well); dialogs and
status-bar strips stay PNG. Everything is 1600 px wide or narrower.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(r"G:\GIT_Repo\byu-cce-drones-content")
RAW = ROOT / ".claude/local/scratch/qgis"
SHOTS = RAW / "shots"
OUT = ROOT / "docs/software/images"
OUT.mkdir(parents=True, exist_ok=True)

JPG_Q = 82


def jpg(src, dst, width=None, crop=None):
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(crop)
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT / dst, "JPEG", quality=JPG_Q, optimize=True)
    print(dst, im.size, f"{(OUT / dst).stat().st_size // 1024} KB")


def png(src, dst, crop=None):
    im = Image.open(src)
    if crop:
        im = im.crop(crop)
    im.save(OUT / dst, "PNG", optimize=True)
    print(dst, im.size, f"{(OUT / dst).stat().st_size // 1024} KB")


# install
jpg(RAW / "qgis_download_ltr.png", "qgis_01_download_ltr.jpg", crop=(0, 0, 1600, 720))
jpg(RAW / "qgis_download_donate.png", "qgis_02_download_donate.jpg", crop=(0, 0, 1600, 900))
# load
jpg(SHOTS / "qgis_01_window.png", "qgis_03_window.jpg")
jpg(SHOTS / "qgis_02_zoom_stall.png", "qgis_04_zoom_stall.jpg")
jpg(ROOT / "docs/labs/images/EB_Parking_Lot.png", "qgis_05_google_maps_lot.jpg", width=1600)
jpg(RAW / "ortho_lot_crop.png", "qgis_06_ortho_lot.jpg", width=1600)
# crs: right two-thirds of the status bar, scaled up 2x so it reads on a slide
for src, dst in [("qgis_03_statusbar_4326.png", "qgis_07_statusbar_4326.png"),
                 ("qgis_04_statusbar_32612.png", "qgis_08_statusbar_32612.png")]:
    im = Image.open(SHOTS / src).crop((1080, 0, 1600, 28))
    im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
    im.save(OUT / dst, "PNG", optimize=True)
    print(dst, im.size)
png(SHOTS / "qgis_05_crs_dialog.png", "qgis_09_crs_dialog.png")
png(SHOTS / "qgis_06_project_units.png", "qgis_10_project_units.png", crop=(0, 0, 857, 420))
# measure
jpg(SHOTS / "qgis_07_measure_line.png", "qgis_11_measure_line.jpg")
jpg(SHOTS / "qgis_08_measure_area.png", "qgis_12_measure_area.jpg")
# digitize
png(SHOTS / "qgis_09_new_layer.png", "qgis_13_new_layer.png", crop=(0, 0, 867, 400))
jpg(SHOTS / "qgis_10_trace_lot.png", "qgis_14_trace_lot.jpg")
jpg(SHOTS / "qgis_11_lot_done.png", "qgis_15_lot_done.jpg")
png(SHOTS / "qgis_12_field_calc.png", "qgis_16_field_calc.png")
png(SHOTS / "qgis_13_attribute_table.png", "qgis_17_attribute_table.png", crop=(0, 0, 640, 130))

total = sum(p.stat().st_size for p in OUT.glob("qgis_*")) // 1024
print(f"total {total} KB in {OUT}")
