import json
import os
from datetime import datetime
from langdetect import detect


def detect_language(text):
    try:
        lang = detect(text)
        if lang == 'en':
            return 'English'
        elif lang == 'vi':
            return 'Vietnamese'
        else:
            return f'Other ({lang})'
    except:
        return 'Unknown'
    
def entities_to_json(entities, output_dir="output", filename=None):
    os.makedirs(output_dir, exist_ok=True)
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"entities_{timestamp}.json"
    
    output_path = os.path.join(output_dir, filename)
    
    entities_json = [
        {
            "text": text,
            "label": label,
            "start": start,
            "end": end
        }
        for text, label, start, end in entities
    ]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(entities_json, f, indent=4, ensure_ascii=False)
    
    return output_path
    