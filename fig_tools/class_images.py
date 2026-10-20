"""Render slide-ready images from real class flights: thermal, NDVI and screenshot panels.

The source photos live on the class SharePoint and in `.claude/local/`, never in the repository,
so every subcommand takes its source paths as arguments and writes a finished JPG to `--out`
(default `review/`). Every output is at most 1600 px wide, carries no EXIF or XMP, and is
re-encoded until it is under `--max-kb` (default 300). Fonts are Arial with DejaVu Sans as the
fallback; the background is the site's figure grey.

Subcommands
-----------
thermal      Autel T640 radiometric TIFF (640x512 int16) beside its matching visible MAX_ frame,
             with a colour bar in degrees C. The raw-to-temperature conversion is the single
             function `raw_to_celsius()` below; read its docstring before trusting a number.
thermal-jpg  A non-radiometric colour IR JPG shown as it is, with a title.
thermal-align  Diagnostic: thermal edges drawn over the visible frame to check `--align`.
ndvi         DJI Mavic 3M capture: RGB, NIR and NDVI panels. Bands are corrected the way DJI's
             guide describes (see `m3m_band_ratio()`), aligned with the per-image homography
             from the XMP, and optionally scaled with a calibration-panel frame.
panel        Two to four existing screenshots side by side with short labels, each cropped to
             a box so that user paths, file names and window chrome are cut out.

Run with the full Anaconda interpreter and, in Git Bash, `< /dev/null`:

    C:/Users/williagp/anaconda3/python.exe fig_tools/class_images.py <subcommand> ... < /dev/null

Needs numpy, scipy, matplotlib, Pillow and tifffile; no exiftool, no GDAL, no OpenCV.

Commands used for the Week 8 deck images (2026-10-20)
-------------------------------------------------------
Sources were first copied out of the read-only OneDrive mirror
`C:\\Users\\williagp\\OneDrive - Brigham Young University\\CE Drone Class - Documents` into
`.claude/local/scratch/class_images/src/` (shown as `$SRC` below) and the CE 594R screenshots
were already extracted into `.claude/local/onedrive_review/docs/media_general_info/` (`$DOC`).
OneDrive paths are given in the comment above each command.

  # East EB lot, 2025-09-16 10:05. OneDrive: Data and Images/2025-09-16/EastEBLot/Autel/
  python fig_tools/class_images.py thermal $SRC/EastEBLot/IRX_0029.TIFF $SRC/EastEBLot/MAX_0029.JPG \\
      --name w06_class_eblot_thermal.jpg --title "Parking lot, 10 a.m.: thermal beside visible" \\
      --crop 40 100 520 512 --annotate "446,400,8,75,shade: cooler asphalt"

  # Parking lot east of the EB, 2025-10-21 09:25. OneDrive: Data and Images/2025-10-21_PrkingLotThermal/
  python fig_tools/class_images.py thermal $SRC/ParkingLot/IRX_0020.TIFF $SRC/ParkingLot/MAX_0020.JPG \\
      --name w06_class_parkinglot_thermal.jpg --title "Our camera's reading, 9:25 a.m."

  # Carterville bridge approach, 2025-10-28 09:44. OneDrive: Data and Images/2025-10-28-Carterville200/
  python fig_tools/class_images.py thermal $SRC/Carterville200/IRX_0169.TIFF $SRC/Carterville200/MAX_0169.JPG \\
      --name w06_class_carterville_thermal.jpg --title "Bridge approach slab, 9:44 a.m., late October" \\
      --crop 120 0 640 512

  # Rock Canyon, 2026-03-05, Autel IR JPG (colour only, no temperatures).
  # OneDrive: SoftWare-Processing/Old/Rock Canyon Flight Plan Lab/Rock Canyon Thunderdome/thermal images/
  python fig_tools/class_images.py thermal-jpg $SRC/RockCanyon_Thunderdome/IRX_0087.jpg \\
      --name w06_class_rockcanyon_irjpg.jpg --title "Rock Canyon, thermal saved as a colour JPG"

  # EB lawn, 2025-09-16 09:53, Mavic 3M capture 0035 with the panel frames 0001-0010.
  # OneDrive: Data and Images/2025-09-16/EastEBGrass/Mavic/
  python fig_tools/class_images.py ndvi $SRC/EastEBGrass_Mavic/DJI_20250916095321_0035 \\
      --panel $SRC/EastEBGrass_Mavic/DJI_20250916094809_0001 --panel-reflectance 0.5 \\
      --name w06_class_eblawn_ndvi.jpg --title "The EB lawn: RGB, near-infrared and NDVI"

  # CE 594R CloudCompare cloth-filter sequence (course-internal screenshots).
  python fig_tools/class_images.py panel $DOC/037.png $DOC/042.png $DOC/043.png $DOC/049.png \\
      --labels "1  Full LiDAR point cloud (12.8 M points)" "2  Off-ground points: trees and brush (4.7 M)" \\
               "3  Ground points left by the cloth filter (8.1 M)" "4  Ground points gridded: bare-earth surface, 1 m cells" \\
      --crops 262,70,1575,838 --cols 2 \\
      --name w06_class_lidar_clothfilter.jpg --title "From point cloud to bare earth: CloudCompare cloth simulation filter"
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

import numpy as np
from PIL import Image, ImageFilter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.gridspec import GridSpec  # noqa: E402

# ---------------------------------------------------------------------------
# House style (matches fig_tools/svgkit.py)
# ---------------------------------------------------------------------------
BG = "#f9f9f9"
INK = "#1a1a1a"
MUTED = "#555555"
ACCENT = "#4a90d9"
plt.rcParams["font.family"] = ["Arial", "DejaVu Sans", "sans-serif"]
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titlecolor"] = INK

MAX_WIDTH = 1600


# ---------------------------------------------------------------------------
# Thermal: raw counts to temperature
# ---------------------------------------------------------------------------
def raw_to_celsius(raw):
    """Convert Autel T640 radiometric TIFF counts to degrees Celsius.

    CURRENT ASSUMPTION: counts are tenths of a kelvin, so  T = raw / 10 - 273.15.
    This gives believable values at the East EB lot (asphalt about 28 C at 10 a.m. in September)
    and at Carterville (about 5 C in late October) but reads -8 C on sunlit asphalt in the
    2025-10-21 parking-lot frames, so the scale is NOT confirmed. A separate session is checking
    the Autel scale against the temperatures Autel's own software reports and will replace this
    function. Until then every colour bar says "uncalibrated" unless `--calibrated` is passed.
    """
    return np.asarray(raw, dtype=float) / 10.0 - 273.15


# Thermal pixel (u, v) -> MAX_ visible pixel (s*u + ox, s*v + oy). Measured on EastEBLot
# IRX_0029 / MAX_0029 from the parking islands and one car; same rig on every Autel flight here.
# Check with `thermal-align` and override with `--align s ox oy` if a flight disagrees.
DEFAULT_ALIGN = (2.45, 1318.0, 874.0)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def read_tiff(path):
    try:
        import tifffile
        return tifffile.imread(path)
    except ImportError:
        return np.array(Image.open(path))


def xmp_tag(path, key, prefix="drone-dji"):
    """Read one XMP attribute straight from the file bytes (no exiftool needed)."""
    with open(path, "rb") as fh:
        b = fh.read()
    i, j = b.find(b"<x:xmpmeta"), b.find(b"</x:xmpmeta>")
    if i < 0:
        raise ValueError(f"no XMP packet in {path}")
    x = b[i:j].decode("utf-8", "replace")
    m = re.search(rf'{prefix}:{key}\s*=\s*"([^"]*)"', x) or re.search(rf"<{prefix}:{key}>([^<]*)<", x)
    if not m:
        raise KeyError(f"{prefix}:{key} not in {path}")
    return m.group(1).strip()


def floats(s):
    return [float(t) for t in re.split(r"[;,\s]+", s.strip()) if t]


def new_figure(width_px, height_px):
    dpi = 100
    fig = plt.figure(figsize=(width_px / dpi, height_px / dpi), dpi=dpi, facecolor=BG)
    return fig


def finish(fig, out_dir, name, max_kb=300, width=MAX_WIDTH):
    """Rasterise the figure, drop every bit of metadata, shrink to `width`, fit under max_kb."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=fig.dpi, facecolor=BG, metadata={})
    plt.close(fig)
    buf.seek(0)
    im = Image.open(buf).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    clean = Image.new("RGB", im.size)
    clean.paste(im)  # a fresh image carries no EXIF, XMP or ICC profile
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    q = 92
    while True:
        clean.save(path, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0 if q > 80 else 2)
        kb = os.path.getsize(path) / 1024
        if kb <= max_kb or q <= 40:
            break
        q -= 4
    print(f"{path}  {clean.width}x{clean.height}  {kb:.0f} KB  (JPEG quality {q})")
    return path


