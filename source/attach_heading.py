import fitz
from collections import defaultdict


def get_chunk_y(pdf_path, chunk_text, page_num):
    """
    Find approximately where the chunk starts on the PDF page.

    Uses PyMuPDF to search for the first meaningful text
    from the chunk.
    """

    pdf_document = fitz.open(pdf_path)

    page = pdf_document[page_num]

    # Take the first few meaningful words from the chunk
    words = chunk_text.split()

    if not words:
        pdf_document.close()
        return None

    # Try several starting lengths because PDF text
    # may not match the chunk exactly.
    search_lengths = [12, 8, 5, 3]

    for length in search_lengths:

        search_text = " ".join(words[:length]).strip()

        if not search_text:
            continue

        rects = page.search_for(search_text)

        if rects:
            y = rects[0].y0

            pdf_document.close()

            return y

    pdf_document.close()

    return None


def attach_headings(chunks, headings, pdf_path):
    """
    Attach the closest previous heading to every chunk.

    Rules:

    1. If a heading exists above the chunk on the same page,
       use the closest heading.

    2. If there is no heading above the chunk on that page,
       use the last heading from a previous page.

    3. If there is no previous heading anywhere,
       use 'Untitled'.

    Parameters
    ----------
    chunks : List[Document]
        Chunks created by your PDF reader/splitter.

    headings : List[dict]
        Headings detected using PyMuPDF.

    pdf_path : str
        Path to the original PDF.

    Returns
    -------
    List[Document]
    """

    # ----------------------------------------
    # Group headings by page
    # ----------------------------------------

    headings_by_page = defaultdict(list)

    for heading in headings:

        headings_by_page[heading["page"]].append(heading)

    # Sort headings from top → bottom
    for page in headings_by_page:

        headings_by_page[page].sort(
            key=lambda h: h["y"]
        )

    # Last heading encountered in the document
    current_heading = "Untitled"

    # ----------------------------------------
    # Process chunks
    # ----------------------------------------

    for chunk in chunks:

        page = chunk.metadata["page"]

        chunk_text = chunk.page_content

        # Find where this chunk starts on the page
        chunk_y = get_chunk_y(
            pdf_path,
            chunk_text,
            page
        )

        # Save position for debugging
        chunk.metadata["chunk_y"] = chunk_y

        page_headings = headings_by_page.get(page, [])
        # ----------------------------------------


        # ----------------------------------------
        # Find headings above this chunk
        # ----------------------------------------

        previous_headings = [
            heading
            for heading in page_headings
            if chunk_y is not None
            and heading["y"] <= chunk_y
        ]

        # ----------------------------------------
        # Use closest previous heading
        # ----------------------------------------

        if previous_headings:

            current_heading = previous_headings[-1]["text"]

        # ----------------------------------------
        # Attach heading
        # ----------------------------------------

        chunk.metadata["heading"] = current_heading

    return chunks