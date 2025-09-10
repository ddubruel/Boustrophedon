import tkinter as tk

import os
import sys
# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__) 
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)


    
from utils.pour_classe_rangs import save_canvas


class GraphiqueUneZone:    
    def __init__(self,
                 canvas,
                 xhg, yhg, longueur, espace,
                 nb_places_par_rang_pour_cette_zone,
                 Nb_rang,
                 zone, # 'Gauche','Centre' ou  'Droite'
                 nomAmphi,  # chaine du genre 'Amphithéatre Chimie'
                 couleurZone,
                 listeCasesCocheesZone,
                 cheminsAbsolus
                 ):
            
        self.canvas = canvas
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.xhg = xhg   # abscisse coin haut à gauche
        self.yhg = yhg
 
        self.longueur =longueur
        self.espace = espace      # espace entre 2 bancs
        self.nb_places_par_rang_pour_cette_zone = nb_places_par_rang_pour_cette_zone 
        self.Nb_rang=Nb_rang # 9 10 14 ou  17
        self.titre=zone  # 'Gauche','Centre' ou  'Droite'
        self.nomAmphi =  nomAmphi    # 'Chimie' par exemple.
        self.couleurZone=couleurZone
        self.listeCasesCocheesZone = listeCasesCocheesZone 
        self.listeDesPlaces=[] # les places codées en D-1-4 par exemple à partir de listeCasesetc...
        self.liste_nom_fic_png=[] # la liste vers les fichiers de l'amphi avec place entourée

        self.cheminsAbsolus = cheminsAbsolus
        print(self.cheminsAbsolus)
        self.cheminPourPngOut = cheminsAbsolus[(self.nomAmphi ,'1_png_out' )]
