from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional, Dict, Any

class MongoDB:
    def __init__(self, url, db_nome):
        """Inicia a conexão com o MongoDB."""
        self.client = MongoClient(url)
        self.db = self.client[db_nome]
        print(self.client)

    def close(self):
        """Fecha a conexão com o MongoDB."""
        self.client.close()

    def insert_one(self, nome_colecao: str, documento: Dict[str, Any]) -> str:
        """Insere um documento em uma coleção. Retorna o ID do documento inserido."""
        try:
            colecao: Collection = self.db[nome_colecao]
            result = colecao.insert_one(documento)
            return True
        except Exception as e:
            print(f"Erro ao inserir documento: {e}")
            return None
        
    def find_one(self, nome_colecao: str, query: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Encontra um documento em uma coleção."""
        try:
            colecao: Collection = self.db[nome_colecao]
            document = colecao.find_one(query, max_time_ms = 1000)
            return document
        except Exception as e:
            print(f"Erro ao encontrar documento: {e}")
            return None
    
    def update_one(self, nome_colecao: str, filtro: Dict[str, Any], atualizacao: Dict[str, Any]) -> bool:
        """Atualiza um documento em uma coleção. Retorna True se o documento foi atualizado."""
        try:
            colecao: Collection = self.db[nome_colecao]
            result = colecao.update_one(filtro, {"$set": atualizacao})
            if result.matched_count > 0:
                print("Atualizou!")
                return True
            else:
                return False
        except Exception as e:
            print(f"Erro ao atualizar documento: {e}")
            return False