import tkinter as tk
from tkinter import messagebox
#
import os
import sys
# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, 'app'))
sys.path.insert(0, project_root)

# charge directement depuis app
from utils.chargeCsv import lit_fichier_csv_et_separe_entete
from utils.gestion_json import sauvFicJson, chargFicJson
from utils.traitementListe import majuscule
from utils.afficheConsigne import afficheConsigne

# 
from utils.p1_Dessine_amphi_a_partir_de_la_grille import Main_Etape_1
from utils.p2_boustro import Main_etape_2

from classes.classe_choixAmphi import choixAmphi
from classes.classe_fusionDataMoodleApogee import fusionDataMoodleApogee

# fenetre de dialogue pour charger fichier csv :
from widget.choixCsv  import  choisir_fichier_csv

class BoustrophedonStructure:
    def __init__(self, root):
        self.root = root
        self.root.title("Composition des amphithéatre.")
        
        #les attributs :
        self.listeEtu : list[list[str]] =[] # la liste des étudiants.
        self.nbEtudiant  : int = 0  #
        self.goEtape2 : bool =False # booléen pour autoriser le passage à l'étape 2.
        
        # fin de la définition des attributs.
        
        self.interface() # dessine l'interface qui ordonne les étapes (instance principale de tkinter).
        
        
    def interface(self) :
        # Etape 0
        tk.Label(root, text="Étape 1 , définition de la liste des étudiants.",
                       font=("Arial", 11, "bold")).pack(pady=10)        
        self.btn0 = tk.Button(root, text="Pour Examen : Charger data Apogée et Moodle ",
                              command=self.run_etape0).pack(pady=5)
        
        self.btn0partiel = tk.Button(root, text="Pour un partiel : Charger data  Moodle ",
                              command=self.run_etape0partiel).pack(pady=5)
        # Etape 1
        tk.Label(root, text="Étape 2 , Choisir un fichier étudiant.",
                       font=("Arial", 11, "bold")).pack(pady=10)          
        self.btn1 = tk.Button(root, text="1. Charger le fichier étudiant ",
                              command=self.run_etape1).pack(pady=5)
        
         # 
        # Etape 2
        tk.Label(root, text="Étape 2 , Plan de l'amphithéatre.",
                       font=("Arial", 11, "bold")).pack(pady=10) 
        self.btn2 = tk.Button(root,
                  text="2. Choisir et définir le plan de l'amphithéatre",
                  command=self.run_etape2,
                  state = tk.DISABLED )
        self.btn2.pack(pady=5)
        
        # Etape 3
        self.btn3 = tk.Button(root,
                              text="3. Générer les tableaux d'émargement",
                              command=self.run_etape3,
                              state = tk.DISABLED 
                              )
        self.btn3.pack(pady=5)
# 
#         # Étape 4 : Envoi des emails
#         tk.Button(root, text="4. Envoyer les emails aux étudiants", command=self.run_etape4).pack(pady=5)

        # Bouton de sortie
        tk.Button(root, text="Quitter", command=self.root.destroy ).pack(pady=10)
    
    def run_etape0(self) :
        """" charge le fichier APOGEE et le fichier MOODLE , cela défini le chemin pour les fichiers de travail.
            Cette étape est nécessaire pour un examen."""
        chemin = fusionDataMoodleApogee(self.root)
        self.cheminApogee = chemin.cheminDuFichierApogee
        self.dictCheminAbsolus=chemin.dictCheminAbsolus # tous les chemins
        
        
    def run_etape0partiel(self) :
        """ charge uniquement fichier MOODLE , cela défini le chemin pour les fichiers de travail.
            Cette étape est nécessaire pour un examen."""
        
        
        
    def run_etape1(self):
        # chargement de la liste des étudiants DANS le répertoire racine du fichier Apogée :
        nomCsv = choisir_fichier_csv(self.root, rep=self.cheminApogee)        
        #self.listeEtu est une liste de sous-liste ,
        #   une sous-liste contient Nom, prénom et numéro d'étudiant.
        self.listeEtu  ,  entete = lit_fichier_csv_et_separe_entete(nomCsv)
        self.amphi = self.listeEtu[0][5] # on récupère le nom de l'amphithéatre du fichier.
        
        self.listeEtu = majuscule(self.listeEtu) 
       
        self.nbEtudiant  =len(self.listeEtu)
        print(f"Il y a {self.nbEtudiant} étudiant(e)s  à placer.")
        
        if self.nbEtudiant !=0 :
            self.btn2.config(state=tk.NORMAL)
        #self.listeCasesCochees, self.nb_places, self.Nb_rang, self.nomAmphi , self.zones =Main_Etape_1(self.root)
                                
        print('FIN Main_Etape_1')
        
