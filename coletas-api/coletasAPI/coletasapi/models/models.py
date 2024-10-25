from coletasapi.middlewares.parser import pagina_processo_parser, multiplicidadeProcesso
from coletasapi.middlewares.error_handler import responseError
from coletasapi.databases import MongoDB
from coletasapi.helpers import valida_tempo_cache
import httpx

#URL do TJAL para consultar processos de primeira instância
url_tjal_primeira_instancia = "https://www2.tjal.jus.br/cpopg/show.do"
url_tjce_primeira_instancia = "https://esaj.tjce.jus.br/cpopg/show.do"
url_tjal_segunda_instancia = "https://www2.tjal.jus.br/cposg5/search.do"
url_tjal_segunda_instancia_show = "https://www2.tjal.jus.br/cposg5/show.do" #acesso direto a página pelo código do processo
url_tjce_segunda_instancia = "https://esaj.tjce.jus.br/cposg5/search.do"
url_tjce_segunda_instancia_show = "https://esaj.tjce.jus.br/cposg5/show.do" #acesso direto a página pelo código do processo

url_mongo = "mongodb://mongodb:27017"
db_nome = "coletas_db"

processos_primeira_instancia_tjal = "processos_primeira_instancia_tjal"
processos_primeira_instancia_tjce = "processos_primeira_instancia_tjce"
processos_segunda_instancia_tjal = "processos_segunda_instancia_tjal"
processos_segunda_instancia_tjce = "processos_segunda_instancia_tjce"

def search_tjal_primeira_instancia(numero_processo):
    """função de requisição de processos de primeira instancia para o TJAL """
    query_string = {
        "processo.numero": numero_processo
    }
    try:
        response = httpx.get(
            url=url_tjal_primeira_instancia,
            params=query_string,
            timeout = 60000
        )
        if response.status_code == 200:
            response = pagina_processo_parser(response, numero_processo, "TJAL", 1)
            return response
        else:
            return responseError(response.status_code, "Erro ao fazer a requisição", response.details)
    except httpx.RequestError as exc:
        return responseError(400, "Erro ao fazer a requisição", exc)
    except httpx.HTTPStatusError as exc:
        return responseError(exc.response.status_code, exc.response.message, exc.response.details)
    except Exception as exc:
        return responseError(400, "Erro ao fazer a requisição", exc)

def search_tjal_segunda_instancia(numero_processo):
    """função de requisição de processos de primeira instancia para o TJAL """
    query_string = {
        "cbPesquisa": "NUMPROC",
        "numeroDigitoAnoUnificado": numero_processo[:15],
        "foroNumeroUnificado": numero_processo[15:],
        "dePesquisaNuUnificado": "UNIFICADO",
        "tipoNuProcesso": "UNIFICADO",
        "dePesquisaNuUnificado": numero_processo.replace(".","").replace("-","")
    }
    try:
        response = httpx.get(
            url=url_tjal_segunda_instancia,
            params=query_string,
            timeout = 1
        )
        if response.status_code == 200:
            #Lida com páginas intermediárias. Pega o codigo do processo se a request não cessar diretamente a página do processo
            intermediario = multiplicidadeProcesso(response)
            if intermediario == False:
                response = pagina_processo_parser(response, numero_processo, "TJAL", 2)
            else:
                query_string = {
                    "processo.codigo": str(intermediario)
                }
                try:
                    response = httpx.get(
                        url=url_tjal_segunda_instancia_show,
                        params=query_string,
                        timeout = 1
                    )
                    if response.status_code == 200:
                        response = pagina_processo_parser(response, numero_processo, "TJAL", 2)
                except httpx.RequestError as exc:
                    return responseError(400, "Erro ao fazer a requisição", exc)
                except httpx.HTTPStatusError as exc:
                    return responseError(exc.response.status_code, exc.response.message, exc.response.details)
                except Exception as exc:
                    return responseError(400, "Erro ao fazer a requisição", exc)
            return response
        else:
            return responseError(response.status_code, "Erro ao fazer a requisição", response.details)
    except httpx.RequestError as exc:
        return responseError(400, "Erro ao fazer a requisição", exc)
    except httpx.HTTPStatusError as exc:
        return responseError(exc.response.status_code, exc.response.message, exc.response.details)
    except Exception as exc:
        return responseError(400, "Erro ao fazer a requisição", exc)

def search_tjce_primeira_instancia(numero_processo):
    """função de requisição de processos de primeira instancia para o TJAL """
    query_string = {
        "processo.numero": numero_processo
    }
    try:
        response = httpx.get(
            url=url_tjce_primeira_instancia,
            params=query_string,
            timeout = 1
        )
        if response.status_code == 200:
            response = pagina_processo_parser(response, numero_processo, "TJCE", 1)
            return response
        else:
            return responseError(response.status_code, "Erro ao fazer a requisição", response.details)
    except httpx.RequestError as exc:
        return responseError(400, "Erro ao fazer a requisição", exc)
    except httpx.HTTPStatusError as exc:
        return responseError(exc.response.status_code, exc.response.message, exc.response.details)
    except Exception as exc:
        return responseError(400, "Erro ao fazer a requisição", exc)
    
