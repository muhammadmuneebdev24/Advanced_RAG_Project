import fitz
from collections import defaultdict


def get_chunk_y(pdf_path, chunk_text, page_num):


    pdf_document = fitz.open(pdf_path)

    page = pdf_document[page_num]

    words = chunk_text.split()

    if not words:
        pdf_document.close()
        return None

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
    
        previous_headings = [
            heading
            for heading in page_headings
            if chunk_y is not None
            and heading["y"] <= chunk_y
        ]

        if previous_headings:

            current_heading = previous_headings[-1]["text"]


        chunk.metadata["heading"] = current_heading

    return chunks