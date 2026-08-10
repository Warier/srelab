# Evidências do desafio `typing-001`

## Estado

`pending`

## Baseline

- Mypy:
- Resultado: 8 erros `return-value` em `app/main.py`; 6 arquivos verificados.

## Solução

- Contrato escolhido:
- Motivo:
- Arquivos alterados:
- Mecanismos para ignorar erros: nenhum.

## Prova final

```text
uv lock --check                           ->
uv run --group typing mypy app            ->
uv run --group lint ruff check .          ->
uv run --group lint ruff format --check . ->
uv run pytest -q                          ->
```

Confirmação de comportamento preservado:
