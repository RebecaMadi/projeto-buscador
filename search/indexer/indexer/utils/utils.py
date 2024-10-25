from datetime import datetime
import logging
import os
import json

def convert_date(date):
    date_time_seconds = datetime.fromtimestamp(date)
    iso_format_date = date_time_seconds.strftime('%Y-%m-%d') 
    return iso_format_date

def get_lawyers(field, lines):
    res = []
    for line in lines:
        res.append({field: line[field]})
    return res

def read_json_file(filepath="./indexer/resources/index.json"):
    try:
        print(os.getcwd())
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as e:
            logging.info(f"Erro ao ler o modelo de mapping: {e}")

def get_related_people(lines):
    res = []
    for line in lines:
        res.append({
            "name": line["name"],
            "role": line["role"]["rawValue"]
        })
    return res

def get_activities(lines):
    res = []
    for line in lines:
        res.append({
            "date": convert_date(line["date"]),
            "description": line["text"]
        })
    return res

def format_documents(docs):
    """ Formata os documentos de acordo com o mappings """

    new_docs = []
    for doc in docs:
        if not doc[1]["justiceSecret"]:
            new_docs.append({
            "_op_type": "index",
            "_index": "lawsuits",
            "_id": doc[0],
            "number": doc[1]["number"],
            "date": convert_date(doc[1]["distributionDate"]) if doc[1]["distributionDate"] else None,
            "court": doc[1]["court"]["rawValue"],
            "judge": doc[1]["judgeName"],
            "kind": doc[1]["kind"],
            "lawyers": get_lawyers("name", doc[1]["representedPersonLawyers"]),
            "nature": doc[1]["nature"],
            "related_people": get_related_people(doc[1]["relatedPeople"]),
            "subject": doc[1]["subject"],
            "value": doc[1]["value"],
            "activities": get_activities(doc[1]["activities"])
        })
    return new_docs
