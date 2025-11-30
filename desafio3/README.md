# Desafio 3 - Docker Compose

Orquestração de múltiplos serviços utilizando Docker Compose: Flask, Redis e PostgreSQL.

A aplicação Flask incrementa um contador armazenado no Redis a cada acesso. Também verifica conexão com PostgreSQL para demonstrar integração com banco de dados relacional.

## Serviços

- **web** - Aplicação Flask na porta 5000
- **cache** - Redis para armazenamento do contador
- **db** - PostgreSQL para demonstração de conectividade

## Configuração Docker Compose

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - cache
      - db

  cache:
    image: redis:alpine

  db:
    image: postgres:alpine
    environment:
      POSTGRES_PASSWORD: senha123
```

O parâmetro `depends_on` garante que os serviços cache e db sejam iniciados antes do web. Todos os serviços compartilham a mesma rede Docker, permitindo comunicação através de nomes: `cache:6379` e `db:5432`.

## Executando o Desafio

```bash
docker compose up --build
```

Para execução em background:
```bash
docker compose up -d
```

Acessar `http://localhost:5000` e recarregar a página para incrementar o contador.

Para resetar o contador: `http://localhost:5000/reset`

## Comandos Úteis

```bash
# Visualizar logs de todos os serviços
docker compose logs

# Visualizar logs de um serviço específico
docker compose logs web

# Verificar status dos serviços
docker compose ps

# Encerrar todos os serviços
docker compose down
```

## Testando a Aplicação

```bash
curl http://localhost:5000
# Contador incrementa

curl http://localhost:5000/reset
# Contador resetado

curl http://localhost:5000
# Contador reinicia em 1
```

Redis foi utilizado para o contador devido à maior performance em operações de leitura/escrita em memória. As imagens Alpine reduzem o tamanho total e aceleram o processo de build.
