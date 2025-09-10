import tkinter as tk
from tkinter import filedialog
 
def choisir_fichier_csv(master ,  titre="Choisir un fichier CSV",rep="./data/listes_etudiants"):
    window = tk.Toplevel(master)
    window.withdraw()  # Ne pas afficher cette fenêtre secondaire

    nom_fichier = filedialog.askopenfilename(
        title=titre,
        initialdir=rep,
        filetypes=[("Fichiers CSV", "*.csv")],
    )

    return nom_fichier