import os
import subprocess
import win32com.client
from docx import Document
import tempfile
import platform


def convert_doc_to_pdf(doc_path):
    doc_path = os.path.abspath(doc_path)
    
    temp_dir = tempfile.gettempdir()
    temp_filename = next(tempfile._get_candidate_names()) + ".pdf"
    temp_pdf_path = os.path.join(temp_dir, temp_filename)
    
    system = platform.system()
    
    if system == "Windows":
        convert_with_windows(doc_path, temp_pdf_path)
    else:
        convert_with_libreoffice(doc_path, temp_pdf_path)
    
    if os.path.exists(temp_pdf_path):
        return temp_pdf_path
    else:
        raise Exception("PDF conversion failed: output file not found")

def convert_with_windows(doc_path, pdf_path):
    
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    try:
        doc = word.Documents.Open(doc_path)
        
        doc.SaveAs(pdf_path, FileFormat=17)
        
        doc.Close()
    except Exception as e:
        raise Exception(f"Error converting document with Word: {e}")
    finally:
        word.Quit()

def convert_with_libreoffice(doc_path, pdf_path):
    output_dir = os.path.dirname(pdf_path)
    
    libreoffice_paths = ["libreoffice", "soffice"]
    libreoffice = None
    
    for path in libreoffice_paths:
        try:
            subprocess.run([path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            libreoffice = path
            break
        except FileNotFoundError:
            continue
    
    if libreoffice is None:
        raise Exception("LibreOffice not found. Please install LibreOffice to convert .doc files.")
    
    process = subprocess.run([
        libreoffice,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        doc_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if process.returncode != 0:
        raise Exception(f"LibreOffice conversion failed: {process.stderr.decode('utf-8')}")
    
    expected_filename = os.path.splitext(os.path.basename(doc_path))[0] + ".pdf"
    actual_pdf_path = os.path.join(output_dir, expected_filename)
    
    if os.path.exists(actual_pdf_path) and actual_pdf_path != pdf_path:
        os.rename(actual_pdf_path, pdf_path)