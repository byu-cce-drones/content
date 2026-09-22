"""Drive QGIS through the Lab 2 Part 4 workflow and save a screenshot at each step.

Run with run_qgis.bat (fresh 'capture' profile). Steps are chained with QTimer so the
GUI can repaint between them. Every step logs to capture.log; a failure in one step
is logged and the chain continues.
"""
import os
import traceback

from qgis.PyQt.QtCore import QTimer, Qt, QPoint, QRect
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QApplication, QLineEdit, QComboBox, QDialog
from qgis.PyQt.QtTest import QTest
from qgis.core import (Qgis, QgsProject, QgsRasterLayer, QgsVectorLayer, QgsFeature,
                       QgsGeometry, QgsPointXY, QgsRectangle, QgsCoordinateReferenceSystem,
                       QgsField, QgsFields, QgsVectorFileWriter, QgsWkbTypes,
                       QgsFillSymbol, QgsSingleSymbolRenderer, QgsDistanceArea,
                       QgsCoordinateTransformContext)
from qgis.PyQt.QtCore import QVariant
from qgis.gui import (QgsProjectionSelectionDialog, QgsNewVectorLayerDialog, QgsFieldCalculator,
                      QgsExpressionBuilderWidget, QgsFileWidget)
from qgis.utils import iface

ROOT = r"G:\GIT_Repo\byu-cce-drones-content"
OUT = os.path.join(ROOT, r".claude\local\scratch\qgis\shots")
TIF = os.path.join(ROOT, r".claude\local\EB-Parking-1-22-26-orthophoto.tif")
SHP = os.path.join(OUT, "parking_lot.shp")
LOG = os.path.join(OUT, "capture.log")
os.makedirs(OUT, exist_ok=True)

# Orthophoto is EPSG:32612, 1 cm pixels, origin (444940.489, 4455329.637).
E0, N0, PX = 444940.489, 4455329.637, 0.01


def m(px, py):
    """Orthophoto pixel -> UTM point."""
    return QgsPointXY(E0 + px * PX, N0 - py * PX)


# Parking stall (pickup truck stall, east row) and asphalt outline of the lot.
STALL = [m(11700, 3380), m(12290, 3380), m(12290, 3643), m(11700, 3643)]
LOT = [m(4900, 3550), m(7600, 3550), m(9000, 3000), m(10000, 2750),
       m(12500, 2750), m(12500, 6550), m(4900, 6550)]

SQFT_PER_M2 = 10.7639


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def save_widget(widget, name):
    path = os.path.join(OUT, name)
    widget.grab().save(path)
    log(f"saved {name} ({widget.width()}x{widget.height()})")


def save_with_dialog(name, cls_name, pos=(12, 150)):
    """Grab the main window and paint a floating dialog of class `cls_name`
    on top of it at `pos`, so the result is clean regardless of what else is
    on screen."""
    from qgis.PyQt.QtGui import QPainter, QPen
    win = iface.mainWindow()
    base = win.grab()
    for w in QApplication.topLevelWidgets():
        if isinstance(w, QDialog) and w.windowTitle() == cls_name and w.isVisible():
            dp = w.grab()
            painter = QPainter(base)
            painter.drawPixmap(pos[0], pos[1], dp)
            painter.setPen(QPen(QColor("#555555"), 1))
            painter.drawRect(pos[0], pos[1], dp.width() - 1, dp.height() - 1)
            painter.end()
            log(f"composited {cls_name} {dp.width()}x{dp.height()} at {pos}")
            break
    base.save(os.path.join(OUT, name))
    log(f"saved {name}")


def canvas_px(pt):
    """Map coordinate -> pixel position on the canvas viewport."""
    p = iface.mapCanvas().getCoordinateTransform().transform(pt).toQPointF()
    return QPoint(int(p.x()), int(p.y()))


