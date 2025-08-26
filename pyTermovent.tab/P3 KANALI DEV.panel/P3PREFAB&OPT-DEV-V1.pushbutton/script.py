# This Python file uses the following encoding: utf-8
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
import Autodesk.Revit.DB as DB
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from Autodesk.Revit.DB.Mechanical import Duct
from pyrevit import forms
from  Autodesk.Revit.DB import BuiltInCategory,ElementId,FilteredElementCollector,Transaction
from FunkcijePrefabrikacije import PrefabrikovanjeElemenata
from PrirubniceSetFunkcija import NadjiPrirubniceSET

if __name__ == '__main__': #GLAVNI PROGRAM - OVDE TREBA ANALIZIRATI KANALE I POZIVATI FUNKCIJU ZA DELJENJE KANALA NA DUZINE I DODAVANJE FITTINGA
    try:
        SelektovaniKanali = [el for el in FilteredElementCollector(doc, uidoc.Selection.GetElementIds()).OfClass(Duct).ToElements() if el.DuctType.GetParameters('Model')[0].AsString()=='P3 - Rectangular']
        SelektovaniFitinzi = [el for el in FilteredElementCollector(doc, uidoc.Selection.GetElementIds()).OfCategory(BuiltInCategory.OST_DuctFitting).ToElements() if el.Symbol.GetParameters('P3 - Code')]
    except:
        forms.alert("PROBLEM PRI UCITAVANJU SELEKCIJE")("PROBLEM PRI UCITAVANJU SELEKCIJE")
    finally:
        
        TRG=TransactionGroup(doc,"P3-PREFABRICATION")
        TRG.Start()
        ElementiNakonPrefabrikacije=PrefabrikovanjeElemenata(SelektovaniKanali)
        SviOdabraniElementi=ElementiNakonPrefabrikacije+SelektovaniFitinzi
        if len(SviOdabraniElementi)==0:
            forms.alert("U ODABIRU NEMA P3 ELEMENATA. IZABERI P3 ELEMENTE!")
        Problematicni=[]
        Rezultat=[]
        for oe in SviOdabraniElementi:
            p=NadjiPrirubniceSET(oe)
            Rezultat.append(p)
            if not p:
                Problematicni.append(oe.Id.IntegerValue)
        if not all(Rezultat):
            forms.alert('Елемент: ID(' + str(Problematicni) +') није добро повезан (СТАВИТИ ЧЕП АКО ЈЕ ОСТАЈЕ НЕПОВЕЗАН)' )
        TRG.Assimilate()







        