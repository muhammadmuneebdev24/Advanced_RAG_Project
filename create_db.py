import os

from source.loader import load_pdf
from source.splitter import text_splitter
from source.embeddings import get_embeddings
from source.vector_database import create_vector_db
from source.attach_heading import attach_headings
from source.heading_detector import detect_headings


PDF_FOLDER = "data"


def main():

    all_chunks = []

    for filename in os.listdir(PDF_FOLDER):

        # Skip non-PDF files
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(PDF_FOLDER, filename)

        print(f"\n{'=' * 60}")
        print(f"Processing: {filename}")
        print(f"{'=' * 60}")

        print("Loading PDF...")
        documents = load_pdf(pdf_path)

        print("Detect Heading...")
        headings = detect_headings(pdf_path)

        print("\nDetected headings:")
        for h in headings:
            print(h)

        print("Splitting text...")
        chunks = text_splitter(documents)

        print("Attach heading...")
        chunks = attach_headings(
            chunks,
            headings,
            pdf_path
        )

        # Collect chunks from this PDF
        all_chunks.extend(chunks)

    print(f"\nTotal Chunks: {len(all_chunks)}")

    print("Loading embeddings...")
    embeddings = get_embeddings()

    print("Creating FAISS database...")
    create_vector_db(
        all_chunks,
        embeddings
    )

    print("Database created successfully!")


if __name__ == "__main__":
    main()