def click(pt, button=Qt.LeftButton):
    vp = iface.mapCanvas().viewport()
    QTest.mouseClick(vp, button, Qt.NoModifier, canvas_px(pt))
    QTest.qWait(150)


def extent_of(points, pad=0.15):
    xs = [p.x() for p in points]
    ys = [p.y() for p in points]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    return QgsRectangle(min(xs) - w * pad, min(ys) - h * pad, max(xs) + w * pad, max(ys) + h * pad)


def zoom_to(points, pad=0.15):
    c = iface.mapCanvas()
    c.setExtent(extent_of(points, pad))
    c.refresh()


def later(ms, fn):
    def wrapped():
        try:
            fn()
        except Exception:
            log(f"error in {fn.__name__}:\n{traceback.format_exc()}")
            # keep the chain going: find the next step by name
            nxt = NEXT.get(fn.__name__)
            if nxt:
                later(500, nxt)
            else:
                os._exit(1)
    QTimer.singleShot(ms, wrapped)


STATE = {}


# ---------------------------------------------------------------- steps

def s01_setup():
    win = iface.mainWindow()
    win.showNormal()
    win.resize(1600, 900)
    win.move(0, 0)
    from qgis.core import QgsSettings
    st = QgsSettings()
    st.setValue("qgis/digitizing/line_width", 4)
    st.setValue("qgis/digitizing/line_color_alpha", 255)
    st.setValue("qgis/digitizing/fill_color_alpha", 50)
    proj = QgsProject.instance()
    proj.setDistanceUnits(Qgis.DistanceUnit.Feet)
    proj.setAreaUnits(Qgis.AreaUnit.SquareFeet)
    lyr = QgsRasterLayer(TIF, "EB-Parking-1-22-26-orthophoto")
    log(f"ortho valid={lyr.isValid()} crs={lyr.crs().authid()}")
    proj.addMapLayer(lyr)
    STATE["ortho"] = lyr
    iface.mapCanvas().setExtent(lyr.extent())
    iface.mapCanvas().refresh()
    later(5000, s02_window)


def s02_window():
    iface.messageBar().clearWidgets()
    QTest.qWait(500)
    save_widget(iface.mainWindow(), "qgis_01_window.png")
    zoom_to(STALL, 0.6)
    later(4000, s03_zoom)


def s03_zoom():
    save_widget(iface.mainWindow(), "qgis_02_zoom_stall.png")
    later(300, s04_status_4326)


def s04_status_4326():
    QgsProject.instance().setCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
    later(2500, s05_status_4326_grab)


def s05_status_4326_grab():
    sb = iface.mainWindow().statusBar()
    save_widget(sb, "qgis_03_statusbar_4326.png")
    save_widget(iface.mainWindow(), "qgis_03b_window_4326.png")
    QgsProject.instance().setCrs(QgsCoordinateReferenceSystem("EPSG:32612"))
    later(2500, s06_status_32612_grab)


def s06_status_32612_grab():
    sb = iface.mainWindow().statusBar()
    save_widget(sb, "qgis_04_statusbar_32612.png")
    later(300, s07_crs_dialog)


def s07_crs_dialog():
    d = QgsProjectionSelectionDialog(iface.mainWindow())
    d.setWindowTitle("Project Coordinate Reference System")
    for le in d.findChildren(QLineEdit):
        if "search" in le.objectName().lower() or "filter" in le.objectName().lower():
            le.setText("32612")
            log(f"crs filter set on {le.objectName()}")
            break
    d.setCrs(QgsCoordinateReferenceSystem("EPSG:32612"))
    d.resize(900, 650)
    d.show()
    STATE["crsdlg"] = d
    later(3000, s08_crs_dialog_grab)


def s08_crs_dialog_grab():
    d = STATE["crsdlg"]
    save_widget(d, "qgis_05_crs_dialog.png")
    d.close()
    later(500, s09_project_props)


