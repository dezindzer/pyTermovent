# This Python file uses the following encoding: utf-8
import os, sys
import clr
clr.AddReference("System.IO")
clr.AddReference("System.Drawing")
clr.AddReference("System.Reflection")
clr.AddReference("System.Threading")
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as WF
import System
import System.IO
from System.Drawing import Color, Icon ,Font, FontStyle, Point, Size, FontFamily, Image,Bitmap, Graphics
from System.Windows.Forms import (DataGridViewSelectionMode, Application,  Button, CheckBox,PictureBox,Form, Panel, RadioButton, ComboBox, GroupBox, Label, CheckedListBox, CheckState, FormBorderStyle, DataGridView, DataGridViewAutoSizeRowsMode,DockStyle)

parametri=['Key Name','Oprema','TAG','TIP','ProizvodjacT','Primena','Mesto ugradnje','Napomene']

class Prozor(Form):
    def __init__(self):
        self.Opcija=None
        self.izabrano=None
        self.izlaz=[]
        #Konstruktor FORME
        self.Text="ДОДЕЛА ИНФОМРАЦИЈА ЕЛЕМЕНТУ ИЗ ВАЗЕ ПОДАТАКА"
        self.Font= Font(FontFamily("Arial"),8.0, FontStyle.Regular)
        self.ClientSize=Size(1000,650)
        self.HelpButton = True
        self.FormBorderStyle = FormBorderStyle.FixedDialog #fiksira velicinu forme
        self.MaximizeBox = False
        self.MinimizeBox = False
        #Kreiranje NASLOVA
        self.naslov = Label()
        self.naslov.Text = "ИЗАБЕРИ ЕЛЕМЕНТ :"
        self.naslov.Font= Font(FontFamily("Arial"),12.0, FontStyle.Bold)
        self.naslov.Location = Point(20,20)
        self.naslov.Height = 25
        self.naslov.Width = 500
        self.CenterToScreen()  
        #kreiranje dugmeta1
        self.dugme1=Button()
        self.dugme1.Location=Point(900,550)
        self.dugme1.Size=Size(80,35)
        self.dugme1.Text="ДАЉЕ"
        self.dugme1.BackColor=Color.FromName('White')
        self.dugme1.Enabled=False
        self.dugme1.Click+=self.pritisnutoDugme
        #kreiranje dugmeta2
        self.dugme2=Button()
        self.dugme2.Location=Point(820,550)
        self.dugme2.Size=Size(80,35)
        self.dugme2.Text="ИЗАЂИ"
        self.dugme2.BackColor=Color.FromName('White')
        self.dugme2.Click+=self.pritisnutoCancel

        #######################################
        #kreiranje Padajuce liste Sistema
        self.PadajucaLista=ComboBox()
        self.PadajucaLista.Location = Point(35, 130)
        self.PadajucaLista.DropDownWidth= 450
        self.PadajucaLista.Width= 440
        self.PadajucaLista.Enabled=True
        #######################################
        #kreiranje Padajuce liste Sistema
        self.PreglednaTabela=DataGridView()
        self.PreglednaTabela.Location = Point(20, 70)
        self.PreglednaTabela.Name='LISTA DOSTUPNIH ELEMENATA'
        self.PreglednaTabela.Size=Size(960,430)
        #self.PreglednaTabela.Enabled=True
        #self.PreglednaTabela.AutoSizeRowsMode =DataGridViewAutoSizeRowsMode.DisplayedCellsExceptHeaders

        self.PreglednaTabela.ColumnCount = len(parametri)
        for i in range(0,len(parametri)):
            self.PreglednaTabela.Columns[i].Name=parametri[i]
            self.PreglednaTabela.Columns[i].Width=200
        #self.PreglednaTabela.Columns[4].Width=550
        self.PreglednaTabela.SelectionMode =DataGridViewSelectionMode.FullRowSelect
        self.PreglednaTabela.AllowUserToAddRows = False
        self.PreglednaTabela.AllowUserToOrderColumns = False
        #self.PreglednaTabela.Dock = DockStyle.Fill


        ############################################
        #kreiranje PADAJUCE LISTE 3
        self.PadajucaLista3= CheckedListBox()
        self.PadajucaLista3.HorizontalScrollbar= True
        self.PadajucaLista3.Location = Point(100, 200)
        self.PadajucaLista3.Width=800
        self.PadajucaLista3.Height=300
        self.PadajucaLista3.CheckOnClick = True
        self.PadajucaLista3.Enabled=False 
       
        # LOGO
        self.Velicina=50
        self.LogoPutanja=sys.path[0]+'\T1.png' # nalazi se putanja fajla koji se izvrsava a zatim se dodaje ime LOGO-a.
        self.ima=Image.FromFile(self.LogoPutanja) # pravi se .net Image
        self.bmp=Bitmap(self.ima,self.Velicina,self.Velicina) # pravi se Bitmap(mapa piksela) od slike u odredjenoj velicini
        self.logo = PictureBox() # Pravi se picture Box
        self.logo.Size=Size(self.Velicina,self.Velicina) #definise se velicina Picture Boxa
        self.logo.Location = Point(45,550)
        self.logo.Image=self.bmp #dodaje se slika Bitmap Picture Boxu
        #THUMBNAIL
        self.thumb=Bitmap(self.ima,64,64) #kreira se Bitmap slika u 64x64 formatu za thumbnail
        self.thumb.MakeTransparent()
        self.icon = Icon.FromHandle(self.thumb.GetHicon()) #pravi se ikonica od slike64x64
        self.Icon = self.icon # postavljamo ikonicu na formu 

        #DODAVANJE DUGMADI I GRUPA NA FORMU
        self.Controls.Add(self.PreglednaTabela)
        self.AcceptButton = self.dugme1
        self.CancelButton = self.dugme2
        self.Controls.Add(self.naslov)
        self.Controls.Add(self.dugme1)
        self.Controls.Add(self.dugme2)
        #self.Controls.Add(self.PadajucaLista)
        
        self.Controls.Add(self.logo)
        ##############################
    # Dogadjaj se ucitava iz DodatneFunkcije.py zato sto radi sa metodama iz RevitAPI-ja

    
    def pritisnutoDugme(self,sender,args):
        '''
        DOGADJAJ NA STISNUTO DUGME 'DALJE'  
        '''
        self.izlaz=(self.PreglednaTabela.SelectedRows)

        self.Close()
 

    def pritisnutoCancel(self,sender,args):
        '''
        DOGADJAJ NA STISNUTO IZADJI DUGME

        '''
        self.Status = False
        self.Close()

            
