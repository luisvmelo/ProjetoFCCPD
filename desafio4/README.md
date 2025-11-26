Desafio 4

Objetivo:
Criar dois microsserviços independentes que se comunicam via HTTP. Service A retorna uma lista de usuários e Service B consome o Service A e formata as informações.

Descrição dos Serviços

-Service A (Provedor): API REST que retorna lista de usuários em JSON
-Service B (Consumidor): Consome dados do Service A via HTTP e formata para HTML

Endpoints e Fluxo de Chamada

Service A - API de Usuários
```
GET /users - Retorna JSON:
[
  {"id": 1, "nome": "Luis"},
  {"id": 2, "nome": "Eduardo"},
  {"id": 3, "nome": "Mayla"}
]
```

Service B - Agregador de Status
```
GET /status - Consome Service A e retorna HTML:
Usuário Luis está ativo<br>
Usuário Eduardo está ativo<br>
Usuário Mayla está ativo
```

Fluxo Completo (A → B)

1. Cliente faz requisição: `GET http://localhost:5002/status`
2. Service B recebe requisição
3. Service B → Service A: `requests.get('http://service-a:5001/users')`
   -DNS do Docker resolve "service-a" para IP do container
   -Service A processa e retorna JSON
4. Service B recebe JSON, formata em HTML
5. Service B → Cliente: Retorna HTML formatado

Empacotamento Docker de Cada Serviço

Service A - Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
EXPOSE 5001
CMD ["python", "app.py"]
```
-Porta 5001 (apenas interna, não exposta ao host)
-Depende apenas de Flask

Service B - Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask requests
COPY app.py .
EXPOSE 5002
CMD ["python", "app.py"]
```
-Porta 5002 (exposta ao host via `-p 5002:5002`)
-Depende de Flask + Requests (para fazer chamadas HTTP)

Service A não expõe porta ao host porque ele é um serviço interno, acessado apenas pelo Service B. Expor porta seria desnecessário e abriria superfície de ataque.

Passo a Passo de Execução

```bash
1. Dar permissão ao script
chmod +x run.sh

2. Executar (cria rede, builda, sobe containers)
./run.sh

3. Testar comunicação
curl http://localhost:5002/status
Saída esperada:
Usuário Luis está ativo<br>Usuário Eduardo está ativo<br>Usuário Mayla está ativo

4. Ver logs do Service B (mostra requisição ao Service A)
docker logs service-b

5. Tentar acessar Service A diretamente (deve falhar)
curl http://localhost:5001/users
Erro: Connection refused (porta não exposta ao host)

6. Acessar Service A via DNS interno
docker exec service-b curl http://service-a:5001/users
Funciona! Retorna JSON

7. Limpar
docker stop service-a service-b
docker rm service-a service-b
docker network rm servicos-rede
docker rmi service-a service-b
```

NO final de contas não foi usado Docker Compose aqui para demonstrar os conceitos básicos de rede manualmente com `docker run`. A biblioteca Requests é a biblioteca padrão Python para HTTP, simples e confiavel. Service A é interno e não expõe porta, acessível apenas via rede Docker. Service B é exposto como único ponto de entrada para o usuário final. A transformação JSON → HTML demonstra transformação de dados entre serviços. A rede bridge customizada permite DNS e isolamento.
