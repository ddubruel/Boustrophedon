import csv

def passe_nb_lignes(nbligne,reader) :
    for _ in range(nbligne):
        print(f"passe_nb_lignes : ligne non prise en compte : {next(reader)}")
    
def complete_tous_rangs(lignes,NbRang) :
    rangsComplets : list[list[int,int,int,str] ]= []
    index: int = 0
    max_index=len(lignes)-1
    for k in range(NbRang,0,-1):
        n_rang = lignes[index][0]
        if n_rang == k :
            rangsComplets.append(lignes[index]) # on garde le rang
            if index < max_index :
                index=index+1
        else :
            rangsComplets.append([k,0,0,'x']) # on crée un rang vide             
    return rangsComplets
        
def  configure_ligne(ligne :  list[str,str,str,str]) -> list[int,int,int,str] :
    try :
        L=[ int(ligne[0]) , int(ligne[1]) ,int(ligne[2]) ,ligne[3] ]
    except ValueError :
        raise ValueError("Attention au format des lignes, vérifier si il y a 3 entiers au début de chaque ligne.")
    return L

def range_rangs_dans_lordre(lignes: list[list[int, int, int, str]]) -> list[list[int, int, int, str]]:
    """Trie les lignes par ordre croissant selon le premier élément de chaque ligne."""
    n = len(lignes)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if lignes[j][0] == lignes[min_index][0]:
                raise ValueError(f"Attention 2 rangs ont le même numéro : {lignes[j][0]} !!")
                
            if lignes[j][0] > lignes[min_index][0]:
                min_index = j
            
        # Échange
        lignes[i], lignes[min_index] = lignes[min_index], lignes[i]
    return lignes

def lit_zone (nligne_zap, reader) -> list[list[int,int,int,str]] :
    lignes: list[list[int,int,int,str] ]= []
    passe_nb_lignes(nligne_zap,reader)
    # lecture de la zone  
    lecture=True
    while lecture :
        ligne=next(reader)
        if '#' not in ligne[0] :
            L=configure_ligne(ligne)
            lignes.append(L)
        else :
            lecture=False        
    L_triees=range_rangs_dans_lordre(lignes)
    

    return L_triees

def lit_2eme_zone (nligne_zap, Gauche , reader) -> list[list[int,int,int,str]] :
    passe_nb_lignes(nligne_zap,reader)
    Droite: list[  list[int,int,int,str] ]= []
    
    SYM_ou_data=next(reader)
    print(f"SYM_ou_data = {SYM_ou_data}")
    if SYM_ou_data[0]=='SYM' :  # alors on symétrise la zone Gauche
        for k in range(len(Gauche)):
            if Gauche[k][3]=='g' :
                Droite.append([ Gauche[k][0],Gauche[k][1],Gauche[k][2], 'd' ])
            elif Gauche[k][3]=='d' :
                Droite.append([ Gauche[k][0],Gauche[k][1],Gauche[k][2], 'g' ])
            else :
                Droite.append([ Gauche[k][0],Gauche[k][1],Gauche[k][2], Gauche[k][3]])                            
    else : 
        Droite_provi=lit_zone(0,reader)
        data=configure_ligne(SYM_ou_data) # ne pas oublier cette ligne
        Droite_provi.append(data)
        Droite=range_rangs_dans_lordre(Droite_provi)        
        return Droite
    
    return Droite




def lit_un_paramètre_numerique(nbzap, reader) -> int :
    passe_nb_lignes(nbzap,reader)
    ligne=next(reader)  #
    try :
        Valeur=int(ligne[0])
    except ValueError :
        raise ValueError("Vérifier que la valeur est bien un entier dans le fichier.")
    return Valeur

def lit_un_paramètre_chaine(nbzap, reader) -> str :
    passe_nb_lignes(nbzap,reader)
    return next(reader)[0]

def compte_le_nombre_d_etudiant(n,zone)  -> int :
    for k in range(len(zone)):
        n=n+zone[k][1]
    return n

