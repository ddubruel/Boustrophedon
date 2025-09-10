import tkinter as tk
from tkinter import ttk

def modifier_configuration(Nb_zone_init=3, Nb_Rang_init=17, Nom_Amphi_init="Petit-Valrose",
                           Gauche_init=None, Centre_init=None, Droite_init=None,
                           on_config_done=None):
    amphitheatres = [
        ("Petit-Valrose", 3, 17), ("Chimie", 2, 14), ("Sc_Physiques", 2, 14),
        ("Mathématiques", 2, 14), ("Sc_Naturelles", 2, 14), ("Informatique", 2, 14),
        ("Biologie", 1, 10), ("Géologie", 1, 9)
    ]

    Gauche = Gauche_init or []
    Centre = Centre_init or []
    Droite = Droite_init or []

    window = tk.Toplevel()
    window.title("Modifier la configuration")

    # Variables
    nom_amphi_var = tk.StringVar(value=Nom_Amphi_init)
    nb_zone_var = tk.IntVar(value=Nb_zone_init)
    nb_rang_var = tk.IntVar(value=Nb_Rang_init)

    current_zone_data = {"G": Gauche, "C": Centre, "D": Droite}
    current_zone = tk.StringVar(value="G")

    # Menus pour configurer les amphithéâtres
    def update_amphi_selection(event=None):
        nom = nom_amphi_var.get()
        for amphi, zones, rangs in amphitheatres:
            if amphi == nom:
                nb_zone_var.set(zones)
                nb_rang_var.set(rangs)
                break

    top_frame = tk.Frame(window)
    top_frame.pack(pady=5)

    tk.Label(top_frame, text="Nom Amphi :").pack(side=tk.LEFT)
    amphi_menu = ttk.Combobox(top_frame, textvariable=nom_amphi_var, values=[a[0] for a in amphitheatres])
    amphi_menu.pack(side=tk.LEFT)
    amphi_menu.bind("<<ComboboxSelected>>", update_amphi_selection)

    tk.Label(top_frame, text="  Zones :").pack(side=tk.LEFT)
    tk.Label(top_frame, textvariable=nb_zone_var).pack(side=tk.LEFT)

    tk.Label(top_frame, text="  Rangs :").pack(side=tk.LEFT)
    tk.Label(top_frame, textvariable=nb_rang_var).pack(side=tk.LEFT)

    # Frame contenant les menus de rang
    frame_zones = tk.Frame(window)
    frame_zones.pack(pady=10)

    lignes_widgets = []

    def ajouter_rang():
        rang = rang_var.get()
        debut = debut_var.get()
        fin = fin_var.get()
        cote = cote_var.get()
        if debut > fin:
            debut, fin = fin, debut
        data = [rang, debut, fin, cote]
        current_zone_data[current_zone.get()].append(data)
        afficher_lignes()

    def afficher_lignes():
        for widget in lignes_widgets:
            widget.destroy()
        lignes_widgets.clear()
        zone_label = tk.Label(window, text=f"Zone {current_zone.get()} :", font=("Arial", 12, "bold"))
        zone_label.pack()
        lignes_widgets.append(zone_label)
        for ligne in current_zone_data[current_zone.get()]:
            ligne_str = f"Rang {ligne[0]} : {ligne[1]} à {ligne[2]} côté {ligne[3]}"
            lbl = tk.Label(window, text=ligne_str)
            lbl.pack()
            lignes_widgets.append(lbl)

    # Menu zone
    zone_frame = tk.Frame(window)
    zone_frame.pack(pady=5)
    tk.Label(zone_frame, text="Zone :").pack(side=tk.LEFT)
    ttk.Combobox(zone_frame, textvariable=current_zone, values=["G", "C", "D"], width=3).pack(side=tk.LEFT)

    # Sélection des rangs et côtés
    input_frame = tk.Frame(window)
    input_frame.pack()

    rang_var = tk.IntVar(value=1)
    debut_var = tk.IntVar(value=1)
    fin_var = tk.IntVar(value=1)
    cote_var = tk.StringVar(value='g')

    ttk.Combobox(input_frame, textvariable=rang_var, values=list(range(1, Nb_Rang_init + 1)), width=5).pack(side=tk.LEFT)
    ttk.Combobox(input_frame, textvariable=debut_var, values=list(range(1, 8)), width=5).pack(side=tk.LEFT)
    ttk.Combobox(input_frame, textvariable=fin_var, values=list(range(1, 8)), width=5).pack(side=tk.LEFT)
    ttk.Combobox(input_frame, textvariable=cote_var, values=["g", "d"], width=5).pack(side=tk.LEFT)

    tk.Button(input_frame, text="Valider rang", command=ajouter_rang).pack(side=tk.LEFT, padx=10)

    # Valider zone
    def valider_config():
        if on_config_done:
            on_config_done(
                nom_amphi_var.get(),
                nb_zone_var.get(),
                nb_rang_var.get(),
                current_zone_data["G"],
                current_zone_data["C"],
                current_zone_data["D"]
            )
        window.destroy()

    tk.Button(window, text="Valider la zone", command=valider_config).pack(pady=10)
