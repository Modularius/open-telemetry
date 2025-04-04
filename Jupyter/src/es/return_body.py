from datetime import datetime
from typing import Optional, List, Dict, Any
from .query import Term, Range
from .lib import Json

class ResponseBody:
    def __init__(self, raw: Json):
        self.hits = raw.get("hits")
        self.fields = raw.get("fields")

class ResponseAggs:
    def __init__(self, raw: Json, names: List[str]):
        self.buckets = raw["buckets"]
        self.fields = raw.get("fields")
