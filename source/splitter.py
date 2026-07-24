import re
import unicodedata
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:

    # Normalize unicode characters
    text = unicodedata.normalize("NFKC", text)

    
    text = text.replace("\t", " ")

    text = re.sub(r"[ ]{2,}", " ", text)

    text = re.sub(r"\n\s*\n+", "\n\n", text)

    text = re.sub(r"\.{2,}", ".", text)

    return text.strip()


def get_chunk_title(text: str):
    """
    Returns the best title for a chunk.

    Priority:
    1. Short standalone headings
    2. First meaningful line
    """

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        return "Untitled"

    for line in lines:

        if (
            len(line) <= 80
            and len(line.split()) <= 10
            and not line.endswith(".")
            and not line.startswith("-")
        ):
           clean_title = re.sub(r"^\d+(\.\d+)*\.?\s+", "", line)
           return clean_title
      
    
    first = re.sub(r"^\d+(\.\d+)*\.?\s+", "", lines[0])
    if len(first) > 70:
        return first[:70] + "..."

    return first

def text_splitter(documents):
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
      chunk.metadata["chunk_title"] = get_chunk_title(chunk.page_content)


    return chunks