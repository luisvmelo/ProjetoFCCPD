Desafio 2

Objetivo:
Demonstrar como Docker Volumes garantem persistência de dados mesmo após containers serem removidos. A aplicação insere timestamps em um banco SQLite a cada execução, mostrando que dados sobrevivem ao ciclo de vida dos containers.

Configuração do Volume
Componentes:
-Volume nomeado (dados-db): Gerenciado pelo Docker, armazena `banco.db`
-Mount point:Volume montado em `/data` dentro do container
-Localização física:`/var/lib/docker/volumes/dados-db/_data/` (Linux)

Foi escolhido volume nomeado ao invés de bind mount porque:
-Funciona igual em Windows, Linux e macOS
-Docker gerencia permissões automaticamente
-É a forma recomendada para produção

`--rm`:
O flag `--rm` remove o container após execução, mostrnado que os dados ainda estão no volume, não no container.

Demonstração da Persistência

Primeira execução:
1. Container inicia, monta volume em `/data`
2. SQLite cria `banco.db` dentro do volume
3. Script cria tabela `registros` se não existir
4. Insere registro com timestamp atual
5. Mostra: 1 registro
6. Container é destruído (`--rm`)
7. Volume permanece intacto

Segunda execução:
1. Novo container (ID diferente)
2. Monta o MESMO volume
3. Banco já existe com 1 registro
4. Insere novo registro
5. Mostra: 2 registros, provando a persistencia 
6. Container destruído novamente

Como provar persistência
```bash
Executa primeira vez
docker run --rm -v dados-db:/data app-persistencia
Saída: 1 registro

Verifica que NÃO há containers rodando
docker ps -a
(vazio, containers foram removidos)

Executa novamente
docker run --rm -v dados-db:/data app-persistencia
Saída: 2 registros (dados persistiram!)
```

Passo a Passo de Execução

```bash
1. Executar script automático (cria volume, builda, executa 2x)
chmod +x run.sh
./run.sh

2. Criar volume
docker volume create dados-db

3. Build da imagem
docker build -t app-persistencia .

4. Primeira execução (vai aparecer 1 registro)
docker run --rm -v dados-db:/data app-persistencia

5. Segunda execução (vai aparecer 2 registros)
docker run --rm -v dados-db:/data app-persistencia

6. Limpar
docker volume rm dados-db
docker rmi app-persistencia
```

Decisões técnicas:
NO final de contas, para esse desafio foi escolhido o SQLite, ele é simples, não requer servidor separado, é feito tudo em 1 arquivo só. Foi usado Timestamps para visualizar acúmulo de dados com prints que mostram claramente quantos registros existem. Por fim, o flag `--rm` "força" boas práticas, poisdados importantes devem estar em volumes.
