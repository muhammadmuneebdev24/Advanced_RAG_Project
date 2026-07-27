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


def get_chunk_title(text: str):
    """
    Returns the best title for a chunk.

    Priority:
    1. Numbered headings
    2. Strong standalone headings
    3. Short title-like lines
    4. First meaningful line as fallback
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return "Untitled"

    candidates = []

    for index, line in enumerate(lines):

        # Remove heading numbering
        clean_title = re.sub(
            r"^\d+(\.\d+)*\.?\s+",
            "",
            line
        ).strip()

        # Ignore very long lines
        if len(clean_title) > 80:
            continue

        words = clean_title.split()

        # Ignore empty lines
        if not words:
            continue

        score = 0


        if re.match(r"^\d+(\.\d+)*\.?\s+", line):
            score += 5


        if clean_title.istitle():
            score += 4

        if clean_title.isupper() and any(
            char.isalpha() for char in clean_title
        ):
            score += 4

        if len(words) <= 10:
            score += 2

        if len(clean_title) <= 60:
            score += 1

        if not clean_title.endswith((".", "?", "!", ":")):
            score += 2


        if len(words) > 15:
            score -= 5


        if clean_title.startswith(("-", "*", "•")):
            score -= 5


        if "," in clean_title and len(words) > 5:
            score -= 2

        # Save candidate
        candidates.append(
            (score, index, clean_title)
        )
    if candidates:

        candidates.sort(
            key=lambda x: (-x[0], x[1])
        )

        best_score, best_index, best_title = candidates[0]

        if best_score >= 4:
            return best_title

    first = re.sub(
        r"^\d+(\.\d+)*\.?\s+",
        "",
        lines[0]
    ).strip()

    if len(first) > 70:
        return first[:70] + "..."

    return first

def text_splitter(documents):

    for doc in documents:
        doc.page_content = clean_text(
            doc.page_content
        )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    for chunk in chunks:

        chunk.metadata["chunk_title"] = (
            get_chunk_title(chunk.page_content)
        )

    return chunks