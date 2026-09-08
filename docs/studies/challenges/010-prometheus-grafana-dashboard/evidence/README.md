# Evidências do desafio `visualization-001`

## Estado

`complete`.

- Stack no PC principal: `prom/prometheus:v3.5.0` e `grafana/grafana:12.1.0`.
- `docker compose config` e `promtool check config` concluíram sem erro; ambos os
  endpoints locais de saúde responderam com sucesso.
- O target `scalepass` ficou `UP` ao coletar o notebook pela LAN.
- O dashboard provisionado contém cinco painéis: disponibilidade, RPS, 5xx, p95 e
  RPS por rota. As consultas estão no JSON versionado.
- Uma rodada exploratória com 200 usuários manteve Prometheus, Grafana e o target
  acessíveis, com séries HTTP chegando ao dashboard.
- Gates Python: testes, cobertura, Ruff e Mypy passam. O dashboard JSON e os
  arquivos de provisioning permitem repetir a configuração sem versionar IP,
  senha, volumes ou capturas de tela.
