from searcher.utils.utils import find_lawsuit_number
from searcher.typings.query_handler import QueryHandler
import logging

logging.basicConfig(level=logging.INFO)

def query_intention(query):
    number = find_lawsuit_number(query["query"])

    handler = QueryHandler(query)

    if number == query["query"]:
        logging.info("Consulta por CNJ.")
        return handler.number_query(query)

    logging.info("Consulta textual.")
    return handler.text_query(query)