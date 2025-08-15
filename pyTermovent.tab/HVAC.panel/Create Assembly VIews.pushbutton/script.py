
# This Python file uses the following encoding: utf-8
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.DB import Transaction
import Autodesk.Revit.DB as DB
from System.Collections.Generic import List # type: ignore

from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInParameter ,BuiltInCategory
from Autodesk.Revit.DB import ElementId
from Autodesk.Revit.DB import AssemblyDetailViewOrientation,XYZ
from pyrevit import revit, DB, forms
doc = revit.doc
import json
import clr
from collections import Counter

clr.AddReference('RevitAPIUI')
uidoc=__revit__.ActiveUIDocument # type: ignore
selectionhand=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()] # type: ignore

view_templates = FilteredElementCollector(doc).OfClass(View).ToElements()
view_template_name_3D= "HANGER 3D Ortho" #
view_template_3D = [v for v in view_templates if v.IsTemplate and v.Name == view_template_name_3D][0]
view_template_name_Sec= "HANGER Section" #
view_template_Sec = [v for v in view_templates if v.IsTemplate and v.Name == view_template_name_Sec][0]
view_template_name_Sec= "HANGER TEMPLATE" #
view_template_SCH = [v for v in view_templates if v.IsTemplate and v.Name == view_template_name_Sec][0]

title_block = None
for symbol in FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_TitleBlocks):
    if symbol.FamilyName == "TERMOVENT - Title Block A3":  # Replace with the name of your desired title block
        title_block = symbol
        break

schedule_category_id = ElementId(BuiltInCategory.OST_MechanicalEquipment)
elements= List[ElementId]()
    
for elementi in selectionhand:
	print(elementi)
	# Get all member IDs of the assembly
	member_ids = elementi.GetMemberIds()
	# Set each member's TK_FAZA_PROJEKTA to match the assembly
	for member_id in member_ids:
			member = doc.GetElement(member_id)
			category_id = member.Category.Id
			print(category_id)

# #Create Assembly
# with revit.Transaction("Create Assembly", doc):
# 	try:
# 		assembly = AssemblyInstance.Create(doc, elements, category_id)
# 	except Exception as e:
# 		print("Failed to create assembly.", e)


	if elementi and elementi.AllowsAssemblyViewCreation():
		with revit.Transaction("Create AssemblyViews", doc):
			print(elementi.Name)
			try:
				orth_view = AssemblyViewUtils.Create3DOrthographic(doc, elementi.Id)
				orth_view.ApplyViewTemplateParameters(view_template_3D)
				elFront_view = AssemblyViewUtils.CreateDetailSection(doc, elementi.Id, AssemblyDetailViewOrientation.ElevationFront)
				elFront_view.ApplyViewTemplateParameters(view_template_Sec)
				elLeft_view = AssemblyViewUtils.CreateDetailSection(doc, elementi.Id, AssemblyDetailViewOrientation.ElevationLeft)
				elLeft_view.ApplyViewTemplateParameters(view_template_Sec)
				schedule = AssemblyViewUtils.CreateSingleCategorySchedule(doc,elementi.Id,schedule_category_id)
				schedule.ApplyViewTemplateParameters(view_template_SCH)
				schedule.Name = elementi.Name + " HANGER PARTLIST"
				sheet = AssemblyViewUtils.CreateSheet(doc, elementi.Id, title_block.Id)
				sheet.Name ="SKLOPNI CRTEZ"
				sheet.SheetNumber = elementi.Name
				
				OR= Viewport.Create(doc, sheet.Id, orth_view.Id, XYZ(1.1,0.5,0))
				FV= Viewport.Create(doc, sheet.Id, elFront_view.Id, XYZ(1.35,0.4,0))
				LV = Viewport.Create(doc, sheet.Id, elLeft_view.Id, XYZ(1.5,0.4,0))
				SV = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, XYZ(1.15,0.9,0))
				
				doc.Regenerate()
			except:
				print("Failed to create views for assembly.",elementi.Name)