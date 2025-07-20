import fitz  # PyMuPDF

def extract_text_with_font(pdf_path):
    doc = fitz.open(pdf_path)
    result = []

    for page_num, page in enumerate(doc):
        spans = []
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    spans.append({
                        "text": span["text"],
                        "bbox": span["bbox"],
                        "font": span.get("font", "helv"),
                        "size": span.get("size", 12),
                        "page": page_num
                    })
        result.append(spans)
    return result
