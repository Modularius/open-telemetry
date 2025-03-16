PUT _index_template/jaeger-service
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
        "requests": {
          "cache": {
            "enable": "true"
          }
        },
        "number_of_shards": "1",
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
        "operationName": {
          "ignore_above": 256,
          "type": "keyword"
        },
        "serviceName": {
          "ignore_above": 256,
          "type": "keyword"
        }
      }
    }
  },
  "index_patterns": [
    "jaeger-service-*"
  ],
  "composed_of": [],
  "ignore_missing_component_templates": []
}