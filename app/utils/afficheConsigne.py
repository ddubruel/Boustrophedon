import tkinter as tk

def afficheConsigne (title, message):
    win = tk.Toplevel()
    win.title(title)
    win.configure(bg="white")  # fond blanc autour

    # Cadre principal
    frame = tk.Frame(win, bg="white", padx=10, pady=10)
    frame.pack()

    # Zone de texte non redimensionnable
    text = tk.Text(frame, wrap="word", height=10, width=60, bg="white", relief="flat", borderwidth=0)
    text.insert("1.0", message)
    text.config(state="disabled")
    text.pack()

    # Bouton Fermer en dessous
    btn = tk.Button(frame, text="Fermer", command=win.destroy)
    btn.pack(pady=(10, 0))

    # Empêche la fenêtre d'être trop grande
    win.resizable(False, False)

if __name__=="__main__" :
    # Exemple
    afficheConsigne("Succès", "Vous pouvez faire :\n\n- Action 1\n- Action 2\n- Action 3\nEt encore plus si besoin...")
