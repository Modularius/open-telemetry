export ES_USERNAME=elastic
export ES_PASSWORD=password
export ES_HOST=http://localhost:9200
export ES_HEADER="\"Content-Type: application/json\""

docker compose --profile elasticsearch_only up -d