def title_block(fig, title, subtitle=None, top=0.97):
    fig.text(0.5, top, title, ha="center", va="top", fontsize=19, fontweight="bold", color=INK)
    if subtitle:
        fig.text(0.5, top - 0.055, subtitle, ha="center", va="top", fontsize=12, color=MUTED)


def parse_box(values, n=4):
    v = [float(x) for x in values]
    if len(v) != n:
        raise SystemExit(f"expected {n} numbers, got {values}")
    return v


def blur_regions(im, boxes, radius=18):
    """Gaussian-blur rectangles (x0 y0 x1 y1 in image pixels) for plates or faces."""
    for b in boxes:
        x0, y0, x1, y1 = [int(round(v)) for v in b]
        patch = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(radius))
        im.paste(patch, (x0, y0))
    return im


# ---------------------------------------------------------------------------
# thermal
# ---------------------------------------------------------------------------
def cmd_thermal(a):
    raw = read_tiff(a.tiff)
    if raw.ndim != 2:
        raise SystemExit(f"expected a single-band thermal TIFF, got shape {raw.shape}")
    temp = raw_to_celsius(raw)
    vis = Image.open(a.jpg).convert("RGB")
    s, ox, oy = a.align if a.align else DEFAULT_ALIGN
    H, W = temp.shape
    x0, y0, x1, y1 = parse_box(a.crop) if a.crop else (0, 0, W, H)
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    tcrop = temp[y0:y1, x0:x1]
    vbox = (s * x0 + ox, s * y0 + oy, s * x1 + ox, s * y1 + oy)
    vbox = tuple(int(round(v)) for v in vbox)
    if a.blur:
        blur_regions(vis, [parse_box(b) for b in a.blur])
    vcrop = vis.crop(vbox)
    # the visible panel is shown at the thermal's aspect; resample to a modest size
    target_w = 1600
    vcrop = vcrop.resize((target_w, round(target_w * (y1 - y0) / (x1 - x0))), Image.LANCZOS)

    vmin = a.vmin if a.vmin is not None else float(np.percentile(tcrop, 1))
    vmax = a.vmax if a.vmax is not None else float(np.percentile(tcrop, 99))

    aspect = (y1 - y0) / (x1 - x0)
    panel_w = 740
    panel_h = panel_w * aspect
    fig_h = panel_h + 150
    fig = new_figure(1600, fig_h)
    gs = GridSpec(1, 3, width_ratios=[1, 1, 0.035], left=0.02, right=0.95, bottom=0.03,
                  top=1 - 110 / fig_h, wspace=0.06, figure=fig)
    ax_v = fig.add_subplot(gs[0, 0])
    ax_t = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])
    ax_v.imshow(vcrop, extent=(x0, x1, y1, y0))
    ax_v.set_title(a.left_label, fontsize=13, color=MUTED, pad=6)
    im = ax_t.imshow(tcrop, cmap=a.cmap, vmin=vmin, vmax=vmax, extent=(x0, x1, y1, y0),
                     interpolation="nearest")
    ax_t.set_title(a.right_label, fontsize=13, color=MUTED, pad=6)
    for ax in (ax_v, ax_t):
        ax.set_axis_off()
    cb = fig.colorbar(im, cax=ax_c)
    cb.set_label("°C" if a.calibrated else "°C (uncalibrated)", fontsize=12, color=INK)
    cb.ax.tick_params(labelsize=11, colors=INK)

    for ann in a.annotate or []:
        parts = ann.split(",", 4)
        px, py, dx, dy = [float(p) for p in parts[:4]]
        label = parts[4].strip()
        ax_t.annotate(label, xy=(px, py), xytext=(px + dx, py + dy), fontsize=13, color=INK,
                      ha="center", va="center",
                      bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=ACCENT, lw=1.2),
                      arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.8, shrinkB=4))
    for ann in a.annotate_vis or []:
        parts = ann.split(",", 4)
        px, py, dx, dy = [float(p) for p in parts[:4]]
        label = parts[4].strip()
        ax_v.annotate(label, xy=(px, py), xytext=(px + dx, py + dy), fontsize=13, color=INK,
                      ha="center", va="center",
                      bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=ACCENT, lw=1.2),
                      arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.8, shrinkB=4))

    title_block(fig, a.title, a.subtitle, top=1 - 14 / fig_h)
    print(f"thermal crop {x0},{y0},{x1},{y1}: min {tcrop.min():.1f}  median {np.median(tcrop):.1f}  "
          f"max {tcrop.max():.1f} C; colour bar {vmin:.1f}..{vmax:.1f}")
    finish(fig, a.out, a.name, a.max_kb)


