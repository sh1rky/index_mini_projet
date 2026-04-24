import math


class Vectoriel:
    """Modèle vectoriel avec similarité cosinus"""

    def rechercher(self, index, requete_mots):
        # Construire le vecteur de la requête
        vecteur_requete = {}
        for mot in requete_mots:
            vecteur_requete[mot] = vecteur_requete.get(mot, 0) + 1

        # Normaliser le vecteur requête
        norme_req = math.sqrt(sum(v ** 2 for v in vecteur_requete.values()))

        resultats = {}
        for doc in index.documents:
            produit = 0
            norme_doc = 0

            for mot in requete_mots:
                poids_doc = index.get_poids(mot, doc)
                poids_req = vecteur_requete.get(mot, 0) / norme_req if norme_req > 0 else 0
                produit += poids_doc * poids_req
                norme_doc += poids_doc ** 2

            norme_doc = math.sqrt(norme_doc)
            if norme_doc > 0 and norme_req > 0:
                score = produit / (norme_doc * norme_req)
                if score > 0:
                    resultats[doc] = score

        return sorted(resultats.items(), key=lambda x: -x[1])