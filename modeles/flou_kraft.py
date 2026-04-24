class FlouKraft:
    """Modèle flou - Kraft (min pour ET, max pour OU)"""

    def rechercher(self, index, requete_mots):
        resultats = {}
        for doc in index.documents:
            poids = [index.get_poids(mot, doc) for mot in requete_mots]
            if not poids:
                continue

            score_et = min(poids)
            score_ou = max(poids)
            score = (score_et + score_ou) / 2

            if score > 0:
                resultats[doc] = score
        return sorted(resultats.items(), key=lambda x: -x[1])