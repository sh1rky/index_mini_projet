import os
import nltk
from indexation import Indexeur
from modeles import *

# Télécharger les données nltk
nltk.download('stopwords')
nltk.download('punkt')


def main():
    print("=" * 60)
    print("TP5 - Système Complet de Recherche d'Information")
    print("=" * 60)

    # Créer les dossiers si nécessaires
    for dossier in ["./collections/pdf", "./collections/txt", "./collections/docx", "./collections/html"]:
        os.makedirs(dossier, exist_ok=True)

    print("\n📁 Dossiers créés:")
    print("   - collections/pdf/    (mettez vos PDF ici)")
    print("   - collections/txt/    (mettez vos TXT ici)")
    print("   - collections/docx/   (mettez vos DOCX ici)")
    print("   - collections/html/   (mettez vos HTML ici)")

    # Indexation
    print("\n📚 Indexation des documents...")
    indexeur = Indexeur()
    nb_docs = indexeur.indexer_dossier("./collections")

    if nb_docs == 0:
        print("\n⚠️  Aucun document trouvé!")
        print("   Veuillez ajouter des fichiers dans les dossiers collections/...")
        return

    # Initialiser les moteurs
    moteurs = {
        "boolean_classique": BooleanClassique(),
        "boolean_etendu": BooleanEtendu(),
        "flou_lukasiewicz": FlouLukasiewicz(),
        "flou_kraft": FlouKraft(),
        "vectoriel": Vectoriel()
    }

    # Lancer l'interface
    print("\n🚀 Lancement de l'interface graphique...")
    from interface import Interface
    app = Interface(indexeur, moteurs)
    app.lancer()


if __name__ == "__main__":
    main()