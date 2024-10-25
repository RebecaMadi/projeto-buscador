from jsonschema import validate, ValidationError
import json

def validateSchema(data):
    try:
        with open("coletasapi/helpers/schema.json", 'r', encoding='utf-8') as file:
            schema = json.load(file)
        validate(instance=data, schema=schema)
        print("Resposta válida!")
        return data
    except ValidationError as e:
        print(f"O JSON de resposta é inválido: {e.message}")
        return False

def validadeSchemaObject(data):
    try:
        with open("coletasapi/helpers/object_schema.json", 'r', encoding='utf-8') as file:
            schema = json.load(file)
        validate(instance=data, schema=schema)
        print("Objeto válida!")
        return data
    except ValidationError as e:
        print(f"O objeto de resposta é inválido: {e.message}")
        return False

def responseError(code, message, details):
    #Modelo de resposta de erros personalizado
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details
        }
    }