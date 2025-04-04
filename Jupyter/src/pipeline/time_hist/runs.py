from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from ...es.request_body import RequestBody, convert_es_to_python_dateformat
from ...es.aggs import Filters, DateHistogram, Terms, Min, Max
from ...es.query import Term, Bool


def get_runs(client, index: str, req_body: RequestBody):
    req_body \
        .with_service_and_op_name("nexus-writer", "Run") \
        .with_fields(["startTime", "duration", "spanID", "tag.run_name", "tag.instrument_name", "tag.run_has_run_stop"]) \
        .with_size(10000)
    
    result = client.search(index=index, body=req_body.build())

    return [hit["fields"] for hit in result.raw["hits"]["hits"]]


class PipelineRuns:
    def __init__(self):
        self.run_start : List[int] = []
        self.run_size : List[int] = []
        self.run_duration : List[int] = []
        pass
    
    def get_frame_children_by_run(self, client, index: str, req_body: RequestBody):
        runs = Terms("parentSpanID", 10000) \
            .with_aggregation("min_time", Min("startTimeMillis").build()) \
            .with_aggregation("max_time", Max("startTimeMillis").build()) \
            .build()
        req_body \
            .with_service_and_op_name("nexus-writer", "Frame Event List") \
            .with_aggregation("by_run", runs)
        
        result = client.search(index=index, body=req_body.build())
        
        buckets = result.raw["aggregations"]["by_run"]["buckets"]
        for bucket in buckets:
            min_time = bucket["min_time"]["value"]
            max_time = bucket["max_time"]["value"]
            self.run_start.append(min_time)
            self.run_size.append(bucket["doc_count"])
            self.run_duration.append(max_time - min_time)