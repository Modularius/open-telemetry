from datetime import datetime
from typing import Optional, List, Dict, Any
from .query import Term, Range, Bool
from .lib import Json

def convert_es_to_python_dateformat(format: str) -> str:
    return format.replace("MM","%m").replace("dd","%d").replace("hh","%H").replace("mm","%M").replace("ss","%S")

class RequestBody:
    def __init__(self, namespace : str):
        self.namespace : Optional[Json] = Term("process.tag.service@namespace", namespace).build()
        self.service_name : Optional[Json] = None
        self.operation_name : Optional[Json] = None
        self.range : Optional[Json] = None
        self.queries : List[Json] = []
        self.aggregations : Json = dict()
        self.source : Optional[bool|Json] = None
        self.fields : List[str] = []
        self.size : Optional[int] = None

    def with_service_and_op_name(self, service_name: str, operation_name: str) -> "RequestBody":
        self.service_name = Term("process.serviceName", service_name).build()
        self.operation_name = Term("operationName", operation_name).build()
        return self

    def with_range(self, time_from_str: Optional[str], time_to_str: Optional[str]) -> "RequestBody":
        time_from = None
        time_to = None
        if time_from_str:
            time_from = int(datetime.strptime(time_from_str, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()*1000)
        if time_to_str:
            time_to = int(datetime.strptime(time_to_str, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()*1000)
        self.range = Range("startTimeMillis", gte=time_from, lte=time_to)
        return self

    def with_aggregation(self, name: str, aggregation: Json) -> "RequestBody":
        self.aggregations[name] = aggregation
        return self

    def with_query(self, query: Json) -> "RequestBody":
        self.queries.append(query)
        return self

    def with_queries(self, query: List[Json]) -> "RequestBody":
        self.queries.extend(query)
        return self

    def with_source(self, source: bool) -> "RequestBody":
        self.source = source
        return self

    def with_size(self, size: int) -> "RequestBody":
        self.size = size
        return self

    def with_fields(self, fields: List[str]) -> "RequestBody":
        self.fields.extend(fields)
        return self

    def build(self):
        if self.namespace:
            self.queries.append(self.namespace)
        if self.service_name:
            self.queries.append(self.service_name)
        if self.operation_name:
            self.queries.append(self.operation_name)
        if self.range:
            self.queries.append(self.range)
        if self.service_name:
            self.queries.append(self.service_name)
        
        body : Dict[str,Any] = { "query": Bool().with_filters(self.queries).build() }
        if self.aggregations != dict():
            body["aggregations"] = self.aggregations

        if self.size:
            body["size"] = self.size

        if self.source:
            body["_source"] = self.source

        if self.fields:
            body["fields"] = self.fields

        return body