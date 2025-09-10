dico={'amphi': 'Petit_Valrose',
 'zones': ['Gauche', 'Centre', 'Droite'],
 'nb_places': [6, 7, 6],
 'Nb_rang': 17,
 'grilles': {'Gauche': [[16, 2]], 'Centre': [[16, 1]], 'Droite': [[16, 1]]}
 }


print (dico['grilles'])
# renvoie    {'Gauche': [[16, 2]], 'Centre': [[16, 1]], 'Droite': [[16, 1]]}
print(dico['grilles'].keys() )
# renvoie dict_keys(['Gauche', 'Centre', 'Droite'])

print( [ dico['grilles'][cle] for cle in dico['grilles'].keys() ] )