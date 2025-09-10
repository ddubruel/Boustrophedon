import tkinter as tk

import os
import sys
# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__) 
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)

from classes.classe_GrilleDeCases			import GrilleDeCases
from utils.gestion_json  import sauvFicJson, chargFicJson
from  utils.support_classe_graphiqueGrilleAmphi import  extraction_liste_cases_cochees
from  utils.support_classe_graphiqueGrilleAmphi import  convertitCaseCocheeEnDico

class graphiqueGrilleAmphiRempli :
    def __init__(self, fenetre , data , fctRappelValider = None )  :
        self.fenetre=fenetre
        self.data = data
        self.fctRappelValider = fctRappelValider
        
        self.grillesDeZone =  [ ]  # on le reconstruit avec les instanciations des classes.
                        
        self._init_interface()   # pour usage interne avec le _ 
         
#		Rappel de la structure si besoin :
#		  self.zones     = data["zones"]
#         self.nb_places = data["nb_places"]
#         self.Nb_rang   = data["Nb_rang"]
#         self.amphi     = data["amphi"]
#         if len(data)==5 : # cas où l'utilisateur a chargé
#                           # le fichier amphi avec les places                              
#             self.grilles = data["grilles"]

    def _init_interface(self):
        
        self.zone_grille = tk.Frame(self.fenetre)
        self.zone_grille.pack(fill=tk.BOTH, expand=True)        
         
        self.canvas  = tk.Canvas(self.zone_grille)
        self.scrollbar = tk.Scrollbar(self.zone_grille, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>",
                          lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.grilles_frame = tk.Frame(self.scroll_frame)
        self.grilles_frame.pack()
        
        label_amphi = tk.Label(self.grilles_frame, text=self.data["amphi"], font=("Arial", 20))
#        label_amphi = tk.Label(self.grilles_frame, text='PROUT', font=("Arial", 20))
        label_amphi.pack(pady=10)
               
        for i in range( len(self.data["zones"]) ) : 
            grille = GrilleDeCases(self.grilles_frame,
                                     nb_cases  = self.data["nb_places"][i],
                                     nb_lignes = self.data["Nb_rang"],
                                     titre     = self.data["zones"][i],
                                     nomAmphi  = self.data["amphi"] 
                                     )
            self.grillesDeZone.append(grille)
        
        if "grilles" in self.data.keys() :
            self.grilles_data = self.data["grilles"] # dictionnaire cle=zone
                                            #         valeur : liste de cases cochée
            # transfère dans les grilles des cases  présentes dans
            # self.grilles_data = data["grilles"]  (voir début __init__)
            for row, col in self.grilles_data.get(self.data["zones"][i], []): # parcourt de la liste des cases cochées
                if row < len(grille.vars) and col < len(grille.vars[row]):
                    grille.vars[row][col].set(1)
                                             
        self.Nb_label = tk.Label(self.scroll_frame, text="", font=("Arial", 9))
        btn_total = tk.Button(self.scroll_frame, text="Calcul total de places",
                              command= self._compterCasesCochees )
        btn_total.pack(pady=10)
        self.Nb_label.pack(pady=10)
        # Conteneur horizontal pour les boutons
        btn_frame = tk.Frame(self.scroll_frame)
        btn_frame.pack(pady=10)
        
        btn_sauv = tk.Button(btn_frame, text="Sauvegarde \n configuration.",
                             command=lambda: sauvFicJson(self.fenetre,
                                                         self.grillesDeZone,
                                                         self.data["zones"],
                                                         self.data["nb_places"],
                                                         self.data["Nb_rang"],
                                                         self.data["amphi"]
                                                         )
                             )        
        btn_sauv.pack(side=tk.LEFT, padx=5)
        
        
        # Bouton de visualiation
        btn_visu= tk.Button(btn_frame,
                  text="Visualisation \n configuration",
                  command = self.validationConfiguration )
        btn_visu.pack(side=tk.LEFT, padx=5)
        # Bouton de fermeture
        btn_fermeture = tk.Button(btn_frame,
                  text="Fermeture \n (si la visualisation vous convient !)",
                  command = self.effaceGrille )
        btn_fermeture.pack(side=tk.LEFT,  padx=5)
        
    def _compterCasesCochees(self):
        nb = 0
        for grille in self.grillesDeZone:
            for ligne in grille.vars:
                for var in ligne:
                    if var.get() == 1:
                        nb = nb + 1
        self.Nb_label.config(text=f"Total : {nb}")

    
    def validationConfiguration(self):
        # récupération à la liste des cases cochées (les coordonnées (ligne,colonne) en liste)
        # fonction importée
        caseCochees = extraction_liste_cases_cochees( self.grillesDeZone ,  self.data["amphi"])
        # On ajoute la nouvelle données pour la "remonter" à la classe parente.
        self.data["grilles"]= convertitCaseCocheeEnDico( caseCochees ,
                                                         self.data["zones"] )    
#        self.effaceGrille()
        
        if self.fctRappelValider :
            self.fctRappelValider(self.data) # on remonte les data vers la classe 
                                     # qui a instancié cette classe
        else :
            print("Pas de retour   dans l'autotest, la frame va être effacée.")
            
    def effaceGrille(self):
        if self.zone_grille:
            self.zone_grille.destroy()
            self.zone_grille = None
        # on crée le bouton de fermeture quand les grilles sont effacées dans un frame
        self.frame_bas = tk.Frame(self.fenetre) 
        self.frame_bas.pack(pady=20)
        btn_visu= tk.Button(self.frame_bas,
                  text="Fermeture de cette fenetre. \n Retour au tableau des étapes.",
                  command = self.fenetre.destroy )
        btn_visu.pack(pady=20)
        print('FINI')
        #
        
            
if __name__=='__main__':
    cas=3
    
    
    if cas == 1 : # cas amphi Petit_Valrose vide
        data = {
        "zones": ['Gauche','Centre','Droite'] ,   # liste   ex : ['Gauche','Centre','Droite']
        "nb_places": [6,7,6],  #  [6,7,6] pour le PV.
        "Nb_rang": 17 ,      
        "amphi": 'Petit_Valrose' ,
         }
    elif cas == 2 : # amphi 1 zone
        data = {'amphi': 'Biologie', 'zones': ['Centre'], 'nb_places': [4], 'Nb_rang': 10,
         'grilles': {'Centre': [[1, 0], [1, 1], [1, 2], [1, 3], [3, 0], [3, 1], [3, 2],
                                [3, 3], [5, 0], [5, 1], [5, 2], [5, 3], [7, 0], [7, 1],
                                [7, 2], [7, 3], [9, 0], [9, 1], [9, 2], [9, 3]]}
         }
    elif cas == 3 : # amphi 2 zones
        data = {'amphi': 'Sc_Naturelles',
         'zones': ['Gauche', 'Droite'],
         'nb_places': [6, 6],
         'Nb_rang': 14,
         'grilles': {'Gauche': [[1, 0], [1, 1], [13, 4], [13, 5]],
                     'Droite': [[1, 0], [1, 1], [13, 1], [13, 5]] }
         }
    elif cas == 4 : # amphi 3 zones
        data = {'amphi': 'Petit_Valrose', 'zones': ['Gauche', 'Centre', 'Droite'], 'nb_places': [5, 6, 5], 'Nb_rang': 17,
         'grilles': {'Gauche': [[0, 0],  [16, 1]],
                     'Centre': [[0, 0], [0, 1],  [16, 4], [16, 5]],
                     'Droite': [[0, 0], [14, 3],  [16, 1]]  }
         }
    print("\n Data définies dans l'autotest : \n ", data ,'\n\n')
    root=tk.Tk()
    graphiqueGrilleAmphiRempli(root,data)
    
    root.mainloop()
    
# Ci après ancien code si besoin , avec un A devant le nom pour éviter
# tout appel involontaire...


def Areconstruire_interface(root, data , result_dict):
    for widget in root.winfo_children():
        widget.destroy()

    zones = data["zones"]
    nb_places = data["nb_places"]
    Nb_rang = data["Nb_rang"]
    amphi = data["amphi"]
    grilles_data = data["grilles"]

    AMPHI=[f"{amphi}"] # uniquement pour bio et géo qui sont différents.
    if len(zones)!=1 :
        AMPHI=definitListeAmphi(zones)  
    
    choix_amphi = tk.StringVar(value=amphi)
    nomAmphi_var = tk.StringVar(value=f"{amphi}")

    # Label dynamique
    label_amphi = tk.Label(root, textvariable=nomAmphi_var, font=("Arial", 20))
    label_amphi.pack(pady=(10, 0))



    self.canvas = tk.Canvas(root)
    self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
    self.canvas.configure(yscrollcommand=self.scrollbar.set)

    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll_frame = tk.Frame(self.canvas)
    self.canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    scroll_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=canvas.bbox("all")))
    grilles_frame = tk.Frame(scroll_frame)
    grilles_frame.pack()
    
    grillesDeZone = []
 
 
        
    for i, zone in enumerate(zones):
        grille = Grille_de_cases(grilles_frame,
                                 nb_cases=nb_places[i],
                                 nb_lignes=Nb_rang,
                                 titre=zone,
                                 nomAmphi=nomAmphi_var.get() # chaine du genre 'Amphithéatre Chimie'
                                 )
                                 
        grillesDeZone.append(grille)
        # recupère les cases si présentes dans le fichier
        cases_cochees = grilles_data.get(zone, [])
        for row, col in grilles_data.get(zone, []):
            if row < len(grille.vars) and col < len(grille.vars[row]):
                grille.vars[row][col].set(1)

    # Calcul du total
    Nb_label = tk.Label(scroll_frame, text="", font=("Arial", 9))
    btn_total = tk.Button(scroll_frame, text="Calcul total de places",
                          command=lambda: compter_cases_cochees(grillesDeZone, Nb_label))
    btn_total.pack(pady=10)
    Nb_label.pack(pady=10)
    # Sauvegarde
    btn_sauv = tk.Button(scroll_frame, text="Sauvegarde configuration",
                         command=lambda: sauvFicJson(root, grillesDeZone, zones, nb_places, Nb_rang, choix_amphi.get()))
    btn_sauv.pack(padx=10)

    # Chargement
    btn_charge = tk.Button(scroll_frame, text="Charge configuration",
                           command=lambda: chargFicJson_et_reconstruire(root))
    btn_charge.pack(padx=10)
    
    # Bouton de sortie
    tk.Button(scroll_frame,
              text="Cliquer ici quand vos paramètres sont bien définis pour passer à la prochaine étape.",
              command=root.destroy ).pack(padx=100)
    root.wait_window(root)  # attend la fermeture de la fenêtre
    nomAmphi=nomAmphi_var.get()
    # SORTIE DES INFO A LA FERMETURE DE LA FENETRE.    
    listeCasesCocheesPourToutesLesZones = extraction_liste_cases_cochees (root , grillesDeZone , nomAmphi )
    print(f"listeCasesCochees ={listeCasesCocheesPourToutesLesZones}")
    
    #Astuce on dépose les variables mises à jour dans le dictionnaire, elle sont mutables
    # et donc seront visibles aussi pour le retour de main().
    result_dict.update({
        "listeCasesCochees": listeCasesCocheesPourToutesLesZones,
        "nb_places": nb_places,
        "Nb_rang": Nb_rang,
        "nomAmphi": nomAmphi
    })

