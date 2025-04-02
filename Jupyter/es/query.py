from typing import Optional, List, Dict, Any

type Json = Dict[str,Any]
type Extra = Optional[Json]

def Bool(filter: List[Json] = [], must: List[Json] = [], should: List[Json] = [], must_not: List[Json] = []) -> Json:
    return {
        "bool": {
            "filter": filter,
            "must": must,
            "should": should,
            "must_not": must_not,
        }
    }

def Term(field: str, value: Any, extra: Extra = None) -> Json:
    term = { field: value }

    if extra:
        for key in extra:
            term[key] = extra[key]

    return { "term": term }

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