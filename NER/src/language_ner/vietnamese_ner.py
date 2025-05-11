from utils import remove_diacritics
from language_ner.english_ner import english_ner
from utils import map_entities_to_original
from deep_translator import GoogleTranslator

def vietnamese_ner(text):
    original_text = text
    non_diacritics_text = remove_diacritics(text)
    
    translator = GoogleTranslator(source='vi', target='en')
    translated_text = translator.translate(text)  
    
    english_entities = english_ner(translated_text)
    mapped_entities = map_entities_to_original(original_text, non_diacritics_text, english_entities)
    
    return mapped_entities