def AchargFicJson_et_reconstruire(fenetre, result_dict):
    data = chargFicJson(fenetre)
    if data:
        reconstruire_interface(fenetre, data, result_dict)
        
def AdefinitListeAmphi(zones) :
    nbZones=len(zones)                   
    if nbZones == 2 :
        AMPHI = [  'Mathématiques', 'Sc_Physiques', 'Chimie', 'Sc_Naturelles','Informatique']
    elif nbZones == 3 :        
        AMPHI = ['Petit_Valrose']    
    return AMPHI






    




def AMain_Etape_0_bis(master):
    tousLesAmphis = ['Biologie', 'Géologie', 'Mathématiques',
                     'Sc_Physiques', 'Chimie', 'Sc_Naturelles',
                     'Informatique', 'Petit_Valrose']
    
    data = definition_amphitheatre(master, tousLesAmphis)

    master.wait_window(data.fenetre_choix)  # attend la fermeture de la fenêtre

    amphi_initial = data.selection_amphi.get()
    zones = data.zones
    nb_places = data.nb_places
    Nb_rang = data.nbRang

    print("Amphi :", amphi_initial)
    print("Zones :", zones)
    print("Places :", nb_places)
    print("Rangs :", nb_places)
    return amphi_initial, zones, nb_places , Nb_rang



def AMain_Etape_0(master):    
    amphi_initial, zones, nb_places , Nb_rang = Main_Etape_0_bis(master)
    listeCasesCocheesPourToutesLesZones, nb_places, Nb_rang, nomAmphi=main(master,
                                                                           amphi_initial,
                                                                           zones,
                                                                           nb_places,
                                                                           Nb_rang) # pour réactualiser ces données
    
    return listeCasesCocheesPourToutesLesZones, nb_places, Nb_rang, nomAmphi , zones


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()
#     amphi_initial, zones, nb_places , Nb_rang = Main_Etape_0_bis(root)    
# 
#     listeCasesCocheesPourToutesLesZones, nb_places, Nb_rang, nomAmphi = main(root,
#                                                                              amphi_initial,
#                                                                              zones,
#                                                                              nb_places,
#                                                                              Nb_rang)
#     
#     print("Dans l'auto test ", nb_places, Nb_rang)
#     print(f"listeCasesCocheesPourToutesLesZones (ligne, colonne)  = {listeCasesCocheesPourToutesLesZones}")
#     print ("fin auto test \n")
#     root.mainloop()
