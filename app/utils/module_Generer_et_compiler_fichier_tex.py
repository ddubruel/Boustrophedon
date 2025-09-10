import subprocess
import os

def generer_fichier_latex(nom_fichier,
                          annee_universitaire,
                          date,
                          horaires,
                          duree,
                          salle,
                          lieu,
                          batiment,
                          epreuve,
                          matiere,
                          nom_image,
                          fic_tex_in,
                          scale,
                          angle):


    contenu = f"""% !TeX TS-program = lualatex
    \\documentclass[french]{{article}}

    \\renewcommand{{\\familydefault}}{{\\sfdefault}} % Définit la police sans-serif par défaut
    \\makeatletter \\renewcommand\\normalsize{{
            \\@setfontsize\\normalsize{{12pt}}{{16pt}}% police à 12 interligne à 16
    }}
     \\makeatother
     
    \\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm]{{geometry}}

    \\usepackage[utf8]{{inputenc}} % Encodage UTF-8
    \\usepackage[T1]{{fontenc}}    % Police T1 pour caractères accentués
    \\usepackage[french]{{babel}} % Langue française

    \\usepackage{{lastpage}}
    \\usepackage{{graphicx}}
    \\usepackage{{setspace}}
    \\usepackage{{fancyhdr}}

    \\pagestyle{{fancy}}
        \\lhead{{\\textbf{{Université Côte d'Azur}}}}  
        \\chead{{ {annee_universitaire} }}  
        \\rhead{{Date : {date} }}  
        \\cfoot{{\\thepage/\\pageref{{LastPage}}}} %
    \\renewcommand{{\\headrulewidth}}{{0.4pt}} 
    \\renewcommand{{\\footrulewidth}}{{0.4pt}}

    \\begin{{document}}

    \\textbf{{Date : {date}}} \\hfill  \\textbf{{Horaires {horaires}}} \\hfill \\textbf{{Durée {duree}}} \\par \\noindent

    Salle : {salle} \\hfill {lieu} \\hfill Bâtiment : {batiment} \\par \\noindent 

    Epreuve : {epreuve} \\hspace{{3cm}} {matiere} \\vspace{{5mm}}
    
    
    
    \\input{{{fic_tex_in}}}
    \\newpage
    \\includegraphics[scale={scale}, angle={angle}]{{{nom_image}}}

    \\end{{document}}
    """
    with open(nom_fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)
            print(f"Ecriture du fichier {nom_fichier}")
    return # juste pour avoir la fin !!!        
    

def compiler_latex(fichier_tex):
    dossier_sortie = "./tex_out/0_Compil"
    os.makedirs(dossier_sortie, exist_ok=True)  # Crée le dossier s'il n'existe pas

    commande = [
        "lualatex",
        "-synctex=1",
        "-interaction=nonstopmode",
        f"-output-directory={dossier_sortie}",
        fichier_tex
    ]

    subprocess.run(commande, check=True)

if __name__=='__main__' :
    print("Exécution à l'intérieur du module")
    nom_fichier="./tex_out/examen.tex"
    generer_fichier_latex(
        nom_fichier,
        annee_universitaire="ANNEE UNIVERSITAIRE 2024/2025",
        date="21/05/2025",
        horaires="11h00 à 13h00",
        duree="2h00",
        salle="SAMPVAL",
        lieu="Grand Amphi Valrose",
        batiment="SPRINCIPAL VALROSE",
        epreuve="SPUF201E",
        matiere="Système 1",
        nom_image="png_out/Amphi_Petit_Valrose.png", # relatif au .tex !!!
        fic_tex_in="./tex_out/table.tex",
        scale=0.5,
        angle=90
        )
    
    compiler_latex(nom_fichier)
    compiler_latex(nom_fichier) # 2 fois pour les numéros de pages !!