def lit_zone_v2 (index : int , L : list[list[int,int,int,str]] ) -> list[list[int,int,int,str]] :
    lignes: list[list[int,int,int,str] ]= []    
    # lecture de la zone  
    DataZone=[]
    
    while '###' not in L[index][0]  :
        ligne=L[index]
        ligne=configure_ligne(ligne)      
        DataZone.append(ligne)
        index=index+1
    DataZone_triee = range_rangs_dans_lordre(DataZone)

    
     
    return index,DataZone_triee

def lit_2eme_zone_v2 (index, L,Gauche) -> list[list[int,int,int,str]] :
    
    Droite: list[  list[int,int,int,str] ]= []
    
    DataZone=[]
    
    if L[index][0]!='SYM'    :      
        index,DataZone = lit_zone_v2 (index, L)
        Droite = range_rangs_dans_lordre(DataZone)
        return index,Droite
    
    else : # on symétrise la zone Gauche
        for k in range(len(Gauche)):
            if Gauche[k][3]=='g' :
                DataZone.append([ Gauche[k][0],Gauche[k][1],Gauche[k][2], 'd' ])
            elif Gauche[k][3]=='d' :
                DataZone.append([ Gauche[k][0],Gauche[k][1],Gauche[k][2], 'g' ])
            else :
                DataZone.append([ Gauche[k][0],Gauche[k][1],Gauche[k][2], Gauche[k][3]])
        #en dehors du test !!!
        print('avant',DataZone)
        Droite = range_rangs_dans_lordre(DataZone)
        print('apres',Droite)
        
    return index,Droite

def charge_v2(nomFicParametres : str )-> [int,str,int,list,list,list,int,str]:
    
    """ cette fonction lit le csv et le convertit en liste
     l'idée est de chercher les lignes de séparation des champs de données
     ##########     """
    L : list[int,int,int,str] = []
    ligne : list[int,int,int,str] =[]
    fichier  = open(nomFicParametres, "r", encoding="utf-8")
    reader = csv.reader(fichier, delimiter=';')
    Data=list(reader)
    fichier.close() #fermeture.
    
    # on extrait  les lignes non vides
    Data_red=[]
    for k in range(len(Data)):    
        if Data[k]!=[] :
            Data_red.append(Data[k])
    Data=Data_red.copy()
    
    # chargement de Nb_zones
    index=0
    while Data[index][0] !='##data' :
        index=index+1
    index=index+1    
    try :
        Nb_zones=int(Data[index][0])
    except ValueError:
        raise ValueError("Attention Nb_zones n'est pas un entier dans le fichier !")
    
    # chargement de Nom_Amphi
    while Data[index][0] !='##data' :
        index=index+1
    index=index+1 
    Nom_Amphi=Data[index][0]
    
    # chargement de Nb_Rang
    while Data[index][0] !='##data' :
        index=index+1
    index=index+1 
    try :
        Nb_Rang=int(Data[index][0])
    except ValueError:
        raise ValueError("Attention Nb_Rang n'est pas un entier dans le fichier !")
    
    # chargement de Gauche
    while Data[index][0] !='##data' :
        index=index+1
    index=index+1    
    index,Gauche = lit_zone_v2 (index, Data)
    Gauche = complete_tous_rangs(Gauche,Nb_Rang)
    N_etudiants=compte_le_nombre_d_etudiant(0,Gauche)
    
    Droite=[]
    if Nb_zones>=2 :
        # chargement de Droite
        while Data[index][0] !='##data' :
            index=index+1
        index=index+1
        index,Droite = lit_2eme_zone_v2 (index, Data , Gauche)
        Droite = complete_tous_rangs(Droite,Nb_Rang)
        N_etudiants=compte_le_nombre_d_etudiant(N_etudiants,Droite)
    
    Centre=[]
    if Nb_zones>=3 :
        # chargement de Centre
        while Data[index][0] !='##data' :
            index=index+1
        index=index+1    
        index,Centre = lit_zone_v2 (index, Data)
        Centre = complete_tous_rangs(Centre,Nb_Rang)
        N_etudiants=compte_le_nombre_d_etudiant(N_etudiants,Centre)
    
    ## Il faut passer les zones Droite et Centre non lues jusqu'à trouver ##alpha_num!!!!
    while Data[index][0] !='##alpha_num' :
        index=index+1
    index=index+1
    print(Data[index][0])
    verif=Data[index]
