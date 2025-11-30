# Desafio 2 - Persistência com Volumes

Demonstração de persistência de dados utilizando Docker Volumes, mesmo após destruição dos containers.

A aplicação insere timestamps em um banco SQLite a cada execução. Mesmo com a destruição do container usando `--rm`, os dados permanecem armazenados no volume.

## Configuração

Volume `dados-db` montado em `/data` dentro do container. O banco SQLite é armazenado em `/data/banco.db`.

### Primeira Execução
- Cria o banco de dados
- Insere 1 registro com timestamp
- Container é destruído após execução

### Segunda Execução
- Novo container é criado (ID diferente)
- Monta o mesmo volume
- Banco já contém 1 registro da execução anterior
- Insere novo registro
- Exibe 2 registros, comprovando a persistência

## Executando o Desafio

```bash
chmod +x run.sh
./run.sh
```

Ou executar manualmente:

```bash
# Criar volume
docker volume create dados-db

# Build da imagem
docker build -t app-persistencia .

# Primeira execução - exibe 1 registro
docker run --rm -v dados-db:/data app-persistencia

# Segunda execução - exibe 2 registros
docker run --rm -v dados-db:/data app-persistencia
```

Verificar que não há containers ativos com `docker ps -a`, mas os dados permanecem no volume.

## Limpeza do Ambiente

```bash
docker volume rm dados-db
docker rmi app-persistencia
```

SQLite foi escolhido por não requerer servidor separado, armazenando tudo em um único arquivo. Volumes nomeados funcionam uniformemente em diferentes sistemas operacionais, com o Docker gerenciando permissões automaticamente.
