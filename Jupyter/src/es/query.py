from typing import Optional, List, Dict, Any
from .lib import Json, Extra

class QueryBuilder:
    def __init__(self, name: str, init: Json):
        self.name = name
        self.json = init
    
    def build(self) -> Json:
        return { self.name: self.json }
    
    def with_extra(self, name: str, extra: Json) -> 'QueryBuilder':
        self.json[name] = extra
        return self

class Bool(QueryBuilder):
    def __init__(self):
        QueryBuilder.__init__(self, "bool", {
            "filter": [],
            "must": [],
            "should": [],
            "must_not": []
        })
    
    def with_must(self, json: Json):
        self.json["must"].append(json)
        return self
    
    def with_filter(self, json: Json):
        self.json["filter"].append(json)
        return self
    
    def with_should(self, json: Json):
        self.json["should"].append(json)
        return self
    
    def with_must_not(self, json: Json):
        self.json["must_not"].append(json)
        return self
    
    def with_musts(self, json: List[Json]):
        self.json["must"].extend(json)
        return self
    
    def with_filters(self, json: List[Json]):
        self.json["filter"].extend(json)
        return self
    
    def with_shoulds(self, json: List[Json]):
        self.json["should"].extend(json)
        return self
    
    def with_must_nots(self, json: List[Json]):
        self.json["must_not"].extend(json)
        return self

def Term(field: str, value: Any, extra: Extra = None) -> QueryBuilder:
    return QueryBuilder("term", { field: value })

def Range(field: str, lt: Optional[Any] = None, gt: Optional[Any] = None, lte: Optional[Any] = None, gte: Optional[Any] = None, format: Optional[str] = None, extra: Extra = None) -> Json:
    range = { field: {} }
    if lt:
        range[field]["lt"] = lt
    if gt:
        range[field]["gt"] = gt
    if lte:
        range[field]["lte"] = lte
    if gte:
        range[field]["gte"] = gte
    if format:
        range[field]["format"] = format
    if extra:
        for key in extra:
            range[key] = extra[key]

    return { "range": range }