import fitz  # PyMuPDF

# 🔤 Map some known fonts to closest standard fonts
FONT_MAP = {
    # Microsoft/Standard Fonts
    "Arial": "helv",
    "Calibri": "helv",
    "Helvetica": "helv",
    "Times-Roman": "times",
    "TimesNewRoman": "times",
    "CourierNew": "courier",
    "Courier": "courier",

    # AI/LLM/Export fonts
    "TimesNewRomanPSMT": "times",
    "LiberationSerif": "times",
    "NotoSans": "helv",
    "NotoSans-Regular": "helv",
    "SourceSansPro": "helv",
    "FreeSerif": "times",
    "DejaVuSans": "helv",
    "FiraSans": "helv",
    "OpenSans": "helv",
    "Roboto": "helv",

    # Common fallbacks
    "Default": "helv",
    "default": "helv"
}


def replace_text_in_pdf(pdf_path, matches, old, new):
    doc = fitz.open(pdf_path)

    for match in matches:
        page = doc[match["page"]]
        full_text = match["text"]
        font = FONT_MAP.get(match["font"], FONT_MAP["default"])
        size = match["size"]
        bbox = match["bbox"]

        if old.lower() not in full_text.lower():
            continue

        # 1. Redact
        rect = fitz.Rect(bbox)
        page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()

        # 2. Re-insert with adjusted text
        words = full_text.split()
        cursor_x = rect.x0
        cursor_y = rect.y1 - 2  # adjust Y position

        for word in words:
            text = new if word.lower() == old.lower() else word
            page.insert_text(
                (cursor_x, cursor_y),
                text + " ",
                fontname="helv",
                fontsize=size,
                color=(0, 0, 0),
                overlay=True
            )
            cursor_x += size * 0.6 * len(text + " ")

    return doc