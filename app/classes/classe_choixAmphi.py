import tkinter as tk
from tkinter import messagebox
import os
import sys
# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__) 
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)

from classes.classe_definitionZonePlacesRangNomAmphi import definitionZonePlacesRangNomAmphi
#from classes.classe_graphiqueGrilleAmphi import graphiqueGrilleAmphi
from classes.classe_graphiqueGrilleAmphiRempli import graphiqueGrilleAmphiRempli 
from utils.gestion_json  import sauvFicJson, chargFicJson 
    
class choixAmphi :
    """definition de l'interface de configuration de
    l'amphi. Affiche dans une fenêtre dédié le choix du nom
    de l'amphi et demande si il est vide ou si c'est un projet
    déja existant. Les attributs de la classe qui vont être définis :
    -le nom de l'ammphi
    -les grilles de remplissage par zone de l'amphi"""
    
    def __init__(self,parent , largeur , hauteur, amphiDuFichierApogee, fctRappelVersMain = None ) :
        self.root =  tk.Toplevel(parent, bg='lightgray')
        self.root.geometry(f"{largeur}x{hauteur}")
        self.root.title ("Choix et définition de l'amphithéatre")
        self.fctRappelVersMain = fctRappelVersMain
        self.data = {} # ce dictionnaire va être rempli.
        self.graphiqueGrille = None                
        self.amphi = amphiDuFichierApogee 
        self.construireWidgets()
                 
    def chargeAmphiExistant(self, parent ) :
        self.data  = chargFicJson(parent)
        # on crée une instance de grille mais vide.
        self.remplitGrilles(parent)
    
    def remplitGrilles(self,parent) :
        # renvoie un dictionnaire comme par exemple :        
        #{'amphi': 'Petit_Valrose',
        # 'zones': ['Gauche', 'Centre', 'Droite'],
        # 'nb_places': [6, 7, 6],
        # 'Nb_rang': 17,
        # 'grilles': {'Gauche': [[16, 2]], 'Centre': [[16, 1]], 'Droite': [[16, 1]]}
        # }                
        def fctRappelValiderAmphiExistant(data):
            self.zones     = data["zones"]
            self.nb_places = data["nb_places"]
            self.Nb_rang   = data["Nb_rang"]
            self.amphi     = data["amphi"]
            if "grilles" in data.keys():
                self.grilles   = data["grilles"]
            # Quand l'utilisateur aura cliqué sur valider dans l'instance 1, la fonction
            # de rappel  est éxécutée et permet de passer à la suite.           
            if self.fctRappelVersMain : 
                self.fctRappelVersMain(data) # on retourne vers le main()
                                         # qui a instancié cette classe
            else :
                print("Pas de retour vers main() dans l''autotest.")
            # fin fonction de rappel
            
        # on affiche la ou les grilles pour cocher les places.
        if  self.graphiqueGrille :
            # elles ont été crées alors on peut les effacer
                self.graphiqueGrille.effaceGrille()
                           
        self.graphiqueGrille=graphiqueGrilleAmphiRempli(self.root, self.data , fctRappelValiderAmphiExistant )
                
    def definitParamAmphi(self):
        """ méthode appellée par le bouton de droite "définition d'un amphi vide" """        
        listeAmphi= ['Biologie', 'Géologie',
                     'Sc_Physiques', 'Chimie',
                     'Sc_Naturelles', 'Informatique',
                    'Mathématiques' ,'Petit_Valrose']                
        def fctRappelValider(data):
            self.data["zones"]     = data["zones"]
            self.data["nb_places"] = data["nb_places"]
            self.data["Nb_rang"]   = data["Nb_rang"]
            self.data["amphi"]     = data["amphi"]           
            self.remplitGrilles(self.root)                            
        definitionZonePlacesRangNomAmphi(self.root, listeAmphi , fctRappel=fctRappelValider , data = None )
        
    def messageTest(self,text) :
        messagebox.showinfo("Succès", text)
        
    def construireWidgets(self):
        
        tk.Label(self.root, text=f"Le fichier étudiant concerne l'amphithéatre {self.amphi}",
                       font=("Arial", 9, "bold")).pack(pady=10) 
        # Frame en haut
        frameEnHaut=tk.Frame(self.root)
        frameEnHaut.pack(pady=5) # Frame étendue horizontalement si option fill=tk.X 
        
        l1 = tk.Label(frameEnHaut, text="Choix de l'amphithéatre :")
        l1.grid(row=0, column=0,columnspan=2)
        
        # 2 premiers boutons
        b1 = tk.Button( frameEnHaut,
                        text="Charge Amphithéatre \n pré-rempli."
                                "\n Le nombre d'étudiant"
                               " \n par rang est figé.\n"
                               "Ajout ou retrait d'étudiants possible.",
                        command=lambda: self.chargeAmphiExistant(self.root))
        
        b1.grid(row=1, column=0, padx = 20) #pack(padx = 20 ,pady=10)
        b2 = tk.Button(frameEnHaut, text="Amphithéatre \n"
                       " vide.\n"
                       "L'utilisateur définit le nombre \n"
                       "d'étudiants par rang.",
                           command=lambda: self.definitParamAmphi())
        b2.grid(row=1, column=1,padx = 20) #pack(pady=10)
               
if __name__=="__main__" :
    root = tk.Tk()
    root.withdraw()
    
    choixAmphi(root,largeur = 1200,hauteur=1200)    
    root.mainloop()
    