import re
import unicodedata
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:

    # Normalize unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Replace repeated dots
    text = re.sub(r"\.{2,}", ".", text)

    return text.strip()




def text_splitter(documents):

    for doc in documents:
        doc.page_content = clean_text(
            doc.page_content
        )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]

    )

    chunks = splitter.split_documents(documents)

   
    return chunks