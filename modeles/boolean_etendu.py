import math


class BooleanEtendu:
    """Modèle booléen étendu (p-norme p=2)"""

    def __init__(self, p=2):
        self.p = p

    def rechercher(self, index, requete_mots):
        resultats = {}
        for doc in index.documents:
            poids = [index.get_poids(mot, doc) for mot in requete_mots]
            if not poids:
                continue

            # Score OR
            score_or = (sum(w ** self.p for w in poids) / len(poids)) ** (1 / self.p)
            # Score AND
            score_and = 1 - (sum((1 - w) ** self.p for w in poids) / len(poids)) ** (1 / self.p)
            # Moyenne
            score = (score_or + score_and) / 2

            if score > 0:
                resultats[doc] = score
        return sorted(resultats.items(), key=lambda x: -x[1])