from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from ...es.request_body import RequestBody, convert_es_to_python_dateformat
from ...es.aggs import Filters, DateHistogram, Terms, Cardinality
from ...es.query import Term, Bool

### These functions count the number of different types of documents
### and bins them by time.

### Data Gathering

class PipelineDigitisersTimeHistograms:
    def __init__(self, expected_digitisers: List[int]):
        self.expected_digitisers = expected_digitisers
        self.time : List[datetime] = []
        self.digitiser_count: Dict[int,List[int]] = {id: [] for id in self.expected_digitisers}
        
    def execute_histogram_query(self, client, index: str, req_body: RequestBody, hist_freq: str, format: str):
        req_body.with_aggregation("hist",
            DateHistogram("startTimeMillis", hist_freq, format)
                .with_aggregation("distinct_digitisers", Terms("tag.digitiser_id", 2*len(self.expected_digitisers)).build())
                .build()
        )

        results = client.search(index=index, body=req_body.build())

        num_buckets = len(results.raw["aggregations"]["hist"]["buckets"])
        self.digitiser_count = {id: list(range(num_buckets)) for id in self.expected_digitisers}

        for (idx, bucket) in enumerate(results.raw["aggregations"]["hist"]["buckets"]):
            self.time.append(datetime.fromtimestamp(bucket["key"]/1_000))

            for digitiser_bucket in bucket["distinct_digitisers"]["buckets"]:
                id = int(digitiser_bucket["key"])
                if id not in self.expected_digitisers:
                    raise Exception(f"Digitiser id {id} is not one of the expected ids: {self.expected_digitisers}")
                self.digitiser_count[id][idx] = digitiser_bucket["doc_count"]

