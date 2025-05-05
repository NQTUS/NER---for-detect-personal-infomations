def extract_pdf_text(page):
    words = page.get_text("words")
    return [word[4] for word in words]

def extract_docx_text(doc):
    texts = []
    for para in doc.paragraphs:
        for run in para.runs:
            text = run.text
            if text:
                texts.append(text)
    return texts