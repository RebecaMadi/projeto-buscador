import re
from fastapi.responses import JSONResponse
from searcher.utils.checker import validateSchema
from searcher.typings.lawsuit import Lawsuit

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
    print(objects)
    objects = objects["hits"]["hits"]

    for obj in objects:
        lawsuit = Lawsuit(obj)
        lawsuits.append(lawsuit.lawsuit)

    response["lawsuits"] = lawsuits

    if validateSchema(response, "response"):
        return JSONResponse(content=response)
    else:
        return JSONResponse(content={"error": "Invalid response format"}, status_code=400)
