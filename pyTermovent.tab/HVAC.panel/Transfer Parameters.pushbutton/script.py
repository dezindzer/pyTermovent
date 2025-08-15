from pyrevit import revit, DB, forms
from pyrevit.forms import ProgressBar
from rpw.ui.forms import FlexForm, Label, TextBox, Button#, ComboBox, Separator, CheckBox
import re
doc = revit.doc

components = [
    Label ("Assembly name contains:"),
    TextBox("assembly_name_contains", Text="VIS"),
    Label ("Override parameter:"),
    TextBox("override_param", Text="TK_FAZA_PROJEKTA"),
    Button("Ok")
]
form = FlexForm("Search", components)
textSearchWindow = form.show()
assembly_name_contains = str(form.values["assembly_name_contains"])
override_param = str(form.values["override_param"])

# Get all assemblies
assembly_instances = DB.FilteredElementCollector(doc) \
    .OfClass(DB.AssemblyInstance) \
    .ToElements()

max_value = len(assembly_instances)
counter = 0
with ProgressBar(cancellable=True, title='Analiziram ... ({value} of {max_value})') as progressbar:
	with revit.Transaction("Faziranje elemenata", doc):
		for assembly in assembly_instances:
			if progressbar.cancelled:
				break
			else:
				counter += 1
				name = assembly.Name
				#filter assembly by name containing
				if re.search(assembly_name_contains, name, re.IGNORECASE):
				# visilice = [e for e in assembly_types if re.search(r"VIS", get_name(e), re.IGNORECASE)]
					# Get the assembly's TK_FAZA_PROJEKTA parameter value
					assembly_param = assembly.LookupParameter(override_param)
					if assembly_param:
						assembly_value = assembly_param.AsString()
						# Get all member IDs of the assembly
						member_ids = assembly.GetMemberIds()
					# Set each member's TK_FAZA_PROJEKTA to match the assembly
					for member_id in member_ids:
							member = doc.GetElement(member_id)
							member_param = member.LookupParameter(override_param)
							if member_param and assembly_value is not None:
								member_param.Set(assembly_value)
			progressbar.update_progress(counter, max_value)