def FormaPrograma(UserCode):      #Kreiranje funkcije u kojoj se kreira objekat klase Prozor i dodeljuju stavke za odabir
    Forma=Prozor()
    Forma.Status=None     # Funkcija FormaPrograma ocekuje Forma.Status, ali ako korisnik iskljuci program na X onda se Status ne definise. Ovim korakom se dodeljuje None dok program ne promeni status u True ili False
    ######  UCITAVANJE LISTE SISTEMA IZ REVITA
    try:
        from DodatneFunkcije_Baza import KolektorBAZE
    except:
        print('Nedostaje modul DodatneFunkcije.py')
    rows=[]
    if KolektorBAZE(UserCode): #popunjava se lista sistema Forme
        ListaElemenata=KolektorBAZE(UserCode)
        for key in ListaElemenata:
            keyEL=ListaElemenata[key] 
            row=[]
            for par in parametri:
                try:
                    Val=keyEL.GetParameters(par)[0].AsValueString()
                except  :
                    Val=''
                row.append(Val)
            rows.append(row)
            Forma.PreglednaTabela.Rows.Add(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]) #PROBLEM . NACI NACIN ZA AUTOMATSKI PRISTUP
            Forma.PreglednaTabela.Refresh()
    else:
        Forma.PreglednaTabela.Text='НЕМА ELEMENATA'  
        ListaElemenata=None


    #row0=['QBM4100-…D','Senzor pritiska','PT','4...20 mA, 3 merna opsega, IP54,  displej kao opcija','kanalski','Siemens','kanal, HEPA filter, sobni senzor za VAV','signal sa manje smetnji, obratiti paznju na merni opseg prema mestu ugradnje I da projektni parametar u sredini opsega, displej kao opcija, ima negativan opseg ali mali sto je problem kod visokih negativnih pritisaka (-50/+50Pa)']
    #row1=['QBM3120-2D','Senzor pritiska','PT','4...20 mA, 3 merna opsega, IP54,  displej kao opcija','kanalski','Siemens','kanal, HEPA filter, sobni senzor za VAV','signal sa manje smetnji, obratiti paznju na merni opseg prema mestu ugradnje I da projektni parametar u sredini opsega, displej kao opcija, ima negativan opseg ali mali sto je problem kod visokih negativnih pritisaka (-50/+50Pa)']
    #row2=['QBM3120-13D','Senzor pritiska','PT','4...20 mA, 3 merna opsega, IP54,  displej kao opcija','kanalski','Siemens','kanal, HEPA filter, sobni senzor za VAV','signal sa manje smetnji, obratiti paznju na merni opseg prema mestu ugradnje I da projektni parametar u sredini opsega, displej kao opcija, ima negativan opseg ali mali sto je problem kod visokih negativnih pritisaka (-50/+50Pa)']

    #rows=[row0,row1,row2]

    #for row in rows:
    Forma.PreglednaTabela.Refresh()

    if rows:
        Forma.dugme1.Enabled=True  # DEAKTIVIRA SE DUGME DALJE JER NEMA NISTA UCITANO ZA TAJ MC User CODE

    Application.EnableVisualStyles()    
    Application.Run(Forma)

    try:
        IzKey=Forma.izlaz.Item[0].Cells[0].Value
        IzEl=ListaElemenata[IzKey]
        return IzKey,IzEl
    except:
        return 


if __name__=='__main__': #ZA TESTIRANJE-NIJE GLAVNI PROGRAM
    UserCode='PT'
    pokrenutUI=FormaPrograma(UserCode)

    #print(pokrenutUI)
    
    
        