import re
import time
import spacy
from spacy.util import is_package
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

nlp_en = spacy.load("en_core_web_sm")

configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)

def english_ner(text):
    
    startTime = time.time()
    
    doc = nlp_en(text)
    entities = []
    tracked_spans = set()  
    
    desired_spacy_labels = {'PERSON', 'ORG', 'GPE', 'LOC'}
    for ent in doc.ents:
        if ent.label_ in desired_spacy_labels:
            label = 'LOC' if ent.label_ in {'GPE', 'LOC'} else ent.label_
            span = (ent.start_char, ent.end_char)
            entities.append((ent.text, label, ent.start_char, ent.end_char))
            tracked_spans.add(span)
    
    presidio_entities = [
        "PHONE_NUMBER", "ADDRESS", "EMAIL_ADDRESS", "CREDIT_CARD", 
        "PERSON", "ORGANIZATION", "LOCATION", "URL"
    ]
    
    analyzer = AnalyzerEngine()
    
    presidio_results = analyzer.analyze(
        text=text, 
        language="en", 
        entities=presidio_entities,
        score_threshold=0.3  
    )
    
    label_mapping = {
        "PERSON": "PERSON",
        "ORGANIZATION": "ORG",
        "LOCATION": "LOC",
        "PHONE_NUMBER": "PHONE_NUMBER",
        "ADDRESS": "ADDRESS",
        "EMAIL_ADDRESS": "EMAIL_ADDRESS",
        "CREDIT_CARD": "CREDIT_CARD",
        "URL": "URL"
    }
    
    for result in presidio_results:
        entity_text = text[result.start:result.end]
        label = label_mapping.get(result.entity_type, result.entity_type)
        span = (result.start, result.end)
        
        overlap = False
        for tracked_start, tracked_end in tracked_spans:
            if (result.start <= tracked_end and result.end >= tracked_start):
                if label == "ADDRESS":
                    entities = [e for e in entities if not (e[2] <= result.end and e[3] >= result.start)]
                    tracked_spans.discard((tracked_start, tracked_end))
                    overlap = False
                    break
                else:
                    overlap = True
                    break
        
        if not overlap:
            entities.append((entity_text, label, result.start, result.end))
            tracked_spans.add(span)
    
    cc_patterns = [
        r'\b(?:\d{4}[-\s]?){3}\d{4}\b',          
        r'\b\d{4}[-\s]?\d{6}[-\s]?\d{5}\b',      
    ]
    
    for pattern in cc_patterns:
        for match in re.finditer(pattern, text):
            cc_text = match.group()
            start_idx = match.start()
            end_idx = match.end()
            
            overlap = False
            for tracked_start, tracked_end in tracked_spans:
                if (start_idx <= tracked_end and end_idx >= tracked_start):
                    overlap = True
                    break
            
            if not overlap:
                entities.append((cc_text, "CREDIT_CARD", start_idx, end_idx))
                tracked_spans.add((start_idx, end_idx))
    
    entities.sort(key=lambda x: x[2])
    
    endTime = time.time()
    print("NER time:", endTime - startTime)
    
    return entities