import re

class SensitiveDataIdentifier:
    def __init__(self):
        self.sensitive_themes = {
            "MENOR_INFRATOR": [
                r"\bmenor infrator\b", 
                r"\bexploração do trabalho infantil\b",
                r"\bdireito da criança e do adolescente ato infracional\b"
            ],
            "VIOLENCIA_DOMESTICA": [
                r"\bdecorrente de violência doméstica\b", 
                r"\bviolência doméstica contra a mulher\b",
                r"\blesão corporal decorrente de violência doméstica\b"
            ],
            "CRIME_ODIO": [
                r"\bfeminicídio\b", 
                r"\bxenofobia\b", 
                r"\bracismo\b"
            ]
        }

    def identify_sensitive_data(self, data: dict) -> str:
        """Identifica as expressões sensíveis dentro do assunto do documento."""
        if data["subject"] ==None:
            return None
        subject = data.get('subject', '').lower()
        
        for key, themes in self.sensitive_themes.items():
            for theme in themes:
                if re.search(theme, subject):
                    return key
        
        return None