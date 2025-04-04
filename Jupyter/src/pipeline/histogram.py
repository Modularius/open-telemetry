from typing import Optional, Tuple, List, Dict, Any
import frame.frame_assembler as fa
import frame.frame as fr
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.dates as mdate
import numpy as np
from es.request_body import RequestBody
from es.aggs import Terms, Min, Max, BucketScript, Histogram

### Data Gathering
def get_durations(client, index: str, req_body: RequestBody, buckets: int, min: int, max: int) -> List[Dict[str,Any]]:
    req_body.with_aggregation("hist", Histogram("duration", int((max - min)/buckets), (min, max)).build())
    
    result = client.search(index=index, body=req_body.build())
    return result.raw["aggregations"]["hist"]["buckets"]

### Data Gathering
def get_min_max_time_by_metadata_timestamp(client, index: str, req_body: RequestBody) -> List[Dict[str,Any]]:

    diff_agg = BucketScript({ "min": "min_time", "max": "max_time" }, "params.max - params.min")

    req_body.with_aggregation("by_metadata_timestamp",
        Terms("tag.metadata_timestamp", 100_000)
            .with_aggregation("min_time", Min("startTime").build())
            .with_aggregation("max_time", Max("startTime").build())
            .with_aggregation("range_of_times", diff_agg.build())
            .build()
    )
    result = client.search(index=index, body=req_body.build())
    res = result.raw["aggregations"]["by_metadata_timestamp"]["buckets"]
    return res


### Data Processing

def process_min_max_range(result) -> Tuple[List[int],List[int]]:
    timestamps_ns = [bucket["key"] for bucket in result]
    buckets = [bucket["range_of_times"]["value"] for bucket in result]
    return (timestamps_ns,buckets)

### Data Display

def convert_es_to_python_dateformat(format: str) -> str:
    return format.replace("MM","%m").replace("dd","%d").replace("hh","%H").replace("mm","%M").replace("ss","%S")

def histograms(collection_of_buckets : List[Tuple[str, List[int],List[int]]], logy = False, height: int = 4):
    plt.rcParams["figure.figsize"] = (10,height)
    _, ax = plt.subplots(len(collection_of_buckets),1, layout='constrained', sharex=True)
    for idx, (title, buckets, weights_num_buckets) in enumerate(collection_of_buckets):
        ax[idx].set_ylabel("Count")
        ax[idx].set_title(f"Message Duration Distribution: {title}")
        if len(weights_num_buckets) == 1:
            ax[idx].hist(buckets, bins=weights_num_buckets[0], log = logy)
        else:
            ax[idx].hist(buckets, bins=buckets, weights = weights_num_buckets, log = logy)
    ax[-1].set_xlabel("Duration (us)")