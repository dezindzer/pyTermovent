# -*- coding: utf-8 -*-

from pyrevit import revit, DB  # type: ignore
import clr  # type: ignore
import sys, os
from datetime import datetime

# Excel interop
clr.AddReference("Microsoft.Office.Interop.Excel")  # type: ignore
import Microsoft.Office.Interop.Excel as Excel  # type: ignore

# .NET Environment for Desktop path
import System  # type: ignore

uidoc = revit.uidoc  # type: ignore
doc = revit.doc  # type: ignore

# pick a schedule
from pyrevit import forms  # type: ignore
schedules = [v for v in DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule)]  # type: ignore
schedule = forms.SelectFromList.show(
    sorted(schedules, key=lambda v: v.Name),  # type: ignore
    name_attr='Name',
    title='Odaberi ViewSchedule za izvoz u Excel'
)
if not schedule:
    sys.exit()

# read table body
table_data = schedule.GetTableData()  # type: ignore
section = table_data.GetSectionData(DB.SectionType.Body)  # type: ignore
rows = section.NumberOfRows  # type: ignore
cols = section.NumberOfColumns  # type: ignore
if rows == 0 or cols == 0:
    forms.alert("Izabrani raspored nema podataka.", exitscript=True)  # type: ignore

# start Excel
excel = Excel.ApplicationClass()  # type: ignore
excel.Visible = True  # type: ignore
wb = excel.Workbooks.Add()  # type: ignore
sheet = wb.ActiveSheet  # type: ignore

# sanitize sheet name (Excel forbids :/\?*[] and length > 31)
def sanitize_sheet_name(name):
    bad = ':/\\?*[]'
    safe = ''.join('_' if ch in bad else ch for ch in (name or 'Sheet1'))
    return (safe or 'Sheet1')[:31]

sheet.Name = sanitize_sheet_name(schedule.Name)  # type: ignore

# header from first body row (index 0)
header_values = [
    schedule.GetCellText(DB.SectionType.Body, 0, c)  # type: ignore
    for c in range(cols)
]
for c, text in enumerate(header_values):
    sheet.Cells(1, c + 1).Value2 = text  # type: ignore
sheet.Range(sheet.Cells(1, 1), sheet.Cells(1, cols)).Font.Bold = True  # type: ignore  # bold header

# write data rows, skipping completely empty rows
excel_row = 2
for r in range(1, rows):
    row_values = [
        schedule.GetCellText(DB.SectionType.Body, r, c)  # type: ignore
        for c in range(cols)
    ]
    if any(val for val in row_values):  # only export if not all empty
        for c, text in enumerate(row_values):
            sheet.Cells(excel_row, c + 1).Value2 = text  # type: ignore
        excel_row += 1

# autosize
sheet.Columns.AutoFit()  # type: ignore

# format as Excel table (header in row 1, data ends at excel_row-1)
last_row = excel_row - 1
last_col = cols
if last_row > 1:  # only create table if there’s data
    table_range = sheet.Range(
        sheet.Cells(1, 1),  # type: ignore
        sheet.Cells(last_row, last_col)  # type: ignore
    )
    # Use explicit enums for clarity
    src = Excel.XlListObjectSourceType.xlSrcRange  # type: ignore
    yes = Excel.XlYesNoGuess.xlYes  # type: ignore
    list_obj = sheet.ListObjects.Add(src, table_range, None, yes)  # type: ignore
    list_obj.Name = "RevitSchedule"  # type: ignore
    try:
        list_obj.TableStyle = "TableStyleMedium2"  # type: ignore
    except Exception:
        pass

# --- Automatic file save to Desktop/Excel Export ---
# Desktop path (handles localized Desktop folders via .NET)
desktop = System.Environment.GetFolderPath(System.Environment.SpecialFolder.Desktop)  # type: ignore
export_dir = os.path.join(desktop, "Excel Export")
if not os.path.isdir(export_dir):
    os.makedirs(export_dir)

# File name: %SheetName%+%Datetime%.xlsx  (Datetime = YYYY-MM-DD_HHMM)
safe_sheetname = sanitize_sheet_name(schedule.Name)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = "{}_{}.xlsx".format(safe_sheetname, timestamp)
fullpath = os.path.join(export_dir, filename)

# Save as .xlsx (OpenXML workbook)
try:
    wb.SaveAs(fullpath, Excel.XlFileFormat.xlOpenXMLWorkbook)  # type: ignore
except Exception as e:
    forms.alert("Greška pri snimanju fajla:\n{}\n\nPokušaj da zatvoriš otvorene fajlove sa istim imenom i probaj ponovo.".format(e))  # type: ignore

# Tip: ostavljamo Excel otvoren (Visible=True) po originalnoj logici
# Ako želiš automatsko zatvaranje:
# wb.Close(SaveChanges=True)  # type: ignore
# excel.Quit()  # type: ignore