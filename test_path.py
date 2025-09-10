import os
import sys


    
# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
# directement comme "from classe.fichieradhoc import tintin" 
current_dir =   os.path.dirname(__file__)
print(f"1) current_dir = '{current_dir}' \n")
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
print(f" current_dir = {app_dir} \n")
print(f" current_dir = {sys.path} \n ")
if app_dir not in sys.path :    
    sys.path.insert(0, app_dir)
    print(f" sys.path = {sys.path} \n")
    