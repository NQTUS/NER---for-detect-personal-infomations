import os
from docx import Document
import zipfile
import pymupdf
from Utils import convert_doc_to_pdf
from ocr import ocr
from text_extractor import extract_pdf_text, extract_docx_text  

def process_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    ext = os.path.splitext(file_path)[1].lower()
    file = None
    
    if ext == '.pdf':
        file, ocr = process_pdf(file_path)
    elif ext == '.docx':
        file, ocr = process_docx(file_path)
    elif ext == '.doc':
        docx_path = convert_doc_to_pdf(file_path)
        if docx_path:
            file, ocr = process_pdf(docx_path)
            try:
                os.remove(docx_path)
            except Exception as e:
                print(f"Warning: Could not delete temporary file {docx_path}: {e}")
    else:
        print(f"Error: Unsupported file format '{ext}'")

    return file, ocr

def process_pdf(pdf_path):
    try:
        doc = pymupdf.open(pdf_path)
        extracted_text = []
        ocr_results = []
        ocr_reader = None
        img_index = 0
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = extract_pdf_text(page)
            images = page.get_images(full=True)
            
            extracted_text.append(" ".join(page_text) if page_text else "No text found.")
            
            for img in images: 
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                    if base_image:  
                        ocr_text, ocr_reader, has_face = ocr(base_image["image"], ocr_reader)
                        ocr_results.append({
                            "page": page_num + 1,
                            "image_index": img_index,
                            "text": ocr_text,
                            "has_face": has_face
                        })
                        img_index += 1
                except Exception as img_error:
                    print(f"Error extracting image {xref} on page {page_num + 1}: {img_error}")
                    continue
        
        doc.close()
        return extracted_text, ocr_results
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return [], []
    
def process_docx(docx_path):
    try:
        doc = Document(docx_path)
        extracted_text = []
        ocr_results = []
        ocr_reader = None
        img_index = 0  
        
        page_text = extract_docx_text(doc)
        extracted_text.append(" ".join(page_text) if page_text else "No Text Found.")
        
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith('word/media/'):
                    with zip_ref.open(file) as img_file:
                        image_data = img_file.read()
                        ocr_text, ocr_readerreader , has_face = ocr(image_data, ocr_reader)
                        
                        ocr_results.append({
                            "image_index": img_index,  #start from 0 
                            "text": ocr_text,
                            "has_face": has_face
                        })
                        img_index += 1
        
        return extracted_text, ocr_results
            
    except Exception as e:
        print(f"ERROR processing DOCX: {e}")
        return [], []