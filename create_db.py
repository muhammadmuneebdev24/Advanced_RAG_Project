from source.loader import load_pdf
from source.splitter import text_splitter
from source.embeddings import get_embeddings
from source.section_parser import build_sections
from source.vector_database import create_vector_db


PDF_PATH = "data/a.pdf"


def main():

    print("Loading PDF...")
    pdf= load_pdf(PDF_PATH)

    print("Building sections...")
    sections = build_sections(pdf)

    print("Splitting text...")
    chunks = text_splitter(sections)

    print("Loading embeddings...")
    embeddings = get_embeddings()

    print("Creating FAISS database...")
    create_vector_db(
        chunks,
        embeddings
    )

    print("Database created successfully!")


if __name__ == "__main__":
    main()