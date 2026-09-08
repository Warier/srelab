# Desafio `concurrency-001`: reproduzir colisão de vendas

## Estado

`active`.

## Resultado esperado

Construir um cenário Locust focado em uma única compra concorrente e classificar
o que ocorre quando 50 clientes tentam comprar um evento novo com 25 ingressos.
O resultado não é corrigir o problema: é produzir evidência que diferencie
rejeição de negócio, erro operacional e violação da invariável de estoque.

O sintoma inicial já foi observado no notebook: em uma rodada com 100 usuários,
uma compra falhou com `sqlite is locked`. A rota de compra lê o evento, reduz o
estoque em memória, cria o pedido e só então faz `commit`. SQLite aceita somente
um escritor por vez, portanto o agendamento das requisições importa.

## O que estudar

1. [Isolamento no SQLite](https://www.sqlite.org/isolation.html): leia a seção
   “Isolation Between Database Connections”; confirme por que existe um escritor
   por vez.
2. [Locking no SQLite](https://www.sqlite.org/lockingv3.html): leia “Overview” e
   “Locking”; relacione `SQLITE_BUSY` à disputa pelo arquivo, não a uma falha de
   autenticação.
3. [Transações e concorrência no dialeto SQLite do SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#transactions-with-sqlite-and-the-sqlite3-driver): observe as
   limitações do driver `sqlite3` e não conclua que `check_same_thread=False`
   resolve escrita concorrente.
4. [Locust: ciclo de vida e tarefas](https://docs.locust.io/en/stable/writing-a-locustfile.html): estude `on_start`, `@task`, `catch_response` e `StopUser`.

Conceitos exatos: concorrência de requisições, transação por requisição, lock de
escrita, resposta de negócio versus erro 5xx e invariável de domínio.

## Entregáveis

```text
load/concurrency/
├── README.md
└── locustfile.py
```

O cenário deve reutilizar as credenciais e o `SCALEPASS_LOAD_EVENT_ID` do `.env`
local existente. CSVs permanecem em `artifacts/load/` e não entram no Git.

## Experimento

1. No notebook, crie um evento novo, exclusivo para a prova, com exatamente 25
   ingressos. Use a conta de carga existente; a aplicação atual permite que ela
   compre mais de uma vez.
2. No PC principal, atualize apenas `SCALEPASS_LOAD_EVENT_ID` no `.env` ignorado.
3. Escreva uma classe Locust que faça login no `on_start`, execute **uma** chamada
   `POST /events/{id}/buy` com `quantity=1` e pare com `StopUser`. Não misture
   catálogo, navegação ou compras repetidas neste cenário.
4. Nomeie a requisição como `POST /events/[event_id]/buy`, use
   `allow_redirects=False` e `catch_response=True`. Preserve no resultado os
   status HTTP recebidos: 303 significa compra aceita; 400 pode ser rejeição por
   estoque; 5xx, timeout ou erro de conexão são falhas operacionais.
5. Rode no PC principal:

   ```bash
   mkdir -p artifacts/load

   uv run --env-file .env --group load locust \
     -f load/concurrency/locustfile.py \
     --headless \
     --host http://<IP_LAN_DO_NOTEBOOK>:8000 \
     -u 50 \
     -r 50 \
     -t 20s \
     --csv artifacts/load/concurrency-001
   ```

6. No notebook, consulte o evento recém-criado com `sqlite3` via Python dentro do
   container. Registre, para aquele `event_id`, `available_tickets`,
   `SUM(orders.quantity)` e `COUNT(orders.id)`. Como o evento começa limpo com
   25 unidades, a checagem é:

   ```text
   available_tickets + SUM(paid order quantities) == 25
   available_tickets >= 0
   ```

   Uma forma de consultar sem instalar ferramenta extra no container é adaptar o
   ID no comando abaixo, executado no notebook:

   ```bash
   docker exec scalepass python -c \
     "import sqlite3; c=sqlite3.connect('/data/scalepass.db'); print(c.execute(\"SELECT e.available_tickets, COALESCE(SUM(o.quantity), 0), COUNT(o.id) FROM events e LEFT JOIN orders o ON o.event_id=e.id AND o.status='paid' WHERE e.id=<EVENT_ID> GROUP BY e.id\").fetchone())"
   ```

## Critérios de aceite

1. Existe cenário dedicado com exatamente uma tentativa de compra por usuário
   virtual, login e parada explícita.
2. A rodada de 50 tentativas contra o evento novo de 25 unidades foi executada e
   os status foram classificados em 303, 400 e falhas operacionais.
3. A consulta pós-carga registra saldo, quantidade vendida e quantidade de pedidos
   para o mesmo evento.
4. A evidência conclui, com números, se houve `database is locked`, timeout,
   resposta 5xx e/ou violação da invariável. Se um sintoma não reaparecer, isso é
   um resultado válido e deve ser registrado sem inventar falha.
5. Nenhuma alteração de WAL, timeout SQLite, retry, lock de aplicação ou
   PostgreSQL é feita neste desafio.
6. `uv run --group lint ruff check .`, `uv run --group lint ruff format --check .`
   e `uv run --group typing mypy app` passam.

## Evidência enxuta

Em `evidence/README.md`, registre somente: comando, estoque inicial, contagem por
classe de status, tupla final `(estoque, quantidade_vendida, pedidos)`, se a
invariável passou e a mensagem mais representativa de falha. Não versione CSV,
log inteiro, IP, conta ou senha.

## Pistas progressivas

1. Comece derivando quais três números precisam ser iguais à realidade: tentativas
   HTTP, pedidos persistidos e unidades vendidas.
2. `StopUser` evita que um mesmo usuário virtual transforme uma única tentativa em
   uma sequência infinita de compras.
3. Se 400 aparecer, leia o corpo: ele pode representar estoque insuficiente e não
   indisponibilidade do banco.
4. Se `database is locked` aparecer, compare tentativas com pedidos persistidos
   antes de pensar em WAL ou retry.
5. Só no desafio seguinte será escolhida uma mudança de persistência e uma garantia
   transacional para corrigir o comportamento.

## Fora do escopo

- corrigir a rota de compra;
- trocar SQLite por PostgreSQL;
- ativar WAL ou aumentar `busy_timeout`;
- serializar compras com lock na aplicação;
- retries, fila, cache, múltiplas instâncias e alerta.

## Git

- Branch: `challenge/011-concurrent-sale-reproduction`.
- Entrada: `challenge/011/start`.
- Conclusão: `challenge/011/solved`.