def cmd_thermal_align(a):
    """Diagnostic overlay: thermal edge contours on the visible frame for the given mapping."""
    temp = raw_to_celsius(read_tiff(a.tiff))
    vis = Image.open(a.jpg).convert("RGB")
    s, ox, oy = a.align if a.align else DEFAULT_ALIGN
    H, W = temp.shape
    fig = new_figure(1600, 1200)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.92])
    ax.imshow(vis)
    xs = np.arange(W) * s + ox
    ys = np.arange(H) * s + oy
    ax.contour(xs, ys, temp, levels=8, cmap="inferno", linewidths=0.8, alpha=0.9)
    ax.plot([ox, ox + s * W, ox + s * W, ox, ox], [oy, oy, oy + s * H, oy + s * H, oy], color=ACCENT, lw=2)
    ax.set_axis_off()
    title_block(fig, f"align check: scale {s}, offset ({ox:.0f}, {oy:.0f})")
    finish(fig, a.out, a.name or "thermal_align_check.jpg", 600)


# ---------------------------------------------------------------------------
# thermal-jpg
# ---------------------------------------------------------------------------
def cmd_thermal_jpg(a):
    im = Image.open(a.jpg).convert("RGB")
    if a.crop:
        im = im.crop(tuple(int(v) for v in parse_box(a.crop)))
    if a.blur:
        blur_regions(im, [parse_box(b) for b in a.blur])
    width = a.width
    panel_w = width - 60
    panel_h = panel_w * im.height / im.width
    fig_h = panel_h + 120
    fig = new_figure(width, fig_h)
    ax = fig.add_axes([30 / width, 20 / fig_h, panel_w / width, panel_h / fig_h])
    ax.imshow(im, interpolation="lanczos")
    ax.set_axis_off()
    title_block(fig, a.title, a.subtitle, top=1 - 14 / fig_h)
    finish(fig, a.out, a.name, a.max_kb, width=width)


