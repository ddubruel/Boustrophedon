import csv
import json
from io import TextIOWrapper
from typing import List
 

def chargeFichierCsv(nomFichier) :
    # Liste pour stocker les lignes
    lignes: list[list[str]] = []
    # ouverture
    fichier : TextIOWrapper = open(nomFichier, "r", encoding="utf-8")
    fichier = open(nomFichier, "r", encoding="utf-8")
    # lecture
    reader = csv.reader(fichier)
    for ligne in reader:
        lignes.append(ligne)  # Ajouter chaque ligne à la liste
    fichier.close()    #fermeture. 
    return lignes

 



def chargeFichierCsvTrie(nomFichier: str, indexColonne: int) -> List[List[str]]:
    
    lignes: list[list[str]] = []
    
    with open(nomFichier, "r", encoding="utf-8") as fichier:
        reader = csv.reader(fichier)
        lignes = list(reader)

    # Vérifie qu'on a au moins une ligne (souvent l'en-tête)
    if len(lignes) <= 1:
        return lignes

    en_tete = lignes[0]
    donnees = lignes[1:]

    # Trie des données selon la colonne choisie
    donnees_triees = sorted(donnees, key=lambda x: x[indexColonne].lower())

    # Retourne l'en-tête suivi des lignes triées
    return [en_tete] + donnees_triees

def lit_fichier_csv_et_separe_entete(nomCsvEntree : str )  -> [list[list[str]], list[str]] :
    """ lit un fichier csv sans son entete"""
    lignes = chargeFichierCsv(nomCsvEntree)
    enteteFichier=lignes[0]
    del lignes[0]
    return lignes, enteteFichier


# ECRITURE CSV :
 
def ecritFichierCsv(nomFichier,data : list[list[str]]) :  
    fichier = open(nomFichier, "w", encoding="utf-8", newline="") # Ouverture
    writer = csv.writer(fichier)  
    for ligne in data:          # Écriture 
        writer.writerow(ligne)
    fichier.close()                # Fermeture    
    print(f"Ecriture du fichier {nomFichier}")
    
def charge_json(nom) :
    fichier = open(nom, "r", encoding="utf-8")                     
    data = json.load(fichier)
    fichier.close()
    return data

def save_json(nom_Fic,data) :
    fichier = open(nom_Fic, "w" , encoding="utf-8" ) 
    json.dump(data, fichier)
    fichier.close()
    print(f"Fichier sauvegardé sous {nom_Fic}")
    
if __name__=='__main__' :
    print("Exécution à l'intérieur du module")
    #nomFicParametres="geo_test.csv"
    #Nb_zones, Nom_Amphi , Nb_Rang , Droite