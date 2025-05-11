import os
import argparse
import time
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
    text = """
        Sarah Johnson, an engineer at Google, lives in Soc Trang, CA. Her phone is 0919325721 and email is sarah.johnson@google.com. She shows her projects at https://sarahj.dev. Meeting on March 15, 2025.
        
        Michael Chen, a marketing consultant, is based in Chicago, IL. Contact: (312) 555-9876, michael.chen@consultingfirm.com. Business site: https://chenmarketing.com. Webinar on April 30, 2025.
        
        Emily Rodriguez, a designer in Austin, TX. Phone: (512) 555-4567, email: emily.rodriguez@designstudio.com. Portfolio: https://emilydesigns.art. Client call tomorrow.
        
        David Patel, a financial advisor in Boston, MA. Phone: (617) 555-7890, email: david.patel@financegroup.com. Website: https://patelfinance.com. Client meeting on May 5, 2025.
        
        They will all attend a conference in Las Vegas, NV, on June 10, 2025.
        """

    
    entities = process_text(text)
    output_path = entities_to_json(entities)
    print(entities)
    print(f"Entities saved to: {output_path}")
    