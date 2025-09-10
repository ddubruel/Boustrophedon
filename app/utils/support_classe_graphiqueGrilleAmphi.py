def extraction_liste_cases_cochees ( grillesDeZone ,  nomAmphi  ) :
    """ fonction pour renvoyer la grille des cases cochées
    fonction support de la classe graphiqueGrilleAmphi ,
    revoie pour chaque zone une liste [[ (numéro_ligne , numéro_colonne ) etc... ]]
    uniquement les coordonnées des cases cochées, ce qui correspond
    aux places occuppées dans l'amphi. """
    
    listeCasesCocheesPourToutesLesZones=[]
    print( f"nomAmphi (dans extraction_liste etc )  = {nomAmphi}")
   
    for grille in grillesDeZone:
        # Traitement des zones Gauche et Centre pour tous les amphis :            
        listePourUneZone=[]
        if grille.titre=='Gauche' or grille.titre=='Centre' :
            for row, ligne in enumerate(grille.vars):
                for col, var in enumerate(ligne):
                    if var.get() == 1:
                        listePourUneZone.append((row, col))
        # Traitement de la zone Droite du 'Petit_Valrose' :                
        elif grille.titre=='Droite' and  'Petit_Valrose' in nomAmphi :
            for row, ligne in enumerate(grille.vars):
                if row<= 14 :
                    for col, var in enumerate(ligne):
                        if var.get() == 1:
                            listePourUneZone.append((row, col))            
                elif row > 14  :  # on décale un peu la numérotation
                    for col, var in enumerate(ligne  ):
                        if var.get() == 1:
                            listePourUneZone.append( (row ,col  + grille.nb_cases - grille.nb_cases//2 ))
        else :
            for row, ligne in enumerate(grille.vars):
                for col, var in enumerate(ligne):
                    if var.get() == 1:
                        listePourUneZone.append((row, col))
            
        listeCasesCocheesPourToutesLesZones.append(listePourUneZone)    
    return listeCasesCocheesPourToutesLesZones

def convertitCaseCocheeEnDico(caseCochees : list[list[list[int] ]] ,
                              zones : list[str] ):
#    print(f" \n Dans convertitCaseCocheeEnDico : \n liste des cases {caseCochees}" )
#    print(f" liste des zones {zones}" )
    dico ={}
    for index , zone in enumerate(zones):
        dico[zone]=caseCochees[index]
#    print(f"Resultat {dico} ")
    return dico

if __name__=='__main__' :
    listeCases  = [ [  [1,0],[9,9] ],[ [10,10],[4,4] ] ]
    listeZones=['Gauche','Droite']
    print(convertitCaseCocheeEnDico(listeCases,listeZones) )
          
