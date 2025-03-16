PUT _index_template/jaeger-span
{
  "priority": 0,
  "template": {
    "settings": {
      "index": {
        "lifecycle": {
          "name": "OTel-Storage"
        },
        "mapping": {
          "nested_fields": {
            "limit": "50"
          }
        },
        "number_of_shards": "1",
        "final_pipeline": "extract-parent-span-id",
        "requests": {
          "cache": {
            "enable": "true"
          }
        },
        "sort": {
          "field": [
            "process.serviceName",
            "process.tag.service@namespace",
            "operationName"
          ],
          "order": [
            "desc",
            "desc",
            "desc"
          ]
        },
        "number_of_replicas": "0"
      }
    },
    "mappings": {
      "dynamic_templates": [
        {
          "span_tags_map": {
            "path_match": "tag.*",
            "mapping": {
              "ignore_above": 256,
              "type": "keyword"
            }
          }
        },
        {
          "process_tags_map": {
            "path_match": "process.tag.*",
            "mapping": {
              "ignore_above": 256,
              "type": "keyword"
            }
          }
        }
      ],
      "properties": {
        "traceID": {
          "ignore_above": 256,
          "type": "keyword"
        },
        "process": {
          "type": "object",
          "properties": {
            "tag": {
              "type": "object",
              "properties": {
                "service@namespace": {
                  "type": "keyword"
                }
              }
            },
            "serviceName": {
              "ignore_above": 256,
              "type": "keyword"
            },
            "tags": {
              "dynamic": false,
              "type": "nested",
              "properties": {
                "type": {
                  "ignore_above": 256,
                  "type": "keyword"
                },
                "value": {
                  "ignore_above": 256,
                  "type": "keyword"
                },
                "key": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              }
            }
          }
        },
        "references": {
          "dynamic": false,
          "type": "nested",
          "properties": {
            "spanID": {
              "ignore_above": 256,
              "type": "keyword"
            },
            "traceID": {
              "ignore_above": 256,
              "type": "keyword"
            },
            "refType": {
              "ignore_above": 256,
              "type": "keyword"
            }
          }
        },
        "startTimeMillis": {
          "format": "epoch_millis",
          "type": "date"
        },
        "flags": {
          "type": "integer"
        },
        "operationName": {
          "ignore_above": 256,
          "type": "keyword"
        },
        "parentSpanID": {
          "ignore_above": 256,
          "type": "keyword"
        },
        "tags": {
          "dynamic": false,
          "type": "nested",
          "properties": {
            "type": {
              "ignore_above": 256,
              "type": "keyword"
            },
            "value": {
              "ignore_above": 256,
              "type": "keyword"
            },
            "key": {
              "ignore_above": 256,
              "type": "keyword"
            }
          }
        },
        "duration": {
          "type": "long"
        },
        "spanID": {
          "ignore_above": 256,
          "type": "keyword"
        },
        "startTime": {
          "type": "long"
        },
        "tag": {
          "type": "object",
          "properties": {
            "metadata_timestamp": {
              "index": true,
              "ignore_malformed": false,
              "store": false,
              "type": "date_nanos",
              "doc_values": true
            },
            "num_cached_frames": {
              "type": "unsigned_long"
            },
            "metadata_frame_number": {
              "type": "unsigned_long"
            }
          }
        },
        "logs": {
          "dynamic": false,
          "type": "nested",
          "properties": {
            "fields": {
              "dynamic": false,
              "type": "nested",
              "properties": {
                "type": {
                  "ignore_above": 256,
                  "type": "keyword"
                },
                "value": {
                  "ignore_above": 256,
                  "type": "keyword"
                },
                "key": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              }
            },
            "timestamp": {
              "type": "long"
            }
          }
        }
      }
    }
  },
  "index_patterns": [
    "jaeger-span-*"
  ],
  "composed_of": [],
  "ignore_missing_component_templates": []
}