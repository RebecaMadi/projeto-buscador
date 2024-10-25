from jsonschema import validate, ValidationError
import json
import logging

logging.basicConfig(level=logging.INFO)

def validateSchema(data, r):
    try:
        with open(f"./schema/{r}.json", 'r', encoding='utf-8') as file:
            schema = json.load(file)
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        logging.info(f"O JSON de resposta é inválido: {e.message}")
        return False