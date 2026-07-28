from langchain_core.documents import Document
from source.heading_detector import extract_spans, detect_headings


def build_sections(pdf_document):

    spans = extract_spans(pdf_document)

    # These are ONLY the main headings
    main_headings = detect_headings(pdf_document)

    heading_lookup = {
        (h["page"], h["text"])
        for h in main_headings
    }

    sections = []

    current_heading = "Untitled"
    current_page = 0
    current_content = []

    for span in spans:

        key = (span["page"], span["text"])

        # -------------------------
        # New Main Heading
        # -------------------------
        if key in heading_lookup:

            # Save previous section
            if current_content:

                sections.append(
                    Document(
                        page_content="\n".join(current_content).strip(),
                        metadata={
                            "heading": current_heading,
                            "page": current_page,
                            "page_label": current_page + 1
                        }
                    )
                )

                current_content = []

            current_heading = span["text"]
            current_page = span["page"]

            # Don't include the heading itself in the content
            continue

        # Everything until the next main heading belongs to this section
        current_content.append(span["text"])

    # -------------------------
    # Save Last Section
    # -------------------------
    if current_content:

        sections.append(
            Document(
                page_content="\n".join(current_content).strip(),
                metadata={
                    "heading": current_heading,
                    "page": current_page,
                    "page_label": current_page + 1
                }
            )
        )

    return sections