#        base_dir = os.path.dirname(os.path.abspath(__file__))
#         # Remonte vers la racine du projet (../../ depuis ce fichier)
#         racineProjet = os.path.abspath(os.path.join(base_dir, '..', '..'))
#         # Construit le chemin absolu vers png_ou
#         self.cheminPourPngOut = os.path.join(racineProjet, 'data','png_out')
        
        self.démarre()
                        
    def démarre(self) :
        self.dessine() # OK
        self.colorieZone()
        self.canvas.update_idletasks() # pour lancer le temps à la fenêtre d'etre tracée.
        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height() 
        self.canvas.create_text(largeur // 2, 25, text=f"  {self.nomAmphi}", font="arial 20", tags="nom_amphi_text")
        self.canvas.create_text(25, 25, text=f"Haut", font="arial 12")
        self.canvas.create_text(largeur-30, 25 , text=f"Haut", font="arial 12")
        
        self.canvas.create_text(25, hauteur-20, text=f"Bas", font="arial 12")
        self.canvas.create_text(largeur-30, hauteur-20 , text=f"Bas", font="arial 12")
        
        self.canvas.create_rectangle(largeur // 2 - 220, hauteur-50-20, largeur // 2 + 220, hauteur-50+20, fill="yellow", outline="", tags="bg_bas")
        self.canvas.create_text(largeur // 2, hauteur-50, text="Zone de dépôts des sacs et téléphones...", font="Arial 15", fill="red", tags="text_bas")
        
        x_milieu_zone = self.xhg + self.longueur//2
        y_bas_zone =  self.yhg + self.Nb_rang * self.espace
        self.canvas.create_text(x_milieu_zone, y_bas_zone, text=f"{self.titre}", font="arial 17")
        self.ecritLaPlace()
        #self.entourePlaceEtSauveFicPng() à utiliser en dehors de la classe un fois toutes les instances des zones existante, sinon le dession est en partie blanc.
        
        
    def dessine(self):
        """"Dessine les traits représentants les pupitres"""
        x0=self.xhg
        y0=self.yhg
        x1=x0+self.longueur
        y1=y0
        if self.Nb_rang <= 14 : # tous les amphis sauf Petit_Valrose
            for k in range(1, self.Nb_rang+1 ,1) :             
                y0=self.yhg +(k-1)* self.espace   # k=1 vaut yhg puis yhg+decalage etc...
                y1=y0
                self.canvas.create_line(x0, y0, x1, y1, width=2)
        if 'Petit_Valrose' in  self.nomAmphi :
            for k in range(1, 16 ,1) :             
                y0=self.yhg +(k-1)* self.espace   # k=1 vaut yhg puis yhg+decalage etc...
                y1=y0
                self.canvas.create_line(x0, y0, x1, y1, width=2)
            # on termine pour les 2 rangs du bas en fonction des zones.
            if     self.titre=='Gauche' :
                x1=x0+self.longueur//2   # on dessine les bancs plus courts.
                for k in range(16, self.Nb_rang+1 ,1) :                    
                    y0=self.yhg +(k-1)* self.espace   
                    y1=y0
                    self.canvas.create_line(x0, y0, x1, y1, width=2)
                ymin = self.yhg + 14  *  self.espace + 1
                ymax = self.yhg + 16  *  self.espace + 2  # + 2 pour effacer le trait du grand rectangle
                xmin = x0 + self.longueur//2 
                xmax = x0 + self.longueur   + 2  # + 2 pour effacer le trait du grand rectangle
                self.canvas.create_rectangle(xmin, ymin , xmax, ymax, fill='white',outline="")                                                  
            elif   self.titre=='Droite' :
                x0 = self.xhg  + self.longueur//2
                x1=self.xhg+self.longueur # on va au bout.
                for k in range(14, self.Nb_rang+1 ,1) :                 
                    y0=self.yhg +(k-1)* self.espace  
                    y1=y0
                    self.canvas.create_line(x0, y0, x1, y1, width=2)
                    ymin = self.yhg + 14  *  self.espace + 1
                    ymax = self.yhg + 16  *  self.espace + 2  # + 2 pour effacer le trait du grand rectangle
                    xmin = self.xhg -2  # - 2 pour effacer le trait du grand rectangle
                    xmax = self.xhg + self.longueur //2   
                    self.canvas.create_rectangle(xmin, ymin , xmax, ymax, fill='white',outline="")                                       
            else  : # zone 'Centre'
                for k in range(14, self.Nb_rang+1 ,1) :                    
                    y0=self.yhg +(k-1)* self.espace  
                    y1=y0
                    self.canvas.create_line(x0, y0, x1, y1, width=2)

            
    def colorieZone(self):
        if self.couleurZone!="":
            x0=self.xhg
            y0=self.yhg   -self.espace     
            x1=self.xhg+self.longueur
            y1=self.yhg+(self.Nb_rang-1)* self.espace            
            rect=self.canvas.create_rectangle(x0, y0 , x1, y1, fill=self.couleurZone)            
            self.canvas.lower(rect)

    def referencePlace(self,row,col):
        prefixe_zone = self.titre[0]    
        rang = self.Nb_rang - row
        numero_place = self.nb_places_par_rang_pour_cette_zone - col
        reference_place = prefixe_zone+"-"+str(rang) +"-"+str(numero_place)
        pas = int (  0.8 * self.longueur  //   (self.nb_places_par_rang_pour_cette_zone - 1)  )  
        xtex = self.xhg + 0.1 * self.longueur + pas * col 
        ytex = self.yhg + row* self.espace 
        return xtex,ytex, reference_place
            
    def ecritLaPlace(self) :
        
        for k, (row,col) in enumerate(self.listeCasesCocheesZone) :            
            xtex,ytex, reference_place = self.referencePlace(row,col)
            self.listeDesPlaces.append(reference_place)
            self.canvas.create_text(xtex, ytex-15,text=reference_place)
            self.canvas.update_idletasks() # pour lancer le temps à la fenêtre d'etre tracée.
            print(reference_place)
                        
    def entourePlaceEtSauveFicPng(self):
        """ à utiliser en dehors sur le graphique final
        contenant toutes les instances ou zones dessinées"""                
        for k, (row,col) in enumerate(self.listeCasesCocheesZone) :
            xtex,ytex, reference_place = self.referencePlace(row,col)                                
            nomFicPng = os.path.abspath(f"{self.cheminPourPngOut}/{reference_place}.png")            
            print('Dans entourePlaceEtSauveFicPng nomFicPng= ',nomFicPng)                            
            self.liste_nom_fic_png.append(nomFicPng)
                        
            R=28
            xC=xtex
            yC=ytex-10                                                            
            self.ref = self.canvas.create_oval(xC-1.4*R,yC-R,xC+1.4*R, yC+R,  outline='red',width=3)  
            self.canvas.winfo_toplevel().update() #root.update()
#            self.canvas.update_idletasks() # pour lancer le temps à la fenêtre d'etre tracée.
            self.canvas.after(200)
            # rem nomFicPng est défini qq lignes au-dessus.
            save_canvas(nomFicPng, self.canvas)                    
            self.canvas.delete(self.ref) # Effacer juste le cercle après la capture
        print('Dans la classe  self.liste_nom_fic_png = ',self.liste_nom_fic_png)
        
    def sauvePlanAmphi(self) :
        self.canvas.winfo_toplevel().update() #root.update()
        self.canvas.after(200)
        self.nomFicPlanAmphiPng = os.path.abspath(f"{self.cheminPourPngOut}/{self.nomAmphi}.png")            
        print(f"Dans entourePlaceEtSauveFicPng nomFicPlanAmphiPng= {self.nomFicPlanAmphiPng}")
        
        save_canvas(self.nomFicPlanAmphiPng, self.canvas) 

if __name__=="__main__" :
    # test Amphi Geo 9 rangs !!!
    # test Amphi Geo 9 rangs !!!
    # test Amphi Geo 9 rangs !!!
    # test Amphi Geo 9 rangs !!!
#     root = tk.Tk()
#     couleurZone=['lightyellow'], ['honeydew'], ['mistyrose']
#     Nb_rang = 9
#     nb_places_par_rang_pour_cette_zone=[5]
#     # donc ici  0<= col <= 4 et   0<= row <= 9 
#     listeCasesCochees =[[(0, 0),(0,1),(0,2),(0,3),(0,4), (8, 0), (8,4)]]
#     
#     
#     root.geometry("550x700")
#     canvas = tk.Canvas(root,bg="white")
#     
#     scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
#     canvas.configure(yscrollcommand=scrollbar.set)
#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    
#     canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)        
#     scroll_frame = tk.Frame(canvas)
#     canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
#     scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
#     grilles_frame = tk.Frame(scroll_frame)
#     grilles_frame.pack()
#         
#     # Test Amphie Bio ou Géo      
#     xhg, yhg = 50, 100
#     longueur, espace = 400, 40
#     
#     
#     zone='Centre' # extrait de la liste !!
#     nomAmphi = 'Amphithéatre Biologie'  # chaine du genre 
#     GraphiqueUneZone(canvas,
#                  xhg, yhg, longueur, espace,
#                  nb_places_par_rang_pour_cette_zone[0],
#                  Nb_rang,
#                  zone, # 'Gauche','Centre' ou  'Droite'
#                  nomAmphi,  # chaine du genre 'Amphithéatre Chimie'
#                  couleurZone[1],
#                  listeCasesCochees[0]
#                  )
#     root.mainloop()
    
    # test Amphi Bio 10 rangs !!!
    # test Amphi Bio 10 rangs !!!
    # test Amphi Bio 10 rangs !!!
    # test Amphi Bio 10 rangs !!!
    root = tk.Tk()
    couleurZone=['lightyellow'], ['honeydew'], ['mistyrose']
    Nb_rang = 10
    nb_places_par_rang_pour_cette_zone=[5]
    # donc ici  0<= col <= 4 et   0<= row <= 9 
    listeCasesCochees =[[(0, 0),(0,1),(0,2),(0,3),(0,4), (9, 0), (9,4)]]
    
    
    root.geometry("550x700")
    canvas = tk.Canvas(root,bg="white")
    
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)        
    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    grilles_frame = tk.Frame(scroll_frame)
    grilles_frame.pack()
        
    # Test Amphie Bio ou Géo      
    xhg, yhg = 50, 100
    longueur, espace = 400, 40
    
    
    zone='Centre' # extrait de la liste !!
    nomAmphi = 'Biologie'  # chaine du genre
    
    cheminsAbsolus = {('Biologie', '1_png_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/1_png_out',
                   ('Biologie', '3_tex_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/3_tex_out',
                   ('Biologie', '4_liste_émargements_pdf'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/4_liste_émargements_pdf',
                   ('Biologie', '2_csv_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/2_csv_out',
                   ('Biologie', '5_json_out'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/5_json_out',
                   ('Biologie', 'zoneDeTransfert'): '/home/denis/00_Universite/Boustrophedon_Mai_2025/ZZ_Version_finale/BOUS_structure/data/Donnees_Etudiants_Apogee_et_Moodle/Amphi_Biologie/2_csv_out/zoneDeTransfert' }

    
    GraphiqueUneZone(canvas,
                 xhg, yhg, longueur, espace,
                 nb_places_par_rang_pour_cette_zone[0],
                 Nb_rang,
                 zone, # 'Gauche','Centre' ou  'Droite'
                 nomAmphi,  # chaine du genre 'Amphithéatre Chimie'
                 couleurZone[1],
                 listeCasesCochees[0],
                 cheminsAbsolus
                 )
    root.mainloop()