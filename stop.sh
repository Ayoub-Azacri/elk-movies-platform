#!/bin/bash

# Docker Compose v2 ships as "docker compose" (plugin), v1 as "docker-compose" (standalone).
# Try v2 first and fall back to v1 so the script works on both setups.
DOCKER_COMPOSE_CMD="docker compose"
if ! docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
fi

if [ "$1" == "--reset" ]; then
    echo "Arrêt avec réinitialisation complète..."
    # Remove containers AND volumes (Elasticsearch data)
    $DOCKER_COMPOSE_CMD down -v
    # Remove the Logstash pointer
    rm -f logs/sincedb_movies
    echo "Données et index supprimés. L'ingestion repartira de zéro."
else
    echo "Arrêt simple..."
    # Stop the containers but keep the volumes and the sincedb
    $DOCKER_COMPOSE_CMD down
    echo "Stack arrêtée. Les données sont conservées."
fi
