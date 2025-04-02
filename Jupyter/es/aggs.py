from typing import Optional, List, Dict, Any

type Json = Dict[str,Any]
type Extra = Optional[Dict[str,Any]]

def Terms(field: str, size: Optional[int] = None, extra: Extra = None) -> Json:
    terms = { "field": field, "size": size }
    
    if size:
        terms["size"] = size

    if extra:
        for key in extra:
            terms[key] = extra[key]
            
    return { "terms" : terms }

def DateHistogram(field: str, fixed_interval:str = "1h", format: Optional[str] = None, extra: Extra = None) -> Json:
    date_hist = { "field": field, "fixed_interval": fixed_interval }
    if format:
        date_hist["format"] = format

    if extra:
        for key in extra:
            date_hist[key] = extra[key]

    return { "date_histogram": date_hist }

def MovingFunction(field: str, window: int, function: str, extra: Extra = None) -> Json:
    moving_function = { "buckets_path": field, "window": window, "script": f"{function}(values)" }

    if extra:
        for key in extra:
            moving_function[key] = extra[key]

    return { "moving_function": moving_function }

def Filters(filters : Json, extra: Extra = None) -> Json:
    filters = { "filters": filters }
    
    if extra:
        for key in extra:
            filters[key] = extra[key]
            
    return { "filters" : filters }
