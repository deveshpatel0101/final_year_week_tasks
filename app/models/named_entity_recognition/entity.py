import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")


def find_entities(text):
    document = {}
    doc = nlp(text)
    for entity in doc.ents:
        document[entity.label_] = entity.text
    return document
