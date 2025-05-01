import json
import os
import re
from datetime import datetime
from langdetect import detect
from rapidfuzz import fuzz, process
from deep_translator import GoogleTranslator
import unicodedata

def remove_diacritics(text):
    normalized = unicodedata.normalize('NFD', text)

    no_diacritics = ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')
    
    return unicodedata.normalize('NFC', no_diacritics)

def find_best_match(text, pattern):
    # Split text into phrases for matching
    phrases = re.findall(r'\w[\w ]*', text)
    best_match = process.extractOne(pattern, phrases, scorer=fuzz.ratio)
    if best_match and best_match[1] >= 50:  
        matched_text = best_match[0]
        start_idx = text.find(matched_text)
        end_idx = start_idx + len(matched_text)
        return matched_text, start_idx, end_idx
    return None

def map_entities_to_original(original_text, non_diacritics_text, english_entities):
    mapped_entities = []
    translator_en_to_vi = GoogleTranslator(source='en', target='vi')
    
    for entity_text, label, en_start, en_end in english_entities:
        if label == 'LOC':
            try:
                vi_entity_text = translator_en_to_vi.translate(entity_text)
                match = find_best_match(original_text, vi_entity_text)
                if match:
                    matched_text, start_idx, end_idx = match
                    mapped_entities.append((matched_text, label, start_idx, end_idx))
            except Exception as e:
                print(f"Error translating '{entity_text}' to Vietnamese: {e}")
        else:
            start_idx = non_diacritics_text.find(entity_text)
            if start_idx != -1:
                end_idx = start_idx + len(entity_text)
                original_entity_text = original_text[start_idx:end_idx]
                mapped_entities.append((original_entity_text, label, start_idx, end_idx))
    
    return mapped_entities


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
    