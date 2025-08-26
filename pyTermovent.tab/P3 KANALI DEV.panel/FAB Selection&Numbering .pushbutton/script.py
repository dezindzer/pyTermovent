##### MORA POSTOJATI PARAMETAR TK_DICT U PROJECT INFORMATION KAO I TK_SELEKCIJA U ELEMENTIMA
##### TK_DICT PARAMETAR JE JSON STRING KOJI SE KORISTI ZA POHRANU PODATAKA O ELEMENTIMA
##### TK_SELEKCIJA PARAMETAR JE STRING KOJI SE KORISTI ZA POHRANU PODATAKA O ELEMENTIMA U TK_DICT
##### TK_FAZA_PROJEKTA PARAMETAR JE STRING KOJI SE KORISTI ZA POHRANU FAZE PROJEKTA
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.DB import Transaction

from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInParameter  
from Autodesk.Revit.DB import ElementId

import json
import clr
from collections import Counter

clr.AddReference('RevitAPIUI')
uidoc=__revit__.ActiveUIDocument
doc=__revit__.ActiveUIDocument.Document
s=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]


DictPar=doc.ProjectInformation.GetParameters('TK_DICT')[0]
try:
	DictParString=doc.ProjectInformation.GetParameters('TK_DICT')[0].AsString()
	DICT = json.loads(DictParString)
except:
	
	DICT={}
Tr=Transaction(doc,'FAB SLEKECIJA%NUMBERING')
Tr.Start()
list=[]

for el in s:
	p=el.GetParameters('TK_SELEKCIJA')[0]
	string="#"
	pin=el.GetParameters('Item Number')[0]
	pf=el.GetParameters('TK_FAZA_PROJEKTA')[0].AsValueString()
	type_id = el.GetTypeId()
	type_element = doc.GetElement(type_id)
	pal = type_element.GetParameters("Type Mark")[0].AsValueString()
	#ps=el.GetParameters('Specification')[0].AsValueString()
	pis=el.GetParameters('Insulation Specification')[0].AsValueString()
	pfs=el.GetParameters('Fabrication Service')[0].AsValueString()
	
	DimStr=''
	for i in el.GetDimensions():
		DimStr+=str(el.GetDimensionValue(i))
		DimStr+="#"
	konektori={}
###### OVAJ DEO ZAKOMENTARISATI KADA SE RADI SA SPIRO PROGRAMOM
	for i in el.ConnectorManager.Connectors:
		fi=i.GetFabricationConnectorInfo()
		konektori[fi.FabricationIndex]=fi.BodyConnectorId
	konstr=str(konektori)
	string+=konstr
###### OVAJ DEO ZAKOMENTARISATI KADA SE RADI SA SPIRO PROGRAMOM
	ProductName=el.ProductName
	
	if ProductName == 'Rectangular Duct':
		string=pal+"#"+pis+"#"+pfs+"#"+DimStr+konstr
		#print('PRAVOUGAONI')
	else:
		string=pal+"#"+pfs+"#"+DimStr
		#print('KRUZNI')
	
	prefixes = [key.split("#")[0] for key in DICT.keys()]
	prefix_counts = Counter(prefixes)
	br=prefix_counts[pal]
	try:
		val=DICT[string]
	except:
		DICT[string]=str(pal)+str(br)

	print(DICT[string])
	p.Set(string)
	pin.Set(DICT[string])

json_string = json.dumps(DICT, indent=4)
DictPar.Set(json_string)

Tr.Commit()

########################################################


