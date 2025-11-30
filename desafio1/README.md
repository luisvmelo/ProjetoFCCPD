# Desafio 1 - Comunicação entre Containers

Demonstração de comunicação entre dois containers Docker utilizando rede bridge customizada.

Um container executa um servidor Flask simples, enquanto outro container realiza requisições HTTP periódicas a cada 5 segundos.

## Funcionamento

O servidor Flask responde "OK" nas rotas `/` e `/status`.

O cliente utiliza Alpine Linux e executa um loop contínuo fazendo requisições ao servidor:
```bash
while true; do wget -qO- http://server:8080 && echo ''; sleep 5; done
```

A comunicação ocorre pelo nome "server" ao invés de endereço IP. O Docker resolve automaticamente quando os containers estão na mesma rede customizada.

### Rede Bridge Customizada

Utiliza-se rede bridge customizada pelos seguintes motivos:
- Containers se comunicam pelo nome através de resolução DNS automática
- Maior isolamento, apenas containers na mesma rede podem se comunicar
- Endereços IP podem mudar entre execuções, mas nomes permanecem consistentes

## Executando o Desafio

```bash
chmod +x run.sh
./run.sh
```

Para verificar a comunicação em tempo real:
```bash
docker logs -f client
```

O terminal exibirá "OK" a cada 5 segundos, confirmando a comunicação ativa entre os containers.

## Limpeza do Ambiente

```bash
docker stop server client
docker rm server client
docker network rm minha-rede
docker rmi server-app
```

Flask foi escolhido pela simplicidade e Alpine pela imagem reduzida que já inclui wget por padrão.
