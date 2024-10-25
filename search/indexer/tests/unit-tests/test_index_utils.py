import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..')) 

from indexer.utils.utils import convert_date, get_lawyers, get_related_people, get_activities, format_documents
import pytest

def test_convert_date():
    timestamp = 1672531199 
    expected_output = "2022-12-31"

    assert convert_date(timestamp) == expected_output, "Erro na conversão de data."

def test_get_lawyers():
    lines = [
            {
        "name": "Rebeca Madi Oliveira",
        "nameRaw": "Tayana Conte",
        "representedPersonId": "fa9eaad5-b219-4091-b445-e2374340b6a2"
        },
        {
        "name": "Tayana Conte",
        "nameRaw": "Tayana Conte",
        "representedPersonId": "fa9eaad5-b219-4091-b445-e2374340b6a2"
        },
    ]

    expected_output = [
        {"name": "Rebeca Madi Oliveira"},
        {"name": "Tayana Conte"},
    ]

    assert get_lawyers("name", lines) == expected_output, "Erro ao retornar advogados."

def test_get_related_people():
    lines = [
        {"name": "Rebeca Madi Oliveira", "role": {"rawValue": "Requerente"}},
        {"name": "Tayana Conte", "role": {"rawValue": "Requerido"}},
    ]

    expected_output = [
        {"name": "Rebeca Madi Oliveira", "role": "Requerente"},
        {"name": "Tayana Conte", "role": "Requerido"},
    ]

    assert get_related_people(lines) == expected_output

def test_get_activities():
    lines = [
        {"date": 1672531199, "text": "prova 1 de aps"},
        {"date": 1672617599, "text": "prova 2 de aps"},
    ]

    expected_output = [
        {"date": "2022-12-31", "description": "prova 1 de aps"},
        {"date": "2023-01-01", "description": "prova 2 de aps"},
    ]

    assert get_activities(lines) == expected_output

def test_format_documents():
    docs = [
        ("1", {
            "number": "001",
            "justiceSecret": False,
            "distributionDate": 1672531199,
            "court": {"rawValue": "Tribunal ICOMP"},
            "judgeName": "Leandro Galvão",
            "kind": "sensível",
            "representedPersonLawyers": [{"name": "Rebeca Madi Oliveira"}],
            "nature": "Amazonica",
            "relatedPeople": [{"name": "Tayana Conte", "role": {"rawValue": "Requerente"}}],
            "subject": "Arquitetura C4",
            "value": 1000,
            "activities": [{"date": 1672531199, "text": "prova 1 de aps"}]
        }),
    ]

    expected_output = [
        {
            "_op_type": "index",
            "_index": "lawsuits",
            "_id": "1",
            "number": "001",
            "date": "2022-12-31",  
            "court": "Tribunal ICOMP", 
            "judge": "Leandro Galvão", 
            "kind": "sensível", 
            "lawyers": [{"name": "Rebeca Madi Oliveira"}],
            "nature": "Amazonica", 
            "related_people": [{"name": "Tayana Conte", "role": "Requerente"}],
            "subject": "Arquitetura C4", 
            "value": 1000,
            "activities": [{"date": "2022-12-31", "description": "prova 1 de aps"}],
        }
    ]

    assert format_documents(docs) == expected_output, "Erro na formatação dos documentos."
    
    docs = [
        ("2", {
            "number": "002",
            "justiceSecret": True,
            "distributionDate": 1672531199,
            "court": {"rawValue": "Tribunal ICOMP"},
            "judgeName": "Leandro Galvão",
            "kind": "sensível",
            "representedPersonLawyers": [{"name": "Rebeca Madi Oliveira"}],
            "nature": "Amazonica",
            "relatedPeople": [{"name": "Tayana Conte", "role": {"rawValue": "Requerente"}}],
            "subject": "Arquitetura C4",
            "value": 1000,
            "activities": [{"date": 1672531199, "text": "prova 2 de aps"}]
        }),
        ]

    assert format_documents(docs) == [], "Erro na formatação dos documentos."