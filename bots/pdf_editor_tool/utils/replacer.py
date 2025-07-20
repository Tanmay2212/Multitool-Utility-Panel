import fitz  # PyMuPDF

def replace_text_in_pdf(pdf_path, matches, old, new):
    doc = fitz.open(pdf_path)

    for match in matches:
        page = doc[match["page"]]
        full_text = match["text"]
        font = match["font"]
        size = match["size"]
        bbox = match["bbox"]

        if old.lower() not in full_text.lower():
            continue

        rect = fitz.Rect(bbox)
        page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()

        words = full_text.split()
        cursor_x = rect.x0
        cursor_y = rect.y1 - 2

        for word in words:
            insert_text = new if word.lower() == old.lower() else word
            page.insert_text(
                (cursor_x, cursor_y),
                insert_text + " ",
                fontname=font,
                fontsize=size,
                color=(0, 0, 0),
                overlay=True
            )
            cursor_x += size * 0.6 * len(insert_text + " ")

    return doc  # 🔥 Return updated PDF doc instead of saving
