from coletasapi.services import search_tjce_mongo_service, search_tjal_mongo_service
from coletasapi.helpers import validaNumeroDeProcesso
from coletasapi.middlewares import validateSchema, responseError
import time

def search_processo_controller(numero_processo, max_cache):
    validacao_processo = validaNumeroDeProcesso(numero_processo)
    if validacao_processo[0]:
        tribunal = validacao_processo[1]
        if tribunal == "TJAL":
            schema =  search_tjal_mongo_service(numero_processo, max_cache, time.time())
        elif tribunal == "TJCE":
            schema =  search_tjce_mongo_service(numero_processo, max_cache, time.time())

        return schema
        """schema = validateSchema(schema)
        if not schema:
            return responseError(500, "Erro interno", "O servidor sofreu um erro inesperado ao retornar a resposta!")
        else:
            return schema"""
    else:
        return responseError(406, "Not Acceptable", "O número do processo é inválido!")

    