# Solução do desafio `visualization-001`

## Estado

`solved`.

Prometheus e Grafana executam no PC principal via Docker Compose, isolados em
`127.0.0.1`. O notebook permanece como alvo limitado e é consultado pela LAN em
`/metrics` a cada cinco segundos. O IP do notebook está somente na cópia local de
`prometheus.yml`; usuário e senha do Grafana ficam somente no `.env` local.

Grafana recebe datasource e dashboard por provisioning. O dashboard `ScalePass
HTTP` tem UID fixo e consulta `up`, `rate` do contador HTTP, percentual 5xx,
`histogram_quantile(0.95, ...)` e tráfego agrupado por rota. Assim, o JSON
versionado, e não alterações manuais na interface, é a fonte de verdade.

Sob carga de 200 usuários, os serviços permaneceram acessíveis e o target ficou
`UP`. Esta etapa torna o comportamento visível; não altera a implementação de
venda nem corrige a limitação concorrente conhecida do SQLite.
