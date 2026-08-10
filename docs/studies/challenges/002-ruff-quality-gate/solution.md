# Solução do desafio `quality-001`

## Estado

`documented`

## Diagnóstico e política

O baseline tinha 16 violações e 4 arquivos fora do formato. Ruff foi adicionado ao
grupo `lint` do uv e configurado no `pyproject.toml` para Python 3.14, 88 colunas e
as famílias `E`, `F`, `I`, `UP`, `B` e `SIM`.

## Alterações realizadas

- imports foram ordenados e o import não usado de `Base` foi removido;
- linhas e assinaturas longas foram reformatadas;
- `Generator[T, None, None]` passou a `Generator[T]`;
- forward references entre os modelos deixaram de usar aspas, conforme a semântica
  de anotações do Python 3.14;
- `except (InvalidOperation, ValueError)` adotou a sintaxe equivalente do Python
  3.14 sem parênteses;
- comentários longos da fixture foram quebrados manualmente.

As mudanças não alteram comportamento funcional. Não foram usados `--unsafe-fixes`,
ignores, exclusões ou `# noqa`.

## Reprodução

```bash
uv lock --check
uv run --group lint ruff check .
uv run --group lint ruff format --check .
uv run pytest -q
```

Na auditoria final: lockfile válido, zero violações, 25 arquivos formatados e os
três testes passando. O warning de compatibilidade do TestClient permanece fora do
escopo.

## Evidência

Consulte [evidence/README.md](evidence/README.md).
