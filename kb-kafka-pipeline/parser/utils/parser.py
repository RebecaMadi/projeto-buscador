import uuid
import json
from datetime import datetime
from .normalizer import Normalizer

class Parser:

    def __init__(self):
        self.normalizer = Normalizer()

    def _data_parser(self, data: dict) -> dict:
        """
        Parser para os dados do processo.
        
        Entrada: dict (dados brutos do lawsuit_raw)
        
        Saída: dict (dados estruturados)
        """
        
        if not data.get('existe', True):
            return None  

        relatedPeople = self._parse_related_people(data['partes_do_processo']) if data['partes_do_processo'] else []
        representedPersonLawyers = self._parse_represented_lawyers(data['partes_do_processo'], relatedPeople) if data['partes_do_processo'] else []
        activities = self._parse_activities(data['lista_das_movimentacoes']) if data['lista_das_movimentacoes'] else []
        
        return {
            'court': self._parse_court(data),
            'nature': data['classe'],
            'kind': data['area'],
            'subject': data['assunto'],
            'distributionDate': self._parse_date(data['data_de_distribuicao']),
            'judgeName': data['juiz'],
            'value': data['valor_da_acao'],
            'justiceSecret': data['segredo_justica'],
            'courtInstance': data['instancia'],
            'number': data['numero_do_processo'],
            'relatedPeople': relatedPeople,
            'representedPersonLawyers': representedPersonLawyers,
            'activities': activities
        }
    
    def _parse_related_people(self, partes_do_processo: list) -> list:
        """
        Realiza a transformação dos dados das partes relacionadas.

        Entrada: lista das partes relacionadas.

        Processamento: normalização dos nomes e criação de ids para as partes.

        Saída: lista de partes relacionadas com a estrutura padrão.
        """

        relatedPeople = []

        for related in partes_do_processo:
            person_id = str(uuid.uuid4())
            relatedPeople.append({
                'id': person_id,
                'nameRaw': related['nome'],
                'name': self.normalizer.nameNormalizer(related['nome']),
                'role': {
                    'rawValue': related['papel'],
                    'normalized': self.normalizer.nameNormalizer(related['papel']),
                },
                'author': self.normalizer.nameNormalizer(related['papel']).lower() in ['autor', 'requerente'],
            })

        return relatedPeople

    def _parse_represented_lawyers(self, partes_do_processo: list, relatedPeople: list) -> list:
        """
        Realiza a transformação dos dados dos advogados das partes relacionadas.

        Entrada: lista dos advogados e lista das partes relacionadas.

        Processamento: normalização dos nomes e relação dos advogados com os ids das partes.

        Saída: lista de partes relacionadas com a estrutura padrão.
        """

        representedPersonLawyers = []
        for related, person in zip(partes_do_processo, relatedPeople):
            token = "advogado(as)"
            if token not in related.keys():
               continue
            for advogado in related[token]:
                representedPersonLawyers.append({
                    'nameRaw': advogado,
                    'name': self.normalizer.nameNormalizer(advogado),
                    'representedPersonId': person['id'],
                })

        return representedPersonLawyers

    def _parse_activities(self, lista_das_movimentacoes: list) -> list:
        """ Estrutura a lista de movimentações. """

        return [
            {'date': self._parse_date(mov['data']), 'text': mov['movimento']}
            for mov in lista_das_movimentacoes
        ]
    
    def _parse_court(self, data: dict) -> dict:
        """ Parser do tribunal. """

        return {'rawValue': data['tribunal']}

    def _parse_date(dself, date_str: str) -> str:
        """Tenta analisar a data em diferentes formatos e retorna o timestamp."""
        if not date_str:
            return None
        date_str = date_str.replace("/", "-")
        for fmt in ('%d-%m-%Y', '%Y-%m-%d'): 
            try:
                return int(datetime.strptime(date_str, fmt).timestamp())
            except ValueError:
                pass
        return None