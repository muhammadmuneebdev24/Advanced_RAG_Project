from source.loader import load_pdf
from source.splitter import text_splitter
from source.embeddings import get_embeddings
from source.vector_database import create_vector_db
from source.attach_heading import attach_headings
from source.heading_detector import detect_headings


PDF_PATH = "data/a.pdf"


def main():

    print("Loading PDF...")
    documents = load_pdf(PDF_PATH)

    print("Detect Heading")
    headings = detect_headings(PDF_PATH)
    print("\nDetected headings:")
    for h in headings:
      print(h)

    print("Splitting text...")
    chunks = text_splitter(documents)


    print("Attach heading ")
    chunks = attach_headings(chunks,headings,PDF_PATH)

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