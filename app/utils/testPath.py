import os
import sys

# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__)
#
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)
    
# ajoute le répertoire de sortie des images. 
cheminRelatif="../../data/png_out"
app_dir = os.path.abspath(os.path.join(current_dir, cheminRelatif))

if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)
    
print(f"current_dir ='{current_dir}'")
input('taper entree')

print(f"app_dir ='{app_dir}'")
input('taper entree')

print(f"sys.path ='{sys.path}'")
input('taper entree')    
    

# Pour avoir les chemins relatifs corrects :
# Récupère le chemin absolu du répertoire contenant ce fichier (ma_classe.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Remonte vers la racine du projet (../../ depuis ce fichier)
        project_root = os.path.abspath(os.path.join(base_dir, '..', '..'))

        # Construit le chemin absolu vers png_out
        png_out_dir = os.path.join(project_root, 'png_out')

        # Assemble le chemin final du fichier PNG
        self.nomFicPng = os.path.join(png_out_dir, f"{reference_place}.png")
    