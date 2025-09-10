import tkinter as tk
class GrilleDeCases:
    def __init__(self, parent, nb_cases, nb_lignes, titre, nomAmphi):
        
        # rem le titre contient le nom de la zone 
        self.nb_cases = nb_cases
        self.nb_lignes = nb_lignes
        self.titre = titre   # contient la zone 'Gauche' 'Droite'  'Centre'

        self.frame = tk.Frame(parent, bd=2, relief="groove", padx=5, pady=5)
        self.frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.label_titre = tk.Label(self.frame, text=titre, font=("Arial", 12, "bold"))
        self.label_titre.grid(row=0, column=0, columnspan=nb_cases, pady=(0, 5))

        self.vars = []
        
        # cas spécial du Petit_Valrose avec 17 rang dont 2 réduits.. donc le 15 et 16
        if nb_lignes==17 and titre=='Gauche':
            for l in range(nb_lignes-2):
                ligne = []
                for k in range(nb_cases):
                    var = tk.IntVar()
                    chk = tk.Checkbutton(self.frame, variable=var)
                    chk.grid(row=l + 1, column=k, padx=2, pady=1)
                    ligne.append(var)
                self.vars.append(ligne)
            for l in range(nb_lignes-2,nb_lignes):
                ligne = []
                for k in range(nb_cases//2):
                    var = tk.IntVar()
                    chk = tk.Checkbutton(self.frame, variable=var)
                    chk.grid(row=l + 1, column=k, padx=2, pady=1)
                    ligne.append(var)
                self.vars.append(ligne)                
        elif nb_lignes==17 and titre=='Droite':
            for l in range(nb_lignes-2):
                ligne = []
                for k in range(nb_cases):
                    var = tk.IntVar()
                    chk = tk.Checkbutton(self.frame, variable=var)
                    chk.grid(row=l + 1, column=k, padx=2, pady=1)
                    ligne.append(var)
                self.vars.append(ligne)
            for l in range(nb_lignes-2,nb_lignes):
                ligne = []
                for k in range(nb_cases - nb_cases//2 , nb_cases):
                    var = tk.IntVar()
                    chk = tk.Checkbutton(self.frame, variable=var)
                    chk.grid(row=l + 1, column=k, padx=2, pady=1)
                    ligne.append(var)
                self.vars.append(ligne)            
        elif   ( 'Sc_Naturelles' in nomAmphi or  'Informatique' in nomAmphi )  : # cas des places PMR dans les amphis            
            
            for l in range(nb_lignes):
                ligne = []
                if l==0 and titre=='Gauche' :
                    for k in range(1+ nb_cases//3 , nb_cases): # le tiers est condamné !
                        var = tk.IntVar()
                        chk = tk.Checkbutton(self.frame, variable=var)
                        chk.grid(row=l + 1, column=k, padx=2, pady=1)
                        ligne.append(var)
                    self.vars.append(ligne)
                else :
                    for k in range(nb_cases):
                        var = tk.IntVar()
                        chk = tk.Checkbutton(self.frame, variable=var)
                        chk.grid(row=l + 1, column=k, padx=2, pady=1)
                        ligne.append(var)
                    self.vars.append(ligne)                        
        elif   ( 'Mathématiques' in nomAmphi or  'Sc_Physiques' in nomAmphi )   :
            for l in range(nb_lignes):
                ligne = []
                if l==0 and titre=='Droite' :
                    for k in range( nb_cases - nb_cases//3 -1 ): # le tiers est condamné !
                        var = tk.IntVar()
                        chk = tk.Checkbutton(self.frame, variable=var)
                        chk.grid(row=l + 1, column=k, padx=2, pady=1)
                        ligne.append(var)
                    self.vars.append(ligne)
                else :
                    for k in range(nb_cases):
                        var = tk.IntVar()
                        chk = tk.Checkbutton(self.frame, variable=var)
                        chk.grid(row=l + 1, column=k, padx=2, pady=1)
                        ligne.append(var)
                    self.vars.append(ligne)
                        
        elif ( 'Chimie' in nomAmphi ) :
            for l in range(nb_lignes):
                ligne = []
                if l==0 and titre=='Droite' :
                    for k in range( nb_cases - nb_cases//2  ): # la moitié est condamnée !
                        var = tk.IntVar()
                        chk = tk.Checkbutton(self.frame, variable=var)
                        chk.grid(row=l + 1, column=k, padx=2, pady=1)
                        ligne.append(var)
                    self.vars.append(ligne)
                else :
                    for k in range(nb_cases):
                        var = tk.IntVar()
                        chk = tk.Checkbutton(self.frame, variable=var)
                        chk.grid(row=l + 1, column=k, padx=2, pady=1)
                        ligne.append(var)
                    self.vars.append(ligne)
               
        else :
            print(nomAmphi)
            print ( 'SC_Naturelles' in nomAmphi or  'Informatique' in nomAmphi )
            for l in range(nb_lignes):
                ligne = []
                for k in range(nb_cases):
                    var = tk.IntVar()
                    chk = tk.Checkbutton(self.frame, variable=var)
                    chk.grid(row=l + 1, column=k, padx=2, pady=1)
                    ligne.append(var)
                self.vars.append(ligne)
        


        self.btn_afficher = tk.Button(self.frame, text=f"Sous total ({titre})",
                                      command=self.afficher_cases_cochees)
        self.btn_afficher.grid(row=nb_lignes + 1, column=0, columnspan=nb_cases, pady=(5, 0))

        self.result_label = tk.Label(self.frame, text="", font=("Arial", 9))
        self.result_label.grid(row=nb_lignes + 2, column=0, columnspan=nb_cases)
        
        self.nbCochee=0 # pour compter les cases cochées.

        self.listeCaseCochees = [] #  la liste des case cochées sous la forme Cases cochées (ligne, colonne) : [(3, 0), (4, 1), (5, 2), (6, 3), (9, 3)]

    def afficher_cases_cochees(self):
        listePourUneZone = []
        self.nbCochee=0
        if self.titre=='Gauche' or self.titre=='Centre' :
            for row, ligne in enumerate(self.vars):
                for col, var in enumerate(ligne):
                    if var.get() == 1:
                        listePourUneZone.append((row, col))
                        self.nbCochee = self.nbCochee + 1 
        # Traitement de la zone Droite du 'Petit_Valrose' :                
        elif self.titre=='Droite'  :
            for row, ligne in enumerate(self.vars):
                if row<= 14 :
                    for col, var in enumerate(ligne):
                        if var.get() == 1:
                            listePourUneZone.append((row, col))
                            self.nbCochee = self.nbCochee + 1
                elif row > 14  :  # on décale un peu la numérotation
                    for col, var in enumerate(ligne  ):
                        if var.get() == 1:
                            listePourUneZone.append((row, col + self.nb_cases - self.nb_cases//2 ))
                            self.nbCochee = self.nbCochee + 1
        print(f"{self.titre} - Cases cochées (ligne, colonne) :", listePourUneZone)
        print(f"{self.titre} - Nombre de places dans la zone :", self.nbCochee)
        self.result_label.config(text=f"Nombre de places : {self.nbCochee}")                
        
    
      
        
        