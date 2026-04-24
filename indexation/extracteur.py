import os
from PyPDF2 import PdfReader
from docx import Document
from bs4 import BeautifulSoup


class Extracteur:
    """Extraction de texte depuis PDF, TXT, DOCX, HTML"""

    @staticmethod
    def extraire_pdf(chemin):
        texte = ""
        try:
            reader = PdfReader(chemin)
            for page in reader.pages:
                texte += page.extract_text() + " "
        except Exception as e:
            print(f"Erreur PDF {chemin}: {e}")
        return texte

    @staticmethod
    def extraire_txt(chemin):
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            try:
                with open(chemin, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                return ""

    @staticmethod
    def extraire_docx(chemin):
        texte = ""
        try:
            doc = Document(chemin)
            for para in doc.paragraphs:
                texte += para.text + " "
        except:
            pass
        return texte

    @staticmethod
    def extraire_html(chemin):
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text()
        except:
            return ""

    @staticmethod
    def extraire(chemin):
        ext = os.path.splitext(chemin)[1].lower()
        if ext == '.pdf':
            return Extracteur.extraire_pdf(chemin)
        elif ext == '.txt':
            return Extracteur.extraire_txt(chemin)
        elif ext == '.docx':
            return Extracteur.extraire_docx(chemin)
        elif ext == '.html':
            return Extracteur.extraire_html(chemin)
        return ""