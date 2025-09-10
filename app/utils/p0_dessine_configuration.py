import tkinter as tk

import os
import sys

# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__)
#
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)
    
# ajoute le répertoire de sortie des images. 
cheminRelatif="../../data/png_out"
app_dir = os.path.abspath(os.path.join(current_dir, cheminRelatif))

if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)
    

from utils.gestion_json 						import sauvFicJson, chargFicJson
from classes.classe_Grille_de_cases 			import Grille_de_cases
from classes. classe_definition_amphitheatre	import definition_amphitheatre


def reconstruire_interface(root, data , result_dict):
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



    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    scroll_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
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

def chargFicJson_et_reconstruire(fenetre, result_dict):
    data = chargFicJson(fenetre)
    if data:
        reconstruire_interface(fenetre, data, result_dict)
        
def definitListeAmphi(zones) :
    nbZones=len(zones)                   
    if nbZones == 2 :
        AMPHI = [  'Mathématiques', 'Sc_Physiques', 'Chimie', 'Sc_Naturelles','Informatique']
    elif nbZones == 3 :        
        AMPHI = ['Petit_Valrose']    
    return AMPHI

def compter_cases_cochees(grillesDeZone, Nb_label):
    nb = 0
    for grille in grillesDeZone:
        for ligne in grille.vars:
            for var in ligne:
                if var.get() == 1:
                    nb += 1
    Nb_label.config(text=f"Total : {nb}")

def extraction_liste_cases_cochees (fenetre , grillesDeZone ,  nomAmphi  ) :
    listeCasesCocheesPourToutesLesZones=[]
    print( f"nomAmphi (dans extraction_liste etc )  = {nomAmphi}")
   
    for grille in grillesDeZone:
        # Traitement des zones Gauche et Centre pour tous les amphis :            
        listePourUneZone=[]
        if grille.titre=='Gauche' or grille.titre=='Centre' :
            for row, ligne in enumerate(grille.vars):
                for col, var in enumerate(ligne):
                    if var.get() == 1:
                        listePourUneZone.append((row, col))
        # Traitement de la zone Droite du 'Petit_Valrose' :                
        elif grille.titre=='Droite' and  'Petit_Valrose' in nomAmphi :
            for row, ligne in enumerate(grille.vars):
                if row<= 14 :
                    for col, var in enumerate(ligne):
                        if var.get() == 1:
                            listePourUneZone.append((row, col))            
                elif row > 14  :  # on décale un peu la numérotation
                    for col, var in enumerate(ligne  ):
                        if var.get() == 1:
                            listePourUneZone.append( (row ,col  + grille.nb_cases - grille.nb_cases//2 ))
        else :
            for row, ligne in enumerate(grille.vars):
                for col, var in enumerate(ligne):
                    if var.get() == 1:
                        listePourUneZone.append((row, col))
            
        listeCasesCocheesPourToutesLesZones.append(listePourUneZone)    
    return listeCasesCocheesPourToutesLesZones


    


def main(parent, amphi_initial, zones, nb_places, Nb_rang):
    result_dict = {} # le dictionnaire qui va récolter les données de main() ou reconstruire_interface()

    fenetre = tk.Toplevel(parent, bg='lightgray')
    fenetre.title("Remplissage des zones")
    largeur,hauteur=900 , 900
    fenetre.geometry(f"{largeur}x{hauteur}")
    
    AMPHI=[f"{amphi_initial}"] # uniquement pour bio et géo qui sont différents.
    if len(zones)!=1 :
        AMPHI=definitListeAmphi(zones)    
    nomAmphi_var = tk.StringVar(value=f"{amphi_initial}")
    choix_amphi = tk.StringVar(value=amphi_initial)
    
    label_amphi = tk.Label(fenetre,
                           textvariable=nomAmphi_var,
                           font=("Arial", 20),
                           name="label_amphi")    
    label_amphi.pack(pady=(10,0))
    
    canvas = tk.Canvas(fenetre)
    scrollbar = tk.Scrollbar(fenetre, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)        

    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

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
        
    Nb_label = tk.Label(scroll_frame, text="", font=("Arial", 9))
    btn_total = tk.Button(scroll_frame, text="Calcul total de places",
                          command=lambda: compter_cases_cochees(grillesDeZone, Nb_label))
    btn_total.pack(pady=10)
    Nb_label.pack(pady=10)
    
    btn_sauv = tk.Button(scroll_frame, text="Sauvegarde configuration",
                         command=lambda: sauvFicJson(fenetre, grillesDeZone, zones, nb_places, Nb_rang, choix_amphi.get()))
    btn_sauv.pack(padx=10)
    
    btn_charge = tk.Button(scroll_frame, text="Charge configuration",
                           command=lambda: chargFicJson_et_reconstruire(fenetre, result_dict))
    btn_charge.pack(padx=10)
        
    # Bouton de sortie
    tk.Button(scroll_frame, text="Cliquer ici quand vos paramètres sont bien définis pour passer à la prochaine étape.", command=fenetre.destroy ).pack(padx=100)
    
    # SORTIE DES INFO A LA FERMETURE DE LA FENETRE.
    parent.wait_window(fenetre)  # attend la fermeture de la fenêtre
    
    if result_dict:   # le dictionnaire est rempli si l'utilisateur a chargé un fichier d'un amphi
        return (result_dict["listeCasesCochees"], result_dict["nb_places"],
                result_dict["Nb_rang"], result_dict["nomAmphi"])
    else :
        nomAmphi=nomAmphi_var.get()
        listeCasesCocheesPourToutesLesZones = extraction_liste_cases_cochees (fenetre ,
                                                                              grillesDeZone ,
                                                                              nomAmphi )
        print(f"listeCasesCochees ={listeCasesCocheesPourToutesLesZones}")
    return listeCasesCocheesPourToutesLesZones, nb_places, Nb_rang, nomAmphi

def Main_Etape_0_bis(master):
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



def Main_Etape_0(master):    
    amphi_initial, zones, nb_places , Nb_rang = Main_Etape_0_bis(master)
    listeCasesCocheesPourToutesLesZones, nb_places, Nb_rang, nomAmphi=main(master,
                                                                           amphi_initial,
                                                                           zones,
                                                                           nb_places,
                                                                           Nb_rang) # pour réactualiser ces données
    
    return listeCasesCocheesPourToutesLesZones, nb_places, Nb_rang, nomAmphi , zones


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    amphi_initial, zones, nb_places , Nb_rang = Main_Etape_0_bis(root)    

    listeCasesCocheesPourToutesLesZones, nb_places, Nb_rang, nomAmphi = main(root,
                                                                             amphi_initial,
                                                                             zones,
                                                                             nb_places,
                                                                             Nb_rang)
    
    print("Dans l'auto test ", nb_places, Nb_rang)
    print(f"listeCasesCocheesPourToutesLesZones (ligne, colonne)  = {listeCasesCocheesPourToutesLesZones}")
    print ("fin auto test \n")
    root.mainloop()
