import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os 
import sys

import random

# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__)
#
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)

from utils.chargeCsv import chargeFichierCsv
from utils.ecritureCsv  import ecritFichierCsv
from utils.chargeCsv  import lit_fichier_csv_et_separe_entete
from utils.gestion_json   import chargeConfig,save_json
from utils.gestion_json   import charge_json
 
def choisir_fichier_csv(master ,  titre="Choisir un fichier CSV",rep="./Data_csv_in"):
    window = tk.Toplevel(master)
    window.withdraw()  # Ne pas afficher cette fenêtre secondaire

    nom_fichier = filedialog.askopenfilename(
        title=titre,
        initialdir=rep,
        filetypes=[("Fichiers CSV", "*.csv")],
    )

    return nom_fichier


def majusculeNomFamille(listeEtudiants) :
    for k in range(0,len(listeEtudiants)):
        a=listeEtudiants[k][1]
        listeEtudiants[k][1]=listeEtudiants[k][1].capitalize()
        

def decouper_codes(data):
    resultat = []
    for code in data:
        # On suppose que le format est toujours L-NN-N
        # Étape 1 : extraire la lettre
        lettre = code[0]

        # Étape 2 : extraire les chiffres entre les tirets
        i = 2  # on commence après la lettre et le premier '-'
        num1 = 0
        ref=""
        while code[i] != '-':
            ref=ref+code[i]
            i=i+1
        num1=int(ref)
        ref
        # Étape 3 : extraire les chiffres
        i =i + 1  # passer le second '-'
        num2 = 0
        ref2=""
        while i < len(code):
            ref2=ref2+code[i]
            i =i + 1
        num2=int(ref2)
        resultat.append([lettre, num1, num2])
    return resultat

def analyse_amphi(references):
    """ renvoie une liste des zones LettreZone
        et renvoie un dictionnaire
            maxi_rang_zone  (cle=zone , valeur = maxi)
            maxi_place_zone (cle=zone , valeur = maxi)"""
    
    maxi_rang_zone  : dict[str,int] = {}
    maxi_place_zone : dict[str,int] = {}
    # extraction des lettres des zones de l'amphi
    ensemble=set()
    for elem in references :
        ensemble.add(elem[0])        
    LettreZone=[]
    for lettre in ensemble :
        LettreZone.append(lettre)
    #print("Lettre des zones : ",Zones)
    # fin extraction.
    # on cree un ensemble avec les ref des places et un autre avec les rangs.
    z_rang={}
    z_place={}
    for lettre in LettreZone :
        z_rang[lettre]=set()
        z_place[lettre]=set()
        for ref in references :
            ref_zone=ref[0]
            rang=ref[1]
            place=ref[2]
            if ref_zone==lettre :
                z_rang[lettre].add(rang)
                z_place[lettre].add(place)
    # recherche des maxi de chaque ensemble et stockage dans le dico.
    maxi_rang_zone={}   
    for cle in z_rang :
        maxi_rang_zone[cle]=max(z_rang[cle])
        
    maxi_place_zone={}    
    for cle in z_place :
        maxi_place_zone[cle]=max(z_place[cle])
        
    return LettreZone , maxi_rang_zone, maxi_place_zone
            
def rang_vide(rang,zone,references)->bool:
    """vérifie si le rang de la zone est vide ou pas"""
    for elem in references :
        if elem[0]==zone :
            if elem[1]==rang :
                return False
    return True

def boustrophedon(Départs_et_sens,maxi_rang_zone,maxi_place_zone,references):
    Bous={}
    for zone in Départs_et_sens :
        Lettre_zone = zone
        rang  = Départs_et_sens[zone][0][0]
        place = Départs_et_sens[zone][0][1] # numero de la place de départ dans le rang de départ
        sens=Départs_et_sens[zone][1]
        maxi_rang  = maxi_rang_zone[zone]
        maxi_place = maxi_place_zone[zone]
        rajout=str(zone)+'-'+str(rang)+'-'+str(place)

        Bous[zone]=[]
   
        while rang <= maxi_rang:        
            while 1<=place and place <= maxi_place :            
                ajout=str(zone)+'-'+str(rang)+'-'+str(place)
                #print(ajout)
                if [zone,rang,place] in references :
                    Bous[zone].append(ajout)
                if sens=='c' :
                    place=place+1
                else :
                    place=place-1                
            rang=rang+1 # on passe au rang d'après
            #print('rang',rang)
            if rang<= maxi_rang :   
                while rang_vide(rang,zone,references) :  # on saute les rangs vides
                    rang=rang+1            
            if sens=='c' :
                sens='d'
                place=maxi_place # 
            else :
                sens='c'
                place=1   #
    return Bous   # fin de la fonction boustrophedon
    

    