#     if Data[index][0]=='SYM' or 'g' in  Data[index]  or 'd' in Data[index] :
#         while Data[index][0] !='##data' :
#             index=index+1
#         index=index+1
        
    # chargement de alpha_num
    alpha_num=Data[index][0]   
    return Nb_zones , Nom_Amphi , Nb_Rang , Gauche , Centre , Droite , N_etudiants , alpha_num
       
def charge(nomFicParametres : str )-> list[list[int,int,int,str]]:
     # Liste pour stocker les lignes
    L : list[int,int,int,str] = []
    ligne : list[int,int,int,str] =[]
    fichier  = open(nomFicParametres, "r", encoding="utf-8")
    reader = csv.reader(fichier, delimiter=';')
    # lecture du nombre de zones
    Nb_zones = lit_un_paramètre_numerique(2,reader)
    print(f"Nb_zones={Nb_zones}")
    # lecture du nom de l'amphithéatre.
    Nom_Amphi =  lit_un_paramètre_chaine(2,reader)
    print(f"Nom_Amphi = {Nom_Amphi}")
    # lecture du nombre de rang commun à toutes les zones:
    Nb_Rang = lit_un_paramètre_numerique(2,reader)
    print(f"Nb_Rang = {Nb_Rang}")
    
    if Nb_zones>=1 : # A faire dans tous les cas
        # lecture de la zone de gauche    
        Gauche = lit_zone (5, reader)
        print(f"Gauche = {Gauche}")
        Gauche = complete_tous_rangs(Gauche,Nb_Rang)
        N_etudiants=compte_le_nombre_d_etudiant(0,Gauche)
        Droite=[]
        Centre=[]
    
    if Nb_zones>=2 : # A faire si au moins 2 zones
        # lecture de la zone de droite ou construction du symétrique si SYM écrit dans fichier        
        Droite = lit_2eme_zone (4,Gauche , reader)
        print(f"Droite = {Droite}")
        Droite = complete_tous_rangs(Droite,Nb_Rang)
        N_etudiants=compte_le_nombre_d_etudiant(N_etudiants,Droite)
        Centre=[]
        
    if Nb_zones>=3 : # A faire pour la troisieme zone.
        Centre =  lit_zone (5, reader)
        print(f"Centre = {Centre}")
        Centre = complete_tous_rangs(Centre,Nb_Rang)
        N_etudiants=compte_le_nombre_d_etudiant(N_etudiants,Centre)
      
        
    fichier.close() #fermeture.
    # on ré ouvre le fichier pour aller chercher la dernière ligne
    # qui aurait pu être au début d'accord, mais c'est comme ça !
    fichier  = open(nomFicParametres, "r", encoding="utf-8")
    reader = csv.reader(fichier, delimiter=';')
    L_donnees = list(reader)           # convertir en liste
    alpha_num = L_donnees[-1][0]     # accéder à la dernière ligne
    fichier.close() #fermeture
    return Nb_zones, Nom_Amphi , Nb_Rang , Gauche , Centre , Droite , N_etudiants,alpha_num
           
    


if __name__=='__main__' :
    print("Exécution à l'intérieur du module")
    #nomFicParametres="geo_test.csv"
    #Nb_zones, Nom_Amphi , Nb_Rang , Droite , Centre , Gauche, N_etudiants,alpha_num = charge(nomFicParametres)
    nomFicParametres="geo_test_v2.csv"
    Nb_zones,Nom_Amphi,Nb_Rang,Gauche,Centre,Droite,N_etudiants,alpha_num =charge_v2(nomFicParametres)
    
    
    