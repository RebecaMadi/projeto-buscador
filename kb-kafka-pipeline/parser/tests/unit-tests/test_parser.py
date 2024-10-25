import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..')) 

import json
import pytest
from utils.parser import Parser
from datetime import datetime

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def id_not_random(result: dict) -> dict:
    """Muda os ids para um padrão, apenas para o teste."""

    people = result["relatedPeople"]
    for i in range(len(people)):
        people[i]["id"] = "123456789"
    result["relatedPeople"] = people

    lawyers = result["representedPersonLawyers"]
    for i in range(len(lawyers)):
        lawyers[i]["representedPersonId"] = "123456789"
    result["representedPersonLawyers"] = lawyers

    return result

input_data = load_json_file('tests/unit-tests/input.json')

expected_output = load_json_file('tests/unit-tests/output.json')

parser = Parser()

result = parser._data_parser(input_data)

result = id_not_random(result)

def test_court():
    assert result['court'] == expected_output['court'], "Campo 'court' está incorreto"

def test_nature():
    assert result['nature'] == expected_output['nature'], "Campo 'nature' está incorreto"

def test_kind():
    assert result['kind'] == expected_output['kind'], "Campo 'kind' está incorreto"

def test_subject():
    assert result['subject'] == expected_output['subject'], "Campo 'subject' está incorreto"

def test_distributionDate():
    assert result['distributionDate'] == expected_output['distributionDate'], "Campo 'distributionDate' está incorreto"

def test_judgeName():
    assert result['judgeName'] == expected_output['judgeName'], "Campo 'judgeName' está incorreto"

def test_value():
    assert result['value'] == expected_output['value'], "Campo 'value' está incorreto"

def test_justiceSecret():
    assert result['justiceSecret'] == expected_output['justiceSecret'], "Campo 'justiceSecret' está incorreto"

def test_courtInstance():
    assert result['courtInstance'] == expected_output['courtInstance'], "Campo 'courtInstance' está incorreto"

def test_number():
    assert result['number'] == expected_output['number'], "Campo 'number' está incorreto"

def test_relatedPeople():
    assert result['relatedPeople'] == expected_output['relatedPeople'], "Campo 'relatedPeople' está incorreto"

def test_representedPersonLawyers():
    assert result['representedPersonLawyers'] == expected_output['representedPersonLawyers'], "Campo 'representedPersonLawyers' está incorreto"

def test_activities():
    assert result['activities'] == expected_output['activities'], "Campo 'activities' está incorreto"

def test_data_parser():
    assert result == expected_output, "O resultado geral está incorreto"