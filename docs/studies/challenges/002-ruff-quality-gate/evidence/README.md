# Evidências do desafio `quality-001`

## Estado

`verified`

## Ambiente

- Python 3.14.3
- uv 0.9.30
- Ruff 0.16.2
- Ubuntu 24.04 no WSL2

## Baseline

- `ruff check .`: 16 ocorrências — `E501` (8), `F401` (1), `I001` (2),
  `UP037` (3) e `UP043` (2).
- `ruff format --check .`: 4 arquivos precisavam de formatação.

As correções organizaram imports, removeram um import não usado, modernizaram
anotações para Python 3.14 e formataram linhas longas. Três comentários longos em
`tests/conftest.py` foram quebrados manualmente durante a auditoria. Não foram
usados fixes inseguros, ignores ou `# noqa`.

## Prova final

```text
uv lock --check                              -> código 0
uv run --group lint ruff check .             -> All checks passed!
uv run --group lint ruff format --check .    -> 25 files already formatted
uv run pytest -q --capture=sys               -> 3 passed, 1 warning in 0.92s
```

O warning já conhecido é emitido pela integração Starlette TestClient/HTTPX e não
foi criado pelas mudanças do Ruff.

## Revisão

O diff contém apenas configuração, lockfile e transformações mecânicas de estilo.
Não houve mudança de regra de negócio nem das assertions dos testes.
