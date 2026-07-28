import fitz

def load_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    return doc