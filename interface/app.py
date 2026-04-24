import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import subprocess


class Interface:
    """Interface graphique complète"""

    def __init__(self, indexeur, moteurs):
        self.indexeur = indexeur
        self.moteurs = moteurs
        self.modele_courant = "boolean_etendu"

        self.fenetre = tk.Tk()
        self.fenetre.title("TP5 - Système de Recherche d'Information")
        self.fenetre.geometry("1000x750")
        self.fenetre.configure(bg='#f0f0f0')

        self._creer_widgets()

    def _creer_widgets(self):
        # Titre
        tk.Label(self.fenetre, text="TP5 - Système Complet de Recherche d'Information",
                 font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#2c3e50').pack(pady=10)

        # Cadre modèle
        cadre_modele = tk.Frame(self.fenetre, bg='#f0f0f0')
        cadre_modele.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(cadre_modele, text="Modèle :", font=("Arial", 12), bg='#f0f0f0').pack(side=tk.LEFT)

        self.combo = ttk.Combobox(cadre_modele, values=list(self.moteurs.keys()),
                                  state="readonly", width=20, font=("Arial", 11))
        self.combo.pack(side=tk.LEFT, padx=10)
        self.combo.set("boolean_etendu")
        self.combo.bind('<<ComboboxSelected>>', self._changer_modele)

        # Description
        self.lbl_desc = tk.Label(cadre_modele, text="", font=("Arial", 10), fg="#555", bg='#f0f0f0')
        self.lbl_desc.pack(side=tk.LEFT, padx=20)
        self._mettre_jour_description()

        # Cadre requête
        cadre_req = tk.Frame(self.fenetre, bg='#f0f0f0')
        cadre_req.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(cadre_req, text="Requête :", font=("Arial", 12), bg='#f0f0f0').pack(anchor=tk.W)

        self.entry = tk.Entry(cadre_req, font=("Arial", 12), bg='white', relief=tk.SUNKEN, bd=2)
        self.entry.pack(fill=tk.X, pady=5)
        self.entry.bind("<Return>", lambda e: self.chercher())

        # Boutons opérateurs
        cadre_btn = tk.Frame(cadre_req, bg='#f0f0f0')
        cadre_btn.pack(fill=tk.X, pady=5)

        for texte in [" ET ", " OU ", " NON ", "Effacer"]:
            if texte == "Effacer":
                btn = tk.Button(cadre_btn, text=texte, command=self._effacer, bg='#e74c3c', fg='white')
            else:
                btn = tk.Button(cadre_btn, text=texte, command=lambda t=texte: self._ajouter_texte(t), bg='#3498db',
                                fg='white')
            btn.pack(side=tk.LEFT, padx=2)

        # Bouton chercher
        tk.Button(cadre_req, text="🔍 CHERCHER", command=self.chercher,
                  bg='#2ecc71', fg='white', font=("Arial", 12, "bold")).pack(pady=10)

        # Exemple
        tk.Label(cadre_req, text="Exemple: intelligence artificielle | data mining | machine learning",
                 font=("Arial", 9), fg='#888', bg='#f0f0f0').pack(anchor=tk.W)

        # Résultats
        tk.Label(self.fenetre, text="Résultats :", font=("Arial", 12), bg='#f0f0f0').pack(anchor=tk.W, padx=20)

        self.txt_resultats = scrolledtext.ScrolledText(self.fenetre, wrap=tk.WORD,
                                                       font=("Courier", 10), height=25)
        self.txt_resultats.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Lien cliquable
        self.txt_resultats.tag_config("lien", foreground="blue", underline=True)
        self.txt_resultats.tag_bind("lien", "<Button-1>", self._ouvrir_document)

        # Barre d'état
        self.status = tk.Label(self.fenetre, text=f"Prêt - {len(self.indexeur.documents)} documents indexés",
                               relief=tk.SUNKEN, anchor=tk.W, bg='#ddd')
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def _ajouter_texte(self, texte):
        self.entry.insert(tk.INSERT, texte)

    def _effacer(self):
        self.entry.delete(0, tk.END)
        self.txt_resultats.delete(1.0, tk.END)

    def _changer_modele(self, event):
        self.modele_courant = self.combo.get()
        self._mettre_jour_description()
        self.status.config(text=f"Modèle changé: {self.modele_courant}")

    def _mettre_jour_description(self):
        descriptions = {
            "boolean_classique": "Booléen classique (ET, OU, NON) - recherche ensembliste",
            "boolean_etendu": "Booléen étendu (p-norme p=2) - scores flous",
            "flou_lukasiewicz": "Flou Lukasiewicz - produit pour ET, somme probabiliste pour OU",
            "flou_kraft": "Flou Kraft - min pour ET, max pour OU",
            "vectoriel": "Modèle vectoriel - similarité cosinus"
        }
        self.lbl_desc.config(text=descriptions.get(self.modele_courant, ""))

    def chercher(self):
        requete = self.entry.get().strip()
        if not requete:
            messagebox.showwarning("Attention", "Entrez une requête")
            return

        self.txt_resultats.delete(1.0, tk.END)

        mots = requete.lower().split()
        moteur = self.moteurs[self.modele_courant]
        resultats = moteur.rechercher(self.indexeur, mots)

        self.txt_resultats.insert(tk.END, f"Requête: {requete}\n")
        self.txt_resultats.insert(tk.END, f"Modèle: {self.modele_courant}\n")
        self.txt_resultats.insert(tk.END, "=" * 60 + "\n\n")

        if resultats:
            self.txt_resultats.insert(tk.END, f"{len(resultats)} document(s) trouvé(s)\n\n")
            for i, (doc, score) in enumerate(resultats[:30], 1):
                # Lien cliquable
                self.txt_resultats.insert(tk.END, f"{i:2d}. ", "lien")
                self.txt_resultats.insert(tk.END, f"{doc}\n", "lien", (doc,))
                self.txt_resultats.insert(tk.END,
                                          f"     Score: {score:.4f}  [{'█' * int(score * 30)}{'░' * (30 - int(score * 30))}] {score * 100:.1f}%\n")

                # Extrait
                extrait = self.indexeur.get_extrait(doc, requete)
                self.txt_resultats.insert(tk.END, f"     Extrait: {extrait}\n")
                self.txt_resultats.insert(tk.END, "-" * 40 + "\n")

            self.status.config(text=f"{len(resultats)} résultat(s) | Modèle: {self.modele_courant}")
        else:
            self.txt_resultats.insert(tk.END, "Aucun résultat trouvé.\n")
            self.status.config(text="Aucun résultat")

    def _ouvrir_document(self, event):
        """Ouvre le document avec l'application par défaut"""
        try:
            idx = self.txt_resultats.index("@%d,%d" % (event.x, event.y))
            tags = self.txt_resultats.tag_names(idx)
            for tag in tags:
                if isinstance(tag, tuple) and len(tag) == 1:
                    doc = tag[0]
                    chemin = self.indexeur.chemins.get(doc, "")
                    if chemin and os.path.exists(chemin):
                        subprocess.run(['start', chemin], shell=True)
                    break
        except:
            pass

    def lancer(self):
        self.fenetre.mainloop()