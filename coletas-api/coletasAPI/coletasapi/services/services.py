from coletasapi.models import search_tjal_primeira_instancia, search_tjce_primeira_instancia, search_tjal_segunda_instancia, search_tjce_segunda_instancia, search_tjce_mongo_model, search_tjal_mongo_model
import json
from coletasapi.models import inserir_processo_mongo
import time

def search_tjal_sync_service(numero_processo, instancia):
    if instancia == 1:
        resultado = search_tjal_primeira_instancia(numero_processo)
    else:
        resultado = search_tjal_segunda_instancia(numero_processo)
    if not resultado:
        print("O processo não tem as informações necessárias no esquema.")
        return []
    else:
        return resultado
    
def search_tjal_mongo_service(numero_processo, max_cache, tempo_consulta):
    resultado_auxiliar = search_tjal_mongo_model(numero_processo, max_cache, tempo_consulta)
    resultado = []
    if resultado_auxiliar[0] == False or resultado_auxiliar[0]==None:
        primeira_instancia = search_tjal_sync_service(numero_processo, 1)
        if primeira_instancia != []:
            inserir = inserir_processo_mongo(1, primeira_instancia, time.time(), numero_processo)
            if inserir:
                resultado.append(primeira_instancia)
            else:
                print(inserir)
    else:
        print("achou no banco")
        resultado.append(resultado_auxiliar[0])

    if resultado_auxiliar[1] == False or resultado_auxiliar[1] == None:
        segunda_instancia = search_tjal_sync_service(numero_processo, 2)
        if segunda_instancia != []:
            inserir = inserir_processo_mongo(2, segunda_instancia, time.time(), numero_processo)
            if inserir:
                resultado.append(segunda_instancia)
            else:
                print(inserir)
    else:
        print("achou no banco")
        resultado.append(resultado_auxiliar[1])
    
    return resultado


def search_tjce_sync_service(numero_processo, instancia):
    if instancia == 1:
        resultado = search_tjce_primeira_instancia(numero_processo)
    else:
        resultado = search_tjce_segunda_instancia(numero_processo)
    if not resultado:
        print("O processo não tem as informações necessárias no esquema.")
        return []
    else:
        return resultado
    
def search_tjce_mongo_service(numero_processo, max_cache, tempo_consulta):
    resultado_auxiliar = search_tjce_mongo_model(numero_processo, max_cache, tempo_consulta)
    resultado = []
    if resultado_auxiliar[0] == False or resultado_auxiliar[0]==None:
        primeira_instancia = search_tjce_sync_service(numero_processo, 1)
        if primeira_instancia != []:
            inserir = inserir_processo_mongo(3, primeira_instancia, time.time(), numero_processo)
            if inserir:
                resultado.append(primeira_instancia)
            else:
                print(inserir)
    else:
        resultado.append(resultado_auxiliar[0])

    if resultado_auxiliar[1] == False or resultado_auxiliar[1] == None:
        segunda_instancia = search_tjce_sync_service(numero_processo, 2)
        if segunda_instancia != []:
            inserir = inserir_processo_mongo(4, segunda_instancia, time.time(), numero_processo)
            if inserir:
                resultado.append(segunda_instancia)
            else:
                print(inserir)
    else:
        resultado.append(resultado_auxiliar[1])
    
    return resultado
        
