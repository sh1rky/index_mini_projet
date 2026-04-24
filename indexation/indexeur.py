import math
import os
from collections import Counter
from .extracteur import Extracteur
from .preprocesseur import Preprocesseur


class Indexeur:
    """Construction de l'index et calcul TF-IDF"""

    def __init__(self):
        self.documents = {}  # nom_fichier -> liste mots preprocesses
        self.tf = {}  # doc -> {terme: tf}
        self.idf = {}  # terme -> idf
        self.tfidf = {}  # doc -> {terme: tfidf}
        self.chemins = {}  # nom_fichier -> chemin complet
        self.extracteur = Extracteur()
        self.preprocesseur = Preprocesseur()

    def indexer_dossier(self, dossier_base="./collections"):
        """Indexe tous les documents dans les sous-dossiers"""
        print("Indexation des documents...")

        types = ['pdf', 'txt', 'docx', 'html']
        docs_mots = {}

        for t in types:
            dossier = os.path.join(dossier_base, t)
            if not os.path.exists(dossier):
                os.makedirs(dossier, exist_ok=True)
                continue

            for fichier in os.listdir(dossier):
                chemin = os.path.join(dossier, fichier)
                nom_unique = f"{t}_{fichier}"

                texte = self.extracteur.extraire(chemin)
                if texte:
                    mots = self.preprocesseur.traiter(texte)
                    if mots:
                        self.documents[nom_unique] = mots
                        self.chemins[nom_unique] = chemin
                        docs_mots[nom_unique] = mots
                        self.tf[nom_unique] = self._calculer_tf(mots)

        # Calculer IDF
        self.idf = self._calculer_idf(docs_mots)

        # Calculer TF-IDF
        for doc in self.documents:
            self.tfidf[doc] = self._calculer_tfidf(self.tf[doc], self.idf)

        print(f"Indexé: {len(self.documents)} documents, {len(self.idf)} termes")
        return len(self.documents)

    def _calculer_tf(self, mots):
        total = len(mots)
        if total == 0:
            return {}
        compteur = Counter(mots)
        return {t: compteur[t] / total for t in compteur}

    def _calculer_idf(self, docs_mots):
        idf = {}
        N = len(docs_mots)
        if N == 0:
            return idf

        tous_termes = set()
        for mots in docs_mots.values():
            tous_termes.update(mots)

        for terme in tous_termes:
            df = sum(1 for mots in docs_mots.values() if terme in mots)
            idf[terme] = math.log(N / df) if df > 0 else 0
        return idf

    def _calculer_tfidf(self, tf, idf):
        return {t: tf[t] * idf.get(t, 0) for t in tf}

    def get_poids(self, terme, doc):
        return self.tfidf.get(doc, {}).get(terme, 0)

    def get_extrait(self, doc, requete_mots, longueur=150):
        """Retourne un extrait du document contenant les mots de la requête"""
        chemin = self.chemins.get(doc, "")
        if not chemin:
            return "Extrait non disponible"

        texte = self.extracteur.extraire(chemin)
        if not texte:
            return "Extrait non disponible"

        # Chercher la position du premier mot de la requête
        texte_lower = texte.lower()
        mots_req = requete_mots.lower().split()

        for mot in mots_req:
            pos = texte_lower.find(mot)
            if pos != -1:
                debut = max(0, pos - 50)
                fin = min(len(texte), pos + 100)
                extrait = texte[debut:fin]
                if debut > 0:
                    extrait = "..." + extrait
                if fin < len(texte):
                    extrait = extrait + "..."
                return extrait

        return texte[:longueur] + "..."