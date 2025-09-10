import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

# Chaine de caractères de l'entete du fichier Apogée.
# DAT_DEB_PES :  date de l'épreuve   ex : 02-JUL-25
# COD_EPR :    code épreuve ex : "SPUF201F"
# HEURE_DEBUT : ex : "14h30"
# LIB_EPR  : libellé de l'épreuve ex : "Système 1"
# HEURE_FIN : ex : "16h30"
# DUREE_EXA : ex :  "2h00"
# COD_SAL : ex "SAMPINFO"
# LIB_SAL : ex "Amphi d'Informatique"
# COD_BAT : SPRINCIPAL
# LIB_BAT : VALROSE
# LIB_NOM_PAT_IND :  nom de famille.
# LIB_PR1_IND : prenom(s)
# COD_ETU : Code étudiant
# C_COD_ANU : ANNEE UNIVERSITAIRE 2024/2025

from module_gestion_fichiers import chargeFichierCsv
from module_gestion_fichiers import ecritFichierCsv


def choisir_fichier_csv(master ,  titre="Choisir un fichier issu de Apogeé format CSV",rep="."):
    window = tk.Toplevel(master)
    window.withdraw()  # Ne pas afficher cette fenêtre secondaire

    nom_fichier = filedialog.askopenfilename(
        title=titre,
        initialdir=rep,
        filetypes=[("Fichiers CSV", "*.csv")],
    )

    return nom_fichier

def retireLignesAvantEtudiants (data) :
    k=0
    element=''
    while 'XX_ETU' not in element :
        ligne=data[k]
        if ligne != [] :
            element=ligne[0]
        k=k+1
        print(k)
    print(f'trouvé en ligne{k}')
    return data[k:]

def CreeDicoMail (dataMoodle):
    """cree le dictionnaire dont la clé est le numéro
    d'étudiant et la valeur le mail"""
    dico={}
    for k in range(1,len(dataMoodle) ):
        ligne = dataMoodle[k]
        dico[ ligne[2] ]=ligne[3]
    return dico

def configureListe (ListeEtuSN, amphi ,dicoMail) :
    """ lit les data SNweb et les place dans le même ordre que
    le code boustrophédon en ajoutant les champs email ,
    numéro VS et amphi """
    dataBous=[]
    dataBous.append(['Prenom','Nom','Numéro','mail','ordre VS','Amphi'])
    print()
    print()
    for k in range(1,len(ListeEtuSN)-1) :
        data=ListeEtuSN[k]
        print("k = ",k, "data =", data)
        print(len(data))
        numero,nom,prenom=data[0],data[1],data[2]
        print('go')
        print(numero)
        print(dicoMail[numero])
        L=[ prenom,nom,numero,dicoMail[numero],k,f"{amphi}"]
        dataBous.append(L)
    return dataBous



if __name__=="__main__" :
    root=tk.Tk()
    root.withdraw()
    fichier_snweb = choisir_fichier_csv(root, "CHOISIR UN FICHIER SN WEB")
    dataSN =chargeFichierCsv(fichier_snweb , encodage='latin1', delimiter=";") # attention encodage pour SNWEB
    print(dataSN[0:2])    
    ListeEtuSN = retireLignesAvantEtudiants (dataSN)
    print(ListeEtuSN[0:3])
    
    fichier_moodle = choisir_fichier_csv(root,"CHOISIR UN FICHIER ISSU DE MOODLE")
    dataMoodle =chargeFichierCsv(fichier_moodle, encodage='utf8', delimiter=",")
    print()
    print()
    print(dataMoodle[0:2])
    print('FIN DATA MOODLE')
    dicoMail=CreeDicoMail(dataMoodle)
    
    dataBous=configureListe (ListeEtuSN, 'Sc_Physiques' ,dicoMail)
    print(dataBous[:3])
    print('sauvevarde')
    
    ecritFichierCsv('AVEC_EMAIL.csv',dataBous  )
    root.mainloop()