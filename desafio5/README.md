# Desafio 5 - API Gateway

Implementação do padrão API Gateway para centralização de acesso a microsserviços.

O Gateway atua como ponto único de entrada, roteando requisições para os microsserviços internos de usuários e pedidos.

## Arquitetura

```
Cliente → Gateway (porta 80) → users-service (porta 5000 interna)
                             → orders-service (porta 5000 interna)
```

## Rotas do Gateway

**Gateway:**
- `GET /users` → encaminha para users-service
- `GET /orders` → encaminha para orders-service
- `GET /` → informações sobre rotas disponíveis

**Users Service:**
```json
[
  {"id": 1, "nome": "Tiago", "email": "tiago@gmail.com"},
  {"id": 2, "nome": "Antonio", "email": "antonio@gmail.com"},
  {"id": 3, "nome": "Hugo", "email": "hugo@gmail.com"}
]
```

**Orders Service:**
```json
[
  {"id": 101, "produto": "Papel", "preco": 25},
  {"id": 102, "produto": "Caneta", "preco": 3},
  {"id": 103, "produto": "Caderno", "preco": 15}
]
```

## Executando o Desafio

```bash
docker compose up --build
```

Para execução em background:
```bash
docker compose up -d
```

## Testando a Aplicação

```bash
# Informações do gateway
curl http://localhost/

# Buscar usuários
curl http://localhost/users

# Buscar pedidos
curl http://localhost/orders

# Tentar acessar serviço diretamente (falha esperada)
curl http://localhost:5000/users
# Connection refused - serviços não expõem portas
```

## Vantagens do API Gateway

- Ponto único de entrada para todos os serviços
- Serviços internos não ficam expostos publicamente
- Centralização de autenticação, logging e rate limiting
- Flexibilidade para adicionar ou remover serviços sem alterar cliente
- Possibilidade de roteamento dinâmico baseado em headers ou parâmetros

## Limpeza do Ambiente

```bash
docker compose down
```

A porta 80 foi escolhida por ser a porta HTTP padrão. Em ambiente de produção, seria recomendado utilizar soluções como Nginx ou Traefik ao invés de Flask com requests.
