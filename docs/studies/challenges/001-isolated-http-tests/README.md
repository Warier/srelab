# Desafio `testing-001`: venda testada por HTTP com banco isolado

## Estado

`active`

## Resultado único esperado

Criar três testes de integração HTTP para o fluxo de compra. Cada teste deve usar
um arquivo SQLite temporário próprio e nenhuma execução pode criar ou modificar o
`scalepass.db` usado pela aplicação local.

Este desafio trata somente da base de testes do fluxo de venda. Lint, formatação,
tipos, cobertura e CI pertencem a desafios posteriores.

## Tempo e dificuldade estimados

- Tempo: 4 a 8 horas de estudo e implementação.
- Nível: júnior intermediário.
- Principal dificuldade: fazer o startup e as dependências HTTP usarem o mesmo
  banco temporário.

## Problema observado

Hoje a única forma de saber se uma venda ainda funciona é repetir manualmente:

1. cadastrar um usuário;
2. criar um evento;
3. comprar ingressos;
4. conferir o estoque e o pedido.

Além disso, o engine e a criação de tabelas são globais. Um teste ingênuo pode
escrever silenciosamente em `scalepass.db`, passando enquanto contamina dados de
desenvolvimento.

## Ferramentas obrigatórias

- `pytest`: runner, fixtures e assertions.
- `httpx`: dependência usada pelo `TestClient` do FastAPI.
- `fastapi.testclient.TestClient`: cliente HTTP síncrono.
- fixture `tmp_path` do pytest: diretório temporário exclusivo por teste.
- SQLite em arquivo temporário: banco real do teste.

Não use SQLite `:memory:` neste desafio. Um arquivo dentro de `tmp_path` reduz as
diferenças entre conexões e torna o isolamento mais fácil de inspecionar.

## Preparação do ambiente com `uv`

Adicione apenas as dependências deste desafio ao grupo `dev`:

```bash
uv add --dev pytest httpx
```

Depois confirme que metadados e lockfile concordam:

```bash
uv lock --check
uv sync --locked
```

O que estudar no `uv`:

- diferença entre dependência de runtime e dependency group;
- por que `--dev` grava em `[dependency-groups]`;
- diferença entre `uv sync`, `uv sync --locked` e `uv sync --frozen`;
- quando `uv run` sincroniza o ambiente automaticamente.

Referências oficiais:

