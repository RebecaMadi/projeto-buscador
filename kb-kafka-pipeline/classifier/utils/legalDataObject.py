class LegalDataObject:

    """Classe que representa um caso judicial e fornece métodos para manipulação de dados."""

    def __init__(self, json_data: dict):
        """
        Inicializa a classe LegalDataObject com os dados do caso a partir de um dicionário JSON.

        Entrada: dict (Dicionário contendo os dados do caso judicial).
        """
        self.court = json_data.get('court')
        self.nature = json_data.get('nature')
        self.kind = json_data.get('kind')
        self.subject = json_data.get('subject')
        self.distribution_date = json_data.get('distributionDate')
        self.judge_name = json_data.get('judgeName')
        self.value = json_data.get('value')
        self.justice_secret = json_data.get('justiceSecret')
        self.court_instance = json_data.get('courtInstance')
        self.number = json_data.get('number')
        self.related_people = json_data.get('relatedPeople', [])
        self.represented_person_lawyers = json_data.get('representedPersonLawyers', [])
        self.activities = json_data.get('activities', [])

    def standardData(self, sensitive_kind) -> dict:

        """Organiza os campos na ordem desejada e retorna os dados formatados com o campo de tema sensível."""

        return {
            'court': self.court,
            'nature': self.nature,
            'kind': self.kind,
            'subject': self.subject,
            'sensitiveKind': sensitive_kind,
            'distributionDate': self.distribution_date,
            'judgeName': self.judge_name,
            'value': self.value,
            'justiceSecret': self.justice_secret,
            'courtInstance': self.court_instance,
            'number': self.number,
            'relatedPeople': self.related_people,
            'representedPersonLawyers': self.represented_person_lawyers,
            'activities': self.activities
        }