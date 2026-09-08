# Evidências do desafio `load-001`

## Estado

`verified`.

Perfil: Locust 2.46.5 executado no PC principal contra o notebook, com 20 usuários,
spawn de 2/s, duração de 2 minutos e container limitado a 384 MiB e 0,5 CPU.

| Rodada | Rota | Requisições | Falhas | RPS | p50 | p95 | p99 |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `GET /api/events` | 1365 | 0 | 11,46 | 15 ms | 43 ms | 69 ms |
| 1 | `GET /events/{id}` | 656 | 0 | 5,51 | 17 ms | 42 ms | 70 ms |
| 1 | `POST /events/{id}/buy` | 213 | 0 | 1,79 | 37 ms | 84 ms | 110 ms |
| 1 | `POST /login` | 20 | 0 | 0,17 | 24 ms | 39 ms | 39 ms |
| 2 | `GET /api/events` | 1377 | 0 | 11,56 | 14 ms | 35 ms | 63 ms |
| 2 | `GET /events/{id}` | 680 | 0 | 5,71 | 17 ms | 40 ms | 65 ms |
| 2 | `POST /events/{id}/buy` | 206 | 0 | 1,73 | 38 ms | 89 ms | 130 ms |
| 2 | `POST /login` | 20 | 0 | 0,17 | 27 ms | 66 ms | 66 ms |

O experimento exploratório com 100 usuários relatou uma ocorrência de `sqlite is
locked` em compra; ele não altera a conclusão do baseline e será tratado como
hipótese do desafio de concorrência.

## Gates do repositório

- 12 testes passaram; cobertura total de 96,72%.
- Ruff sem violações e 45 arquivos formatados.
- Mypy sem erros; `locust --version` confirmou a versão 2.46.5.
