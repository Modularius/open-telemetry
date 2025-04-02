from typing import Optional, List, Dict, Any

def TermsAgg(field: str, size:int = 100_000) -> Dict[str,Any]:
    return { "terms": { "field": field, "size": size } }

def DateHistogramAgg(field: str, fixed_interval:str = "1h") -> Dict[str,Any]:
    return { "date_histogram": { "field": field, "fixed_interval": fixed_interval } }

def MovingFunctionAgg(field: str, window: int, function: str) -> Dict[str,Any]:
    return { "date_histogram": { "buckets_path": field, "window": window, "script": f"{function}(values)" } }