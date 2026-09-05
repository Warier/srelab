# Desafio `delivery-001`: imagem Docker reproduzível

## Estado

`solved`.

## Resultado esperado

Construir uma imagem do ScalePass a partir do lockfile, executá-la como usuário não
root sob limites de CPU/memória e provar disponibilidade e persistência SQLite.

## Arquivos

Crie apenas:

- `Dockerfile` multi-stage;
- `.dockerignore`;
- ajustes mínimos de documentação do produto para execução da imagem.

## Requisitos da imagem

- Python 3.14 em base slim;
- estágio de build usando uv e `uv sync --locked --no-dev`;
- estágio runtime sem ferramentas de desenvolvimento;
- processo `uvicorn app.main:app --host 0.0.0.0 --port 8000`;
- usuário sem UID 0;
- porta `8000` exposta;
- dados SQLite em `/data`, configurados por `SCALEPASS_DATABASE_URL`;
- `HEALTHCHECK` consultando `/api/events` sem instalar curl apenas para isso;
- contexto sem `.git`, `.venv`, bancos, caches ou documentação de estudos.

Não copie o `.venv` do host e não execute `uv sync` no startup do container.

## Prova local

```bash
docker build -t scalepass:0.1.0 .
docker run -d --name scalepass \
  --memory=512m --cpus=1 \
  -p 8000:8000 \
  --mount source=scalepass-data,target=/data \
  scalepass:0.1.0
```

Confirme:

```bash
curl --fail http://localhost:8000/api/events
docker inspect --format '{{.State.Health.Status}}' scalepass
docker exec scalepass id -u
docker image inspect scalepass:0.1.0 --format '{{.Size}}'
```

Crie um usuário/evento, remova e recrie o container usando o mesmo volume e prove
que o evento continua disponível.

## Critérios de aceite

- build limpo termina sem depender do `.venv` local;
- container fica `healthy` e responde HTTP 200;
- UID dentro do container é diferente de `0`;
- limites de `512 MiB` e `1 CPU` aparecem no inspect;
- dado persiste após recriação do container;
- testes, Mypy e Ruff continuam passando no host;
- evidência registra apenas imagem, health, UID, limites e persistência.

## Estudo direcionado

- imagem versus container;
- layers, cache de build e `.dockerignore`;
- multi-stage build;
- PID 1, sinais e formato exec de `CMD`;
- usuário não root, volume e limites de recursos;
- healthcheck versus simples processo em execução.

Referências:

- [Docker: guia para Python](https://docs.docker.com/guides/python/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Boas práticas de build](https://docs.docker.com/build/building/best-practices/)

## Fora do escopo

Compose, Kubernetes, registry, deploy remoto, PostgreSQL e observabilidade.

## Git

- Branch futura: `challenge/006-reproducible-docker-image`.
- Tags futuras: `challenge/006/start` e `challenge/006/solved`.
