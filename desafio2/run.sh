#!/bin/bash

docker volume create dados-db
docker build -t app-persistencia .

echo "Primeira execução:"
docker run --rm -v dados-db:/data app-persistencia

echo ""
echo "Segunda execução (deve mostrar 2 registros):"
docker run --rm -v dados-db:/data app-persistencia