#         lignes, enteteFichier = lit_fichier_csv_et_separe_entete(nomCsv_noms_etudiants)
# 
# 
#         Nb_etudiant_a_placer = len(lignes)
#         print("Nombre d'étudiants dans le fichier ",Nb_etudiant_a_placer)
#         print()
#         
#         majusculeNomFamille(lignes)
#         random.shuffle(lignes)  # mélange de la liste à placer
        

    def run_etape2(self):
        def fctRappelVersMain(data) :
            """ fonction de rappel pour l'instance de la classe choixAmphi"""
            self.zones     = data["zones"]
            self.nb_places = data["nb_places"]
            self.Nb_rang   = data["Nb_rang"]
            self.amphi     = data["amphi"]            
            self.grilles = data["grilles"]
            print('\n \n dans main() ....')
            self.data = data
            
            self.listeCasesCochees=[] 
            for cle in self.grilles :
                self.listeCasesCochees.append(self.grilles[cle])
                
            #exemple 'grilles': {'Gauche': [[16, 2]], 'Centre': [[16, 1]], 'Droite': [[16, 1]]} }
            
            
            
            # lancement de la visualisation graphique de la géométrie de l'amphithéatre
            (self.Liste_refDesPlaces,
             self.Liste_des_nomFichiersPng ,
             self.nomFicJson_places_seules,
             self.nomFicJson_places_et_chemin_img,
             self.nomFicPlanAmphiPng              ) = Main_Etape_1(
                                                    self.root,
                                                    self.listeCasesCochees,
                                                    self.nb_places,
                                                    self.Nb_rang,
                                                    self.amphi  ,
                                                    self.zones  ,
                                                    self.dictCheminAbsolus)
            
            afficheConsigne("Consignes", 'Vous pouvez faire : \n'
                                          '1) Modifier la configuration. \n'
                                          '2) puis Visualiser la configuration. \n'
                                          'ou :\n'
                                          '1) Fermer le plan (avec la petitre croix). \n'
                                          '2) Fermer la fenêtre "Choix et définition".\n'
                                          '3) Cliquer sur le bouton de "Générer les tables etc".'
            )
            self.btn3.config(state=tk.NORMAL) # pour activer le bouton de génération des émargements.
                
        # instanciation de la classe choixAmphi pour aller récupérer les param
        # qui seront remontés avec la fonction de rappel.    
        choixAmphi(root,largeur = 1200,hauteur=1200,amphiDuFichierApogee = self.amphi,  fctRappelVersMain = fctRappelVersMain )            
        
            
    def run_etape3(self):
        
        # utilisation de p2_etc...
#         sortie de Main_Etape_1 :
#             ( self.Liste_refDesPlaces,
#              self.Liste_des_nomFichiersPng ,
#              ,
#              ,
#              self.nomFicPlanAmphiPng )
        print(self.dictCheminAbsolus)
        
        Main_etape_2(self.root,
                 self.nomFicJson_places_seules,
                 self.nomFicJson_places_et_chemin_img,
                 self.amphi  ,
                 self.zones,
                 self.dictCheminAbsolus
                  )
        messagebox.showinfo("Succès", f"L'étape 3 été exécutée avec succès.")
                                     

    def run_etape4(self):
        Main_etape_4( self.root)
        
#        self.run_script("p4_envoi_mail_et_PJ.py")

#    def run_script(self, filename):
#        try:
#            subprocess.run(["/home/denis/Env_virtuel_python/bin/python", filename], check=True)
            #messagebox.showinfo("Succès", f"Le script {filename} a été exécuté avec succès.")
#        except subprocess.CalledProcessError as e:
#            messagebox.showerror("Erreur", f"Échec de l'exécution de {filename} :\n{e}")


if __name__ == '__main__':
    root = tk.Tk()
    app = BoustrophedonStructure(root)
    root.mainloop()
