# Solução do desafio `observability-001`

## Estado

`documented`.

`app/metrics.py` define um Counter e um Histogram no registry padrão. O middleware
mede toda requisição de aplicação, preserva status 500 em exceções e usa o
template resolvido pelo FastAPI; isso evita uma série diferente para cada ID.

`GET /metrics` usa o formato do `prometheus-client` e é excluído da medição. A
carga curta no notebook aumentou as séries de catálogo, detalhe e compra. Ainda
não há Prometheus server, consulta PromQL ou dashboard.
