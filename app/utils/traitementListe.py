def majuscule( listeEtudiant : list[list[str]] ) -> list[list[str]]:
    resultat =[]
    for k in range(len(listeEtudiant)) :
        ligne=listeEtudiant[k]
        for l in range(2) :
            nom =  ligne[l]
            ligne[l]=nom.upper()
    return listeEtudiant
        