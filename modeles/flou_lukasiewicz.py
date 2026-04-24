class FlouLukasiewicz:
    """Modèle flou - Lukasiewicz (produit pour ET, somme probabiliste pour OU)"""

    def rechercher(self, index, requete_mots):
        resultats = {}
        for doc in index.documents:
            poids = [index.get_poids(mot, doc) for mot in requete_mots]
            if not poids:
                continue

            # ET : produit
            score_et = 1
            for w in poids:
                score_et *= w

            # OU : somme probabiliste
            score_ou = 0
            for w in poids:
                score_ou = score_ou + w - (score_ou * w)

            score = (score_et + score_ou) / 2

            if score > 0:
                resultats[doc] = score
        return sorted(resultats.items(), key=lambda x: -x[1])