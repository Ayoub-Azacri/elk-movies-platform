#!/bin/bash

echo "Démarrage de la stack ELK..."

mkdir -p logs
touch logs/sincedb_movies
chmod 666 logs/sincedb_movies

# Docker Compose v2 ships as "docker compose" (plugin), v1 as "docker-compose" (standalone).
# Try v2 first and fall back to v1 so the script works on both setups.
DOCKER_COMPOSE_CMD="docker compose"
if ! docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
fi
# Start Elasticsearch first so we can apply the explicit mapping before Logstash runs.
# If Logstash starts before the index exists, it creates movies_clean with dynamic mapping.
$DOCKER_COMPOSE_CMD up -d elasticsearch --progress quiet 2>/dev/null || $DOCKER_COMPOSE_CMD up -d elasticsearch

echo "En attente d'Elasticsearch..."
until curl -sf http://localhost:9200 > /dev/null; do
    sleep 2
done

# Pre-create movies_clean with explicit mapping before Logstash starts.
# This prevents Logstash from creating the index with dynamic mapping on first index.
if ! curl -sf http://localhost:9200/movies_clean > /dev/null 2>&1; then
    if [ -f mapping/movies_clean_mapping.json ]; then
        echo "Création de l'index movies_clean avec le mapping explicite..."
        curl -s -X PUT "http://localhost:9200/movies_clean" \
          -H "Content-Type: application/json" \
          -d @mapping/movies_clean_mapping.json > /dev/null
    fi
fi

# Start remaining services (logstash, kibana)
$DOCKER_COMPOSE_CMD up -d --progress quiet 2>/dev/null || $DOCKER_COMPOSE_CMD up -d

# Automatic Python detection
if python3 --version > /dev/null 2>&1; then
    PYTHON_CMD="python3"
elif python --version > /dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "Erreur : Python n'est pas installé."
    exit 1
fi

echo ""
echo "Pour suivre l'ingestion en temps réel, ouvre un autre terminal et lance :"
echo "  ==> $PYTHON_CMD monitor_ingestion.py"
echo ""

echo "En attente de la fin de l'ingestion..."
prev=0
while true; do
    current=$(curl -s "http://localhost:9200/movies_raw/_count" | "$PYTHON_CMD" -c "import sys,json; d=json.load(sys.stdin); print(d.get('count', 0))")
    if [ "$current" -eq "$prev" ] && [ "$current" -gt 0 ]; then
        break
    fi
    prev=$current
    sleep 30
done

echo "Application du fix replica..."
curl -s -X PUT http://localhost:9200/movies_raw/_settings \
  -H "Content-Type: application/json" \
  -d '{"index": {"number_of_replicas": 0}}' > /dev/null

if curl -sf http://localhost:9200/movies_clean > /dev/null 2>&1; then
    curl -s -X PUT http://localhost:9200/movies_clean/_settings \
      -H "Content-Type: application/json" \
      -d '{"index": {"number_of_replicas": 0}}' > /dev/null
fi

RAW_COUNT=$(curl -s "http://localhost:9200/movies_raw/_count" 2>/dev/null | "$PYTHON_CMD" -c "import sys,json; print(json.load(sys.stdin).get('count', 0))" 2>/dev/null || echo "N/A")
CLEAN_COUNT=$(curl -s "http://localhost:9200/movies_clean/_count" 2>/dev/null | "$PYTHON_CMD" -c "import sys,json; print(json.load(sys.stdin).get('count', 0))" 2>/dev/null || echo "N/A")

echo ""
echo "Stack démarrée."
echo "Kibana          -> http://localhost:5601"
echo "Elasticsearch   -> http://localhost:9200"
echo "movies_raw      -> $RAW_COUNT docs"
echo "movies_clean    -> $CLEAN_COUNT docs"
echo "Monitoring      -> $PYTHON_CMD monitor_ingestion.py"