def s09_project_props():
    def grab_modal():
        try:
            w = QApplication.activeModalWidget()
            log(f"modal: {w.__class__.__name__ if w else None}")
            if w:
                save_widget(w, "qgis_06_project_units.png")
                w.reject()
        except Exception:
            log(traceback.format_exc())
    QTimer.singleShot(3000, grab_modal)
    later(4500, s10_measure_line)
    iface.showProjectPropertiesDialog("General")


def s10_measure_line():
    zoom_to(STALL, 0.5)
    QTest.qWait(2500)
    iface.actionMeasure().trigger()
    QTest.qWait(800)
    click(STALL[0])
    click(STALL[1])
    click(STALL[1], Qt.RightButton)
    QTest.qWait(500)
    place_measure_dialog()
    later(1500, s11_measure_line_grab)


def place_measure_dialog():
    win = iface.mainWindow()
    for w in QApplication.topLevelWidgets():
        if isinstance(w, QDialog) and w.windowTitle() == "Measure" and w.isVisible():
            w.move(win.pos().x() - 2000, win.pos().y() + 140)  # off-screen; composited later
            log("measure dialog placed")


def s11_measure_line_grab():
    save_with_dialog("qgis_07_measure_line.png", "Measure")
    iface.actionPan().trigger()
    QTest.qWait(500)
    iface.actionMeasureArea().trigger()
    QTest.qWait(800)
    for p in STALL:
        click(p)
    click(STALL[-1], Qt.RightButton)
    QTest.qWait(500)
    place_measure_dialog()
    later(1500, s12_measure_area_grab)


def s12_measure_area_grab():
    save_with_dialog("qgis_08_measure_area.png", "Measure")
    iface.actionPan().trigger()
    later(500, s13_new_layer_dialog)


def s13_new_layer_dialog():
    d = QgsNewVectorLayerDialog(iface.mainWindow())
    d.setCrs(QgsCoordinateReferenceSystem("EPSG:32612"))
    for cb in d.findChildren(QComboBox):
        idx = cb.findText("Polygon")
        if idx >= 0:
            cb.setCurrentIndex(idx)
            log(f"geometry combo {cb.objectName()} -> Polygon")
            break
    for fw in d.findChildren(QgsFileWidget):
        fw.setFilePath(r"C:\Users\student\Documents\lab2\parking_lot.shp")
        break
    d.show()
    STATE["newdlg"] = d
    later(2500, s14_new_layer_grab)


def s14_new_layer_grab():
    d = STATE["newdlg"]
    save_widget(d, "qgis_09_new_layer.png")
    d.close()
    later(500, s15_make_layer)


def s15_make_layer():
    crs = QgsCoordinateReferenceSystem("EPSG:32612")
    fields = QgsFields()
    fields.append(QgsField("name", QVariant.String, len=40))
    opts = QgsVectorFileWriter.SaveVectorOptions()
    opts.driverName = "ESRI Shapefile"
    w = QgsVectorFileWriter.create(SHP, fields, QgsWkbTypes.Polygon, crs,
                                   QgsCoordinateTransformContext(), opts)
    f = QgsFeature(fields)
    f.setGeometry(QgsGeometry.fromPolygonXY([STALL]))
    f.setAttribute("name", "stall")
    w.addFeature(f)
    del w
    lyr = QgsVectorLayer(SHP, "parking_lot", "ogr")
    log(f"vector valid={lyr.isValid()} crs={lyr.crs().authid()} n={lyr.featureCount()}")
    sym = QgsFillSymbol.createSimple({"color": "0,0,0,0", "outline_color": "#e74c3c",
                                      "outline_width": "0.9", "outline_width_unit": "MM"})
    lyr.setRenderer(QgsSingleSymbolRenderer(sym))
    QgsProject.instance().addMapLayer(lyr)
    STATE["vec"] = lyr
    iface.setActiveLayer(lyr)
    zoom_to(LOT, 0.12)
    QTest.qWait(3000)
    lyr.startEditing()
    iface.actionAddFeature().trigger()
    QTest.qWait(800)
    for p in LOT[:5]:
        click(p)
    later(1500, s16_trace_grab)


