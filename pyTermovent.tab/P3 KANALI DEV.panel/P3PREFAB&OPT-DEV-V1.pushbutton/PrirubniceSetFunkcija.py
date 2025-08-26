# This Python file uses the following encoding: utf-8

def NadjiPrirubniceSET(element):
    '''
    OVA FUNNKCIJA NA ULAZU OCEKUJE REVIT ELEMENT, A NA IZLAZU UPISUJE PARAMETAR * * Flange SA BROJEM -1,0,1,2
    -1 - NEMA PRUBNICA
    0 - STANDARDNA
    1 - U PRIRUBNICA
    2 - F PRIRUBNICA

    Funkcija se moze zvati samo ukoliko je u toku transakcija ili Subtransakcija
    '''
    import clr
    from  Autodesk.Revit.DB import BuiltInParameter,ElementId,FilteredElementCollector,Transaction
    from  Autodesk.Revit.DB import PartType
    doc=__revit__.ActiveUIDocument.Document 
    clr.AddReference('RevitAPIUI')
    uidoc=__revit__.ActiveUIDocument

    dozvoljenaKategorija=['Duct Fittings',  'Duct Accessories', 'Air Terminals', 'Ducts','Mechanical Equipment']
    konektori=[]
    Nekonektovani=[]
    #ISPITUJE SE ELEMENT NA ULAZU FUNKCIJE KOJE JE KATEGORIJE - U ZAVISNOSTI OD KATEGORIJE DRUGACIJE SE CITA KOJI SU KONEKTORI
    if element.Category.Name=='Duct Fittings': 
        k=element.MEPModel.ConnectorManager.Connectors		
        TipElementa=doc.GetElement(element.GetTypeId())
        KODelementa=TipElementa.GetParameters('P3 - Code')[0].AsInteger() # Ne treba Try jer je na ulazu element koji sigurno ima vrednost P3Code-a
        if KODelementa == 843:       #Ukoliko je Cap element funkcije ovim se prekida i vraca praznu listu nastavku programa . 
            return False  
    elif element.Category.Name=='Ducts':
        k=element.ConnectorManager.Connectors
        dozvoljenaKategorija=dozvoljenaKategorija[0:3]
        KODelementa=None
    else: 
        print('Kategorija elementa nije dobra')
        exit(1)

    for ElKon in k:
        if ElKon.IsConnected:
            konektori.append(ElKon)
        else:
            Nekonektovani.append(ElKon)
    if len(Nekonektovani) != 0:  #AKO JE LISTA NEKONEKTOVANIH KONEKTORA VECA OD 0 , FUNKCIJA VRACA FALSE I PREKIDA SE ZA TAJ ELEMENT.
        return False
    
    UklonjeniKonektori=[]
    for Kon in konektori:  #PROLAZI SE KROZ SVAKI KONEKTOR ELEMENTA
        TipSeta=None
        try:
            parW=doc.GetElement(Kon.GetMEPConnectorInfo().GetAssociateFamilyParameterId(ElementId(BuiltInParameter.CONNECTOR_WIDTH)))
        except:
            parW=None
        for Par in Kon.AllRefs:  #PROLAZI SE KROZ SVE UPARENE KONEKTORE TOG KONEKTORA (MOZE BITI VISE KONEKTORA KONEKTOVANO NA OVAJ KONEKTOR npr. IZOLACIJA)
            if Par.Owner.Category.Name in dozvoljenaKategorija:  # ISPITUJE SE DA LI JE KONEKTOVANI ELEMENT U DOZVOLJENIM KATEGORIJAMA
                tip=doc.GetElement(Par.Owner.GetTypeId())     #CITA SE TIP KONEKTOVANOG FITINGA
                model=tip.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL).AsString()  #CITA SE MODEL TIPA KONEKTOVANOG FITINGA
                if Par.Owner.Category.Name == 'Duct Fittings':
                    try:
                        paramF=tip.GetParameters('P3 - Code')[0].AsInteger()
                    except:
                        paramF=None
                    finally:
                        if KODelementa == 812 and not Kon.GetMEPConnectorInfo().IsPrimary:
                            TipSeta='0'
                        elif KODelementa == 812 and Kon.GetMEPConnectorInfo().IsPrimary and paramF==801:
                            TipSeta='2'
                        elif paramF == 812 and Par.GetMEPConnectorInfo().IsPrimary:  # U ovom slucaju se uzima konektovani konektor cipelice (PAR) jer konektor uboda cita dimenziju kanala a ne otvora od cipelice
                            TipSeta='1'
                        elif model == 'P3-TAP' and Par.GetMEPConnectorInfo().IsPrimary:
                            TipSeta='1'
                        elif paramF ==812 and not Par.GetMEPConnectorInfo().IsPrimary:
                            TipSeta='0'
                        elif model == 'P3-TAP'and not Par.GetMEPConnectorInfo().IsPrimary:
                            TipSeta='2'
                        elif paramF ==843:
                            UklonjeniKonektori.append(Kon) # ODSTRANJUJE SE KONEKTOR KOJI PRIPADA END CAP-u ili CEPU JER NA NJEGA NE IDE PRIRUBNICA
                        elif Par.Owner.MEPModel.PartType == PartType.Union or paramF:
                            TipSeta='0'
                elif Par.Owner.Category.Name == 'Ducts':
                    if KODelementa == 812 and Kon.GetMEPConnectorInfo().IsPrimary:   #ako je primaran konektor elementa onda je ubod u kanal , u svakom drugom slucaju ako je P3 kanal onda je  S
                        TipSeta='2'
                    elif model == 'P3 - Rectangular':
                        TipSeta='0'
                elif Par.Owner.Category.Name == 'Duct Accessories':
                    try:
                        paramDA=Par.Owner.GetParameters('TK_SetTipPrirubnice')[0].AsString()
                        if paramDA.upper()=='U':
                            TipSeta='1'
                        elif paramDA.upper()=='F':
                            TipSeta='2'
                    except:
                        TipSeta='1'
                elif Par.Owner.Category.Name == 'Air Terminals':
                    TipSeta='2'
                elif Par.Owner.Category.Name == 'Mechanical Equipment':
                    TipSeta='1'
                else:
                    print('KATEGORIJA KONEKTOVANOG ELEMENTA NIJE DOZVOLJENA')
                    exit(1)

        if parW!=None and TipSeta!=None:
            
            try:
                Param=element.GetParameters(parW.Name +' Flange')[0]
                Param.Set(TipSeta)
            except:
                return False
                #Tr=Transaction(doc, "P3 - FLANGES SET") #--TRANSAKCIJA
                #Tr.Start()   #--TRANSAKCIJA
                #Param.Set(TipSeta)
                #Tr.Commit()
        

    return True

