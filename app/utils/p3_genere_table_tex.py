import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox

import json
import os

# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__)
#
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)
    

from utils.module_gestion_fichiers import  charge_json, chargeFichierCsv,ecritFichierCsv
from utils.module_genere_table_tex  import lit_csv_etudiants_placés_et_génère_table_tex
from utils.module_genere_table_tex  import ecrit_table_tex
from utils.module_Generer_et_compiler_fichier_tex import generer_fichier_latex, compiler_latex


def choisir_fichier_csv(master ,  titre="Choisir un fichier CSV",rep="./Data_csv_in"):
    window = tk.Toplevel(master)
    window.withdraw()  # Ne pas afficher cette fenêtre secondaire

    nom_fichier = filedialog.askopenfilename(
        title=titre,
        initialdir=rep,
        filetypes=[("Fichiers CSV", "*.csv")],
    )

    return nom_fichier

def definit_nom_et_cree_table_tex(nom_fichier,nom_amphi,zone) :
    nom_fichier_final= f"./tex_out/Emargements_{nom_amphi}_zone_{zone}.tex"
    latex_filename=f"./tex_out/table_{nom_amphi}_{zone}.tex"         
    # nb de case du tableau sur la page (18 au max !!)
    lit_csv_etudiants_placés_et_génère_table_tex(
           nom_fichier  ,
           latex_filename ,
           nb_ligne_tableau = 18 ,
           tri = False ,
           colonne = 0) 
    return nom_fichier_final,latex_filename

def definit_nom_et_cree_table_tex_pour_amphi(nom_fichier,nom_amphi) :
    nom_fichier_final= f"./tex_out/Emargements_{nom_amphi}.tex"
    latex_filename=f"./tex_out/table_{nom_amphi}.tex"         
    # nb de case du tableau sur la page (18 au max !!)
 
    return nom_fichier_final,latex_filename


def definit_zone(nom_fichier):
    print("nom_fichier" , nom_fichier )
    # on retire le chemin 
    nom_seul_csv=""
    for k in range(len(nom_fichier)-1,0,-1):   # l'extension .csv !!
        if nom_fichier[k]!='/' :
            nom_seul_csv=nom_fichier[k] + nom_seul_csv
        else :
            break
    print(nom_seul_csv)
    if "_G" in nom_seul_csv :
        return "G"
    elif "_D" in nom_seul_csv :
        return  "D"
    elif "_C" in nom_seul_csv :
        return "C"
    else :
        raise ValueError(f"pb dans les zones, il manque peut être le  fichier  nommé : {nom_seul_csv}")


def lit_fichier_pour_entetes_listes_emargement(master):
    nomCsv_data=choisir_fichier_csv(master, "Fichier csv contenant les données de l'épreuve : ","./Data_csv_in/Entete_liste_emargement" )
    print("fichier choisi : ", nomCsv_data )
    data = chargeFichierCsv(nomCsv_data)
    #print(data)
    annee_universitaire	=data[0][1]
    date				=data[1][1] 
    horaires			=data[2][1]
    duree				=data[3][1]
    salle				=data[4][1]
    lieu				=data[5][1]
    batiment			=data[6][1]
    epreuve				=data[7][1]
    matiere				=data[8][1]
    
    
    return annee_universitaire,date, horaires,duree,salle,lieu,batiment,epreuve,matiere
    
def definit_scale_et_angle(Nb_zones):
    if Nb_zones==1 :
        return 0.9, 0 
    elif Nb_zones==2 :
        return 0.7, 90 
    elif Nb_zones==3  :
        return 0.47, 90 
        
def Main_etape_3(master ,
                 liste_fichier_par_zone,
                 nom_Fic_zones,
                Nom_Amphi,
                Nb_zones,
                nomFicPngPlanAmphi):
    
    annee_universitaire,date, horaires,duree,salle,lieu,batiment,epreuve,matiere = lit_fichier_pour_entetes_listes_emargement(master)
    
 
    for nom_fichier in liste_fichier_par_zone  :    
        zone = definit_zone(nom_fichier)
        nom_fichier_final,latex_filename = definit_nom_et_cree_table_tex( nom_fichier, Nom_Amphi ,zone)
        scale_par,angle_par = definit_scale_et_angle(Nb_zones)
 
        generer_fichier_latex(
                nom_fichier_final,
                annee_universitaire,
                date,
                horaires,
                duree,
                salle,
                lieu,
                batiment,
                epreuve,
                matiere,
                nom_image=nomFicPngPlanAmphi, 
                fic_tex_in=latex_filename, #  "./tex_out/table.tex"
                scale=scale_par ,
                angle=angle_par
                )
       
        compiler_latex(nom_fichier_final) # compiler 2 fois pour avoir les numéros de pages corrects.
        compiler_latex(nom_fichier_final)
            #
    # on cret un seul fichier pour tout l'amphi par ordre alphabétique.
    dataToutesLesZones=[]   
    for nom_fichier in liste_fichier_par_zone  :
        entete_et_data =  chargeFichierCsv(nom_fichier)    
        data=entete_et_data[1:]
        dataToutesLesZones=dataToutesLesZones + data 
    
    dataToutesLesZonesOrdreAlpha = sorted(dataToutesLesZones, key=lambda x: x[1])
    
    nom_fichier_final= f"./tex_out/Emargements_ALPHABETIQUE_{Nom_Amphi}.tex"
    latex_fichier_table=f"./tex_out/table_{Nom_Amphi}.tex"
    
    ecrit_table_tex(dataToutesLesZonesOrdreAlpha  ,
                latex_filename = latex_fichier_table,
                nb_ligne_tableau=18 ,
                colonne = 0)
    
    scale_par,angle_par = definit_scale_et_angle(Nb_zones) # pour la taille et l'orientation du plan
    
    generer_fichier_latex(
            nom_fichier_final,
            annee_universitaire,
            date,
            horaires,
            duree,
            salle,
            lieu,
            batiment,
            epreuve,
            matiere,
            nom_image=nomFicPngPlanAmphi, 
            fic_tex_in=latex_fichier_table, #  "./tex_out/table.tex"
            scale=scale_par ,
            angle=angle_par
            )

    compiler_latex(nom_fichier_final) # compiler 2 fois pour avoir les numéros de pages corrects.
    compiler_latex(nom_fichier_final)
    
    # effacement des fichier LaTeX intermédiaires.
    chemin = "tex_out/0_Compil"
    liste = os.listdir(chemin)
    fichiers =            [fichier for fichier in liste if ".aux" in fichier ]
    fichiers = fichiers + [fichier for fichier in liste if ".log" in fichier ]
    fichiers = fichiers+  [fichier for fichier in liste if ".gz" in fichier ]
    # Suppression
    for file in fichiers :
        file=chemin+'/'+file
        if os.path.exists(file):
            os.remove(file)
            print(f"Fichier {file} supprimé.")
    

if __name__=='__main__':
    root = tk.Tk()
    
    Nom_Amphi='Biologie'
    master= root
    
    liste_fichier_par_zone = ['/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/2_csv_out/liste_Etudiants_amphi_Biologie_zone_C.csv']


    nom_Fic_zones = './json_out/liste_zones.json'
      
    nomFicPngPlanAmphi=  f"./png_out/{Nom_Amphi}.png"
    Nb_zones=1
    Main_etape_3(root ,
                 liste_fichier_par_zone,
                 nom_Fic_zones,
                Nom_Amphi,
                Nb_zones,
                nomFicPngPlanAmphi)
    
    root.mainloop()