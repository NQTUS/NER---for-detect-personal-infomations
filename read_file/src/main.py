import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'NER', 'src')))

from file_processor import process_file
from utils import entities_to_json, detect_language, has_private_info
from language_ner.english_ner import english_ner
from language_ner.vietnamese_ner import vietnamese_ner

def process_text(text):
    language = detect_language(text)
    print(f"Detected language: {language}")

    if language == 'English':
        entities = english_ner(text)
    elif language == 'Vietnamese':
        entities = vietnamese_ner(text)
    else:
        entities = []
        print(f"NER not supported for {language}")
        
    return entities

if __name__ == "__main__":
    file_path = r"C:\MaHoa\read_file\test_files\test_pdf.pdf"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    
    texts, ocr = process_file(file_path)
    pages = len(texts)
    if texts:
        for page in range(pages):
            text = texts[page]
            # print("Extracted text:", text)
            entities = process_text(text)
            output_path = entities_to_json(entities, output_dir=output_dir, filename=f"page_{page + 1}.json")
            # print(entities)
            print(f"Entities saved to: {output_path}")
    else:
        print("Failed to extract text from the file Or no text found.")
        
    if ocr:
        private_img = []
        for result in ocr:
            page = result["page"]
            image_index = result["image_index"]
            text = result["text"]
            has_face = result["has_face"]
            
            if has_private_info(result, process_text):
                private_img.append({"page": page, "image_index": image_index})
                
        if private_img:
            output_path = os.path.join(output_dir, "private_info_images.json")
            with open(output_path, "w") as f:
                json.dump(private_img, f, indent=4)
            print(f"Private images info saved to: {output_path}")
            
    else:
        print("No text and face found.")