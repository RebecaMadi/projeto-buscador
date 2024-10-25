from bs4 import BeautifulSoup
import json
import re
from coletasapi.helpers.auxiliares import add_partes_do_processo, add_lista_das_movimentacoes
from coletasapi.middlewares.error_handler import validateSchema, responseError, validadeSchemaObject

def normalize_json(data):
    if isinstance(data, dict):
        return {key: normalize_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [normalize_json(item) for item in data]
    elif isinstance(data, str):
        return data.strip()
    elif data is None:
        return 'null'
    return data

#As páginas HTML dos processos seguem padrões parecxidos para as informações que procuramos, por isso vamos usar o mesmo parser para todos. Note, isso não inclui a verificação da existencia ou da validade do número do processo, é apenas um parser.
def pagina_processo_parser(ctx, numero_processo, tribunal, instancia):
    #"Tradução" da resposta para html
    contexto = BeautifulSoup(ctx.content, 'html.parser')
    
    #Preparo da resposta final
    with open("coletasapi/helpers/response_schema.json", 'r', encoding='utf-8') as file:
        #response_schema é o schema padrão de resposta para facilitar o processo
        response_schema = json.load(file)

    #Atualizando as informações já conhecidas
    response_schema["tribunal"] = tribunal
    response_schema["existe"] = True
    response_schema["instancia"] = instancia
    response_schema["numero_do_processo"] = numero_processo

    #Verificação de erro. O site não retorna um status de erro no caso de algo inesperado acontecer, precisamos identificar peça mensagem no html.
    #Os erros relacionados a validação da consulta geralmente são tratados no controllers e no models, mas vamos adicionar essa verificação no caso de passar algo incomum
    erro = contexto.find(id="mensagemRetorno")
    if  erro:
        return response_schema

    #Verifica se o processo é segredo de justiça
    segredo = "É necessário informar uma senha para acessar processo em segredo de justiça, bem como para acessar autos dos demais processos."
    senha = "Senha do processo"
    if segredo in contexto.get_text() and senha in contexto.get_text():
        response_schema["segredo_justica"] = True
        return response_schema
    response_schema["segredo_justica"] = False

    #Procurando o restante das informações
    #Observação: se alguma informação não for encontrada ela continuará como "null" 

    #Classe: A informação da classe do processo está na div class="lh-1-1 line-clamp__2" com o id="classeProcesso
    classe = contexto.find(id="classeProcesso")
    if classe:
        response_schema["classe"] = classe.text.strip()

    #Assunto: A informação sobre o assunto está na classe class="lh-1-1 line-clamp__2" com o id="assuntoProcesso"
    assunto = contexto.find(id="assuntoProcesso")
    if assunto:
        response_schema["assunto"] = assunto.text.strip()

    #Juiz: A informação sobre o juiz está na classe class="line-clamp__2" com o id="juizProcesso"
    juiz = contexto.find(id="juizProcesso")
    if juiz:
        response_schema["juiz"] = juiz.text.strip()

    #Data da distribuição: essa informação está na classe class="col-lg-3 mb-2" na div com id="dataHoraDistribuicaoProcesso"
    data_de_distribuicao = contexto.find(id="dataHoraDistribuicaoProcesso")
    if data_de_distribuicao:
        data_de_distribuicao = data_de_distribuicao.text.split(" ")[0]
        response_schema["data_de_distribuicao"] = data_de_distribuicao

    #Área: essa informação está na classe class="col-lg-2 col-xl-2 mb-2" na div com id="areaProcesso"
    area = contexto.find(id="areaProcesso")
    if area:
        response_schema["area"] = area.text.strip()

    #Valor da ação: essa informação está na classe class="col-lg-2 mb-2" na div com id="valorAcaoProcesso"
    valor_da_acao = contexto.find(id="valorAcaoProcesso")
    if valor_da_acao:
        #Manipulação da string para obter o valor desejado. Ex: R$         281.178,42 para 281178.42
        valor_da_acao = valor_da_acao.text.split(" ")[-1]
        valor_da_acao = valor_da_acao.replace(".", "")
        valor_da_acao = valor_da_acao.replace(",", ".")
        response_schema["valor_da_acao"] = float(valor_da_acao)
    
    #Partes do processo: essa informação está em uma tabela com id="tableTodasPartes"
    partes_do_processo = contexto.find(id="tableTodasPartes")
    if partes_do_processo == None:
        #Em casos de não ter o campo todas as partes. Existem alguns processos não possuem
        partes_do_processo = contexto.find(id="tablePartesPrincipais")
    if partes_do_processo: 
        #Cada elemento da tabela está dentro de um elementp tr com a classe de nome fundoClaro
        partes_do_processo = partes_do_processo.select(".fundoClaro")
        for parte in partes_do_processo:
            #A informação contendo o papel está em um span com classe de nome class="mensagemExibindo tipoDeParticipacao"
            papel = parte.find(class_="mensagemExibindo tipoDeParticipacao")
            papel = papel.text.strip() if papel else "null"
            papel = papel.replace(":","") if papel else "null"

            #As informações sobre clientes e advogados estão na classe class_="nomeParteEAdvogado". Como a formatação está bagunçada farei algumas manipulações na string para obter as informações desejadas
            parte_e_advogados = parte.find(class_="nomeParteEAdvogado")
            #Limpeza dos dados
            parte_e_advogados = parte_e_advogados.text.replace("\t", "").split("\n")
            parte_e_advogados = [pessoa.strip() for pessoa in parte_e_advogados if pessoa.strip() and pessoa.strip() != "\xa0"]
            tamanho = len(parte_e_advogados)                                                      
            #O site colocou textos intermedários na resposta, após uma análise percebi que as informações que eu buscava estavam nas posições pares da lista (0 indexado).
            parte_e_advogados = [pessoa for (pessoa, i) in zip(parte_e_advogados, range(tamanho)) if i%2 == 0]
            nome = parte_e_advogados[0] #Elemento da posição 0 é o cliente, o restante serão os advogados
            tamanho = len(parte_e_advogados)
            if tamanho > 1:
                #adição ao JSON
                response_schema = add_partes_do_processo(response_schema, nome, papel, parte_e_advogados[1:])
            if tamanho == 1:
                response_schema = add_partes_do_processo(response_schema, nome, papel, False)
    

    #No caso das Movimentações vamos separar por instancias, pois há divergencia na nomeação das tags
    if instancia == 1:
        #Lista das movimentações: essa informação está na tabela com id="tabelaTodasMovimentacoes"
        idTable = "tabelaTodasMovimentacoes"
        #Cada movimentação está em uma classe que termina com "containerMovimentacao"
        containerMovimentacao = ".containerMovimentacao"
        #A data da movimentação está disponível no td de classe dataMovimentacao
        dataMovimentacao = "dataMovimentacao"
        #A descrição da movimentação está disponível no td de classe com nome descricaoMovimentacao
        descricaoMovimentacao = "descricaoMovimentacao"
    else:
        #Lista das movimentações: essa informação está na tabela com id="tabelaTodasMovimentacoes"
        idTable = "tabelaTodasMovimentacoes"
        #Cada movimentação está em uma classe que termina com "movimentacaoProcesso"
        containerMovimentacao = ".movimentacaoProcesso"
        #A data da movimentação está disponível no td de classe dataMovimentacaoProcesso
        dataMovimentacao = "dataMovimentacaoProcesso"
        #A descrição da movimentação está disponível no td de classe com nome descricaoMovimentacaoProcesso
        descricaoMovimentacao = "descricaoMovimentacaoProcesso"
    
    lista_das_movimentacoes = contexto.find(id=idTable)
    if lista_das_movimentacoes:
        #Cada movimentação está em uma classe ontainerMovimentacao
        lista_das_movimentacoes = lista_das_movimentacoes.select(containerMovimentacao)
        for movimentacao in lista_das_movimentacoes:
            #A data da movimentação está disponível no td de classe dataMovimentacao
            data = movimentacao.find(class_=dataMovimentacao).text.strip()
            #A descrição da movimentação está disponível no td de classe  descricaoMovimentacao
            descricao = movimentacao.find(class_=descricaoMovimentacao).text.strip()
            #Limpeza das strings
            descricao = "\n".join([desc.strip() for desc in descricao.replace("\t", "").split("\n") if desc.strip() and desc.strip() != "\xa0"])
            #adição ao JSON
            response_schema = add_lista_das_movimentacoes(response_schema, data, descricao)

    #print(json.dumps(response_schema, ensure_ascii=False, indent=2))
    #Validação do Schema
    
    response_schema = validadeSchemaObject(response_schema)
    if not response_schema:
        return False
    else:
        response_schema = normalize_json(response_schema)
        return response_schema


def multiplicidadeProcesso(ctx):
    contexto = BeautifulSoup(ctx.content, 'html.parser')
    codigo_processo = contexto.find(id="processoSelecionado")
    if codigo_processo:
        return codigo_processo["value"].strip()
    else:
        return False