from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from ...es.request_body import RequestBody, convert_es_to_python_dateformat
from ...es.aggs import Filters, DateHistogram, Terms, Min, Max
from ...es.query import Term, Bool

### These functions count the number of different types of documents
### and bins them by time.

filters = Filters({
    #"count_traces": Term("operationName", "process_digitiser_trace_message").build(),
    "count_digitiser_eventlists": Term("operationName", "process_digitiser_event_list_message").build(),
    "count_frame_eventlists": Term("operationName", "process_frame_assembled_event_list_message").build(),
    "count_Frames": Term("operationName", "Frame").build(),
    "count_incomplete_Frames": Bool()
        .with_must(Term("operationName", "Frame").build())
        .with_must(Term("tag.frame_is_expired", "true").build())
        .build(),
    "count_discarded_digitiser_eventlists": Bool()
        .with_must(Term("operationName", "process_digitiser_event_list_message").build())
        .with_must(Term("tag.is_discarded", "true").build())
        .build(),
}).build()

### Data Gathering

class PipelineMessageTimeHistograms:
    def __init__(self):
        self.time : List[datetime] = []
        #self.num_digitiser_traces : List[int] = []
        self.num_digitiser_eventlists : List[int] = []

        self.num_frame_eventlists : List[int] = []
        self.num_frames : List[int] = []

        self.num_incomplete_frames : List[int] = []
        self.num_discarded_digitiser_eventlists : List[int] = []
        
    def execute_histogram_query(self, client, index: str, req_body: RequestBody, hist_freq: str, format: str):
        req_body.with_aggregation("hist",
            DateHistogram("startTimeMillis", hist_freq, format)
                .with_aggregation("by_op_name", filters)
                .build()
        )

        results = client.search(index=index, body=req_body.build())

        for bucket in results.raw["aggregations"]["hist"]["buckets"]:
            self.time.append(datetime.fromtimestamp(bucket["key"]/1_000))

            filter_buckets = bucket["by_op_name"]["buckets"]
            #self.num_digitiser_traces.append(filter_buckets["count_traces"]["doc_count"])
            self.num_digitiser_eventlists.append(filter_buckets["count_digitiser_eventlists"]["doc_count"])
            self.num_frame_eventlists.append(filter_buckets["count_frame_eventlists"]["doc_count"])
            self.num_frames.append(filter_buckets["count_Frames"]["doc_count"])
            self.num_incomplete_frames.append(filter_buckets["count_incomplete_Frames"]["doc_count"])
            self.num_discarded_digitiser_eventlists.append(filter_buckets["count_discarded_digitiser_eventlists"]["doc_count"])


