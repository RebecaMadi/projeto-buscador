from searcher.middlewares.query_intention import query_intention
from searcher.typings.searcher import Searcher
from searcher.middlewares.getPostgresLawsuit import get_lawsuit
import logging

def search_controller(query):
    query_dsl = query_intention(query)

    searcher = Searcher()

    if query_dsl[1]:
        return searcher.search_by_text(query_dsl[0])
    else:
        return searcher.search_by_CNJ(query_dsl[0])

def search_postgres_controller(id):
    return get_lawsuit(id)