def search_tjce_segunda_instancia(numero_processo):
    """função de requisição de processos de primeira instancia para o TJAL """
    query_string = {
        "cbPesquisa": "NUMPROC",
        "numeroDigitoAnoUnificado": numero_processo[:15],
        "foroNumeroUnificado": numero_processo[15:],
        "dePesquisaNuUnificado": "UNIFICADO",
        "tipoNuProcesso": "UNIFICADO",
        "dePesquisaNuUnificado": numero_processo.replace(".","").replace("-","")
    }
    try:
        response = httpx.get(
            url=url_tjce_segunda_instancia,
            params=query_string,
            timeout = 1
        )
        if response.status_code == 200:
            #Lida com páginas intermediárias. Pega o codigo do processo se a request não cessar diretamente a página do processo
            intermediario = multiplicidadeProcesso(response)
            if intermediario == False:
                response = pagina_processo_parser(response, numero_processo, "TJCE", 2)
            else:
                query_string = {
                    "processo.codigo": str(intermediario)
                }
                try:
                    response = httpx.get(
                        url=url_tjce_segunda_instancia_show,
                        params=query_string,
                        timeout = 1
                    )
                    if response.status_code == 200:
                        response = pagina_processo_parser(response, numero_processo, "TJCE", 2)
                except httpx.RequestError as exc:
                    return responseError(400, "Erro ao fazer a requisição", exc)
                except httpx.HTTPStatusError as exc:
                    return responseError(exc.response.status_code, exc.response.message, exc.response.details)
                except Exception as exc:
                    return responseError(400, "Erro ao fazer a requisição", exc)
            return response
        else:
            return responseError(response.status_code, "Erro ao fazer a requisição", response.details)
    except httpx.RequestError as exc:
        return responseError(400, "Erro ao fazer a requisição", exc)
    except httpx.HTTPStatusError as exc:
        return responseError(exc.response.status_code, exc.response.message, exc.response.details)
    except Exception as exc:
        return responseError(400, "Erro ao fazer a requisição", exc)
    
def search_tjal_mongo_model(numero_processo, max_cache, tempo_consulta):
    """Função que realiza a busca do processo nas duas instancias do tribunal TJAL"""
    db = MongoDB(url_mongo, db_nome)

    query = {
        "numero_do_processo": numero_processo
    }
    resultado = []

    #procura na coleção da primeira instância
    resultado_auxiliar = db.find_one(processos_primeira_instancia_tjal, query)
    
    if resultado_auxiliar:
        validacao = valida_tempo_cache(resultado_auxiliar, max_cache, tempo_consulta)
        if validacao:
            resultado.append(resultado_auxiliar["processo"])
        else:
            resultado.append(False)
    else:
        resultado.append(False)

    #procura na coleção da segunda instância
    resultado_auxiliar = db.find_one(processos_segunda_instancia_tjal, query)

    if resultado_auxiliar:
        validacao = valida_tempo_cache(resultado_auxiliar, max_cache, tempo_consulta)
        if validacao:
            resultado.append(resultado_auxiliar["processo"])
        else:
            resultado.append(False)
    else:
        resultado.append(False)

    db.close()
    return resultado

def search_tjce_mongo_model(numero_processo, max_cache, tempo_consulta):
    """Função que realiza a busca do processo nas duas instancias do tribunal TJCE"""
    db = MongoDB(url_mongo, db_nome)

    query = {
        "numero_do_processo": numero_processo
    }
    resultado = []

    #procura na coleção da primeira instância
    resultado_auxiliar = db.find_one(processos_primeira_instancia_tjce, query)

    if resultado_auxiliar:
        validacao = valida_tempo_cache(resultado_auxiliar, max_cache, tempo_consulta)
        if validacao:
            resultado.append(resultado_auxiliar["processo"])
        else:
            resultado.append(False)
    else:
        resultado.append(False)

    #procura na coleção da segunda instância
    resultado_auxiliar = db.find_one(processos_segunda_instancia_tjce, query)

    if resultado_auxiliar:
        validacao = valida_tempo_cache(resultado_auxiliar, max_cache, tempo_consulta)
        if validacao:
            resultado.append(resultado_auxiliar["processo"])
        else:
            resultado.append(False)
    else:
        resultado.append(False)
    db.close()
    return resultado

def inserir_processo_mongo(colecao, processo, tempo_coleta, numero_processo):
    db = MongoDB(url_mongo, db_nome)

    documento = {
        "numero_do_processo": numero_processo,
        "tempo_coleta": tempo_coleta,
        "processo": processo
    }

    if colecao == 1:
        colecao_nome = processos_primeira_instancia_tjal
    elif colecao == 2:
        colecao_nome = processos_segunda_instancia_tjal
    elif colecao == 3:
        colecao_nome = processos_primeira_instancia_tjce
    else:
        colecao_nome = processos_segunda_instancia_tjce
    try:
        query = {
            "numero_do_processo": numero_processo
        }
        procura = db.find_one(colecao_nome, query)
        if procura is None:
            db.insert_one(colecao_nome, documento)
        else:
            update = db.update_one(colecao_nome, query, documento)
            print("update:", update)
        db.close()
        return True
    except Exception as exc:
        print("Erro ao inserir na base de dados:")
        return responseError(500, "Erro ao inserir na base de dados:", exc)