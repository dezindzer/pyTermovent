
# This Python file uses the following encoding: utf-8
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.DB import Transaction
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List

from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInParameter ,BuiltInCategory
from Autodesk.Revit.DB import ElementId
from Autodesk.Revit.DB import AssemblyDetailViewOrientation,XYZ

import json
import clr
from collections import Counter

clr.AddReference('RevitAPIUI')
uidoc=__revit__.ActiveUIDocument
doc=__revit__.ActiveUIDocument.Document
s=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

view_templates = FilteredElementCollector(doc).OfClass(View).ToElements()
view_template_name_3D= "HANGER 3D Ortho" #
view_template_3D = [v for v in view_templates if v.IsTemplate and v.Name == view_template_name_3D][0]
view_template_name_Sec= "HANGER Section" #
view_template_Sec = [v for v in view_templates if v.IsTemplate and v.Name == view_template_name_Sec][0]
view_template_name_Sec= "HANGER TEMPLATE" #
view_template_SCH = [v for v in view_templates if v.IsTemplate and v.Name == view_template_name_Sec][0]

title_block = None
for symbol in FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_TitleBlocks):
    if symbol.FamilyName == "TERMOVENT - Title Block A4":  # Replace with the name of your desired title block
        title_block = symbol
        break

schedule_category_id = ElementId(BuiltInCategory.OST_MechanicalEquipment)
elements= List[ElementId]()
for i in s:
	elements.AddRange(i.GetSubComponentIds())
	for e in i.GetSubComponentIds():
		elements.AddRange(doc.GetElement(e).GetSubComponentIds())
	elements.Add(i.Id)
	category_id = i.Category.Id
t = Transaction(doc, "Create Assembly")
t.Start()

try:
	assembly = AssemblyInstance.Create(doc, elements, category_id)
	t.Commit()
except Exception as e:
	print("Failed to create assembly.", e)
	t.RollBack()


if assembly and assembly.AllowsAssemblyViewCreation():
	tcav = Transaction(doc, "Create AssemblyViews")
	tcav.Start()
	#print(assembly.Name)
	try:
		orth_view = AssemblyViewUtils.Create3DOrthographic(doc, assembly.Id)
		orth_view.ApplyViewTemplateParameters(view_template_3D)
		elFront_view = AssemblyViewUtils.CreateDetailSection(doc, assembly.Id, AssemblyDetailViewOrientation.ElevationFront)
		elFront_view.ApplyViewTemplateParameters(view_template_Sec)
		elLeft_view = AssemblyViewUtils.CreateDetailSection(doc, assembly.Id, AssemblyDetailViewOrientation.ElevationLeft)
		elLeft_view.ApplyViewTemplateParameters(view_template_Sec)
		schedule = AssemblyViewUtils.CreateSingleCategorySchedule(doc,assembly.Id,schedule_category_id)
		schedule.ApplyViewTemplateParameters(view_template_SCH)
		schedule.Name = assembly.Name + " HANGER PARTLIST"
		sheet = AssemblyViewUtils.CreateSheet(doc, assembly.Id, title_block.Id)
		sheet.Name ="SKLOPNI CRTEZ"
		sheet.SheetNumber = assembly.Name

		OR= Viewport.Create(doc, sheet.Id, orth_view.Id, XYZ(1.1,0.5,0))
		FV= Viewport.Create(doc, sheet.Id, elFront_view.Id, XYZ(1.35,0.4,0))
		LV = Viewport.Create(doc, sheet.Id, elLeft_view.Id, XYZ(1.5,0.4,0))
		SV = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, XYZ(1.15,0.9,0))

		doc.Regenerate()
	except Exception as e:
		print("Failed to create views for assembly.",e)
		tcav.RollBack()

	tcav.Commit()
#####################################################