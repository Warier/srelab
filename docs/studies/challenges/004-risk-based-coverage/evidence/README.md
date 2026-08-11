# Evidências do desafio `testing-002`

## Estado

`verified`

## Resultado

- Baseline: 77% de cobertura, 38 statements ausentes e 10 branches parciais.
- Final: 96,72%, com 7 statements ausentes e 1 branch parcial.
- Suíte: 12 casos passando em 2,82s.

## Riscos cobertos

- login inválido sem autenticação;
- cadastro duplicado sem aceitar a segunda senha;
- dados inválidos sem persistir evento;
- consulta/compra de evento inexistente sem pedido;
- quantidade fora de `1..10` sem alterar estoque ou criar pedido.

## Gates

```text
pytest-cov -> 12 passed; cobertura 96,72%; limite 90% atingido
mypy app   -> sem erros em 6 arquivos
ruff check -> sem violações
ruff format --check -> 37 arquivos formatados
```

- Banco usado pelos testes: SQLite temporário por caso.
- `pragma: no cover`: nenhum.
