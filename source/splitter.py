import re
import unicodedata
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str):
    """
    Clean extracted PDF text before chunking.
    """

    text = unicodedata.normalize("NFKC", text)

    text = text.replace("\t", " ")

    text = re.sub(r"[ ]{2,}", " ", text)

    text = re.sub(r"\n\s*\n+", "\n\n", text)

    text = re.sub(r"\.{2,}", ".", text)

    return text.strip()


def text_splitter(sections):
    """
    Split section Documents into chunks while
    preserving metadata.
    """

    for section in sections:
        section.page_content = clean_text(section.page_content)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(sections)

    return chunks