def reparti_Etudiants_dans_zones(nomCsv_noms_etudiants ,Zones ,BousTriZone ,lignes ,
                                 enteteFichier , dico_place_fichier,
                                 Nb_places,Nb_etudiant_a_placer,Nom_Amphi,cheminsAbsolus):
    liste_fichier_par_zone=[]
    ref=[]
    i=0
    for zone in Zones :
        j=0
        place = BousTriZone[zone]
        verif=len(place)
        contenuZone=[]
        while j < len(BousTriZone[zone]) :
            if i> Nb_etudiant_a_placer-1 :  # -1 car python compte à partir de zéro  !!!
                break # tous les étudiants ont été placé.
            #print('i=',i,' j=',j)
            lignes[i].append(place[j])    # on ajoute une place en face d'un étudiant.            
            lignes[i].append(dico_place_fichier[place[j]])
            contenuZone=contenuZone+[lignes[i]]
            j=j+1 # on passe à la place suivante
            i=i+1 # on passe à l'étudiant suivant
            
        print(f" Nom_Amphi {Nom_Amphi}")

        nom_fic_csv_sortie = f"{cheminsAbsolus[( Nom_Amphi , '2_csv_out' )]}/liste_Etudiants_amphi_{Nom_Amphi}_zone_{zone}.csv "
        entete_pour_zone = enteteFichier + [zone]
        
        liste_fichier_par_zone=liste_fichier_par_zone+[nom_fic_csv_sortie]
        contenuZone = [entete_pour_zone] + contenuZone
        #print("chemin =",nom_fic_csv_sortie)
        
        ecritFichierCsv(nom_fic_csv_sortie,contenuZone)
        
    return liste_fichier_par_zone

