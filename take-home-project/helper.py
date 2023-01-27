"""
This file fetches data from Reactome.org for some keywords and returns them as DocumentArray
"""
from reactome_data_script import get_information_for_term
from docarray import Document, DocumentArray
from config import KEYWORDS

# function to parse only the "summation" field's text from the docs, for indexing
def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)

"""
Fetches data from Reactome.org for some keywords and returns them as DocumentArray, removes duplicates
"""
def get_docs():
    all_documents = DocumentArray()
    already_seen = set()
    for keyword in KEYWORDS:
        result = get_information_for_term(keyword)
        summation_generator = item_generator(result, 'summation')
        for text in summation_generator:
            if text not in already_seen:
                document = Document(text=text)
                all_documents.append(document)
                already_seen.add(text)
    return all_documents


if __name__=='__main__':
    get_docs()
