import csv
from app.utils.module_gestion_fichiers import chargeFichierCsv


def ecrit_fichier_tex(latex_filename,latex_code):
    with open(latex_filename, "w", encoding="utf-8") as texfile:
        texfile.write(latex_code)
    print("Le fichier LaTeX a été généré dans", latex_filename)
    
def passeSurDeuxLignes(chaine):
    """
    Transforme un nom en une version LaTeX avec \\shortstack{...},
    en séparant les parties sur deux lignes selon un espace ou un tiret.
    
    :param noms: str, le nom à transformer
    :return: str, la chaîne formatée pour LaTeX
    """
    import re
    
    chaine=re.sub(r'--', r'-', chaine)
    chaine=re.sub(r' -', r' ', chaine)
    
    # Séparer sur le premier espace ou tiret trouvé
    match = re.split(r'[ -]', chaine, maxsplit=1)
    
    if len(match) == 2:
        return f'\\shortstack{{{match[0]} \\\\ {match[1].capitalize()}}}'
    else:
        return chaine  # Retourner inchangé s'il n'y a pas de séparateur


def Remplit_table_Latex(data_rows,chunk_size) :     
    # Liste pour stocker le code LaTeX de chaque tableau
    latex_tables = []
    # ajoute un \n à la place des tirets 
    # Création d'un tableau pour chaque bloc de données
    for i in range(0, len(data_rows), chunk_size):
        chunk = data_rows[i:i+chunk_size]
        table = r"""\begin{tabular}{|l|l|l|l|p{6cm}|}
    \hline
    Noms & Prénoms & Numéro & Place & Signature \\
    \hline
    """
        for row in chunk:
            # On récupère les 4 premières colonnes en gérant d'éventuelles lignes incomplètes
            prenoms = passeSurDeuxLignes(row[1]) if len(row) > 0 else ""
            noms    = passeSurDeuxLignes(row[0]) if len(row) > 1 else ""
            numero  = row[2] if len(row) > 2 else ""
            place   = row[6] if len(row) > 3 else ""
                        
            # On ajoute \rule{0pt}{1cm} dans la première case pour imposer une hauteur minimale de 1 cm
            table += f"\\rule{{0pt}}{{1cm}} {prenoms} & {noms} & {numero} & {place} & \\\\ \\hline\n"
        table += r"\end{tabular}"
        latex_tables.append(table)

    # Assemblage final : on sépare les tableaux par un saut de page
    latex_code = "\n\\newpage\n".join(latex_tables)

    return latex_code 

def lit_csv_etudiants_placés_et_génère_table_tex(nomFicParametres  ,
                                                 latex_filename = 'table.tex',
                                                 nb_ligne_tableau=18 ,
                                                 tri = False ,
                                                 colonne = 0) :
    
    entete_et_data =  chargeFichierCsv(nomFicParametres)    
    data=entete_et_data[1:]
    latex_code= Remplit_table_Latex(data,nb_ligne_tableau)       
    ecrit_fichier_tex(latex_filename,latex_code)
    
def ecrit_table_tex(dataFichierEtudiantSansEntete  ,
                    latex_filename = 'table.tex',
                    nb_ligne_tableau=18 ,
                    colonne = 0) :    
    latex_code= Remplit_table_Latex(dataFichierEtudiantSansEntete,nb_ligne_tableau)       
    ecrit_fichier_tex(latex_filename,latex_code)

if __name__=='__main__' :
    print("Exécution à l'intérieur du module")
    #nomFicParametres="geo_test.csv"
    #Nb_zones, Nom_Amphi , Nb_Rang , Droite , Centre , Gauche, N_etudiants,alpha_num = charge(nomFicParametres)
    nomFicParametres="etu_PV_zone_G.csv"
   # latex_filename = 'table.tex'
    
    #entete_et_data =  chargeFichierCsv(nomFicParametres)
    #data=entete_et_data[1:]
    
    # Pour respecter une hauteur maximale de 24 cm par page,
    # on considère que chaque ligne (y compris l'en-tête) occupe 1 cm.
    # Ainsi, on autorise 1 en-tête + 23 lignes de données par tableau.
    chunk_size = 18    # nb de case du tableau (mettre le contenu d'un rang !!)
    
    #latex_code= Remplit_table_Latex(data,chunk_size)
       
    #ecrit_fichier_tex(latex_filename,latex_code)
 
    lit_csv_etudiants_placés_et_génère_table_tex(nomFicParametres  , latex_filename = 'table.tex', nb_ligne_tableau=18 ) 

    
  