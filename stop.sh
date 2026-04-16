#!/bin/bash

if [ "$1" == "--reset" ]; then
    echo "Arrêt avec réinitialisation complète..."
    # Remove containers AND volumes (Elasticsearch data)
    docker-compose down -v
    # Remove the Logstash pointer
    rm -f logs/sincedb_movies
    echo "Données et index supprimés. L'ingestion repartira de zéro."
else
    echo "Arrêt simple..."
    # Stop the containers but keep the volumes and the sincedb
    docker-compose down
    echo "Stack arrêtée. Les données sont conservées."
fi