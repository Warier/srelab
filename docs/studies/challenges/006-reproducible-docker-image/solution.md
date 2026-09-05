# Solução do desafio `delivery-001`

## Estado

`documented`

## Build e runtime

O Dockerfile possui dois estágios. O builder usa uv 0.9.30 para sincronizar apenas
dependências de runtime a partir do lockfile. O runtime usa Python slim, recebe
somente `.venv` e `app/`, e inicia Uvicorn diretamente como PID 1.

`.dockerignore` exclui Git, ambientes, testes, documentação, bancos e caches do
contexto de build.

## Segurança, limites e persistência

O processo roda como `scalepass` (UID/GID 10001). O banco é configurado para
`/data/scalepass.db`, montado no volume nomeado. O healthcheck usa `urllib` da
biblioteca padrão, sem adicionar curl à imagem final. A prova executou sob 512 MiB
e 1 CPU, e confirmou o dado após recriar o container.

Consulte [evidence/README.md](evidence/README.md).
