import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Télécharger les données nltk une seule fois
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')


class Preprocesseur:
    """Prétraitement du texte : minuscules, stopwords, stemming"""

    def __init__(self):
        self.stopwords_fr = set(stopwords.words('french'))
        self.stopwords_en = set(stopwords.words('english'))
        self.stopwords_fr.update(["les", "des", "ces", "ses", "aux", "dans", "par", "sur", "avec"])
        self.stemmer = PorterStemmer()

    def nettoyer(self, texte):
        """Mise en minuscules et suppression des caractères spéciaux"""
        texte = texte.lower()
        texte = re.sub(r'[^a-zàâéèêëîïôûüç\s]', '', texte)
        return texte

    def supprimer_stopwords(self, mots):
        """Supprime les mots vides français et anglais"""
        return [m for m in mots if m not in self.stopwords_fr and m not in self.stopwords_en and len(m) > 2]

    def appliquer_stemming(self, mots):  # <--- CHANGEMENT ICI
        """Applique le stemming sur les mots"""
        return [self.stemmer.stem(m) for m in mots]  # <--- .stem() mta3 stemmer

    def traiter(self, texte):
        """Pipeline complet de prétraitement"""
        texte = self.nettoyer(texte)
        mots = texte.split()
        mots = self.supprimer_stopwords(mots)
        mots = self.appliquer_stemming(mots)  # <--- CHANGEMENT ICI
        return mots