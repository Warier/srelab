# Evidências do desafio `observability-001`

## Estado

`verified`.

- `GET /metrics` respondeu 200 no notebook durante carga pela LAN.
- O scrape apresentou séries normalizadas: `GET /api/events` (341),
  `GET /events/{event_id}` (144), `POST /login` (20) e
  `POST /events/{event_id}/buy` (48), todas com status esperado.
- O histograma de compra registrou 48 observações e soma de 1,847 s; a série não
  contém IDs concretos nem a rota `/metrics`.
- A carga curta utilizou 20 usuários, spawn de 2/s e duração de 30 segundos.

## Gates do repositório

- 15 testes passaram; cobertura total de 96,06%.
- Mypy sem erros; Ruff sem violações e 50 arquivos formatados.
