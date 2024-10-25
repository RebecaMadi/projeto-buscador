from elasticsearch import Elasticsearch, helpers
from indexer.utils.utils import format_documents
import logging

class Index:
    """ Classe para acesso ao elasticsearch. """

    def __init__(self):
        self.host = "http://elasticsearch:9200"
        self.indice = "lawsuits"
        self.connect()

    def connect(self):
        try:
            self.conn = Elasticsearch(request_timeout=6000, hosts=self.host)
        except Exception as e:
            logging.info(f"Erro ao conectar com elasticsearch: {e}")
    
    def create_index(self, settings, mappings):
        if not self.conn.indices.exists(index="lawsuits"):
            try:
                self.conn.indices.create(index=self.indice, settings=settings, mappings=mappings)
            except Exception as e:
                logging.info(f"Erro ao criar o indice: {e}")

    def insert_documents(self, docs):
        try:
            docs = format_documents(docs)
            helpers.bulk(self.conn, docs, chunk_size=1000)
        except Exception as e:
                print(e)
                logging.info(f"Erro ao inserir documentos: {e}")