if __name__=='__main__':   #TEST PROGRAM KOJI TESTIRA FUNKCIJU NadjiPrirubnice NA POJEDINACNOM ELEMENTU A ZATIM PRAVI PRIRPREMLJENU LISTU ZA IZLAZ I ISPIS.
    
    import clr
    from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory,Transaction,TransactionGroup
    doc=__revit__.ActiveUIDocument.Document
    clr.AddReference('RevitAPIUI')
    uidoc=__revit__.ActiveUIDocument
    doc=__revit__.ActiveUIDocument.Document

    SelektovaniFitinzi = [el for el in FilteredElementCollector(doc, uidoc.Selection.GetElementIds()).OfCategory(BuiltInCategory.OST_DuctFitting).ToElements() if el.Symbol.GetParameters('P3 - Code')]
    Rezultat=[]
    Problematicni=[]
    Tr=TransactionGroup(doc, "P3 - FLANGES SET")  #--TRANSAKCIJA
    Tr.Start()   #--TRANSAKCIJA
    for kan in SelektovaniFitinzi: 
        p=NadjiPrirubniceSET(kan)
        Rezultat.append(p)
        if not p:
            Problematicni.append(kan.Id.IntegerValue)

    if all(Rezultat):
        Tr.Commit()
    else:
        Tr.RollBack()
        print('Елемент: ID(' + str(Problematicni) +') није добро повезан (СТАВИТИ ЧЕП АКО ЈЕ ОСТАЈЕ НЕПОВЕЗАН) или није из P3 програма производа' )
