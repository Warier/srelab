# Evidências do desafio `testing-001`

## Estado

`verified`

## Ambiente

- Python: 3.14.
- uv: 0.9.30.
- Sistema operacional: Ubuntu 24.04.

## Execuções

### Primeira execução

```text
uv run pytest -q
...                                                                      [100%]
3 passed, 1 warning in 0.28s
```

### Segunda execução

```text
uv run pytest -q
...                                                                      [100%]
3 passed, 1 warning in 0.28s
```

Nas duas execuções, o warning foi:

```text
StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is
deprecated; install `httpx2` instead.
```

## Integridade de `scalepass.db`

- SHA-256 antes: `215e1ebf74c9910f757c55396ce911cba6292872f0aa1dc8d18d9ff27a6020c9`.
- SHA-256 depois: `215e1ebf74c9910f757c55396ce911cba6292872f0aa1dc8d18d9ff27a6020c9`.

## Isolamento implementado

Para garantir que a aplicação rode de forma isolada sem tocar no banco de
desenvolvimento, a fixture `client` em `tests/conftest.py` usa:

- **SQLite temporário:** `tmp_path` fornece um diretório exclusivo por função de
  teste, no qual é criado `test_scalepass.db`.
- **Engine no startup:** `app.database.engine` é substituído antes da entrada no
  context manager do `TestClient`. Portanto, o lifespan executa `create_tables()`
  no banco temporário.
- **Sessões HTTP:** um `sessionmaker` local é associado ao engine temporário e
  `app.dependency_overrides[get_db]` entrega essas sessões às requisições.
- **Cookies:** o mesmo `TestClient` é usado ao longo de cada cenário; no cenário de
  visitante, seus cookies são removidos.
- **Teardown:** as sessões são fechadas, os overrides são limpos e o engine global
  original é restaurado.

## Auditoria independente

Em 2026-08-09, após o commit `10c8530`:

- `uv lock --check`: código de saída `0`;
- primeira execução `uv run pytest -q --capture=sys`: `3 passed`, `1 warning`,
  `0.71s`;
- segunda execução `uv run pytest -q --capture=sys`: `3 passed`, `1 warning`,
  `0.70s`;
- SHA-256 antes e depois:
  `215e1ebf74c9910f757c55396ce911cba6292872f0aa1dc8d18d9ff27a6020c9`.

O comando sem `--capture=sys` falhou apenas no mecanismo de captura do executor de
auditoria: um arquivo temporário interno do Pytest desapareceu durante a execução.
Isso não foi uma falha de cenário, banco ou aplicação. A repetição com captura
`sys` manteve testes e assertions idênticos.

## Limitações conhecidas

- O engine temporário não recebe `dispose()` explícito no teardown.
- A substituição de uma referência global funciona para a execução sequencial
  atual, mas precisaria mudar antes de paralelizar testes no mesmo processo.
- O warning de compatibilidade entre Starlette TestClient e `httpx` não afeta os
  resultados. Ele não foi silenciado nem tratado dentro deste desafio.
- Os bancos criados em `tmp_path` são descartados. Para inspecioná-los, uma
  execução de diagnóstico pode definir `pytest --basetemp=<diretório>`.