- [uv: development dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/#development-dependencies)
- [uv: locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)

## Estrutura mínima esperada

```text
tests/
├── conftest.py
└── test_ticket_purchase.py
```

`conftest.py` deve concentrar fixtures compartilhadas. O arquivo de teste deve
conter os três cenários exigidos abaixo. Alterações em `app/` são permitidas apenas
quando necessárias para injetar ou substituir o banco.

## Testes obrigatórios

### 1. `test_authenticated_user_can_buy_ticket`

Pelo cliente HTTP:

1. cadastrar e manter autenticado um usuário;
2. criar um evento com estoque inicial conhecido;
3. comprar dois ingressos;
4. confirmar redirecionamento de sucesso;
5. confirmar que `/orders` exibe o pedido;
6. confirmar por `GET /api/events` que o estoque caiu exatamente em dois.

### 2. `test_buying_more_tickets_than_available_is_rejected`

Pelo cliente HTTP:

1. criar um evento com estoque `2`;
2. tentar comprar `3`;
3. confirmar status `400`;
4. confirmar que o estoque continua `2`;
5. confirmar que nenhum pedido foi criado para essa tentativa.

### 3. `test_visitor_cannot_buy_ticket`

Pelo cliente HTTP:

1. disponibilizar um evento;
2. usar um cliente sem sessão autenticada;
3. tentar comprar um ingresso;
4. confirmar status `303` e destino `/login`;
5. confirmar que o estoque não mudou.

## Regras de isolamento

- Cada teste recebe um SQLite diferente dentro de `tmp_path`.
- Os testes não compartilham usuários, eventos ou pedidos.
- Startup, `create_tables()` e `get_db()` devem apontar para o banco do teste.
- Overrides e sessões devem ser encerrados ao final da fixture, inclusive quando o
  teste falhar.
- Não altere `SCALEPASS_DATABASE_URL` globalmente depois que os módulos já foram
  importados como forma de contornar o problema.
- Não faça mock de `Session`, SQLAlchemy ou das funções de rota.

## O que estudar antes de implementar

### Pytest

Estude apenas:

- descoberta de funções `test_*`;
- assertions simples;
- fixtures declaradas com `@pytest.fixture`;
- setup/teardown com `yield`;
- escopos `function` e `session`;
- fixture `tmp_path`.

Referências oficiais:

- [pytest: get started](https://docs.pytest.org/en/stable/getting-started.html)
- [pytest: fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest: temporary directories](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
- [pytest: talks and tutorials selecionados pelo projeto](https://docs.pytest.org/en/stable/talks.html)
- [Vídeo recomendado: pytest training — PyConDE 2022](https://www.youtube.com/watch?v=ofPHJrAOaTE)

### FastAPI e HTTPX

Estude apenas:

- criação e uso de `TestClient`;
- uso do cliente como context manager para executar o lifespan;
- persistência de cookies dentro da mesma instância do cliente;
- desativação de redirects automáticos com `follow_redirects=False`;
- `app.dependency_overrides` e sua limpeza após o teste.

Referências oficiais:

- [FastAPI: testing with TestClient](https://fastapi.tiangolo.com/tutorial/testing/)
- [FastAPI: overriding dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)

### SQLAlchemy e SQLite

Estude apenas:

- criação de engine para uma URL SQLite temporária;
- `check_same_thread=False` quando o cliente e a aplicação usam threads distintas;
- criação das tabelas no engine correto;
- abertura e fechamento de uma `Session` por requisição.

Referência oficial:

- [SQLAlchemy: SQLite dialect and threading](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#threading-pooling-behavior)

## Critérios de aceite objetivos

Todos precisam ser verdadeiros:

1. `uv lock --check` encerra com código `0`.
2. `uv run pytest -q` mostra exatamente os três testes obrigatórios passando.
3. Uma segunda execução imediata também passa, sem depender da primeira.
4. A suíte termina em menos de 10 segundos no PC principal.
5. O hash de `scalepass.db` é idêntico antes e depois da suíte.
6. Se `scalepass.db` não existir antes, ele continua inexistente depois.
7. Os testes não dependem de ordem nem de dados criados manualmente.
8. Nenhum teste usa mock do banco ou chama diretamente uma função de rota.

## Evidências a registrar

Em `evidence/README.md`, registre:

- saída resumida das duas execuções de `uv run pytest -q`;
- duração de cada execução;
- hash do banco antes e depois, ou confirmação de ausência antes/depois;
- caminho temporário usado durante uma execução com `pytest --basetemp`, se quiser
  inspecionar o arquivo;
- decisões tomadas para garantir que lifespan e dependências compartilhem o mesmo
  engine.

## Fora do escopo

- Ruff ou qualquer outro linter;
- Mypy, Pyright ou outro type checker;
- relatório de cobertura;
- GitHub Actions ou outra CI;
- testes de concorrência;
- correção do mecanismo de senha;
- PostgreSQL, containers, Redis ou filas;
- testes unitários de funções auxiliares.

## Pistas progressivas

Leia somente se travar.

<details>
<summary>Pista 1 — o banco local apareceu durante o teste</summary>

Sobrescrever apenas `get_db()` pode não ser suficiente: observe o que o lifespan
executa antes da primeira requisição e qual engine essa função conhece.
</details>

<details>
<summary>Pista 2 — erro “no such table”</summary>

Confirme se as tabelas foram criadas no mesmo engine que produz as sessões entregues
às rotas. Dois arquivos ou dois engines distintos não compartilham schema.
</details>

<details>
<summary>Pista 3 — login desaparece entre requisições</summary>

Cookies pertencem à instância do cliente. Use o mesmo `TestClient` durante as etapas
de um cenário autenticado.
</details>

## Checkpoint Git

- Tag inicial: `challenge/001/start`.
- Branch: `challenge/001-isolated-http-tests`.
- Tag futura da solução: `challenge/001/solved`.
- Solução oficial: [solution.md](solution.md), ainda `pending`.
