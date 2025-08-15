
# This Python file uses the following encoding: utf-8
from pyrevit import revit, DB, script, forms
#from pyrevit.framework import List
from itertools import izip
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, Separator, CheckBox
import sys, clr
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, BuiltInCategory, ElementId, AssemblyDetailViewOrientation, XYZ
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from System.Collections.Generic import List # type: ignore

doc = revit.doc
clr.AddReference('RevitAPIUI')
uidoc=__revit__.ActiveUIDocument # type: ignore
def Canceled():
    forms.alert('User canceled the operation', title="Canceled", exitscript=True)
#    Canceled() 

selectionhand=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()] # type: ignore


viewPlans = FilteredElementCollector(doc).OfClass(ViewPlan) 
viewports = FilteredElementCollector(doc).OfClass(Viewport) 

def vPt(ViewTypez):
    return {v.Name: v for v in viewPlans if v.IsTemplate == True and v.ViewType == ViewTypez}

#Dictionary
floorplan_template_dict = vPt(ViewType.FloorPlan)
floorplan_template_dict["<None>"] = None
section_template_dict = vPt(ViewType.Section)
section_template_dict["<None>"] = None
threeD_template_dict = vPt(ViewType.ThreeD)
threeD_template_dict["<None>"] = None
schedule_template_dict = vPt(ViewType.Schedule)
schedule_template_dict["<None>"] = None
titleblocks = DB.FilteredElementCollector(revit.doc).OfCategory(DB.BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType()
tblock_dict = {'{}: {}'.format(tb.FamilyName, revit.query.get_name(tb)): tb for tb in titleblocks}
tblock_dict["<None>"] = None

schedule_category_id = ElementId(BuiltInCategory.OST_MechanicalEquipment)
elements= List[ElementId]()

#Define menu

components = [
    Label ("Select Titleblock"),
    ComboBox(name="tb", options=sorted(tblock_dict)), #default="Papir A2: A2 - SRB"),
    Separator(),
    Label("View Template for Floor Plans"),
    ComboBox(name="vt_floor_plans", options=sorted(floorplan_template_dict)), #default="Osnova 1.50"),
    Label("View Template for Sections Plans"),
    ComboBox(name="vt_section_plans", options=sorted(section_template_dict)),
    Label("View Template for 3D Views"),
    ComboBox(name="vt_3d_views", options=sorted(threeD_template_dict)),
    Separator(),
	Label("View Template for Schedule"),
    ComboBox(name="vt_schedule", options=sorted(schedule_template_dict)),
    Label(""),
    CheckBox(name="Breskvica", checkbox_text="Play me", default=True),
    Button("Ok")
]

form = FlexForm("View Settings", components)

viewSettings = form.show()

if viewSettings == True:
    chosen_tb = tblock_dict[form.values["tb"]]
    chosen_vt_floor_plan = floorplan_template_dict[form.values["vt_floor_plans"]]
    chosen_vt_section_plan = section_template_dict[form.values["vt_section_plans"]]
    chosen_vt_3d_view = threeD_template_dict[form.values["vt_3d_views"]]
    chosen_vt_schedule = schedule_template_dict[form.values["vt_schedule"]]

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
				orth_view.ApplyViewTemplateParameters(chosen_vt_3d_view)
				elFront_view = AssemblyViewUtils.CreateDetailSection(doc, elementi.Id, AssemblyDetailViewOrientation.ElevationFront)
				elFront_view.ApplyViewTemplateParameters(chosen_vt_section_plan)
				elLeft_view = AssemblyViewUtils.CreateDetailSection(doc, elementi.Id, AssemblyDetailViewOrientation.ElevationLeft)
				elLeft_view.ApplyViewTemplateParameters(chosen_vt_section_plan)
				schedule = AssemblyViewUtils.CreateSingleCategorySchedule(doc, elementi.Id, schedule_category_id)
				schedule.ApplyViewTemplateParameters(chosen_vt_schedule)
				schedule.Name = elementi.Name + " HANGER PARTLIST"
				sheet = AssemblyViewUtils.CreateSheet(doc, elementi.Id, chosen_tb.Id)
				sheet.Name ="SKLOPNI CRTEZ"
				sheet.SheetNumber = elementi.Name
				
				OR= Viewport.Create(doc, sheet.Id, orth_view.Id, XYZ(1.1,0.5,0))
				FV= Viewport.Create(doc, sheet.Id, elFront_view.Id, XYZ(1.35,0.4,0))
				LV = Viewport.Create(doc, sheet.Id, elLeft_view.Id, XYZ(1.5,0.4,0))
				SV = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, XYZ(1.15,0.9,0))
				
				doc.Regenerate()
			except:
				print("Failed to create views for assembly.",elementi.Name)