# ---------------------------------------------------------------------------
# ndvi: DJI Mavic 3M
# ---------------------------------------------------------------------------
M3M_GUIDE_URL = ("https://dl.djicdn.com/downloads/DJI_Mavic_3_Enterprise/20230829/"
                 "Mavic_3M_Image_Processing_Guide_EN.pdf")


class Band:
    """One Mavic 3M multispectral band with the XMP it needs."""

    def __init__(self, path):
        self.path = path
        self.raw = read_tiff(path).astype(float)
        self.name = xmp_tag(path, "BandName")
        self.black = float(xmp_tag(path, "BlackLevel"))
        self.gain = float(xmp_tag(path, "SensorGain"))
        self.etime = float(xmp_tag(path, "ExposureTime"))          # microseconds
        self.gain_adj = float(xmp_tag(path, "SensorGainAdjustment"))
        self.irradiance = float(xmp_tag(path, "Irradiance"))
        self.vig = floats(xmp_tag(path, "VignettingData"))
        self.cx = float(xmp_tag(path, "CalibratedOpticalCenterX"))
        self.cy = float(xmp_tag(path, "CalibratedOpticalCenterY"))
        dw = xmp_tag(path, "DewarpData").split(";")[-1]
        self.fx, self.fy, self.dcx, self.dcy, self.k1, self.k2, self.p1, self.p2, self.k3 = floats(dw)
        self.H = np.array(floats(xmp_tag(path, "CalibratedHMatrix"))).reshape(3, 3)
        self.bits = 16 if self.raw.max() > 255 else 8
        self.saturation = 65520.0 if self.bits == 16 else 255.0


