"""Build the blank final project flight sign-up sheet, to upload to Google Sheets.

Each trip gets one row per drone, because only one of each drone can be out at a time, so a group
signs up for a drone on a trip. Edit FLIGHT_DAYS and DRONES each semester and rerun. The sheet
collects student names, so it is written outside the repository by default and never committed.

    python fig_tools/make_flight_signup.py                      # writes ./final_project_flight_signup.xlsx
    python fig_tools/make_flight_signup.py ~/Desktop/signup.xlsx

The trip rules on docs/final_project/schedule.md and overview.md (Drones) should match.
"""

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

# (day label, [(trip time, most groups allowed on this trip), ...])
FLIGHT_DAYS = [
    ("Thursday, November 12", [("8:00–8:50", 3), ("9:00–9:50", 2)]),
    ("Thursday, November 19", [("8:00–8:50", 2), ("9:00–9:50", 2)]),
]

# One of each is available per trip. Listed in order of demand, most wanted first.
DRONES = ["Thermal (Autel)", "Multispectral", "Mini"]

PERMISSIONS = ["None needed", "LAANC (with TA)", "Property owner", "LAANC + owner"]

COLUMNS = [
    ("Trip Time", 14),
    ("Drone", 17),
    ("Group #", 9),
    ("Project / Site", 30),
    ("Person 1", 16),
    ("Person 2", 16),
    ("TA", 14),
    ("Permission", 18),
]

BLUE = "1F4E79"
HEADER_FILL = PatternFill("solid", fgColor=BLUE)
TRIP_FILL = PatternFill("solid", fgColor="DDEBF7")
THIN = Side(style="thin", color="999999")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def build(out: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Final Project Flights"

    ws["A1"] = "Final Project Flights — be at EB B122 by the start of your trip"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = (
        "Pick one empty drone row on one trip and fill in your group. One of each drone per trip. "
        "The trip leaves on time. Use the Mini unless your project needs thermal or multispectral."
    )
    ws["A2"].font = Font(italic=True, color="555555")

    perm = DataValidation(type="list", formula1='"' + ",".join(PERMISSIONS) + '"', allow_blank=True)
    ws.add_data_validation(perm)

    r = 4
    for day, trips in FLIGHT_DAYS:
        ws.cell(r, 1, day).font = Font(bold=True, size=12)
        groups = sum(n for _, n in trips)
        ws.cell(r, 4, f"{groups} groups this day").font = Font(italic=True, color="555555")
        r += 1
        for col, (name, _) in enumerate(COLUMNS, 1):
            cell = ws.cell(r, col, name)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = HEADER_FILL
            cell.alignment = CENTER
            cell.border = BOX
        r += 1
        for time, most in trips:
            first = r
            for drone in DRONES:
                for col in range(1, len(COLUMNS) + 1):
                    ws.cell(r, col).border = BOX
                    ws.cell(r, col).alignment = CENTER
                ws.cell(r, 2, drone).fill = TRIP_FILL
                perm.add(ws.cell(r, len(COLUMNS)))
                r += 1
            ws.cell(first, 1, f"{time}\n(up to {most} groups)").fill = TRIP_FILL
            ws.merge_cells(start_row=first, start_column=1, end_row=r - 1, end_column=1)
        r += 1

    for i, (_, width) in enumerate(COLUMNS):
        ws.column_dimensions[chr(65 + i)].width = width
    ws.freeze_panes = "A4"

    wb.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("final_project_flight_signup.xlsx"))
