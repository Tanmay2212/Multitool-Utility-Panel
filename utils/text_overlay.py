# utils/text_overlay.py

import fitz  # PyMuPDF

def add_text_to_pdf(input_path, output_path, old_text, new_text):
    """
    Replaces `old_text` with `new_text` in the PDF and saves to output_path.
    """
    doc = fitz.open(input_path)

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    if old_text in span["text"]:
                        rect = fitz.Rect(span["bbox"])
                        # draw a white rectangle to 'erase'
                        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                        # add new text in the same position
                        page.insert_text(rect.tl, new_text, fontsize=span["size"], fontname=span["font"])

    doc.save(output_path)
    doc.close()
