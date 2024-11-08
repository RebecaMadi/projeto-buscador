import re
from fastapi.responses import JSONResponse
from searcher.utils.checker import validateSchema
from searcher.typings.lawsuit import Lawsuit
from datetime import datetime

def find_lawsuit_number(query):
    pattern = r'\b\d{2,7}[-_\.]?\d{2}[-_\.]?\d{4}[-_\.]?\d{1}[-_\.]?\d{2}[-_\.]?\d{4}\b'
    match = re.search(pattern, query)
    if match:
        return match.group(0)
    return None

def format_response(objects):
    """ Retorna a resposta no formato desejado """

    response = {}
    response["hits"] = objects["hits"]["total"]["value"]
    lawsuits = []
    objects = objects["hits"]["hits"]

    for obj in objects:
        lawsuit = Lawsuit(obj)
        lawsuits.append(lawsuit.lawsuit)

    response["lawsuits"] = lawsuits

    if validateSchema(response, "response"):
        return JSONResponse(content=lawsuits)
    else:
        return JSONResponse(content={"error": "Invalid response format"}, status_code=400)

def format_date(timestamp):
    """Converte um timestamp Unix para o formato 'YYYY-MM-DD'."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

def format_db_response(obj):
    formatted_response = {
        "id": obj.get("id", ""),
        "number": obj.get("number", ""),
        "court": obj.get("court", {}).get("rawValue", ""),
        "nature": obj.get("nature", ""),
        "type": obj.get("kind", ""),
        "subject": obj.get("subject", ""),
        "instance": obj.get("courtInstance", "1"),
        "distributionDate": format_date(obj["distributionDate"]) if obj.get("distributionDate") else None,
        "judge": obj.get("judgeName", ""),
        "caseValue": obj.get("value", 0.0),
        "related_people": [],
        "representedPersonLawyers": [],
        "movements": []
    }

    for person in obj.get("relatedPeople", []):
        formatted_response["related_people"].append({
            "name": person.get("name", ""),
            "role": person.get("role", {}).get("normalized", "")
        })
    
    person_map = {p["id"]: p["name"] for p in obj.get("relatedPeople", [])}
    for lawyer in obj.get("representedPersonLawyers", []):
        represented_name = person_map.get(lawyer.get("representedPersonId"), "")
        formatted_response["representedPersonLawyers"].append({
            "name": lawyer.get("name", ""),
            "representedPerson": represented_name
        })

    for activity in obj.get("activities", []):
        formatted_response["movements"].append({
            "date": format_date(activity["date"]) if activity.get("date") else None,
            "description": activity.get("text", "")
        })
    
    return formatted_response
