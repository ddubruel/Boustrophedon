
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageDraw, ImageGrab
import json
import csv

import os
import sys

# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__)
#
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)
    
from classes.classe_rang import rangs
from utils.pour_classe_rangs import save_canvas
from utils.modificationConfigAmphi  import modifier_configuration
from utils.charge_geo_amphi import charge, charge_v2

from classes.classe_graphique_une_zone import GraphiqueUneZone

def save_json(nom_Fic, data):
    print('Sauvegarde des données :',data)
    with open(nom_Fic, "w", encoding="utf-8") as fichier:
        json.dump(data, fichier)
    print(f"Fichier sauvegardé sous {nom_Fic}")
    print()

def dessiner_rangs_grille(fenetre, largeur, hauteur,  xhg, yhg, longueur, espace,
                        listeCasesCocheesPourToutesLesZones,
                         nb_places_par_rang_par_zon,
                         Nb_rang,
                         nomAmphi,
                         listeDesZones ,
                         cheminsAbsolus):
    
    fenetre.title("Dessin des amphithéatres et des places")    
    fenetre.geometry(f"{largeur}x{hauteur}")
    label_amphi = tk.Label(fenetre,
                           textvariable=nomAmphi,
                           font=("Arial", 20),
                           name="label_amphi")    
    label_amphi.pack(pady=(10,0))
    
    canvas = tk.Canvas(fenetre,bg="white")
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
    couleurZone=['lightyellow'], ['honeydew'], ['mistyrose']
    grillesDesZones=[]
    refDesPlaces=[]
    nomFichiersPng=[]
    for i, zone in enumerate(listeDesZones):        
        graphiqueZone = GraphiqueUneZone (canvas,
                                 xhg[i], yhg, longueur[i], espace,
                                 nb_places_par_rang_par_zon[i],
                                 Nb_rang,
                                 zone, # 'Gauche','Centre' ou  'Droite'
                                 nomAmphi,  # chaine du genre 'Amphithéatre Chimie'
                                 couleurZone[i],
                                 listeCasesCocheesPourToutesLesZones[i],
                                 cheminsAbsolus
                                 )
        grillesDesZones.append(graphiqueZone)
            
    
    # A mettre dans un bouton plus tard .... : 
    for graphiqueZone in  grillesDesZones:        
        refDesPlaces.append(graphiqueZone.listeDesPlaces)
        print(refDesPlaces)
        
        graphiqueZone.entourePlaceEtSauveFicPng() # sauve les fichier et crée la liste des fichiers dans l'instance.
        nomFichiersPng.append(graphiqueZone.liste_nom_fic_png) # recup  de la liste des fichiers png de l'instance.
    
    
    def aplatitListe(L) : 
        liste_plate = []
        for sous_liste in L:
            liste_plate.extend(sous_liste)
        return liste_plate
    
    nomFichiersPng = aplatitListe(nomFichiersPng)
    refDesPlaces = aplatitListe(refDesPlaces)
    
  
    graphiqueZone.sauvePlanAmphi()  # on sauvegarde le plan sans ovale indiquant une place.
    nomFicPlanAmphiPng = graphiqueZone.nomFicPlanAmphiPng
    
    return refDesPlaces,nomFichiersPng ,nomFicPlanAmphiPng

def rassemble_liste_en_dico(  referencePlace , liste_nom_fic_png ) :    
    
    reference_et_chemin_fichier={}
    for k in range(len(referencePlace)):
         
        reference_et_chemin_fichier[referencePlace[k]]=liste_nom_fic_png[k]
 #       Resultat.append( [liste_nom_fic_png[k] , referencePlace[k] ])
    
    return reference_et_chemin_fichier
    




