from collections import Counter
import re

# -----------------------------
# CONFIG
# -----------------------------

FONT_SIZE_WEIGHT = 4
BOLD_WEIGHT = 3
SHORT_LINE_WEIGHT = 2
ALPHA_WEIGHT = 1
UPPERCASE_WEIGHT = 1

ENDS_WITH_PERIOD_PENALTY = -3
LONG_LINE_PENALTY = -4

HEADING_THRESHOLD = 6

MAX_HEADING_WORDS = 10


# -----------------------------
# Extract every text span
# -----------------------------

def extract_spans(pdf_document):

    spans = []

    for page_number, page in enumerate(pdf_document):

        page_dict = page.get_text("dict")

        for block in page_dict["blocks"]:

            if block["type"] != 0:
                continue

            for line in block["lines"]:

                for span in line["spans"]:

                    text = span["text"].strip()

                    if not text:
                        continue

                    # Remove bullets/icons
                    text = re.sub(r"^[^\w]+", "", text).strip()

                    spans.append({
                        "text": text,
                        "font_size": round(span["size"], 1),
                        "font": span["font"],
                        "flags": span["flags"],
                        "page": page_number,
                        "bbox": span["bbox"]
                    })

    return spans


# -----------------------------
# Body font
# -----------------------------

def get_body_font_size(spans):

    counter = Counter()

    for span in spans:
        counter[span["font_size"]] += 1

    return counter.most_common(1)[0][0]


# -----------------------------
# Helpers
# -----------------------------

def is_bold(font_name, flags):

    font_name = font_name.lower()

    return "bold" in font_name or bool(flags & 16)


def mostly_alphabetic(text):

    letters = sum(c.isalpha() for c in text)

    return letters >= len(text) * 0.6


# -----------------------------
# Heading score
# -----------------------------

def score_heading(span, body_font_size):

    score = 0

    text = span["text"]
    words = text.split()

    if span["font_size"] > body_font_size:
        score += FONT_SIZE_WEIGHT

    if is_bold(span["font"], span["flags"]):
        score += BOLD_WEIGHT

    if len(words) <= MAX_HEADING_WORDS:
        score += SHORT_LINE_WEIGHT

    if len(words) > 15:
        score += LONG_LINE_PENALTY

    if text.endswith("."):
        score += ENDS_WITH_PERIOD_PENALTY

    if mostly_alphabetic(text):
        score += ALPHA_WEIGHT

    if text.isupper():
        score += UPPERCASE_WEIGHT

    return score


# -----------------------------
# Detect Main Headings
# -----------------------------

def detect_headings(pdf_document):

    spans = extract_spans(pdf_document)

    print("\n===== Extracted Spans =====")

    for s in spans[:50]:
        print(
            s["text"],
            "| Size:", s["font_size"],
            "| Font:", s["font"],
            "| Flags:", s["flags"]
        )

    body_font = get_body_font_size(spans)

    # Count every bold font size
    font_counter = Counter()

    for span in spans:
        if is_bold(span["font"], span["flags"]):
            font_counter[span["font_size"]] += 1

    if not font_counter:
        return []

    # Choose the largest bold font that appears more than once
    heading_font = None

    for size in sorted(font_counter.keys(), reverse=True):

        if font_counter[size] >= 2:
            heading_font = size
            break

    if heading_font is None:
        heading_font = max(font_counter.keys())

    headings = []
    seen = set()

    for span in spans:

        # Must be bold
        if not is_bold(span["font"], span["flags"]):
            continue

        # Must use heading font
        if span["font_size"] != heading_font:
            continue

        # Ignore very top title on first page
        if span["page"] == 0 and span["bbox"][1] < 120:
            continue

        # Basic quality checks
        score = score_heading(span, body_font)

        if score < HEADING_THRESHOLD:
            continue

        key = (span["page"], span["text"])

        if key in seen:
            continue

        seen.add(key)

        headings.append({
            "text": span["text"],
            "page": span["page"],
            "score": score,
            "bbox": span["bbox"]
        })

    headings.sort(key=lambda h: (h["page"], h["bbox"][1]))

    print("\n===== Main Headings =====")

    for h in headings:
        print(
            h["text"],
            "| Score:", h["score"],
            "| Page:", h["page"] + 1
        )

    return headings