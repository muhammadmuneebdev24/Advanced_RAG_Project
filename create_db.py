from source.loader import load_pdf
from source.splitter import text_splitter
from source.embeddings import get_embeddings
from source.vector_database import create_vector_db


PDF_PATH = "data/ragPDF.pdf"


def main():

    print("Loading PDF...")
    documents = load_pdf(PDF_PATH)

    print("Splitting text...")
    chunks = text_splitter(documents)

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