def m3m_band_ratio(b: Band, vignette=True):
    """Camera signal divided by sunlight-sensor signal, following DJI's Mavic 3M Image
    Processing Guide v1.0 (2023-08), Eq. 6-9:
        https://dl.djicdn.com/downloads/DJI_Mavic_3_Enterprise/20230829/Mavic_3M_Image_Processing_Guide_EN.pdf

      Step 1 (Eq. 7-8): vignetting, I * (k5 r^6 + ... + k0 r + 1), r from the calibrated optical centre.
      Eq. 9:  X_camera = (I/2^bits - BlackLevel/2^bits) / (SensorGain * ExposureTime/1e6)
      Eq. 6:  X_camera * SensorGainAdjustment / Irradiance   (Irradiance = X_LS * pLS_X)

    The result is proportional to surface reflectance by one factor rho_NIR that DJI's guide
    does not publish; it is the same for every band after SensorGainAdjustment, so NDVI from
    these ratios needs no further calibration (Eq. 6). A calibration panel of known
    reflectance supplies rho and turns the ratios into absolute reflectance; `cmd_ndvi` does
    that when `--panel` is given and the panel is not saturated.

    Check made 2026-10-20 on an asphalt frame: multiplying by the polynomial corrects in the
    right direction (raw falls to 0.40 at the corners, the polynomial rises to 3.2) but
    over-corrects by about 10 % at mid-frame. It is applied as published.
    """
    img = b.raw.copy()
    if vignette:
        yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]]
        r = np.hypot(xx - b.cx, yy - b.cy)
        k = b.vig
        img = img * (1.0 + k[0] * r + k[1] * r**2 + k[2] * r**3 + k[3] * r**4 + k[4] * r**5 + k[5] * r**6)
    scale = 2.0 ** b.bits
    cam = (img / scale - b.black / scale) / (b.gain * b.etime / 1e6)
    return cam * b.gain_adj / b.irradiance


def undistort(img, b: Band):
    """Step 2 of the guide: Brown-Conrady undistort with the DewarpData intrinsics, the same
    mapping as OpenCV's undistort() (camera matrix fx, fy, cx+CenterX, cy+CenterY)."""
    from scipy.ndimage import map_coordinates
    h, w = img.shape
    cx, cy = b.cx + b.dcx, b.cy + b.dcy
    vv, uu = np.mgrid[0:h, 0:w].astype(float)
    x = (uu - cx) / b.fx
    y = (vv - cy) / b.fy
    r2 = x * x + y * y
    radial = 1 + b.k1 * r2 + b.k2 * r2**2 + b.k3 * r2**3
    xd = x * radial + 2 * b.p1 * x * y + b.p2 * (r2 + 2 * x * x)
    yd = y * radial + b.p1 * (r2 + 2 * y * y) + 2 * b.p2 * x * y
    src_u = b.fx * xd + cx
    src_v = b.fy * yd + cy
    return map_coordinates(img, [src_v, src_u], order=1, mode="constant", cval=np.nan)


def warp_homography(img, H):
    """Step 3 of the guide: dst = H * src. Sampled backwards with H^-1 so every output pixel is
    filled."""
    from scipy.ndimage import map_coordinates
    h, w = img.shape
    Hinv = np.linalg.inv(H)
    vv, uu = np.mgrid[0:h, 0:w].astype(float)
    ones = np.ones_like(uu)
    src = Hinv @ np.stack([uu.ravel(), vv.ravel(), ones.ravel()])
    su = (src[0] / src[2]).reshape(h, w)
    sv = (src[1] / src[2]).reshape(h, w)
    return map_coordinates(img, [sv, su], order=1, mode="constant", cval=np.nan)


def phase_shift(ref, mov):
    """Integer (dy, dx) that moves `mov` onto `ref`, from phase correlation of gradient magnitude."""
    from scipy.ndimage import gaussian_filter

    def gm(x):
        x = np.nan_to_num(x, nan=float(np.nanmedian(x)))
        gy, gx = np.gradient(gaussian_filter(x, 1.0))
        g = np.hypot(gx, gy)
        return (g - g.mean()) / (g.std() + 1e-9)

    A, B = np.fft.fft2(gm(ref)), np.fft.fft2(gm(mov))
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-12
    c = np.abs(np.fft.ifft2(R))
    dy, dx = np.unravel_index(np.argmax(c), c.shape)
    if dy > c.shape[0] // 2:
        dy -= c.shape[0]
    if dx > c.shape[1] // 2:
        dx -= c.shape[1]
    return int(dy), int(dx)


