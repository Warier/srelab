# Evidências do desafio `delivery-001`

## Estado

`verified`

## Imagem e container

- Imagem: `scalepass:0.1.0`, 170.8 MB.
- Build: `docker build --no-cache` passou usando somente `pyproject.toml`,
  `uv.lock` e `app/`; `.venv` não entrou no contexto.
- Health: `healthy`.
- Usuário: UID `10001` (`scalepass`), não root.
- Limites: `memory=536870912` (512 MiB) e `nano_cpus=1000000000` (1 CPU).
- HTTP: `GET /api/events` retornou 200.
- Persistência: o evento de id `1` permaneceu após remover e recriar o container
  usando o volume nomeado `scalepass-data`.

## Gates do host

- 12 testes passaram; cobertura 96,72%.
- Mypy sem erros; Ruff sem violações; 37 arquivos formatados.
