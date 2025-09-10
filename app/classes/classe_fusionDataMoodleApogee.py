import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys

# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__) 
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)

from utils.chargeCsv import choisir_fichier_csv
from utils.chargeCsv import chargeFichierCsv
from utils.chargeCsv import  lit_fichier_csv_et_separe_entete
from utils.afficheConsigne import afficheConsigne
from utils.ecritureCsv import ecritFichierCsv


# Chaine de caractères de l'entete du fichier Apogée.
# DAT_DEB_PES :  date de l'épreuve   ex : 02-JUL-25       utile pour entête
# COD_EPR :    code épreuve ex : "SPUF201F"               utile pour entête
# HEURE_DEBUT : ex : "14h30"							  utile pour entête
# LIB_EPR  : libellé de l'épreuve ex : "Système 1"		  utile pour entête
# HEURE_FIN : ex : "16h30"								  utile pour entête
# DUREE_EXA : ex :  "2h00"								  utile pour entête
# COD_SAL : ex "SAMPINFO"								  utile pour entête !!! plusieurs valeurs  !!!
# LIB_SAL : ex "Amphi d'Informatique"                     utile pour entête !!! plusieurs valeurs  !!!
# COD_BAT : SPRINCIPAL                                    utile pour entête 
# LIB_BAT : VALROSE                                       utile pour entête
# LIB_NOM_PAT_IND :  nom de famille.											n_étudiants
# LIB_PR1_IND : prenom(s)														n_étudiants
# COD_ETU : Code étudiant														n_étudiants
# C_COD_ANU : "ANNEE UNIVERSITAIRE 2024/2025"    		  utile pour entête

