import os
import argparse
from language_ner.english_ner import english_ner
from language_ner.vietnamese_ner import vietnamese_ner
from utils import entities_to_json, detect_language

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
    parser = argparse.ArgumentParser(description="Process text file for Named Entity Recognition (NER)")
    parser.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Path to the input text file (e.g., ../other_folder/input.txt)"
    )
    args = parser.parse_args()


    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        exit(1)

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    except Exception as e:
        print(f"Error: Failed to read file '{args.input_file}': {str(e)}")
        exit(1)

    if not text:
        print("Error: Input file is empty.")
        exit(1)

    # Process the text for NER
    entities = process_text(text)
    
    # Save entities to JSON
    output_path = entities_to_json(entities)