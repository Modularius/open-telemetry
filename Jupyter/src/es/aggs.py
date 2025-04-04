from typing import Optional, List, Dict, Any, Tuple
from .lib import Json, Extra

class AggBuilder:
    def __init__(self, name: str, json: Json, _allow_aggs: bool = True):
        self._allow_aggs = _allow_aggs
        self.name = name
        self.json = json
        self.aggregations = dict()
    
    def with_aggregation(self, name: str, json: Json) -> 'AggBuilder':
        if self._allow_aggs:
            self.aggregations[name] = json
        else:
            raise Exception(f"Aggregations not allowed for {self.name}")

        return self

    def with_extra(self, name: str, json: Json) -> 'AggBuilder':
        self.json[name] = json
        return self

    def build(self) -> Json:
        json = { self.name: self.json }
        if self.aggregations != dict():
            json["aggregations"] = self.aggregations
        return json

def Min(field: str) -> AggBuilder:
    json = { "field": field }
    
    return AggBuilder("min", json, False)

def Max(field: str) -> AggBuilder:
    json = { "field": field }
    
    return AggBuilder("max", json, False)

def BucketScript(buckets_path: Json, script: str) -> AggBuilder:
    bucket_script = { "buckets_path": buckets_path, "script": script }
    
    return AggBuilder("bucket_script", bucket_script)

def Terms(field: str, size: Optional[int] = None) -> AggBuilder:
    terms = { "field": field, "size": size }
    
    if size:
        terms["size"] = size

    return AggBuilder("terms", terms)

def DateHistogram(field: str, fixed_interval:str = "1h", format: Optional[str] = None) -> AggBuilder:
    date_hist = { "field": field, "fixed_interval": fixed_interval }
    if format:
        date_hist["format"] = format

    return AggBuilder("date_histogram", date_hist)

def Histogram(field: str, interval:int, hard_bounds: Optional[Tuple[int,int]] = None) -> AggBuilder:
    json = { "field": field, "interval": interval }
    if hard_bounds:
        json["hard_bounds"] = { "min": hard_bounds[0], "max": hard_bounds[1] }

    return AggBuilder("histogram", json)

def MovingFunction(field: str, window: int, function: str) -> AggBuilder:
    moving_function = { "buckets_path": field, "window": window, "script": f"{function}(values)" }

    return AggBuilder("moving_function", moving_function)

def Filters(filters : Json) -> AggBuilder:
    filters = { "filters": filters }
            
    return AggBuilder("filters", filters)
