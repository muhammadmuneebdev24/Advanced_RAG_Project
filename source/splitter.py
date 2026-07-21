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


def text_splitter(documents):
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    return chunks