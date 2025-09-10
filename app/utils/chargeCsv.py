import csv
from io import TextIOWrapper
from tkinter import messagebox, filedialog

import tkinter as tk
 
def chargeFichierCsv(nomFichier : str , delimiteur=',') -> list[list[str]] :  
    # Liste pour stocker les lignes
    lignes: list[list[str]] = []
    # ouverture
    fichier : TextIOWrapper = open(nomFichier, "r", encoding="utf-8")
    fichier = open(nomFichier, "r", encoding="utf-8")
    # lecture
    reader = csv.reader(fichier, delimiter = delimiteur)
    for ligne in reader:
        lignes.append(ligne)  # Ajouter chaque ligne à la liste
    fichier.close()    #fermeture. 
    return lignes

def lit_fichier_csv_et_separe_entete(nomCsvEntree : str , delimiteur=',')  -> [list[list[str]], list[str]] :
    """ lit un fichier csv sans son entete"""
    lignes = chargeFichierCsv(nomCsvEntree, delimiteur )
    enteteFichier=lignes[0]
    del lignes[0]
    return lignes, enteteFichier

def choisir_fichier_csv(master ,  titre="Choisir un fichier issu de Apogeé format CSV",rep="."):
    window = tk.Toplevel(master)
    window.withdraw()  # Ne pas afficher cette fenêtre secondaire

    nom_fichier = filedialog.askopenfilename(
        title=titre,
        initialdir=rep,
        filetypes=[("Fichiers CSV", "*.csv")],
    )

    return nom_fichier