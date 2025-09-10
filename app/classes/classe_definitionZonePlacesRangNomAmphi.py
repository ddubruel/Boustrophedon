import tkinter as tk

class definitionZonePlacesRangNomAmphi:
    
    """ Présente les widget pour définir les éléments du dictionaire:
                {
                "zones": self.zones,   # liste   ex : ['Gauche','Droite']
                "nb_places": self.nb_places,   [6,7,6] pour le PV.
                "Nb_rang": self.nbRang,      9, 10 ,14 ou  17
                "amphi": self.nom_amphi    'Biologie' ou etc.
                }
                """
    
    def __init__(self, parent, tousLesAmphis, fctRappel = None , data = None):
        self.parent=parent
        self.tousLesAmphis = tousLesAmphis
        self.fctRappel = fctRappel
        self.data = data
        
        self.fenetre_choix = tk.Toplevel(parent, bg='lightgray')
        self.fenetre_choix.title("Choix de l'Amphithéâtre")
        
        if self.data== None :
            self.initialisePourAmphiVide()
        
    def initialisePourAmphiVide (self) :
        # Initialisation de la variable avec la première valeur
        self.selection_amphi = tk.StringVar(self.fenetre_choix)
        self.selection_amphi.set(self.tousLesAmphis[0])  # Affiche le premier par défaut

        self.nbRang = 0
        self.nb_places = []
        self.zones = []

        self.nom_amphi = self.selection_amphi.get() 
        # Label + Menu déroulant
        tk.Label(self.fenetre_choix, text="Choisir un amphithéâtre :", bg='lightgray', font=("Arial", 12)).pack(pady=(10, 5))
        self.menu_amphi = tk.OptionMenu(self.fenetre_choix,  # la fenêtre
                                        self.selection_amphi, # le choix affiché par
                                                              # défaut ou modifié par user
                                        *self.tousLesAmphis,     # la liste de choix possible
                                        command=self.maj_interface) # la commande
        
        self.menu_amphi.config(width=20)  # Largeur fixe pour voir le texte sélectionné
        self.menu_amphi.pack(pady=(0, 10))

        self.zone_frame = tk.Frame(self.fenetre_choix, bg='lightgray')
        self.zone_frame.pack(pady=10)

        self.bouton_valider = tk.Button(self.fenetre_choix, text="Valider 1", command=self.valider)
        self.bouton_valider.pack(pady=10)

        # Appelle une première fois pour initialiser selon la première valeur
        self.maj_interface(self.tousLesAmphis[0])
        
    def initialisePourAmphiAvecData (self) :
        pass
        
    def maj_interface(self, nom_amphi):
    
        self.nom_amphi = nom_amphi
        
        for widget in self.zone_frame.winfo_children():
            widget.destroy()

        self.zones = []
        self.nb_places = []

        if nom_amphi == 'Biologie':
            self.nbRang = 10
            self.ajouter_champ_rangs("Nombre de places dans un rang :", default=4)

        elif nom_amphi == 'Géologie':
            self.nbRang = 9
            self.ajouter_champ_rangs("Nombre de places dans un rang :", default=4)

        elif nom_amphi in ['Sc_Physiques', 'Chimie', 'Sc_Naturelles', 'Informatique','Mathématiques']:
            self.nbRang = 14
            self.ajouter_double_champ_rangs("Nombre de places dans un rang  (zone Gauche)",
                                            "Nombre de places dans un rang  (zone Droite)",
                                            default_gauche=6,
                                            default_droite=6)

        elif nom_amphi == 'Petit_Valrose':
            self.nbRang = 17
            self.ajouter_triple_champ_rangs("Nombre de places dans un rang  (zone Gauche)",
                                            "Nombre de places dans un rang  (zone Centre)",
                                            "Nombre de places dans un rang  (zone Droite)",
                                            defaults=[6, 7, 6])
        

    def ajouter_champ_rangs(self, label, default=4):
        tk.Label(self.zone_frame, text=label, bg='lightgray').grid(row=0, column=0, sticky="w")
        self.entry = tk.Entry(self.zone_frame)
        self.entry.insert(0, str(default))
        self.entry.grid(row=0, column=1)
        self.zones = ['Centre']

    def ajouter_double_champ_rangs(self, label1, label2, default_gauche, default_droite):
        tk.Label(self.zone_frame, text=label1, bg='lightgray').grid(row=0, column=0, padx=5)
        self.entry1 = tk.Entry(self.zone_frame, width=5)
        self.entry1.insert(0, str(default_gauche))
        self.entry1.grid(row=0, column=1, padx=5)

        tk.Label(self.zone_frame, text=label2, bg='lightgray').grid(row=0, column=2, padx=5)
        self.entry2 = tk.Entry(self.zone_frame, width=5)
        self.entry2.insert(0, str(default_droite))
        self.entry2.grid(row=0, column=3, padx=5)

        self.zones = ['Gauche', 'Droite']

    def ajouter_triple_champ_rangs(self, label1, label2, label3, defaults):
        tk.Label(self.zone_frame, text=label1, bg='lightgray').grid(row=0, column=0, padx=5)
        self.entry1 = tk.Entry(self.zone_frame, width=5)
        self.entry1.insert(0, str(defaults[0]))
        self.entry1.grid(row=0, column=1, padx=5)

        tk.Label(self.zone_frame, text=label2, bg='lightgray').grid(row=0, column=2, padx=5)
        self.entry2 = tk.Entry(self.zone_frame, width=5)
        self.entry2.insert(0, str(defaults[1]))
        self.entry2.grid(row=0, column=3, padx=5)

        tk.Label(self.zone_frame, text=label3, bg='lightgray').grid(row=0, column=4, padx=5)
        self.entry3 = tk.Entry(self.zone_frame, width=5)
        self.entry3.insert(0, str(defaults[2]))
        self.entry3.grid(row=0, column=5, padx=5)

        self.zones = ['Gauche','Centre', 'Droite']

    def valider(self):        
        print('Lancement de self.valider')

        if self.nom_amphi in ['Biologie', 'Géologie']:
            try:
                val = int(self.entry.get())
                self.nb_places = [val]
            except:
                print("Entrée invalide")
                return

        elif self.nom_amphi in ['Sc_Physiques', 'Chimie', 'Sc_Naturelles', 'Informatique','Mathématiques' ]:
            try:
                gauche = int(self.entry1.get())
                droite = int(self.entry2.get())
                self.nb_places = [gauche, droite]
            except:
                print("Entrée invalide")
                return

        elif self.nom_amphi == 'Petit_Valrose':
            try:
                gauche = int(self.entry1.get())
                centre = int(self.entry2.get())
                droite = int(self.entry3.get())
                self.nb_places = [gauche, centre, droite]
            except:
                print("Entrée invalide")
                return
        self.fenetre_choix.destroy()
        # Appel du callback avec les données
        if self.fctRappel:
            self.fctRappel({
                "zones": self.zones,
                "nb_places": self.nb_places,
                "Nb_rang": self.nbRang,
                "amphi": self.nom_amphi
            })        
        

if __name__=="__main__" :
    root = tk.Tk()
    root.withdraw()
    listeAmphi = ['Biologie' ,'Géologie' ,
                  'Petit_Valrose','Sc_Physiques',
                'Chimie', 'Sc_Naturelles',
                'Informatique','Mathématiques' ]
    
    def fctRappelValider(data):
        # pour utilisation dans classe penser à remplacer zones par self.zones etc !!!
            zones     = data["zones"]
            nb_places = data["nb_places"]
            Nb_rang   = data["Nb_rang"]
            amphi     = data["amphi"]            
            print(f"\n Données validées de l'amphi: \n  "
                  f"Nom : {amphi} \n"
                  f"zone(s) {zones} \n "
                  f"Nombre de places par rang et par zone(s) {nb_places} \n"
                  f"Nombre de rang dans l'amphithéatre {Nb_rang} \n\n"
                  f" print('Dans AmphiVide') Après... ")
            
    instance = definitionZonePlacesRangNomAmphi(root, listeAmphi,fctRappelValider)

    
    root.mainloop()
                                    