Desafio 1

Objetivo:
Demonstrar a comunicação entre dois containers Docker usando uma rede bridge customizada. Um container roda um servidor Flask na porta 8080, e outro container age como cliente fazendo requisições HTTP periódicas ao servidor.

Arquitetura da Solução

Componentes:
-Container Servidor (Flask): Aplicação web simples que responde "OK" nas rotas `/` e `/status`
-Container Cliente (Alpine): Executa um loop infinito com `wget` fazendo requisições ao servidor a cada 5 segundos
-Rede Docker Customizada (minha-rede): Rede bridge que conecta ambos os containers e permite comunicação via DNS

Foi escolhido uma rede bridge customizada ao invés de usar a padrão porque:
-Permite resolução DNS automática (containers se comunicam por nome, não por IP)
-Melhor isolamento (só quem está na rede consegue se comunicar)
-IPs podem mudar entre execuções, mas nomes permanecem consistentes

Funcionamento Detalhado

Fluxo de Comunicação

1. Servidor Flask escuta em `0.0.0.0:8080` (aceita conexões de qualquer IP)
2. Cliente Alpine executa loop:
```bash
while true; do wget -qO- http://server:8080 && echo ''; sleep 5; done
```
3. Docker DNS resolve "server" para o IP do container servidor (ex: 172.18.0.2)
4. Cliente faz requisição HTTP, Servidor responde e Cliente imprime nos logs
5. Loop aguarda 5 segundos e repete

Logs e Verificação

Ao executar `docker logs -f client`, vai aparecer:
```
OK
OK
OK
...
```

Cada linha aparece a cada 5 segundos, provando que a comunicação tá ativa.

Passo a Passo para Executar

```bash
1. Dar permissão ao script
chmod +x run.sh

2. Executar script (cria rede, builda servidor, sobe containers)
./run.sh

3. Verificar comunicação em tempo real
docker logs -f client
(Ctrl+C para sair)

4. Testar manualmente (opcional)
docker exec client wget -qO- http://server:8080

5. Limpar ambiente
docker stop server client
docker rm server client
docker network rm minha-rede
docker rmi server-app
```

Foi escolhido Flask porque é leve e simples, permite adicionar rotas facilmente. Alpine Linux porque a imagem é minimalista, já tem `wget` incluído. Foi usado wget ao invés de curl porque Alpine vem com wget por padrão. O loop com sleep de 5 segundos é um intervalo razoavel para demonstrar comunicação sem sobrecarregar.
