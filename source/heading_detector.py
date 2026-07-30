import fitz
from collections import Counter


def extract_spans(pdf_document):


    spans = []

    for page_num, page in enumerate(pdf_document):

        blocks = page.get_text("dict")["blocks"]

        for block in blocks:

            if block["type"] != 0:
                continue

            for line in block["lines"]:

                for span in line["spans"]:

                    text = span["text"].strip()

                    if not text:
                        continue

                    spans.append({
                        "text": text,
                        "page": page_num,
                        "font_size": round(span["size"], 1),
                        "font": span["font"],
                        "flags": span["flags"],
                        "bbox": span["bbox"]
                    })

    return spans


def is_bold(font_name, flags):

    return (
        "bold" in font_name.lower()
        or bool(flags & 16)
    )


def detect_headings(pdf_path):

    print(">>> detect_headings() is running <<<")



    pdf_document = fitz.open(pdf_path)
    spans = extract_spans(pdf_document)

    if not spans:
        return []
    
    PAGE_NUMBER = 2      # Change this to the page you want (0-based)

    for span in spans:
        if span["page"] == PAGE_NUMBER:
            print(
                span["text"],
                span["font_size"],
                span["font"],
                span["flags"]
            )

    font_counter = Counter(
        span["font_size"]
        for span in spans
    )

    body_font = font_counter.most_common(1)[0][0]

    headings = []
    seen = set()

    # ---------------------------------------
    # Find document title size
    # ---------------------------------------

    first_page_fonts = [
        span["font_size"]
        for span in spans
        if span["page"] == 0
    ]

    document_title_size = (
        max(first_page_fonts)
        if first_page_fonts
        else None
    )

    # ---------------------------------------
    # Detect headings
    # ---------------------------------------

    for span in spans:

        text = span["text"]
        words = text.split()

        # Must be bold
#        if not is_bold(span["font"], span["flags"]):
 #           continue

        # Must be larger than body text
        if span["font_size"] <= body_font:
            continue

        # Ignore document title
        if (
            span["page"] == 0
            and document_title_size is not None
            and span["font_size"] == document_title_size
        ):
            continue

        # Heading should be reasonably short
        if len(words) > 8:
            continue

        # Reject sentences
        if text.endswith("."):
            continue

        # Reject specification lines
        if ":" in text:
            continue

        # Reject comma-heavy lines
        if "," in text:
            continue

        # Reject lines with many numbers
        if sum(c.isdigit() for c in text) > 3:
            continue

        # Reject URLs
        if "http" in text.lower():
            continue

        key = (span["page"], text)

        if key in seen:
            continue

        seen.add(key)

        headings.append({
            "text": text,
            "page": span["page"],
            "y": span["bbox"][1]
        })

    # Sort by page and vertical position
    headings.sort(
        key=lambda h: (h["page"], h["y"])
    )

    return headings

