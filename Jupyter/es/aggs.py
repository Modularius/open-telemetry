from typing import Optional, List, Dict, Any

def TermsAgg(field: str, size:int = 100_000) -> Dict[str,Any]:
    return { "terms": { "field": field, "size": size } }

def DateHistogramAgg(field: str, fixed_interval:str = "1h", format: Optional[str] = None) -> Dict[str,Any]:
    date_hist = { "field": field, "fixed_interval": fixed_interval }
    if format:
        date_hist["format"] = format
    return { "date_histogram": date_hist }

def MovingFunctionAgg(field: str, window: int, function: str) -> Dict[str,Any]:
    return { "date_histogram": { "buckets_path": field, "window": window, "script": f"{function}(values)" } }