class fusionDataMoodleApogee :    
    def __init__(self, root) :
        self.root = root
        
        self.fusionne()
            
    def _créeArborescence(self,listeDesAmphi) :
        """ on charge le fichier contenant les infos Apogées et Moodle
        dans le repertoire de ces fichiers on crée les répertoires :
            --Amphi_{nomAmphi} __ pngOut (pour les sorties graphiques)   
                               |_ texOut (pour les fichier LaTeX)
                               |_listes_Emargement_pdf (pour les sorties de LaTeX)
                               |_csv_out (pour les fichier csv avec l'envoi aux étudiants)
                                   |_csv_pour_envoi_mail
                                       |_zoneDeTransfert (pour les itérations sur les envoi de mail)"""
                
        #print('1',self.nomFicApogee)        
        cheminDesProjets = os.path.dirname(os.path.abspath(self.nomFicApogee))  # def du chemin en absolu
        self.dictCheminAbsolus ={}
        for amphi in listeDesAmphi :
            
            nomRepPourAmphi = f"Amphi_{amphi}"
            chemin_projet_amphi  = os.path.join( cheminDesProjets , nomRepPourAmphi)
            os.makedirs(chemin_projet_amphi, exist_ok=True)
            
            # Liste des répertoires à créer dans chacun des f"Amphi_{amphi}"
            repertoires = ['1_png_out',
                           '3_tex_out',
                           '4_liste_émargements_pdf',
                           '2_csv_out',         # va contenir un sous répertoire
                           '5_json_out',]
            for sousRep in repertoires:
                chemin_complet = os.path.join( chemin_projet_amphi, sousRep )
                self.dictCheminAbsolus[(amphi,sousRep)]=chemin_complet
                os.makedirs(chemin_complet, exist_ok=True)
            # Création des sous répertoire 2_csv_out/csv_pour_envoi_mail
            # et  2_csv_out/csv_pour_envoi_mail/zoneDeTransfert        
            sous_rep = os.path.join(chemin_projet_amphi, '2_csv_out','csv_pour_envoi_mail')
            self.dictCheminAbsolus[(amphi,'csv_pour_envoi_mail')] = sous_rep
            os.makedirs(sous_rep, exist_ok=True)
                                    
            sous_rep = os.path.join(chemin_projet_amphi, '2_csv_out','csv_pour_envoi_mail','zoneDeTransfert')
            self.dictCheminAbsolus[(amphi,'zoneDeTransfert')]=sous_rep
            os.makedirs(sous_rep, exist_ok=True)
            
        print(self.dictCheminAbsolus)
        # exemple de contenu pour 3 amphi dans le fichier Apogée.   
        # {('Informatique', '1_png_out'): '/home.../Amphi_Informatique/1_png_out',
        #  ('Informatique', '3_tex_out'): '/home.../Amphi_Informatique/3_tex_out',
        #  ('Informatique', '4_liste_émargements_pdf'): '/home.../Amphi_Informatique/4_liste_émargements_pdf',
        #  ('Informatique', '2_csv_out'): '/home.../Amphi_Informatique/2_csv_out',
        #  ('Informatique', '5_json_out'): '/home.../Amphi_Informatique/5_json_out',
        #  ('Informatique', 'zoneDeTransfert'): '/home.../Amphi_Informatique/2_csv_out/zoneDeTransfert',
        #  
        #  ('Petit_Valrose', '1_png_out'): '/home.../Amphi_Petit_Valrose/1_png_out',
        #  ('Petit_Valrose', '3_tex_out'): '/home.../Amphi_Petit_Valrose/3_tex_out',
        #  ('Petit_Valrose', '4_liste_émargements_pdf'): '/home.../Amphi_Petit_Valrose/4_liste_émargements_pdf',
        #  ('Petit_Valrose', '2_csv_out'): '/home.../Amphi_Petit_Valrose/2_csv_out',
        #  ('Petit_Valrose', '5_json_out'): '/home.../Amphi_Petit_Valrose/5_json_out',
        #  ('Petit_Valrose', 'zoneDeTransfert'): '/home.../Amphi_Petit_Valrose/2_csv_out/zoneDeTransfert',
        #  
        #  ('Sc_Physiques', '1_png_out'): '/home.../Amphi_Sc_Physiques/1_png_out',
        #  ('Sc_Physiques', '3_tex_out'): '/home.../Amphi_Sc_Physiques/3_tex_out',
        #  ('Sc_Physiques', '4_liste_émargements_pdf'): '/home.../Amphi_Sc_Physiques/4_liste_émargements_pdf',
        #  ('Sc_Physiques', '2_csv_out'): '/home.../Amphi_Sc_Physiques/2_csv_out',
        #  ('Sc_Physiques', '5_json_out'): '/home.../Amphi_Sc_Physiques/5_json_out',
        #  ('Sc_Physiques', 'zoneDeTransfert'): '/home.../Amphi_Sc_Physiques/2_csv_out/zoneDeTransfert'}       
        

    def fusionne(self) :  
        # chargement du fichier csv Apogée 
        
        tk.messagebox.showwarning(title=None, message="Chargement du fichier APOGEE")
        self.nomFicApogee = choisir_fichier_csv(self.root,
                                            "Choisir un fichier issu de Apogée format CSV")
        
        self.cheminDuFichierApogee =  os.path.dirname(self.nomFicApogee)
                     
        self.dataEtudiantApogee, self.enteteApogee  = lit_fichier_csv_et_separe_entete(self.nomFicApogee ,
                                                                               delimiteur=';' )
        
        tk.messagebox.showwarning(title=None, message="Le fichier APOGEE est chargé.")
        
        
        # chargement du fichier csv Moodle avoir les emails étudiants
        tk.messagebox.showwarning(title=None, message="Chargement du fichier  MOODLE.")
        self.nomFicMoodle = choisir_fichier_csv(self.root,
                                                "Choisir un fichier issu de Moodle format CSV",
                                                self.cheminDuFichierApogee)
        
        self.dataEtudiantMoodle, self.enteteMoodle  = lit_fichier_csv_et_separe_entete(self.nomFicMoodle ,
                                                                               delimiteur=',' )
        
        tk.messagebox.showwarning(title=None, message="Fichier MOODLE chargé")
        
        # verif de la compatibilité avant d'aller plus loin.
        nbEtudiantApogee = len(self.dataEtudiantApogee)
        nbEtudiantMoodle = len(self.dataEtudiantMoodle)
        
        if nbEtudiantMoodle <= nbEtudiantApogee :
            afficheConsigne("Attention", f"Il y a {nbEtudiantApogee} candidats pour {nbEtudiantMoodle}.\n\n"
                                        f"Le fichier exportés depuis Moodle est peut être incomplet.\n"
                                        f"En continuant vous ne pourrez pas effectuer tous les envois de courriel.\n")
        
        # définition du dictionnaire  clé = champ de l'entete et valeur = indice de la colonne dans le tableau.
        self.valIndex =  self.dicoDataEntete(self.enteteApogee)
        # self.valIndex  est un dictionnaire dont la clé est le code de l'entete
        #										et la valeur l'indice de la colonne
        # exemple de self.valIndex   {	'DAT_DEB_PES': 0, 'DHH_DEB_PES': 1, 'DMM_DEB_PES': 2,
        #								'COD_EPR': 3, 'HEURE_DEBUT': 4, 'COD_PES': 5, 'LIB_EPR': 6,
        #							 	'HEURE_FIN': 7, 'DUREE_EXA': 8, 'LIB_TYP_EXE_EPR': 9,
        #								'COD_SAL': 10, 'GROUPE_IND': 11, 'LIB_GPE': 12,
        #								'LIB_SAL': 13, 'COD_BAT': 14, 'LIB_BAT': 15,
        #								'NUM_PLC_AFF_PSI': 16, 'LIB_NOM_PAT_IND': 17,
        #								'LIB_PR1_IND': 18, 'COD_ETU': 19, 'C_CPT_IND': 20,
        #								'C_COD_ANU': 21, 'C_CPT_EPR': 22}
        # 
        # on définit les valeurs pour l'entête de la feuille d'émargement
        self.listeChampsUtiles=[ 'DAT_DEB_PES',
                                'COD_EPR',
                                'HEURE_DEBUT',
                                'LIB_EPR',
                                'HEURE_FIN',
                                'DUREE_EXA',
                                'COD_SAL',
                                'LIB_SAL',
                                'COD_BAT',
                                'LIB_BAT',                            
                                'C_COD_ANU'
                                ]
        self.dicoValEntete = self.extraitValeurPourEnteteEmargement(self.listeChampsUtiles ,
                                                self.dataEtudiantApogee,
                                                self.valIndex)
        #pour  self.dicoValEntete ,  exemple de dictionnaire dans le cas où il y a 3 amphithéatres :
        #{'DAT_DEB_PES': ['02-JUL-25'],
        # 'COD_EPR'    : ['SPUF201F'],
        # 'HEURE_DEBUT': ['14h30'],
        # 'LIB_EPR'    : ['Système 1'],
        # 'HEURE_FIN'  : ['16h30'],
        # 'DUREE_EXA'  : ['2h00'],
        # 'COD_SAL'    : ['SAMPINFO', 'SAMPVAL', 'SPHYS2'],
        # 'LIB_SAL'    : ["Amphi d'Informatique", 'Grand amphi Valrose', 'AMPHI DE PHYSIQUE 2'],
        # 'COD_BAT'    : ['SPRINCIPAL'],
        # 'LIB_BAT'    : ['VALROSE'],
        # 'C_COD_ANU'  : ['ANNEE UNIVERSITAIRE 2024/2025']}
        
        
        # self.definitNomAmphi() :
        # definit la liste des  nom d'amphi par rapport au code COD_SAL d'apogée
        # definit également le dictionnaire self.COD_SAL_2_code_BOUS
        # ex : cle = COD_SAL ex 'SCHIMIE'   et valeur =  "nom explicite utilisé plus tard"  ex 'Chimie'
        self.listeDesAmphi, self.COD_SAL_2_code_BOUS = self.definitNomAmphi(self.dicoValEntete)
        
        # on crée l'arborescence des fichiers de sortie(voir la decription
        # dans le détail de la méthode.
        self._créeArborescence(self.listeDesAmphi)
                
        #définition du dictionnaire dont la clé est le numéro d'étudiant
        # et la valeur, la chaîne contenant le courriel.
        self.dicoMail = self.CreeDicoMail (self.dataEtudiantMoodle)

        
        # définition de la liste avec les données utilise pour le code Boustrophédon
        self.dataBous = self.configureListe (
                                        self.dataEtudiantApogee ,
                                        self.dicoMail,
                                        self.valIndex,
                                        self.COD_SAL_2_code_BOUS)
        # self.dataBous contient toutes les infos de tous les étudiants dans les amphi (séparation à faire).
        # [['Prenom', 'Nom', 'Numéro', 'mail', 'ordre VS', 'Amphi'],
        # ['AMBRYNE', 'HAMOUMI', '22410380', 'ambryne.hamoumi@etu.univ-cotedazur.fr', '0', 'Informatique'] , etc ]
        
        # generation d'autant de fichier csv format bous que d'amphithéatre dans apogée.
        #print(self.listeDesAmphi)
        if len(self.listeDesAmphi) > 1 :
            listeNomEtCheminFichier = self.genereFicCsv(self.dataBous,self.listeDesAmphi,self.cheminDuFichierApogee)
            

        
    def dicoDataEntete(self, enteteApogee):
        """genère un dictionnaire qui donne l'index d'un champ
        exemple   self.valIndex[0] = 'DAT_DEB_PES'      """
        valIndex={}
        for k in range(len(enteteApogee)) :
            valIndex[enteteApogee[k]]= k
        return valIndex
            
    def extraitValeurPourEnteteEmargement(self,listeChampsUtiles,dataEtudiantApogee,valIndex):
        """définit les valeurs pour l'entete de la fiche d'émargement
        et compte le nombre d'amphi différents pour faire un seul fichier
        cotnenant toutes les données étudiant par amphithéatre """
        
        # création et initialisation du dictionnaire des valeurs de l'entête.
        # on initialise à des listes vides pour prévoir le cas où il y a plusieurs
        # amphi par exemple.
        dicoValEntete={}
        for champ in listeChampsUtiles :
            dicoValEntete[champ]=[]
        
        for k in range(len(dataEtudiantApogee)):
            ligneDataEtudiant = dataEtudiantApogee[k]
            for champ in listeChampsUtiles :
                indiceColonne  = valIndex[champ]
                valeur = ligneDataEtudiant[indiceColonne]
                if valeur not in dicoValEntete[champ] :
                    dicoValEntete[champ].append(valeur)
        # exemple de dictionnaire dans le cas où il y a 3 amphithéatres :
        #{'DAT_DEB_PES': ['02-JUL-25'],
        # 'COD_EPR'    : ['SPUF201F'],
        # 'HEURE_DEBUT': ['14h30'],
        # 'LIB_EPR'    : ['Système 1'],
        # 'HEURE_FIN'  : ['16h30'],
        # 'DUREE_EXA'  : ['2h00'],
        # 'COD_SAL'    : ['SAMPINFO', 'SAMPVAL', 'SPHYS2'],
        # 'LIB_SAL'    : ["Amphi d'Informatique", 'Grand amphi Valrose', 'AMPHI DE PHYSIQUE 2'],
        # 'COD_BAT'    : ['SPRINCIPAL'],
        # 'LIB_BAT'    : ['VALROSE'],
        # 'C_COD_ANU'  : ['ANNEE UNIVERSITAIRE 2024/2025']}
        return dicoValEntete
        
    def definitNomAmphi(self,dicoValEntete) :
        """ Traduit le nom de l'amphi Apogée en nom d'amphi code Boustrophédon
        nom sans espace et qui est écrit sur les plans des amphi, ex Petit_Valrose """
        
        listeAmphi= ['Biologie', 'Géologie',
                     'Sc_Physiques', 'Chimie',
                     'Sc_Naturelles', 'Informatique',
                     'Mathématiques' ,'Petit_Valrose']
        COD_SAL_2_code_BOUS = {'SAMPINFO' : 'Informatique'  ,
                               'SAMPVAL'  : 'Petit_Valrose',
                               'SPHYS2'   : 'Sc_Physiques',
                               'SAMPBIOL' : 'Biologie',
                               'SAMPHIM'  : 'Mathématiques' ,
                               'SCHIMIE'  : 'Chimie',
                               'SAMPGEOL' : 'Géologie',
                               'SSNAT'    : 'Sc_Naturelles'
                               }
        listeDesAmphi=[]
        for code  in  dicoValEntete['COD_SAL'] :
            listeDesAmphi.append(COD_SAL_2_code_BOUS[code])                    
        #print( f" self.listeDesAmphi = {self.listeDesAmphi}")
        return  listeDesAmphi ,   COD_SAL_2_code_BOUS 
        
    def CreeDicoMail (self,dataMoodle):
        """crée le dictionnaire dont la clé est le numéro
        d'étudiant et la valeur le mail"""
        dico={}
        for k in range(1,len(dataMoodle) ):
            ligne = dataMoodle[k]
            dico[ ligne[2] ]=ligne[3]
        return dico

    def configureListe (self,dataEtudiantApogee ,dicoMail,valIndex,COD_SAL_2_code_BOUS) :        
        """ lit les data apogee et les place dans le même ordre que
        le code boustrophédon en ajoutant les champs email ,
        numéro VS et amphi """
        dataBous=[]
        # entete du fichier format BOUS.
        dataBous.append(['Prenom','Nom','Numéro','mail','ordre VS','Amphi'])
        # etiquette des colonnes à extraire de dataEtudiantApogee
        # LIB_NOM_PAT_IND :  nom de famille. 
        # LIB_PR1_IND : prenom(s) 
        # COD_ETU : Code étudiants
        for k in range(len(dataEtudiantApogee)) :
            dataUnEtudiant=dataEtudiantApogee[k]
            Prenom = dataUnEtudiant [ valIndex['LIB_PR1_IND'] ]
            Nom    = dataUnEtudiant [ valIndex['LIB_NOM_PAT_IND'] ]
            Numéro = dataUnEtudiant [ valIndex['COD_ETU'] ]            
            mail   = dicoMail[ Numéro ]
            ordreScol  = str(k+1)
            codeSalle = dataUnEtudiant [ valIndex['COD_SAL'] ] 
            Amphi  = COD_SAL_2_code_BOUS[ codeSalle ]
            dataBous.append( [Prenom, Nom, Numéro, mail, ordreScol, Amphi] )
        return dataBous

    def  genereFicCsv(self,dataBous,listeDesAmphi,cheminDuFichierApogee) :
        listeNomEtCheminFichier=[]
        indice = 1        
        for amphi in listeDesAmphi  :
            #
            # REDEFINIR ICI chemin
            chemin = f"{cheminDuFichierApogee}/Amphi_{amphi}/2_csv_out"
            #
            nomFichier=f"{chemin}/liste_Etudiants_amphi_{amphi}.csv"
            
            dataFicMonoAmphi= [ ['Prenom', 'Nom', 'Numéro', 'mail', 'ordreScol', 'Amphi']  ]  #entête
            while indice < len(dataBous) :
                dataUnEtudiant = dataBous[indice]
                #print(f"dateUnEtudiant ={dataUnEtudiant}")
                if dataUnEtudiant[5] == amphi :
                    dataFicMonoAmphi.append(dataUnEtudiant)
                    indice = indice + 1                    
                else :
                    break # on sort de la boucle while
            
            ecritFichierCsv(nomFichier,dataFicMonoAmphi)            
        
    
    
if __name__=="__main__" :
    root=tk.Tk()
    root.withdraw()
    
    data = fusionDataMoodleApogee(root)
 
    
    
    root.mainloop()
