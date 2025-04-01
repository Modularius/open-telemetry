GET /jaeger-span*/_search
{
    "size": 0,
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        "startTimeMillis": {
                            "gte": 1743422400000
                        }
                    }
                },
                {
                    "term": {
                        "process.tag.service@namespace": {
                            "value": "pipeline-musr"
                        }
                    }
                },
                {
                    "term": {
                        "operationName": {
                            "value": "process_digitiser_trace_message"
                        }
                    }
                },
                {
                    "term": {
                        "process.serviceName": {
                            "value": "trace-to-events"
                        }
                    }
                }
            ]
        }
    },
    "aggs": {
        "stats": {
            "extended_stats_bucket": {
                "buckets_path": "timestamp>diff"
            }
        },
        "timestamp": {
            "terms": {
                "field": "tag.metadata_timestamp",
                "size": 100000
            },
            "aggs": {
                "digitisers": {
                    "terms": {
                        "field": "tag.digitiser_id"
                    }
                },
                "size": {
                    "cardinality": {
                        "field": "startTime"
                    }
                },
                "max": {
                    "max": {
                        "field": "startTime"
                    }
                },
                "min": {
                    "min": {
                        "field": "startTime"
                    }
                },
                "diff": {
                    "bucket_script": {
                        "buckets_path": {
                            "min": "min",
                            "max": "max"
                        },
                        "script": "params.max - params.min"
                    }
                }
            }
        }
    }
}