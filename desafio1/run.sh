#!/bin/bash

docker network create minha-rede
docker build -t server-app .
docker run -d --name server --network minha-rede server-app
docker run -d --name client --network minha-rede alpine sh -c "while true; do wget -qO- http://server:8080 && echo ''; sleep 5; done"

echo "Pronto! Para ver os logs: docker logs -f client"
