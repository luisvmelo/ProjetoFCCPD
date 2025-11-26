Desafio 5

Objetivo:
Criar uma arquitetura com API Gateway centralizando o acesso a dois microsserviços. O Gateway funciona como ponto único de entrada para acessar users-service e orders-service.

Visão Geral

Arquitetura com Gateway como ponto único de entrada:

-Gateway (porta 80): Roteia requisições do cliente para os microsserviços internos
-Users Service (interno): Gerencia dados de usuários
-Orders Service (interno): Gerencia dados de pedidos

Conceito: Gateway centraliza acesso, permitindo autenticação, logging e roteamento em um único ponto antes de distribuir para os serviços especializados.

Arquitetura: Roteamento no Gateway

Código do Gateway (gateway/app.py)

```python
@app.route('/users')
def users():
    response = requests.get('http://users-service:5000/users')
    return response.json()

@app.route('/orders')
def orders():
    response = requests.get('http://orders-service:5000/orders')
    return response.json()
```

Como funciona:
1. Cliente acessa `http://localhost/users`
2. Gateway recebe requisição na rota `/users`
3. Gateway faz requisição interna: `http://users-service:5000/users`
   -DNS do Docker Compose resolve "users-service" para IP do container
4. Users Service responde com JSON
5. Gateway retorna JSON ao cliente

docker-compose.yml

```yaml
services:
  gateway:
    build: ./gateway
    ports:
      - "80:80"              # Único serviço exposto externamente
    depends_on:
      - users-service        # Aguarda serviços internos iniciarem
      - orders-service

  users-service:
    build: ./users-service
    # SEM ports: não acessível do host

  orders-service:
    build: ./orders-service
    # SEM ports: não acessível do host

networks:
  api-network:               # Todos na mesma rede interna
    driver: bridge
```

Serviços internos não expõem portas porque:
-Segurança: Apenas Gateway é acessível externamente
-Simplicidade: Cliente interage com 1 endpoint ao invés de N
-Centralização: Autenticação, rate limiting, logs no Gateway

Fluxos de Requisição Completos

Fluxo 1: Buscar Usuários

```
Cliente
  ↓ GET http://localhost/users
Gateway (porta 80)
  ↓ requests.get('http://users-service:5000/users')
Users Service (porta 5000 interna)
  ↓ Processa e retorna JSON
Gateway
  ↓ Retorna JSON ao cliente
Cliente recebe:
[
  {"id": 1, "nome": "Tiago", "email": "tiago@gmail.com"},
  {"id": 2, "nome": "Antonio", "email": "antonio@gmail.com"},
  {"id": 3, "nome": "Hugo", "email": "hugo@gmail.com"}
]
```

Fluxo 2: Buscar Pedidos

```
Cliente
  ↓ GET http://localhost/orders
Gateway (porta 80)
  ↓ requests.get('http://orders-service:5000/orders')
Orders Service (porta 5000 interna)
  ↓ Processa e retorna JSON
Gateway
  ↓ Retorna JSON ao cliente
Cliente recebe:
[
  {"id": 101, "produto": "Papel", "preco": 25},
  {"id": 102, "produto": "Caneta", "preco": 3},
  {"id": 103, "produto": "Caderno", "preco": 15}
]
```

Como Subir com Docker Compose

```bash
Subir todos os serviços
docker compose up --build

Subir em background
docker compose up -d

Ver logs
docker compose logs gateway
docker compose logs users-service
docker compose logs orders-service

Ver status
docker compose ps

Derrubar
docker compose down
```

Endpoints e Respostas Esperadas

```bash
1. Rota raiz (informações do gateway)
curl http://localhost/
Saída:
{
  "message": "API Gateway",
  "available_routes": [...]
}

2. Buscar usuários
curl http://localhost/users
Saída:
[{"id":1,"nome":"Tiago","email":"tiago@gmail.com"},...]

3. Buscar pedidos
curl http://localhost/orders
Saída:
[{"id":101,"produto":"Papel","preco":25},...]

4. Tentar acessar serviço diretamente (deve falhar)
curl http://localhost:5000/users
Erro: Connection refused (porta não exposta)
```

Vantagens do API Gateway

1. Ponto único de entrada: Cliente não precisa saber IPs/portas dos serviços
2. Segurança: Serviços internos não expostos publicamente
3. Centralização: Autenticação, logging, rate limiting no gateway
4. Flexibilidade: Posso adicionar/remover serviços sem alterar cliente
5. Roteamento dinâmico: Gateway pode rotear baseado em headers, query params, etc.

NO final de contas foi usado o padrão Gateway que é um padrão arquitetural comum em microsserviços. A porta 80 é a porta HTTP padrão, facilita acesso (não precisa especificar porta na URL). O depends_on garante a ordem certa, serviços sobem antes do gateway. Foi adicionado tratamento de erro onde gateway retorna 503 se serviço estiver indisponivel. A biblioteca Requests faz proxy HTTP simples, em produção usaria load balancer tipo Nginx ou Traefik. A rede compartilhada coloca todos na mesma rede Docker para comunicação interna.