def find_panel(raw, centre, half=300):
    """Return (box, inner_mask) of the brightest compact blob within `half` px of `centre`.
    The DJI/MicaSense-style panel is a white square; the inner half of its bounding box is used."""
    from scipy import ndimage
    cx, cy = centre
    sub = raw[int(cy - half):int(cy + half), int(cx - half):int(cx + half)]
    thr = np.percentile(sub, 97)
    lab, n = ndimage.label(sub >= thr)
    if n == 0:
        return None
    sizes = ndimage.sum(sub >= thr, lab, range(1, n + 1))
    k = int(np.argmax(sizes)) + 1
    ys, xs = np.where(lab == k)
    x0, x1 = xs.min() + int(cx - half), xs.max() + int(cx - half)
    y0, y1 = ys.min() + int(cy - half), ys.max() + int(cy - half)
    w, h = x1 - x0, y1 - y0
    inner = (x0 + w // 4, y0 + h // 4, x1 - w // 4, y1 - h // 4)
    return (x0, y0, x1, y1), inner


def cmd_ndvi(a):
    pre = a.prefix
    bands = {k: Band(f"{pre}_MS_{k}.TIF") for k in ("R", "NIR")}
    for b in bands.values():
        print(f"{b.name}: gain {b.gain}  exposure {b.etime:.0f} us  irradiance {b.irradiance:.0f}  "
              f"gain_adj {b.gain_adj:.4f}  raw max {b.raw.max():.0f}")

    # --- band ratio (DJI method), undistort, homography -----------------------------------
    proc = {}
    for k, b in bands.items():
        ratio = m3m_band_ratio(b, vignette=not a.no_vignette)
        if not a.no_dewarp:
            ratio = undistort(ratio, b)
            ratio = warp_homography(ratio, b.H)
        proc[k] = ratio
    dy, dx = phase_shift(proc["R"], proc["NIR"])
    print(f"residual NIR->R shift after XMP homography: dy {dy} dx {dx} px", end="")
    if a.align == "phase" or (a.align == "auto" and (abs(dy) > 2 or abs(dx) > 2)):
        proc["NIR"] = np.roll(proc["NIR"], (dy, dx), (0, 1))
        print("  -> applied")
    else:
        print("  -> kept the homography alignment")

    # --- calibration panel, optional ------------------------------------------------------
    factor = {"R": None, "NIR": None}
    panel_note = "no panel frame given"
    if a.panel:
        panel_note_parts = []
        usable = True
        for k in ("R", "NIR"):
            pb = Band(f"{a.panel}_MS_{k}.TIF")
            found = find_panel(pb.raw, (pb.cx, pb.cy))
            if not found:
                print(f"panel {k}: no bright blob found near the centre")
                usable = False
                continue
            box, inner = found
            x0, y0, x1, y1 = inner
            patch_raw = pb.raw[y0:y1, x0:x1]
            sat = float((patch_raw >= pb.saturation - 1).mean())
            patch_ratio = m3m_band_ratio(pb, vignette=not a.no_vignette)[y0:y1, x0:x1]
            print(f"panel {k}: box {box}, inner mean raw {patch_raw.mean():.0f}, "
                  f"saturated {100 * sat:.0f} %, mean ratio {patch_ratio.mean():.4g}")
            if sat > 0.02:
                usable = False
                panel_note_parts.append(f"{k} {100 * sat:.0f} % saturated")
            else:
                factor[k] = a.panel_reflectance / float(patch_ratio.mean())
        if usable and all(factor.values()):
            panel_note = (f"panel reflectance assumed {a.panel_reflectance:.2f} in both bands; "
                          f"factors R {factor['R']:.4g}, NIR {factor['NIR']:.4g}")
        else:
            panel_note = "panel frame unusable: " + ", ".join(panel_note_parts or ["not found"])
            factor = {"R": None, "NIR": None}
    print("panel:", panel_note)

    R, N = proc["R"], proc["NIR"]
    ndvi_ls = (N - R) / (N + R + 1e-12)
    if factor["R"] and factor["NIR"]:
        Rr, Nr = R * factor["R"], N * factor["NIR"]
        ndvi_pan = (Nr - Rr) / (Nr + Rr + 1e-12)
        d = ndvi_pan - ndvi_ls
        veg = ndvi_ls > 0.5
        print(f"panel-adjusted vs sunlight-sensor NDVI: mean diff {np.nanmean(d):+.3f}, "
              f"mean |diff| {np.nanmean(np.abs(d)):.3f}, over vegetation {np.nanmean(d[veg]):+.3f}")
        ndvi = ndvi_pan
        label_calib = (f"calibrated to reflectance with the sunlight sensor and panel "
                       f"(panel reflectance assumed {a.panel_reflectance:.2f})")
    else:
        ndvi = ndvi_ls
        label_calib = ("bands normalized by the sunlight sensor (DJI method); "
                       "the panel frames are saturated, so reflectance is relative, not absolute")

    # --- crop the warped borders ------------------------------------------------------------
    m = a.margin
    R, N, ndvi = R[m:-m, m:-m], N[m:-m, m:-m], ndvi[m:-m, m:-m]
    h, w = ndvi.shape
    print(f"NDVI percentiles 5/50/95: {np.nanpercentile(ndvi, [5, 50, 95]).round(2)}")

    # --- the RGB frame, cropped to the multispectral footprint through DewarpHMatrix -------
    rgb = Image.open(f"{pre}_D.JPG").convert("RGB")
    Hd = np.array(floats(xmp_tag(f"{pre}_MS_NIR.TIF", "DewarpHMatrix"))).reshape(3, 3)
    sx, tx, sy, ty = Hd[0, 0], Hd[0, 2], Hd[1, 1], Hd[1, 2]
    rbox = (int(round(sx * m + tx)), int(round(sy * m + ty)),
            int(round(sx * (w + m) + tx)), int(round(sy * (h + m) + ty)))
    rgb = rgb.crop(rbox)
    rgb = rgb.resize((1200, round(1200 * rgb.height / rgb.width)), Image.LANCZOS)

    # --- layout -----------------------------------------------------------------------------
    aspect = h / w
    panel_w = 500
    panel_h = panel_w * aspect
    fig_h = panel_h + 175
    fig = new_figure(1600, fig_h)
    gs = GridSpec(1, 4, width_ratios=[1, 1, 1, 0.04], left=0.015, right=0.955, bottom=0.03,
                  top=1 - 115 / fig_h, wspace=0.05, figure=fig)
    ax1, ax2, ax3, axc = [fig.add_subplot(gs[0, i]) for i in range(4)]
    ax1.imshow(rgb)
    ax1.set_title("RGB camera", fontsize=13, color=MUTED, pad=6)
    lo, hi = np.nanpercentile(N, [1, 99])
    ax2.imshow(N, cmap="gray", vmin=lo, vmax=hi)
    ax2.set_title("Near-infrared band (860 nm)", fontsize=13, color=MUTED, pad=6)
    im = ax3.imshow(ndvi, cmap="RdYlGn", vmin=a.vmin, vmax=a.vmax)
    ax3.set_title("NDVI = (NIR − Red) / (NIR + Red)", fontsize=13, color=MUTED, pad=6)
    for ax in (ax1, ax2, ax3):
        ax.set_axis_off()
    cb = fig.colorbar(im, cax=axc)
    cb.set_label("NDVI", fontsize=12, color=INK)
    cb.ax.tick_params(labelsize=11, colors=INK)
    subtitle = a.subtitle if a.subtitle is not None else label_calib
    title_block(fig, a.title, subtitle, top=1 - 14 / fig_h)
    finish(fig, a.out, a.name, a.max_kb)


# ---------------------------------------------------------------------------
# panel: screenshots side by side
# ---------------------------------------------------------------------------
def cmd_panel(a):
    n = len(a.images)
    if not (2 <= n <= 4):
        raise SystemExit("panel takes two to four images")
    labels = a.labels or [""] * n
    if len(labels) != n:
        raise SystemExit("one --labels entry per image")
    crops = [None] * n
    if a.crops:
        if len(a.crops) == 1:
            a.crops = a.crops * n
        if len(a.crops) != n:
            raise SystemExit("one --crops entry per image, or one for all")
        crops = [tuple(int(v) for v in c.split(",")) for c in a.crops]
    ims = []
    for p, c in zip(a.images, crops):
        im = Image.open(p).convert("RGB")
        if c:
            im = im.crop(c)
        ims.append(im)
    cols = a.cols or n
    rows = -(-n // cols)
    gap = 14
    cell_w = (1600 - gap * (cols + 1)) / cols
    aspect = max(im.height / im.width for im in ims)
    cell_h = cell_w * aspect
    label_h = 30
    top_h = 70 if not a.subtitle else 100
    fig_h = top_h + rows * (cell_h + label_h + gap) + gap
    fig = new_figure(1600, fig_h)
    for i, (im, lab) in enumerate(zip(ims, labels)):
        r, c = divmod(i, cols)
        x = (gap + c * (cell_w + gap)) / 1600
        y = 1 - (top_h + r * (cell_h + label_h + gap) + cell_h) / fig_h
        ax = fig.add_axes([x, y, cell_w / 1600, cell_h / fig_h])
        ax.imshow(im, interpolation="lanczos")
        ax.set_axis_off()
        fig.text(x + 0.004, y - 6 / fig_h, lab, ha="left", va="top", fontsize=13, color=INK)
    title_block(fig, a.title, a.subtitle, top=1 - 14 / fig_h)
    finish(fig, a.out, a.name, a.max_kb)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--out", default="review", help="output folder (default review/)")
        p.add_argument("--name", required=True, help="output file name, e.g. w06_class_x.jpg")
        p.add_argument("--title", required=True)
        p.add_argument("--subtitle", default=None)
        p.add_argument("--max-kb", type=float, default=300)

    p = sub.add_parser("thermal", help="radiometric TIFF beside its visible frame")
    p.add_argument("tiff")
    p.add_argument("jpg")
    common(p)
    p.add_argument("--crop", nargs=4, metavar=("X0", "Y0", "X1", "Y1"), help="thermal pixel box")
    p.add_argument("--vmin", type=float)
    p.add_argument("--vmax", type=float)
    p.add_argument("--calibrated", action="store_true", help="drop the 'uncalibrated' label")
    p.add_argument("--cmap", default="inferno")
    p.add_argument("--align", nargs=3, type=float, metavar=("SCALE", "OX", "OY"),
                   help=f"thermal->visible pixel mapping (default {DEFAULT_ALIGN})")
    p.add_argument("--annotate", action="append", metavar="X,Y,DX,DY,TEXT",
                   help="callout on the thermal panel: arrow tip at X,Y (thermal px), text offset DX,DY")
    p.add_argument("--annotate-vis", action="append", metavar="X,Y,DX,DY,TEXT",
                   help="same, on the visible panel (thermal px coordinates)")
    p.add_argument("--blur", action="append", nargs=4, metavar=("X0", "Y0", "X1", "Y1"),
                   help="blur a box of the visible frame (visible px) for plates or faces")
    p.add_argument("--left-label", default="Visible camera")
    p.add_argument("--right-label", default="Thermal camera")
    p.set_defaults(func=cmd_thermal)

    p = sub.add_parser("thermal-align", help="overlay check for --align")
    p.add_argument("tiff")
    p.add_argument("jpg")
    p.add_argument("--out", default="review")
    p.add_argument("--name", default=None)
    p.add_argument("--align", nargs=3, type=float, metavar=("SCALE", "OX", "OY"))
    p.set_defaults(func=cmd_thermal_align)

    p = sub.add_parser("thermal-jpg", help="colour IR JPG as it is")
    p.add_argument("jpg")
    common(p)
    p.add_argument("--crop", nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("--blur", action="append", nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("--width", type=int, default=1280)
    p.set_defaults(func=cmd_thermal_jpg)

    p = sub.add_parser("ndvi", help="Mavic 3M capture: RGB, NIR, NDVI")
    p.add_argument("prefix", help="path up to the capture number, e.g. .../DJI_20250916095321_0035")
    common(p)
    p.add_argument("--panel", default=None, help="prefix of a calibration-panel capture")
    p.add_argument("--panel-reflectance", type=float, default=0.5,
                   help="panel reflectance if the certified value is unknown (default 0.5)")
    p.add_argument("--align", choices=["homography", "phase", "auto"], default="auto")
    p.add_argument("--no-vignette", action="store_true")
    p.add_argument("--no-dewarp", action="store_true")
    p.add_argument("--margin", type=int, default=60, help="border pixels to drop after warping")
    p.add_argument("--vmin", type=float, default=-0.2)
    p.add_argument("--vmax", type=float, default=1.0)
    p.set_defaults(func=cmd_ndvi)

    p = sub.add_parser("panel", help="two to four screenshots side by side")
    p.add_argument("images", nargs="+")
    common(p)
    p.add_argument("--labels", nargs="+")
    p.add_argument("--crops", nargs="+", metavar="X0,Y0,X1,Y1", help="one box per image, or one for all")
    p.add_argument("--cols", type=int, default=None)
    p.set_defaults(func=cmd_panel)

    a = ap.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
