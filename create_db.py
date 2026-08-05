import os
from source.loader import load_pdf
from source.splitter import text_splitter
from source.embeddings import get_embeddings
from source.vector_database import create_vector_db
from source.attach_heading import attach_headings
from source.heading_detector import detect_headings
from Hashing import calculate_file_hash
from database.query import hash_exist,insert_pdf,update_status


PDF_FOLDER = "data"


def main():

    all_chunks = []
    processed_files = []


    for filename in os.listdir(PDF_FOLDER):

        # Skip non-PDF files
        if not filename.lower().endswith(".pdf"):
             continue

        pdf_path = os.path.join(PDF_FOLDER, filename)

#Now we are calculating hashing 
        file_hash = calculate_file_hash(pdf_path)

#If hash exist 
        if hash_exist(file_hash):
          print(f"{filename} already processed. Skipping...")
          continue

#If hash doesnot exist inserting pdf 
        insert_pdf(filename, file_hash)

        try:

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
          processed_files.append(file_hash)


        except Exception as e:
          print(f"Error processing {filename}: {e}")
          update_status(file_hash, "FAILED")
          continue

    if not all_chunks:
      print("No new PDFs found. Vector database is already up to date.")
      return
    
    try:       

      print(f"\nTotal Chunks: {len(all_chunks)}")

      print("Loading embeddings...")
      embeddings = get_embeddings()

      print("Creating FAISS database...")
      create_vector_db(
        all_chunks,
        embeddings
      )
      for file_hash in processed_files:
         update_status(file_hash, "COMPLETED")

      print("Database created successfully!")
    except Exception as e :

        print(f"Error creating FAISS: {e}")

        for file_hash in processed_files:
           update_status(file_hash, "FAILED")

        print("Failed to create vector database")

if __name__ == "__main__":
    main()