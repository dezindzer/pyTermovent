# This Python file uses the following encoding: utf-8
def KolektorBAZE(UserCode):
    '''
    U DICTIONARY SE IZ REVITA VRSI SAKUPLJANJE SVIH POSTOJECIH ELEMENATA U BAZI PODATAKA
    '''
    #parametri=['Oprema','TAG','TIP','Proizvođač T','Model','Opis','Primena/Sistemi','Mesto ugradnje','Kalibracija-Sertifikat','Napomena pro izboru / VAŽNO']

    try:
        from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, ElementId
        doc=__revit__.ActiveUIDocument.Document
        viewid=ElementId(2866399)
        allKeys = FilteredElementCollector(doc,viewid).WhereElementIsNotElementType()
        a={}
        for i in allKeys:
            key=i.get_Parameter(BuiltInParameter.REF_TABLE_ELEM_NAME).AsValueString()
            Tag=i.GetParameters('TAG')[0].AsValueString()
            if Tag == UserCode:
                a[key]=i
            else:
                continue
           
        return a  

    except:
        print('NIJE MOGUC PRISTUP REVITU B')
        return False