def Main_Etape_1(parent,listeCasesCocheesPourToutesLesZones,
                 nb_places_par_rang_par_zon,
                 Nb_rang,
                 nomAmphi,
                 listeDesZones,
                 cheminsAbsolus):                
    """ parent : la fenêtre mère
        listeCasesCocheesPourToutesLesZones : liste de liste du style [ [(0,0) , (14,3], [(1,1)]
                            chaque zone est une liste de place attribué (ligne, colonne)
        nb_places_par_rang_par_zon , ex [14,14] pour Chimie, [6,7,6] pour Petit Valrose
                    contient le nombre maxi d'étudiant par rangée et par zone
        Nb_rang : 9 (bio) ou 10 (géo) ou 14 (Amphi Chimie etc ) ou 17 (PV)
        nomAmphi : chaîne (titre des images) avec "Amphithéatre Chimie" par exemple.
        listeDesZones :  ['Gauche', 'Centre','Droite ]  pour le PV par exemple
                         [ 'Centre' ]   pour Bio et Géo.   """

    
    fenetreDessinAmphi=tk.Toplevel(parent)
    
    Nb_zones = len(listeDesZones)
    
    if Nb_zones == 1:
        largeur, hauteur = 550, 700        
        
        longueur =[400]
        espace =  40         
        xhg = [50]   # car le code prendra xhg[i] lors de l'instanciation de la classe.
        yhg = 100   # valeur constante pour toutes les classes.
    elif Nb_zones == 2:
        largeur, hauteur = 1000, 800
        
        longueur =[400 , 400]
        espace =  40
        yhg = 100
        largeur_escalier = 75
        x_hg_0 = 50
        x_hg_1 = 50 + largeur_escalier + longueur[0]
        xhg=[x_hg_0 , x_hg_1 ]
        

    elif Nb_zones == 3:
        largeur, hauteur = 1600, 900        
        longueur =[400 , 500, 400]
        espace =  35        
        yhg = 75
        largeur_escalier = 75
        x_hg_0 = 50
        x_hg_1 = 50 + largeur_escalier + longueur[0]
        x_hg_2 = 50 + largeur_escalier + longueur[0] + largeur_escalier + longueur[1]
        xhg = [ x_hg_0  ,  x_hg_1  , x_hg_2 ]     
        
    refDesPlaces, nomFichiersPng, nomFicPlanAmphiPng = dessiner_rangs_grille(fenetreDessinAmphi, largeur, hauteur,  xhg, yhg, longueur, espace,
                                     listeCasesCocheesPourToutesLesZones,
                                     nb_places_par_rang_par_zon,
                                     Nb_rang,
                                     nomAmphi,
                                     listeDesZones,
                                     cheminsAbsolus)

    # Construit le chemin absolu vers png_out
    png_out_dir = cheminsAbsolus[(nomAmphi,'1_png_out')]
    json_out_dir = cheminsAbsolus[(nomAmphi,'5_json_out')]
    # Assemble le chemin final du fichier PNG
 
    nomFicJson_places_seules =  f"{json_out_dir}/Amphi_{nomAmphi}.json"
    nomFicJson_places_et_chemin_img = f"{json_out_dir}/Amphi_reference_et_chemin_fichier_{nomAmphi}.json"
    

    # sauvegarde dans un dictionaire dico[place]=Chemin_vers_fichier_png :
    dico_des_references_et_chemin_fichier=rassemble_liste_en_dico( refDesPlaces ,
                                                                nomFichiersPng)
    # sauvegarde des fichier json
    save_json(nomFicJson_places_et_chemin_img, dico_des_references_et_chemin_fichier)
    print('eeeee')
    print('1',nomFicJson_places_et_chemin_img)
    print('2',dico_des_references_et_chemin_fichier)
    
    save_json(nomFicJson_places_seules, refDesPlaces)
    
    
    return refDesPlaces , nomFichiersPng , nomFicJson_places_seules, nomFicJson_places_et_chemin_img ,nomFicPlanAmphiPng


def rassemble_liste(  referencePlace , liste_nom_fic_png ) :    
    return reference_et_chemin_fichier

def main_local_1_zone():
    """pour tester ce module avec une seule zone"""
    root = tk.Tk()
    root.withdraw()
    root.geometry("550x1100")
        
    
    listeCasesCocheesPourToutesLesZones = [[(0, 0),(0,1),(0,2),(0,3),(0,4), (9, 0), (9,4)]]
    nb_places_par_rang_par_zon=[5]
    Nb_rang   = 10
    nomAmphi = "Biologie"
    listeDesZones=['Centre']
  
    dicoExemple = {('Biologie', '1_png_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/1_png_out',
                   ('Biologie', '3_tex_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/3_tex_out',
                   ('Biologie', '4_liste_émargements_pdf'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/4_liste_émargements_pdf',
                   ('Biologie', '2_csv_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/2_csv_out',
                   ('Biologie', '5_json_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/5_json_out',
                   ('Biologie', 'zoneDeTransfert'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/2_csv_out/zoneDeTransfert' }
    
    Main_Etape_1(root,listeCasesCocheesPourToutesLesZones,
                 nb_places_par_rang_par_zon,
                 Nb_rang,
                 nomAmphi,
                 listeDesZones,
                 dicoExemple)
    root.mainloop()
    
def main_local_2_zone():
    """pour tester ce module avec deux zones"""
    root = tk.Tk()
    root.withdraw()
    
        
    
    listeCasesCocheesPourToutesLesZones = [
                                            [(0, 0), (0, 5), (13, 0), (13, 5)],
                                            [(0, 0), (0, 2), (1, 0), (1, 2), (1, 5), (13, 0), (13, 5)]
                                          ]
    nb_places_par_rang_par_zon=[6,6]
    Nb_rang   = 14
    nomAmphi = "Mathématiques"
    listeDesZones=['Gauche','Droite']
  

    Main_Etape_1(root,listeCasesCocheesPourToutesLesZones,
                 nb_places_par_rang_par_zon,
                 Nb_rang,
                 nomAmphi,
                 listeDesZones  )
    root.mainloop()


def main_local_3_zone():
    """pour tester ce module avec deux zones"""
    root = tk.Tk()
    root.withdraw()
    
        
    
    listeCasesCocheesPourToutesLesZones = [
                                            [(0, 0), (0, 5), (14, 2), (16, 0), (16, 2)],
                                            [(0, 0), (0, 6), (16, 0), (16, 6)],
                                            [(0, 0), (0, 5), (16, 3), (16, 5)]
                                          ]
 
    nb_places_par_rang_par_zon=[6,7,6]
    Nb_rang   = 17
    nomAmphi = "Petit_Valrose"
    listeDesZones=['Gauche','Centre','Droite']
  

    Main_Etape_1(root,listeCasesCocheesPourToutesLesZones,
                 nb_places_par_rang_par_zon,
                 Nb_rang,
                 nomAmphi,
                 listeDesZones  )
    root.mainloop()
    
    
if __name__ == "__main__":
    main_local_1_zone()
