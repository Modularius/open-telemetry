from datetime import datetime
from typing import Optional, List, Dict, Any
import es
import es.query

#def filter_term(term):
#    return { "filter": { "term": term } }

def filter_term_op_name(op_name):
    return es.query.Term("operationName", op_name)

def filter_bool_must_terms(terms):
    return { "filter": es.query.Bool(must=[{ "term": term } for term in terms]) }

def convert_es_to_python_dateformat(format: str) -> str:
    return format.replace("MM","%m").replace("dd","%d").replace("hh","%H").replace("mm","%M").replace("ss","%S")

def add_range_to(time_from_str: Optional[str], time_to_str: Optional[str], prev: List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    time_from = None
    time_to = None
    if time_from_str:
        time_from = int(datetime.strptime(time_from_str, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()*1000)
    if time_to_str:
        time_to = int(datetime.strptime(time_to_str, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()*1000)

    prev.append(es.query.Range("startTimeMillis", gte=time_from, lte=time_to))
    return prev

class ESQuery:
    def __init__(self, namespace : str):
        self.queries = [ es.query.Term("process.tag.service@namespace", namespace) ]
        pass

    def add_service_and_op_name(self, service_name: str, operation_name: str) -> "ESQuery":
        self.queries.extend([es.query.Term("process.serviceName", service_name), es.query.Term("operationName", operation_name)])
        return self

    def add_range(self, time_from: Optional[str], time_to: Optional[str]) -> "ESQuery":
        self.queries = add_range_to(time_from, time_to, self.queries)
        return self

    def add_query(self, query: Dict[str,Any]) -> "ESQuery":
        self.queries.append(query)
        return self

    def get_queries(self):
        return self.queries
    
    def get_queries_with(self, extras):
        return self.queries + extras