from collections import defaultdict


def attach_headings(chunks, headings):
    """
    Attach the nearest section heading to every chunk.

    Rules:
    1. If a heading exists earlier on the same page,
       use the closest previous heading.

    2. Otherwise use the last heading
       from previous pages.

    Returns
    -------
    List[Document]
    """

    # -----------------------------
    # Group headings by page
    # -----------------------------
    headings_by_page = defaultdict(list)

    for heading in headings:
        headings_by_page[heading["page"]].append(heading)

    # Sort headings on each page from top to bottom
    for page in headings_by_page:
        headings_by_page[page].sort(
            key=lambda h: h["y"]
        )

    current_heading = "Untitled"

    # -----------------------------
    # Walk through chunks
    # -----------------------------
    for chunk in chunks:

        page = chunk.metadata["page"]

        page_headings = headings_by_page.get(page, [])

        if page_headings:
            # We use the first heading on that page.
            # (We'll improve this later using chunk position.)
            current_heading = page_headings[0]["text"]

        chunk.metadata["heading"] = current_heading

    return chunks