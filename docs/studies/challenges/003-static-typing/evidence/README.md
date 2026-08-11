# Evidências do desafio `typing-001`

## Estado

`verified`

## Baseline

- Mypy 2.3.0: 8 erros `return-value` em `app/main.py`; 6 arquivos verificados.

## Solução

- Mypy foi adicionado ao grupo `typing` e configurado em modo estrito.
- As seis rotas com respostas HTML ou redirect passaram a declarar a classe-base
  `Response`.
- A primeira tentativa com `HTMLResponse | RedirectResponse` passou no Mypy, mas
  impediu o FastAPI de iniciar; foi rejeitada após o teste de regressão.
- Nenhum erro foi ignorado ou desativado.

## Prova final

```text
uv lock --check                           -> código 0
uv run --group typing mypy app            -> sem erros em 6 arquivos
uv run --group lint ruff check .          -> sem violações
uv run --group lint ruff format --check . -> 28 arquivos formatados
uv run pytest -q --capture=sys            -> 3 passed, 1 warning em 1.00s
```

O warning do TestClient já era conhecido e não foi causado por este desafio.
