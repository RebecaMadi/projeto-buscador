class Normalizer:
    """Classe para a normalização de palavras."""

    def __init__(self):
        """Construtor vazio."""
        pass
    
    def nameNormalizer(self, name: str) -> str:
        """
        Normaliza um nome de acordo com o especificado no documento do projeto.
        
        Entrada: str (nome bruto)

        Processamento: retirar titulação.

        Saída: str (nome puro)
        """

        prefixes = ["Dr. ", "Dra. ", "Mr. ", "Mrs. ", "Advogado ", "Advogada "]
    
        for prefix in prefixes:
            name = name.replace(prefix, "").strip()

        normalized_words = [
            word.lower() if word.lower() in ['de', 'do', 'da', 'dos', 'das'] else word.capitalize()
            for word in name.split()
        ]

        return ' '.join(normalized_words)