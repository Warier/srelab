# Solução do desafio `testing-001`

## Estado

`documented`

## Diagnóstico do acoplamento ao banco local

O lifespan chama `create_tables()`, que lê `app.database.engine` no momento da
execução. Sobrescrever somente a dependência `get_db()` isolaria as sessões HTTP,
mas deixaria a criação do schema conectada ao banco local. O teste precisa fazer
lifespan e sessões apontarem para o mesmo engine temporário.

## Estrutura das fixtures

Uma fixture `client`, com escopo padrão `function`, recebe `tmp_path` e cria:

1. um arquivo SQLite exclusivo para o teste;
2. um engine ligado a esse arquivo;
3. um `sessionmaker` ligado ao engine temporário;
4. um override de `get_db()` que fecha cada sessão em `finally`;
5. um `TestClient` usado como context manager para executar o lifespan.

Após o `yield`, o override é removido e o engine original do módulo é restaurado.

## Alterações necessárias na aplicação

Não foi necessária uma alteração permanente em `app/`. Durante a fixture,
`app.database.engine` é substituído antes de entrar no context manager do
`TestClient`; assim, `create_tables()` usa o banco temporário. A dependência
`get_db()` também é substituída para produzir sessões no mesmo banco.

## Implementação dos três cenários

Os testes de integração cobrem exatamente:

- compra autenticada de dois ingressos, pedido visível e estoque `10 -> 8`;
- rejeição de três ingressos quando há dois, sem pedido nem mudança de estoque;
- visitante redirecionado a `/login`, sem mudança de estoque.

Todas as interações com o comportamento da aplicação passam pela interface HTTP.

## Comandos de reprodução

```bash
uv lock --check
uv run pytest -q
uv run pytest -q
```

No ambiente do auditor, o mecanismo de captura temporária do executor removeu um
arquivo interno do Pytest. A suíte foi reproduzida duas vezes com captura de saída
explícita, sem alterar o comportamento testado:

```bash
uv run pytest -q --capture=sys
uv run pytest -q --capture=sys
```

## Evidências de isolamento

As duas execuções do autor terminaram com `3 passed` em `0.28s`. A auditoria
independente terminou com `3 passed` em `0.71s` e `0.70s`. O SHA-256 de
`scalepass.db` permaneceu igual a
`215e1ebf74c9910f757c55396ce911cba6292872f0aa1dc8d18d9ff27a6020c9`.

Detalhes e saídas estão em [evidence/README.md](evidence/README.md).

## Alternativas consideradas

- Configurar a URL por variável de ambiente antes dos imports exigiria controlar
  ordem e cache de módulos; não foi usada.
- Usar SQLite em memória aumentaria as diferenças entre conexões e contrariaria o
  objetivo de inspecionar um banco por teste.
- Fazer mock de SQLAlchemy diminuiria a fidelidade do teste de integração; não foi
  usado.
- Uma fábrica de aplicação eliminaria a mutação global, mas é uma refatoração
  arquitetural maior do que o resultado único deste desafio.

## Limitações restantes

- O engine temporário não recebe `dispose()` explícito no teardown. As sessões são
  fechadas e o arquivo é temporário, mas o ciclo de vida pode ser endurecido.
- A troca do engine global impede paralelismo seguro entre testes no mesmo processo.
- A combinação atual de FastAPI/Starlette emite um aviso de depreciação sobre o
  backend `httpx` do `TestClient`; ele não afeta os resultados deste desafio.

## Commits relevantes

- `10c8530` — implementação dos três testes e da fixture isolada.
- `challenge/001/start` — estado inicial reproduzível.
- `challenge/001/solved` — solução incorporada à `main`.
