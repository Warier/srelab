# Desafio `testing-002`: cobertura de branches orientada a risco

## Estado

`solved`

## Resultado esperado

Usar pytest-cov para localizar decisões de negócio sem teste e adicionar cenários
HTTP que elevem a cobertura de branches de `app/` de 77% para pelo menos 90%.
O percentual é uma trava; o objetivo principal são os riscos cobertos.

## Baseline medido

```text
208 statements, 38 missing
36 branches, 10 partial
TOTAL 77%
```

## Preparação

```bash
uv add --group coverage pytest-cov
```

Configure no `pyproject.toml`:

```toml
[tool.coverage.run]
branch = true
source = ["app"]

[tool.coverage.report]
show_missing = true
fail_under = 90
```

Baseline reproduzível:

```bash
uv run --group coverage pytest --cov=app --cov-report=term-missing
```

## Cenários obrigatórios

Adicione testes HTTP isolados para estes cinco riscos:

1. login com credenciais inválidas retorna `400` e não autentica;
2. cadastro duplicado retorna `400` e não cria outro usuário;
3. dados inválidos de evento retornam `400` e não persistem evento;
4. consultar e comprar evento inexistente retorna `404` sem criar pedido;
5. quantidade `0` ou `11` retorna `400`, preservando estoque e pedidos.

Parametrização é permitida. Cada teste deve verificar efeito persistido, não apenas
status ou texto. Reuse a fixture de banco temporário; não use mocks.

## Prova final

```bash
uv lock --check
uv run --group coverage pytest --cov=app --cov-report=term-missing
uv run --group typing mypy app
uv run --group lint ruff check .
uv run --group lint ruff format --check .
```

## Critérios de aceite

- os cinco riscos estão cobertos por HTTP e com assertions de estado;
- branch coverage total é no mínimo 90%;
- `fail_under = 90` faz o comando falhar abaixo do limite;
- banco local continua intocado;
- Mypy e Ruff continuam passando;
- nenhuma linha usa `# pragma: no cover` para atingir a meta;
- a evidência registra apenas baseline, cenários adicionados e resumo final.

## Estudo direcionado

- statement coverage versus branch coverage;
- linhas ausentes e branches parciais;
- cobertura como mapa de risco, não como garantia de qualidade;
- parametrização e assertions de efeitos colaterais.

Referência: [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/).

## Fora do escopo

CI, testes concorrentes, testes unitários de mocks e busca de 100% de cobertura.

## Git

- Tag inicial: `challenge/004/start`.
- Branch: `challenge/004-risk-based-coverage`.
- Tag futura: `challenge/004/solved`.
