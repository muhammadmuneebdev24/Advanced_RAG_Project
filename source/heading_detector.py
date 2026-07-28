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

    pdf_document = fitz.open(pdf_path)
    spans = extract_spans(pdf_document)

    font_counter = Counter(span["font_size"] for span in spans)
    body_font = font_counter.most_common(1)[0][0]

    headings = []
    seen = set()

    # Largest font on first page (usually document title)
    first_page_fonts = [
        span["font_size"]
        for span in spans
        if span["page"] == 0
    ]

    document_title_size = max(first_page_fonts)

    for span in spans:

        text = span["text"]
        words = text.split()

        # must be bold
        if not is_bold(span["font"], span["flags"]):
            continue

        # larger than body text
        if span["font_size"] <= body_font:
            continue

        # ignore huge document title on first page
        if (
            span["page"] == 0
            and span["font_size"] == document_title_size
        ):
            continue

        # short heading
        if len(words) > 8:
            continue

        # reject sentences
        if text.endswith("."):
            continue

        # reject specification lines
        if ":" in text:
            continue

        # reject comma-heavy text
        if "," in text:
            continue

        # reject many numbers
        if sum(c.isdigit() for c in text) > 3:
            continue

        # reject urls
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
    headings.sort(key=lambda h: (h["page"], h["y"]))

    return headings

