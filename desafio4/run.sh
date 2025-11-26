#!/bin/bash

docker network create servicos-rede

cd service-a
docker build -t service-a .
cd ..

cd service-b
docker build -t service-b .
cd ..

docker run -d --name service-a --network servicos-rede service-a
docker run -d --name service-b --network servicos-rede -p 5002:5002 service-b

echo "Pronto! Teste com: curl http://localhost:5002/status"
