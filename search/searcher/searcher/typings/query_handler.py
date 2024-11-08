from searcher.utils.utils import find_lawsuit_number
import re

class QueryHandler:

    def __init__(self, query):
        self.elasticsearch_query_dsl = {}
        self.elasticsearch_query_dsl["query"] = {"bool": {}}
        self.set_size(query)
        self.set_from(query)
    
    def set_size(self, query):
        self.elasticsearch_query_dsl["size"] = query.get("limit", 10) 
    
    def set_from(self, query):
        self.elasticsearch_query_dsl["from"] = query.get("offset", 0)
    
    def add_query(self, query):
        self.elasticsearch_query_dsl["query"]["bool"]["must"] = [{
            "query_string": {
                "query": query["query"],
                "analyzer": "default",
                "fields": ["subject", "judge", "related_people.name", "related_people.role", "lawyers.name", "nature", "kind.text"],
                "default_operator": "AND"
            }
        }]

    def add_number_filter(self, cnj):
        self.elasticsearch_query_dsl["query"]["bool"]["filter"].append({"term": {"number": cnj}})

    def add_court_filter(self, query):
        if query["filters"].get("court"):
            self.elasticsearch_query_dsl["query"]["bool"]["filter"].append({ "term": { 
                "court": query["filters"]["court"] 
                }})

    def add_date_filter(self, query):
        date = query["filters"].get("date")
        if date:
            operator_map = { ">": "gt","=": "gte","<": "lt"}
            elastic_operator = operator_map.get(date["operator"])
            date_filter = date["date"]
            self.elasticsearch_query_dsl["query"]["bool"]["filter"].append({
                "range": {
                    "date": {
                        elastic_operator: date_filter
                    }
                }
            })

    def add_filters(self, query):
        self.add_court_filter(query)
        self.add_date_filter(query)
    
    def text_query(self, query):
        """ Retorna uma EQDSL para uma consulta textual. """

        number = find_lawsuit_number(query["query"])
        if query.get("filters") or number:
            self.elasticsearch_query_dsl["query"]["bool"]["filter"] = []
        if query.get("filters"):
            self.add_filters(query)
        if number:
            query["query"] = re.sub(number, '', query["query"])
            self.add_number_filter(number)
        self.add_query(query)

        return (self.elasticsearch_query_dsl, 1)
    
    def number_query(self, query):
        """ Retorna uma EQDSL para uma consulta por número de processos. """

        self.elasticsearch_query_dsl["query"]["bool"]["filter"] = []
        self.add_number_filter(query["query"])
        if query.get("filters"):
            self.add_filters(query)
        
        return (self.elasticsearch_query_dsl, 0)