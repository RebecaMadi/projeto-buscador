import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..')) 

from searcher.typings.query_handler import QueryHandler
from searcher.utils.utils import format_response

import pytest
from fastapi.responses import JSONResponse
import json

@pytest.fixture
def query_handler():
    query = {
        "query": "Processo número 12345-67.2021.8.01.0001",
        "limit": 5,
        "offset": 10,
        "filters": {
            "court": "TJAL",
            "date": {"operator": ">", "date": "2023-01-01"}
        }
    }
    return QueryHandler(query)

def test_get_size(query_handler):
    assert query_handler.elasticsearch_query_dsl["size"] == 5, "Erro no método get_size."

def test_get_from(query_handler):
    assert query_handler.elasticsearch_query_dsl["from"] == 10, "Erro no método get_from."

def test_text_query(query_handler):
    query = {
        "query": "Processo número 12345-67.2021.8.01.0001",
        "limit": 5,
        "offset": 10,
        "filters": {
            "court": "TJAL",
            "date": {"operator": ">", "date": "2023-01-01"}
        }
    }
    elasticsearch_query_dsl, _ = query_handler.text_query(query)
    
    date_expected_output = {
        "range": {
            "date": {
                "gt": "2023-01-01"
            }
        }
    }

    query_expected_output = [{
        "query_string": {
            "query": "Processo número ",
            "analyzer": "default",
            "fields": ["subject", "judge", "related_people.name", "related_people.role", "lawyers.name", "nature", "kind.text"],
            "default_operator": "AND"
        }
    }]

    number_expected_output = {"term": {"number": "12345-67.2021.8.01.0001"}}
    assert "filter" in elasticsearch_query_dsl["query"]["bool"], "Erro no método text_query (filtros)."
    assert elasticsearch_query_dsl["query"]["bool"]["must"], "Erro no método text_query (consulta principal)."
    assert elasticsearch_query_dsl["query"]["bool"]["filter"][0] == {"term": {"court": "TJAL"}}, "Erro no método add_court_filter."
    assert elasticsearch_query_dsl["query"]["bool"]["filter"][1] == date_expected_output, "Erro no método add_date_filter."
    assert elasticsearch_query_dsl["query"]["bool"]["must"] == query_expected_output, "Erro no método add_query."
    assert elasticsearch_query_dsl["query"]["bool"]["filter"][2] == number_expected_output, "Erro no método add_number_filter."


def test_number_query():
    query = {
        "query": "12345-67.2021.8.01.0001",
        "filters": {"court": "TJAL"}
    }
    q = QueryHandler(query)
    elasticsearch_query_dsl, _ = q.number_query(query)

    assert elasticsearch_query_dsl["query"]["bool"]["filter"][0]["term"]["number"] == "12345-67.2021.8.01.0001", "Erro no método number_query."

def test_format_response():
    objects = {
        "hits": {
            "total": {"value": 1},
            "hits": [
                {
                    "_id": "1",
                    "_source": {
                        "number": "001",
                        "court": "Tribunal ICOMP",
                        "nature": "Civil",
                        "kind": "Ação",
                        "subject": "Duagrama de Classes",
                        "date": "2023-01-01",
                        "judge": "Tayana Conte",
                        "related_people": [{"name": "Rebeca Madi Oliveira",
                                            "role": "Ré"}],
                        "lawyers": [{"name": "Matheus Oliveira"}],
                        "activities": [{"date": "2022-12-31", "description": "prova 1 de aps"}]
                    },
                    "highlight": {}
                }
            ]
        }
    }
    
    response = format_response(objects)
    
    assert isinstance(response, JSONResponse), "A resposta deve ser um JSONResponse."
    assert response.status_code == 200, "O código de status deve ser 200."

    response_data = json.loads(response.body.decode('utf-8'))

    assert response_data["hits"] == 1, "O número total de hits deve ser 1."
    assert len(response_data["lawsuits"]) == 1, "Deve haver um processo retornado."
    assert response_data["lawsuits"][0]["number"] == "001", "O número do processo deve ser '001'."
    assert response_data["lawsuits"][0]["court"] == "Tribunal ICOMP", "O tribunal deve ser 'Tribunal ICOMP'."
    assert response_data["lawsuits"][0]["nature"] == "Civil", "A natureza do processo deve ser 'Civil'."
    assert response_data["lawsuits"][0]["kind"] == "Ação", "O tipo do processo deve ser 'Ação'."
    assert response_data["lawsuits"][0]["subject"] == "Duagrama de Classes", "O assunto deve ser 'Duagrama de Classes'."
    assert response_data["lawsuits"][0]["judge"] == "Tayana Conte", "O juiz deve ser 'Tayana Conte'."
    assert response_data["lawsuits"][0]["related_people"][0]["name"] == "Rebeca Madi Oliveira", "A pessoa relacionada deve ser 'Rebeca Madi Oliveira'."
    assert response_data["lawsuits"][0]["lawyers"][0]["name"] == "Matheus Oliveira", "O advogado deve ser 'Matheus Oliveira'."
