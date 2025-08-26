# This Python file uses the following encoding: utf-8
# Import Revit API modules
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Windows_Forma import FormaPrograma
from DodatneFunkcije_Baza import KolektorBAZE
import sys
import System.Windows.Forms as WF
# Get the active Revit document and active view
uiapp = __revit__.ActiveUIDocument
doc=__revit__.ActiveUIDocument.Document    
view = doc.ActiveView
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter
 

if __name__ == '__main__': #GLAVNI PROGRAM
    selektovanoU_revitu=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]   #TREBA NAPRAVITI FILTER SAMO DA CITA ELEMENTE DETAIL ITEMS
    Codes=[el.Symbol.GetParameters('MC User Code')[0].AsValueString() for el in selektovanoU_revitu]
    result = all(map(lambda x: x == Codes[0], Codes)) #provera da li su svi elementi isti
    if len(selektovanoU_revitu)==0:
        WF.MessageBox.Show('НИШТА НИЈЕ СЕЛЕКТОВАНО У РЕВИТУ ! \nСЕЛЕКТУЈ И ПОНОВО ПОКРЕНИ ПРОГРАМ','УПС !')
        sys.exit(1)
    elif not result:
        WF.MessageBox.Show('СЕЛЕКТОВАНИ ЕЛЕМЕНТИ НЕМАЈУ ИСТИ "User Code" ! \nСЕЛЕКТУЈ САМО ЕЛЕМЕНТЕ СА ИСТИМ КОДОМ' ,'УПС !')
        sys.exit(1)
    else:
        par= selektovanoU_revitu[0].Symbol.GetParameters('MC User Code')[0].AsValueString()
    
    Forma=FormaPrograma(par)
    try:
        key=Forma[0]
        keyEL=Forma[1]
        t=Transaction(doc, "Parametar Baza Set")
        t.Start() 
        for el in selektovanoU_revitu:
            paramKEY=el.GetParameters('BAZA')[0]
            paramKEY.Set(keyEL.Id)
        doc.Regenerate()
        t.Commit()

    except:
        sys.exit(1)