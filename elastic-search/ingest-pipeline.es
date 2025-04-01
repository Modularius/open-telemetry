curl
-u ${ES_USERNAME}:${ES_PASSWORD}
-H ${ES_HEADER}
-XPUT
-d'{
  "description": "Extracts parentSpanID from References if a reference exists with refType equal to CHILD_OF.",
  "processors": [
    {
      "script": {
        "lang": "painless",
        "source": "
            for(tag in ctx.references)
            {
              if (tag.refType == \"CHILD_OF\") {
                ctx[\"parentSpanID\"] = tag.spanID;
                break;
              }
            }
        "
      }
    }
  ]
}'
${ES_HOST}/_ingest/pipeline/extract-parent-span-id6