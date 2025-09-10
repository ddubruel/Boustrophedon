# ECRITURE CSV :
import csv
def ecritFichierCsv(nomFichier,data : list[list[str]]) : 
    fichier = open(nomFichier, "w", encoding="utf-8", newline="") # Ouverture
    writer = csv.writer(fichier)  
    for ligne in data:          # Écriture 
        writer.writerow(ligne)
    fichier.close()                # Fermeture    
    print(f"Ecriture du fichier {nomFichier}")