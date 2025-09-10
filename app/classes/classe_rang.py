import os
import sys
# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__) 
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)

from utils.pour_classe_rangs import save_canvas

class rangs:     
    def __init__(self, canvas, xhg,yhg,DATA_zone,longueur,espace,prefixeZone,couleurZone,Nom_Amphi,referencePlace,liste_nom_fic_png):
        self.canvas = canvas
        self.xhg = xhg   # abscisse coin haut à gauche
        self.yhg = yhg
        self.DATA_zone=DATA_zone
        self.nrang= int(DATA_zone[2]) # nb de rangs
        self.longueur=longueur
        self.espace=espace      # espace entre 2 bancs
        self.prefixeZone=prefixeZone
        self.referencePlace=referencePlace
        self.liste_nom_fic_png=liste_nom_fic_png
        self.couleurZone=couleurZone
        self.Nom_Amphi=Nom_Amphi
        
    def dessine(self):                
        x0=self.xhg
        y0=self.yhg
        x1=x0+self.longueur
        y1=y0
        for k in range(1, self.nrang+1 ,1) :            
            y0=self.yhg +(k-1)* self.espace   # k=1 vaut yhg puis yhg+decalage etc...
            y1=y0
            self.canvas.create_line(x0, y0, x1, y1, width=2)

    def placeEtudiant(self):
          
        # pour info DATA_zone=[Nb_zones, Nom_Amphi , Nb_Rang , Gauche]
        # Gauche = "numero du rang; nb d étudiant ; nb maxi ; alignement"
        Nb_zones=self.DATA_zone[0]
        nrang=self.DATA_zone[2]
        zone = self.DATA_zone[3]
        alpha_num=self.DATA_zone[-1]
        for k in range(self.nrang , 0, -1 ) :
            N_etu_maxi=zone[k-1][2]        
            N_etu_rang=zone[k-1][1]            
            pasX= 0.8* self.longueur // (N_etu_maxi-1)  # espace entre 2 étudiants          
            numRang=(self.nrang+1  - k)   #on inverse l'ordre le numéro 1 est en bas !!!            
            for l in range(1 , 1+N_etu_rang) :   # commencer à 1 pour le (l-1)*pasX>0  pour xtex=
                    
                    if  zone[k-1][3] =='d' :# cas d'alignement à gauche
                        if alpha_num=='alpha' :
                            texte=f"{self.prefixeZone}-{numRang}{str(chr(64+ l))}" # lettre commençant par  (chr65=A pour l=1) !!
                            self.referencePlace.append(texte)
                        elif alpha_num=='num':
                            texte=f"{self.prefixeZone}-{numRang}-{l}" # lettre commençant par  (chr65=A pour l=1) !!
                            self.referencePlace.append(texte)
                        else :
                            raise ValueError("Paramètre alpha_num mal défini dans fichier d'entrée !")
                        
                        xtex= self.xhg + int(0.9 * (self.longueur) ) - (l-1)* pasX
                        ytex= self.yhg +(k-1)* self.espace                    
                        self.canvas.create_text(xtex, ytex-10,text=texte) #décalage de 10 pour éviter la ligne
                    elif zone[k-1][3] =='g' :# cas d'alignement à droite
                        if alpha_num=='alpha' :
                            texte=f"{self.prefixeZone}-{numRang}{str(chr(64+ N_etu_maxi-l+1) )}" # lettre commençant par  (chr65=A pour l=1) !!
                            self.referencePlace.append(texte)
                        elif alpha_num=='num':
                            texte=f"{self.prefixeZone}-{numRang}-{N_etu_maxi-l+1}"
                            self.referencePlace.append(texte)
                        else :
                            raise ValueError("Paramètre alpha_num mal défini dans fichier d'entrée !")
                            
                        xtex= self.xhg + int(0.9 * (self.longueur) ) - (N_etu_maxi-l)* pasX
                        ytex= self.yhg +(k-1)* self.espace                    
                        self.canvas.create_text(xtex, ytex-10,text=texte) #décalage de 10 pour éviter la ligne
            if self.prefixeZone=='C' :                
                    ytex= self.yhg +(k-1)* self.espace 
                    self.canvas.create_text(self.xhg-20, ytex-10 ,text=f"{numRang}", fill="blue")                                       
                    self.canvas.create_text(self.xhg +20 +self.longueur, ytex-10 ,text=f"{numRang}", fill="blue")                
            if self.prefixeZone=='G' :
                    ytex= self.yhg +(k-1)* self.espace 
                    self.canvas.create_text(self.xhg-20, ytex-10 ,text=f"{numRang}", fill="blue")                                       
                    #self.canvas.create_text(self.xhg +20 +self.longueur, ytex-10 ,text=f"{numRang}", fill="blue")                
            if self.prefixeZone=='D' :                    
                    ytex= self.yhg +(k-1)* self.espace 
                    #self.canvas.create_text(self.xhg-20, ytex-10 ,text=f"{numRang}", fill="blue")                                       
                    self.canvas.create_text(self.xhg +20 +self.longueur, ytex-10 ,text=f"{numRang}", fill="blue")  
                
                        
    def entourePlace(self):
        
        # pour info DATA_zone=[Nb_zones, Nom_Amphi , Nb_Rang , Gauche]
        # Gauche = "numero du rang; nb d étudiant ; nb maxi ; alignement ;  N_etudiants, alpha_num " 
        Nb_zones=self.DATA_zone[0]
        nrang=self.DATA_zone[2]
        zone = self.DATA_zone[3]
        alpha_num = self.DATA_zone[-1]
        for k in range(self.nrang , 0, -1 ) :
            N_etu_maxi=zone[k-1][2]        
            N_etu_rang=zone[k-1][1]
            pasX= 0.8* self.longueur // (N_etu_maxi-1)  # espace entre 2 étudiants 
            numRang=(self.nrang+1  - k)   #on inverse l'ordre le numéro 1 est en bas !!!
            for l in range(1 , 1+N_etu_rang) :   # commencer à 1 pour le (l-1)*pasX>0  pour xtex=
 
                if  zone[k-1][3] =='d' :# cas d'alignement à droite
                    if alpha_num=='alpha' :
                        nomFicPng=f"./data/png_out/{self.Nom_Amphi}-{self.prefixeZone}-{numRang}{str(chr(64+ l))}.png" # lettre commençant par  (chr65=A pour l=1) !!
                        self.liste_nom_fic_png.append(nomFicPng)
                    elif alpha_num=='num':
                        nomFicPng=f"./data/png_out/{self.Nom_Amphi}-{self.prefixeZone}-{numRang}-{l}.png" # lettre commençant par  (chr65=A pour l=1) !!
                        self.liste_nom_fic_png.append(nomFicPng)
                    xtex= self.xhg + int(0.1 * (self.longueur) ) + (N_etu_maxi-l)* pasX
                    ytex= self.yhg +(k-1)* self.espace                
                elif zone[k-1][3] =='g' : # cas d'alignement à gauche
                    if alpha_num=='alpha' :
                        nomFicPng=f"./data//png_out/{self.Nom_Amphi}-{self.prefixeZone}-{numRang}{str(chr(64+ N_etu_maxi-l+1) )}.png" # lettre commençant par  (chr65=A pour l=1) !!
                        self.liste_nom_fic_png.append(nomFicPng)
                    elif alpha_num=='num':
                        nomFicPng=f"./data/png_out/{self.Nom_Amphi}-{self.prefixeZone}-{numRang}-{N_etu_maxi-l+1}.png"
                        self.liste_nom_fic_png.append(nomFicPng)
                    xtex= self.xhg + int(0.1 * (self.longueur) ) + (l-1)* pasX
                    ytex= self.yhg +(k-1)* self.espace
                R=28
                xC=xtex
                yC=ytex-10                                                            
                self.ref = self.canvas.create_oval(xC-1.4*R,yC-R,xC+1.4*R, yC+R,  outline='red',width=3)  
                self.canvas.winfo_toplevel().update() #root.update()
                self.canvas.after(200)
                save_canvas(nomFicPng, self.canvas)                    
                self.canvas.delete(self.ref) # Effacer juste le cercle après la capture
                    
    def colorieZone(self):
        if self.couleurZone!="":
            x0=self.xhg
            y0=self.yhg   -self.espace     
            x1=self.xhg+self.longueur
            y1=self.yhg+(self.nrang-1)* self.espace            
            rect=self.canvas.create_rectangle(x0, y0 , x1, y1, fill=self.couleurZone)            
            self.canvas.lower(rect)

    def retire_banc_PV(self,canvas) :
        Nb_zones=self.DATA_zone[0]
        if Nb_zones==3 : # pour le PV uniquement !!
            x_m=self.xhg + self.longueur//2 
            y_m=self.yhg  + (self.nrang-3)* self.espace            
            if self.prefixeZone=='G' :
                x_g=self.xhg+self.longueur
                y_g=self.yhg+(self.nrang-1)* self.espace               
                rect=canvas.create_rectangle(x_m, y_m+1 , x_g+2, y_g+2, fill='white',outline='')            
                
            if self.prefixeZone=='D' :
                x_d=self.xhg 
                y_d=self.yhg+(self.nrang-1)* self.espace
                rect=canvas.create_rectangle(x_m+2, y_m+1 , x_d-2, y_d+2, fill='white',outline='') 