def Main_etape_2(master,nomFicJson_places_seules ,
                nomFicJson_places_et_chemin_img,
                Nom_Amphi,
                zones  :list [str] ,
                cheminsAbsolus):

    ref_places=chargeConfig(nomFicJson_places_seules)
    
     
    
    if len(zones)==1 :
        Départs_et_sens = {
                    'C' : [ [1, 1],'c' ] ,    #Sens='c'   avec 'c' pour croissant et 'd' pour décroissant
                   }
    elif len(zones)==2 :
        Départs_et_sens = {
                        'G' : [ [1, 1],'c' ] ,    #Sens='c'   avec 'c' pour croissant et 'd' pour décroissant
                        'D' : [ [1, 1],'c' ] 
                       }
    elif len(zones)==3 :
        Départs_et_sens = {
                        'G' : [ [1, 4],'c' ] ,    #Sens='c'   avec 'c' pour croissant et 'd' pour décroissant
                        'C' : [ [1, 1],'c' ] ,
                        'D' : [ [1, 3],'d' ] ,
                       }
 
 
    # avant lors de l'étape via le bouton :
    # nomCsv_noms_etudiants  =choisir_fichier_csv(master, "Fichier csv contenant la liste des étudiants : ","./Data_csv_in/Liste_des_etudiants_par_Amphi" )
       
    nomCsv_noms_etudiants = f"{cheminsAbsolus[( Nom_Amphi , '2_csv_out' )]}/liste_Etudiants_amphi_{Nom_Amphi}.csv"
    
    print(f" Amphi {Nom_Amphi}   // nomCsv_noms_etudiants { nomCsv_noms_etudiants}")
    print()
    print()
    
    # noms du fichier contenant les dictionnaires place-> chemin fichier
    nomJson_place_vers_fic = nomFicJson_places_et_chemin_img
    
    references=decouper_codes(ref_places)
    
    Nb_places = len(references)
    print(f"Nb_places dans l'amphithéatre = {Nb_places}")
    
    LettreZone , maxi_rang_zone , maxi_place_zone = analyse_amphi(references)
    
     
    # création du Boustrophédon :
    BousTriZone=boustrophedon(Départs_et_sens,maxi_rang_zone,maxi_place_zone,references)
    
    lignes, enteteFichier = lit_fichier_csv_et_separe_entete(nomCsv_noms_etudiants)
    
    Nb_etudiant_a_placer = len(lignes)
    print("Nombre d'étudiants dans le fichier ",Nb_etudiant_a_placer)
    print()
    if Nb_places < Nb_etudiant_a_placer :
        messagebox.showwarning("Attention",
                               f"Vous n'avez que {Nb_places} places pour"
                               f" {Nb_etudiant_a_placer} étudiants. "
                               f" La liste d'émargement sera incomplète.")
    elif Nb_places > Nb_etudiant_a_placer :
        messagebox.showwarning("Attention",
                               f"Vous avez plus de  places que d'étudiants."
                               f" {Nb_etudiant_a_placer} étudiants. "
                               f" {Nb_places} places.")
    
    majusculeNomFamille(lignes)
    random.shuffle(lignes)  # mélange de la liste à placer

    dico_place_fichier=charge_json(nomJson_place_vers_fic)
 
    #print("Avant appel",nomCsv_noms_etudiants)
    
    liste_fichier_par_zone= reparti_Etudiants_dans_zones(nomCsv_noms_etudiants,LettreZone,BousTriZone,
                                                         lignes,enteteFichier,dico_place_fichier,
                                                         Nb_places,Nb_etudiant_a_placer,Nom_Amphi,cheminsAbsolus)
       
    # les fichiers en sortie :

    # fichier contenant le nom des csv avec les etudiants placés... pour passer l'info à 3_genere_table.
    #nom_Fic_par_zone = "./json_out/liste_fichiers_csv_etudiants_par_zone.json"
    nom_Fic_par_zone= f"{cheminsAbsolus[( Nom_Amphi , '5_json_out' )]}/liste_fichiers_csv_etudiants_par_zone.json"
    
    # fichier contenant juste la ref des zones...
    #nom_Fic_zones= "./json_out/liste_zones.json"
    nom_Fic_zones = f"{cheminsAbsolus[( Nom_Amphi , '5_json_out' )]}/liste_zones.json"

    save_json(nom_Fic_par_zone , liste_fichier_par_zone)
    
    
     # contient le noms des fichiers *.csv des etudiants placé par zone 
    print(f"Le Fichier {nom_Fic_par_zone} sauvegardé. \n"
          f" Ce fichier contient les zone des fichiers csv des étudiants placé par zone.\n \n")          
    
    save_json(nom_Fic_zones , LettreZone)
    print(f"Fichier {nom_Fic_zones} sauvegardé.\n"
          f" Ce fichier contient la ref (juste la lettre) des  zones, D, C ou G  .\n \n")
    
    print('liste_fichier_par_zone = ', liste_fichier_par_zone)
    print('nom_Fic_zones  = ', nom_Fic_zones)
    print('Nom_Amphi  = ', Nom_Amphi )
        
    return liste_fichier_par_zone, nom_Fic_zones


if __name__=="__main__" :
    root=tk.Tk()
    nomAmphi='Biologie'
    
    cheminsAbsolus = {('Biologie', '1_png_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/1_png_out',
                   ('Biologie', '3_tex_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/3_tex_out',
                   ('Biologie', '4_liste_émargements_pdf'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/4_liste_émargements_pdf',
                   ('Biologie', '2_csv_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/2_csv_out',
                   ('Biologie', '5_json_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/5_json_out',
                   ('Biologie', 'zoneDeTransfert'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/2_csv_out/zoneDeTransfert' }
    
    # nomFicJson_places_seules=f"./json_out/pour_auto_test_p2/Amphi_{nomAmphi}.json"
    nomFicJson_places_seules = f"{ cheminsAbsolus[ (nomAmphi, '5_json_out') ] }/Amphi_{nomAmphi}.json"
    print(nomFicJson_places_seules)
    
    
    #nomFicJson_places_et_chemin_img="./json_out/pour_auto_test_p2/Amphi_reference_et_chemin_fichier_"+nomAmphi+".json"
    nomFicJson_places_et_chemin_img=f"{ cheminsAbsolus[ (nomAmphi, '5_json_out') ] }/Amphi_reference_et_chemin_fichier_{nomAmphi}.json"
    print(nomFicJson_places_et_chemin_img)
    
    zones=['Centre']
         
    Main_etape_2(root,
                 nomFicJson_places_seules,
                 nomFicJson_places_et_chemin_img,
                 nomAmphi  ,
                 zones,
                 cheminsAbsolus
                  )       
    root.mainloop()