def s16_trace_grab():
    save_widget(iface.mainWindow(), "qgis_10_trace_lot.png")
    QTest.keyClick(iface.mapCanvas().viewport(), Qt.Key_Escape)
    QTest.qWait(300)
    lyr = STATE["vec"]
    f = QgsFeature(lyr.fields())
    f.setGeometry(QgsGeometry.fromPolygonXY([LOT]))
    f.setAttribute("name", "lot")
    lyr.addFeature(f)
    lyr.commitChanges()
    iface.actionPan().trigger()
    iface.mapCanvas().refresh()
    later(2500, s17_done_grab)


def s17_done_grab():
    save_widget(iface.mainWindow(), "qgis_11_lot_done.png")
    later(300, s18_field_calc)


def s18_field_calc():
    lyr = STATE["vec"]
    d = QgsFieldCalculator(lyr, iface.mainWindow())
    for le in d.findChildren(QLineEdit):
        if "outputfieldname" in le.objectName().lower():
            le.setText("area_ft2")
            log(f"field name set on {le.objectName()}")
            break
    for cb in d.findChildren(QComboBox):
        if "outputfieldtype" in cb.objectName().lower():
            for i in range(cb.count()):
                if "decimal" in cb.itemText(i).lower():
                    cb.setCurrentIndex(i)
                    log(f"field type -> {cb.itemText(i)}")
                    break
    from qgis.PyQt.Qsci import QsciScintilla
    eds = d.findChildren(QsciScintilla)
    log(f"field calc editors: {[e.__class__.__name__ for e in eds]}")
    for e in eds:
        e.setText("$area")
    log(f"expression set on {len(eds)} editors")
    d.show()
    STATE["fcdlg"] = d
    later(3000, s19_field_calc_grab)


def s19_field_calc_grab():
    d = STATE["fcdlg"]
    save_widget(d, "qgis_12_field_calc.png")
    d.close()
    # compute the field for real
    lyr = STATE["vec"]
    da = QgsDistanceArea()
    da.setSourceCrs(lyr.crs(), QgsCoordinateTransformContext())
    da.setEllipsoid("WGS84")
    lyr.startEditing()
    lyr.addAttribute(QgsField("area_ft2", QVariant.Double, len=12, prec=1))
    lyr.updateFields()
    idx = lyr.fields().indexOf("area_ft2")
    for f in lyr.getFeatures():
        a = da.measureArea(f.geometry()) * SQFT_PER_M2
        lyr.changeAttributeValue(f.id(), idx, round(a, 1))
        log(f"{f['name']}: {a:.1f} ft2")
    lyr.commitChanges()
    later(500, s20_attr_table)


def s20_attr_table():
    lyr = STATE["vec"]
    d = iface.showAttributeTable(lyr)
    d.resize(760, 300)
    STATE["attr"] = d
    later(2500, s21_attr_grab)


def s21_attr_grab():
    d = STATE["attr"]
    save_widget(d, "qgis_13_attribute_table.png")
    log("all steps finished")
    QgsProject.instance().setDirty(False)
    os._exit(0)


STEPS = [s01_setup, s02_window, s03_zoom, s04_status_4326, s05_status_4326_grab,
         s06_status_32612_grab, s07_crs_dialog, s08_crs_dialog_grab, s09_project_props,
         s10_measure_line, s11_measure_line_grab, s12_measure_area_grab, s13_new_layer_dialog,
         s14_new_layer_grab, s15_make_layer, s16_trace_grab, s17_done_grab, s18_field_calc,
         s19_field_calc_grab, s20_attr_table, s21_attr_grab]
NEXT = {a.__name__: b for a, b in zip(STEPS, STEPS[1:])}

log("capture started")
later(3000, s01_setup)
