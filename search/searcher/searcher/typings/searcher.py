from elasticsearch import Elasticsearch, helpers
from searcher.utils.utils import format_response
import logging

logging.basicConfig(level=logging.INFO)

class Searcher:

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = Elasticsearch(request_timeout=6000, hosts="http://elasticsearch:9200")
        except Exception as e:
            logging.info(f"Erro ao conectar com elasticsearch: {e}")

    def search_by_CNJ(self, query):
        try:
            logging.info(query)
            response = self.conn.search(index="lawsuits", body={**query})
        except Exception as e:
            logging.info(f"Erro ao realizar a consulta: {e}")

        if not response["_shards"]["successful"]:
            return []
        
        return format_response(response)

    def search_by_text(self, query):
        try:
            logging.info(query)
            response = self.conn.search(index="lawsuits", body={
                **query,
                "highlight": {
                    "number_of_fragments": 1,
                    "order": "score",
                    "pre_tags": ["<b>"],
                    "post_tags": ["</b>"],
                    "fields": {
                        "subject": {},
                        "judge": {},
                        "related_people.name": {},
                        "lawyers.name": {},
                        "nature": {},
                        "kind": {}
                    }
                }
            })
        except Exception as e:
            logging.info(f"Erro ao realizar a consulta: {e}")

        if not response["_shards"]["successful"]:
            return []
        
        return format_response(response)