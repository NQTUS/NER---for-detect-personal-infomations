import easyocr
from PIL import Image
import numpy as np
import io
from face_detector import detect_face

def ocr(image_data, reader=None):
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)  
    image = Image.open(io.BytesIO(image_data))
    image_np = np.array(image)
    
    has_face = detect_face(image_np)
    
    ocr_results = reader.readtext(image_np, detail=0)
    ocr_text = " ".join(ocr_results).strip() if ocr_results else "No text detected in image"
    
    return ocr_text, reader, has_face