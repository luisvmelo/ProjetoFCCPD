Desafio 3

Objetivo:
Usar Docker Compose para orquestrar múltiplos serviços dependentes. A aplicação tem 3 serviços (web, cache e db) que se comunicam entre si.

Visão Geral dos Serviços

-web (Flask): API que incrementa contador no Redis e verifica conexão com Postgres
-cache (Redis): Armazena contador de visitas em memória
-db (PostgreSQL): Banco de dados relacional (demonstra integração multi-serviço)

Arquitetura do docker-compose.yml

Estrutura dos Services

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - cache
      - db
    networks:
      - app-network

  cache:
    image: redis:alpine
    networks:
      - app-network

  db:
    image: postgres:alpine
    environment:
      POSTGRES_PASSWORD: senha123
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

Explicação dos Conceitos

depends_on:
Garante ordem de inicialização. O serviço `web` só inicia depois que `cache` e `db` estiverem rodando. Evita erros de "conexão recusada" ao tentar conectar em serviços que ainda não subiram.

networks:
Todos os serviços compartilham a rede `app-network`. Isso permite comunicação via DNS (ex: `redis://cache:6379`, `postgresql://db:5432`). Serviços fora da rede não conseguem se comunicar.

environment:
Define variáveis de ambiente necessárias. PostgreSQL requer `POSTGRES_PASSWORD` para iniciar.

build vs image:
-`build: .` constrói imagem a partir do Dockerfile no diretório atual (usado em `web`)
-`image: redis:alpine` usa imagem pronta do Docker Hub (usado em `cache` e `db`)

Comunicação Entre Serviços na Prática

Fluxo de Requisição Completo

1. Usuário acessa `http://localhost:5000/`
2. Container web recebe requisição
3. Web → Redis: `redis_client.incr('contador_visitas')`
   -Conecta em `cache:6379` (DNS resolve para IP do container Redis)
   -Redis incrementa contador e retorna valor atualizado
4. Web → Postgres: `psycopg2.connect(host='db', ...)`
   -Conecta em `db:5432` para testar conexão
   -Fecha conexão imediatamente (apenas teste)
5. Web → Usuário: Retorna resposta formatada com contador e status

Endpoints Disponíveis

-GET /: Mostra contador de visitas e status do Postgres
-GET /reset: Reseta contador para 0

Exemplo de Teste

```bash
Primeira visita
curl http://localhost:5000/
Contador: 1

Recarregar várias vezes
curl http://localhost:5000/
Contador: 2
curl http://localhost:5000/
Contador: 3

Resetar
curl http://localhost:5000/reset

Verificar
curl http://localhost:5000/
Contador: 1 (resetou)
```

Como Subir, Derrubar e Testar

```bash
Subir todos os serviços
docker compose up --build

Subir em background (libera o terminal)
docker compose up -d

Testar via curl
curl http://localhost:5000

Ver logs de todos os serviços
docker compose logs

Ver logs de um serviço específico
docker compose logs web
docker compose logs cache

Ver status dos serviços
docker compose ps

Derrubar tudo
docker compose down

Derrubar e remover volumes
docker compose down -v
```

NO final de contas foi escolhido Redis para contador porque é mais rápido que armazenar no Postgres, demonstra cache em memória. Postgres como demonstração para mostrar integração com banco relacional, poderia ser usado para logs. Foi usado Alpine nas imagens porque as imagens ficam menores (~5MB vs ~100MB), o deploy fica mais rápido. A rede customizada é melhor que rede padrão, permite DNS e isolamento. O depends_on evita race conditions na inicialização.
