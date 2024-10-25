import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..')) 

from indexer.typings.index import Index
import pytest
import json
from elasticsearch import Elasticsearch
import logging

def search_by_id(id):
    """ Busca o documento pelo id. """
    try:
        conn = Elasticsearch(request_timeout=6000, hosts="http://elasticsearch:9200")
        response = conn.get(index="lawsuits", id=id)
        return response
    except Exception as e:
        logging.info(f"Erro ao realizar a consulta: {e}")
    
    return None

def load_test_message(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_response(response):
    """ Remove campos automáticos da response do elasticsearch"""

    return response["_source"]

def test_index_integration():
    """ Insere um documento e depois busca por ele. """

    message = load_test_message("tests/integration-tests/data/test_message.json")
    resp = load_test_message("tests/integration-tests/data/test_response.json")

    indice = Index()
    indice.insert_documents(message)

    assert resp == filter_response(search_by_id(message[0][0]).body), "A resposta do Elasticsearch não corresponde à esperada."    
