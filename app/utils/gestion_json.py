import tkinter as tk
from tkinter import filedialog
import json
import os
import sys

# Ajoute le dossier "data" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
# current_dir =   os.path.dirname(__file__) 
# app_dir = os.path.abspath(os.path.join(current_dir, "../../data/Configurations_Amphi"))
# if app_dir not in sys.path :    
#     sys.path.insert(0, app_dir)
# 
# app_dir = os.path.abspath(os.path.join(current_dir, "/data/Configurations_Amphi"))

def DemandeNomFichierJsonPourChargement  (master ,
                          titre="Choisir un fichier de configuration json",
                          rep="data"):
    
    window = tk.Toplevel(master)
    window.withdraw()  # Ne pas afficher cette fenêtre secondaire

    nom_fichier = filedialog.askopenfilename(
        title=titre,
        initialdir=rep,
        filetypes=[("Fichiersjson", "*.json")],
    )
    return nom_fichier

def chargeConfig(nomFic):
    try:
        with open(nomFic, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data  # renvoie le dictionnaire complet !
    except FileNotFoundError:
        print("Fichier json '{nomFic}' introuvable.")
        return None
    
def charge_json(nomFic):
    try:
        with open(nomFic, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data  # renvoie le dictionnaire complet !
    except FileNotFoundError:
        print("Fichier json '{nomFic}' introuvable.")
        return None

def save_json(nomFic,donnees) :
    try:
        with open(nomFic, "w") as f:
            json.dump(donnees, f)
    except FileNotFoundError:
        print("Ecriture du fichier {nomFic} impossible.")
 

def chargFicJson(fenetre):
    # DEMANDER FICHIER A CHARGER....
    nomFic=DemandeNomFichierJsonPourChargement(fenetre) 
    alldata = chargeConfig(nomFic)
    return alldata
    
#%
#% ECRITURE JSON
#%
def DemandeNomFichierJsonPourSauvegarde(master,                               
                              titre="Enregistrer un fichier de configuration json",
                              rep="data",
                              nom_defaut="config.json"):
    # S'assurer que le répertoire existe
    os.makedirs(rep, exist_ok=True)

    # Boîte de dialogue pour choisir où enregistrer le fichier
    window = tk.Toplevel(master)
    window.withdraw()  # Ne pas afficher la fenêtre

    nom_fichier = filedialog.asksaveasfilename(
        title=titre,
        initialdir=rep,
        initialfile=nom_defaut,
        defaultextension=".json",
        filetypes=[("Fichiers JSON", "*.json")],
    )
    if nom_fichier:  # Si l'utilisateur n'annule pas
        return nom_fichier
    else :
        return None 
    
    
def sauvegardeConfig( nomFic , grillesDeZone ,  zones , nb_places , Nb_rang , amphi ):                    
    # on construit un dictionnaire avec les clé étant le nom des variables
    # et la valeur, le contenu des variables.
    
    sauvegarde = {
        "amphi": amphi,
        "zones": zones,
        "nb_places": nb_places,
        "Nb_rang": Nb_rang,
        "grilles": {}  # utiliser un dict avec les titres
    }

    for grille in grillesDeZone:
        cases_cochees = []
        for row, ligne in enumerate(grille.vars):
            for col, var in enumerate(ligne):
                if var.get() == 1:
                    cases_cochees.append([row, col])
        sauvegarde["grilles"][grille.titre] = cases_cochees

    with open(nomFic, "w") as f:
        json.dump(sauvegarde, f)
    print("Configuration sauvegardée.")

def sauvFicJson(fenetre,grillesDeZone, zones, nb_places, Nb_rang, amphi ):
        # DEMANDER FICHIER A SAUVEGARDER....
    nomFic = DemandeNomFichierJsonPourSauvegarde(fenetre)
    sauvegardeConfig( nomFic, grillesDeZone,  zones, nb_places, Nb_rang, amphi )
     