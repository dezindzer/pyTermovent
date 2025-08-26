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

            
def FormaPrograma():      #Kreiranje funkcije u kojoj se kreira objekat klase Prozor i dodeljuju stavke za odabir
    Forma=Prozor()

    Application.EnableVisualStyles()    
    Application.Run(Forma)


if __name__=='__main__': #ZA TESTIRANJE-NIJE GLAVNI PROGRAM
    pokrenutUI=FormaPrograma()
    selektovanoU_revitu=[doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

    #print(pokrenutUI)
    
    
        

'''
#OVAJ PROGRAM U REVIT PYTGHON SCHELU PRIKAZTUJE SLICICU TIPA NA UI PROZORU
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
picSize=Size(64,64)

bitmap=s0.Symbol.GetPreviewImage(picSize)
logo=PictureBox()
logo.Size=Size(64,64)
logo.Image=bitmap

logo

proz=Form()
proz.Text="ДОДЕЛА ИНФОМРАЦИЈА ЕЛЕМЕНТУ ИЗ ВАЗЕ ПОДАТАКА"
proz.Font= Font(FontFamily("Arial"),8.0, FontStyle.Regular)
proz.ClientSize=Size(1000,650)
proz.HelpButton = True
proz.FormBorderStyle = FormBorderStyle.FixedDialog #fiksira velicinu forme
proz.MinimizeBox = False

proz.Controls.Add(logo)



Application.EnableVisualStyles()    
Application.Run(proz)

'''