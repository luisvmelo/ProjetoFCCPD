# Desafio 4 - Microsserviços

Implementação de dois microsserviços independentes que se comunicam via HTTP.

Service A fornece dados de usuários em formato JSON. Service B consome esses dados e os transforma em HTML.

## Endpoints

**Service A** (porta 5001 interna):
```json
GET /users
[
  {"id": 1, "nome": "Luis"},
  {"id": 2, "nome": "Eduardo"},
  {"id": 3, "nome": "Mayla"}
]
```

**Service B** (porta 5002 exposta):
```
GET /status
Luis ativo<br>Eduardo ativo<br>Mayla ativo
```

Service B realiza requisição interna ao Service A através de `http://service-a:5001/users`.

## Executando o Desafio

```bash
chmod +x run.sh
./run.sh
```

Testar a aplicação:
```bash
curl http://localhost:5002/status
```

### Isolamento de Serviços

Service A não expõe porta para o host. Apenas Service B consegue acessá-lo através da rede Docker interna. Esta configuração é intencional, mantendo Service A como serviço interno.

Tentar acesso direto ao Service A:
```bash
curl http://localhost:5001/users
# Connection refused - porta não exposta ao host
```

Acessar Service A através do Service B:
```bash
docker exec service-b curl http://service-a:5001/users
# Retorna JSON dos usuários
```

## Limpeza do Ambiente

```bash
docker stop service-a service-b
docker rm service-a service-b
docker network rm servicos-rede
docker rmi service-a service-b
```

Docker Compose não foi utilizado neste desafio para demonstrar configuração manual com `docker run`. Service B utiliza a biblioteca requests para realizar requisições HTTP.
