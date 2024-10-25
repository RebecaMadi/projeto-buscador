from coletasapi.middlewares import pagina_processo_parser
import json
import sys
sys.path.append('..')

class Processo:
    def __init__(self, numero_processo, tribunal, instancia, html):
      self.numero_processo = numero_processo
      self.tribunal = tribunal
      self.instancia =  instancia
      self.html = html

class Html:
    def __init__(self, content):
        self.content = content

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
    

def test_crawler():
    """Testa o parser do crawler"""
    with open("./tests/test_html.txt", 'r', encoding='utf-8') as file:
        html = Html(file.read())
    numero_processo = "0710802-55.2018.8.02.0001"
    tribunal = "TJAL"
    instancia = 1
    crawler_data = Processo(numero_processo, tribunal, instancia, html)
    response = pagina_processo_parser(crawler_data.html, crawler_data.numero_processo, crawler_data.tribunal, crawler_data.instancia)

    with open("./tests/response_crawler.json", 'r', encoding='utf-8') as file:
        expected = json.load(file)
    expected = normalize_json(expected)
    response = normalize_json(response)
    assert expected == response

test_crawler()
