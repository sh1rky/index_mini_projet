class BooleanClassique:
    """Modèle booléen classique (ensembles)"""

    def rechercher(self, index, requete_mots):
        resultats = {}
        for doc in index.documents:
            # ET : tous les mots doivent être présents
            tous_presents = all(index.get_poids(mot, doc) > 0 for mot in requete_mots)
            if tous_presents:
                # Score = moyenne des poids
                poids = [index.get_poids(mot, doc) for mot in requete_mots]
                resultats[doc] = sum(poids) / len(poids) if poids else 0
        return sorted(resultats.items(), key=lambda x: -x[1])