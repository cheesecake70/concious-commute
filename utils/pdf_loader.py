import os
import pypdf
import unicodedata

class PDFLoader:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Normalizes unicode characters, replaces common PDF ligatures/bullet glyphs,
        and removes non-printable control characters.
        """
        # Normalize characters (e.g. decompose ligatures)
        text = unicodedata.normalize("NFKC", text)
        
        # Replace common PDF bullet points and ligatures
        replacements = {
            "\uf0b7": "* ",  # Bullet points
            "\u2022": "* ",  # Bullet points
            "\u201c": '"',   # Smart double quotes
            "\u201d": '"',
            "\u2018": "'",   # Smart single quotes
            "\u2019": "'",
            "\u2013": "-",   # En dash
            "\u2014": "-",   # Em dash
            "\uf02d": "-",
            "\uf0fc": "✓",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        # Strip out any control characters (like backspace, null, etc.) except tabs and newlines
        cleaned = []
        for char in text:
            category = unicodedata.category(char)
            if category[0] != "C" or char in ("\n", "\t"):
                cleaned.append(char)
                
        return "".join(cleaned).strip()

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extracts and cleans all readable text from a PDF file.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
            
        try:
            reader = pypdf.PdfReader(pdf_path)
            text_parts = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            raw_text = "\n".join(text_parts)
            return PDFLoader.clean_text(raw_text)
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF at {pdf_path}: {str(e)}")
