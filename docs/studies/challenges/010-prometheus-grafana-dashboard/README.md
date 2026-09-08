# Desafio `visualization-001`: dashboard Prometheus e Grafana

## Estado

`active`.

## Resultado esperado

Executar Prometheus e Grafana no PC principal, coletar `GET /metrics` do
ScalePass no notebook pela LAN e provisionar um dashboard versionado que mostre
disponibilidade, taxa de requisições, erros, p95 e tráfego por rota.

O notebook continua sendo somente o alvo limitado. O stack de observação roda no
PC principal para não disputar seus 384 MiB e 0,5 CPU com a aplicação medida.

```text
PC principal
  Prometheus ── scrape a cada 5 s ──LAN──> notebook /metrics
       │
       └── consulta PromQL ──> Grafana (dashboard versionado)
```

## Conceitos antes de começar

- O `prometheus-client` apenas expõe números no processo; Prometheus os busca
  periodicamente e guarda uma série temporal.
- Um scrape é uma amostra, não um log de cada requisição. A frequência de 5 s
  define a resolução observável neste laboratório.
- Grafana não armazena as métricas do ScalePass: ele consulta o Prometheus e as
  apresenta em painéis.
- Counter cresce desde o início do processo; use `rate(...[1m])` para obter uma
  taxa. O counter volta a zero após reinício, e Prometheus trata a queda como
  reset quando usado com `rate`.
- Histogram fornece buckets cumulativos. `histogram_quantile` estima p95 a partir
  de `*_bucket`, não a partir de uma média.

## Arquivos a criar

```text
observability/
├── compose.yaml
├── .env.example
├── prometheus/
│   └── prometheus.yml.example
└── grafana/
    ├── dashboards/scalepass-http.json
    └── provisioning/
        ├── dashboards/dashboard-provider.yaml
        └── datasources/prometheus.yaml
```

O `prometheus.yml` real e `observability/.env` são cópias locais, ignoradas pelo
Git. O primeiro contém o IP LAN do notebook; o segundo contém a senha de admin do
Grafana. Versione exemplos, não valores reais.

## Stack esperado

Use Docker Compose no PC principal. Não use `latest`: fixe uma versão explícita e
registrada para as imagens oficiais `prom/prometheus` e `grafana/grafana`.

O Compose deve:

- publicar Prometheus apenas em `127.0.0.1:9090` e Grafana em `127.0.0.1:3000`;
- ter volumes nomeados separados para dados de Prometheus e Grafana;
- montar a configuração real do Prometheus como somente leitura;
- montar os arquivos de provisioning e dashboard do Grafana como somente leitura;
- definir senha de admin por variável em `observability/.env` e desabilitar
  cadastro público no Grafana.

No `prometheus.yml`, configure `scrape_interval: 5s`, `scrape_timeout: 3s` e um
job `scalepass` que aponta para `<IP_LAN_DO_NOTEBOOK>:8000`, com `metrics_path:
/metrics`. Inclua também o próprio Prometheus como target interno. Use nomes de
job estáveis; eles serão labels nas consultas.

No provisioning de datasource, use `http://prometheus:9090` — o nome do serviço
resolve pela rede interna do Compose — e atribua um UID fixo, por exemplo
`prometheus`. No provider de dashboards, carregue JSON de uma pasta montada,
defina `allowUiUpdates: false` e use um UID fixo para o dashboard.

## Dashboard obrigatório

Crie e versione `scalepass-http.json` com ao menos cinco painéis, todos com fonte
Prometheus provisionada:

| Painel | Consulta PromQL de referência | O que responde |
|---|---|---|
| Target | `up{job="scalepass"}` | Prometheus consegue fazer scrape? |
| RPS | `sum(rate(scalepass_http_requests_total{job="scalepass"}[1m]))` | Quanto tráfego chega? |
| Erros 5xx | `100 * sum(rate(scalepass_http_requests_total{job="scalepass",status_code=~"5.."}[1m])) / sum(rate(scalepass_http_requests_total{job="scalepass"}[1m]))` | Que fração falha no servidor? |
| p95 | `histogram_quantile(0.95, sum by (le) (rate(scalepass_http_request_duration_seconds_bucket{job="scalepass"}[1m])))` | Como está a cauda de latência? |
| RPS por rota | `sum by (route) (rate(scalepass_http_requests_total{job="scalepass"}[1m]))` | Qual fluxo consome tráfego? |

Adicione título, unidade e legenda que tornem o painel legível sem abrir a query.
Mantenha o intervalo da dashboard em pelo menos cinco minutos durante a prova.

O painel de 5xx não trata 4xx como falha do servidor. Se quiser uma visão de
requisições inválidas, crie painel separado para `status_code=~"4.."`; misturar os
dois produz diagnóstico enganoso.

## Passo a passo de execução

1. Confirme `docker compose version` no PC principal. Crie os exemplos versionados
   e as cópias locais:

   ```bash
   cp observability/prometheus/prometheus.yml.example observability/prometheus/prometheus.yml
   cp observability/.env.example observability/.env
   ```

2. Edite somente as cópias locais: IP do notebook e senha de Grafana. Não use a
   senha de qualquer outro serviço.

3. Valide antes de iniciar:

   ```bash
   docker compose -f observability/compose.yaml config
   docker compose -f observability/compose.yaml run --rm --entrypoint promtool \
     prometheus check config /etc/prometheus/prometheus.yml
   ```

4. Inicie e valide saúde:

   ```bash
   docker compose -f observability/compose.yaml up -d
   curl --fail http://127.0.0.1:9090/-/ready
   curl --fail http://127.0.0.1:3000/api/health
   ```

   Abra `http://127.0.0.1:9090/targets` e espere `scalepass` ficar `UP`.

5. No Grafana local, confira a datasource provisionada e crie os painéis. Exporte
   o JSON para `grafana/dashboards/scalepass-http.json`; a cópia versionada é a
   fonte de verdade. Reinicie o Grafana ou aguarde o provider recarregar o arquivo.

6. Execute o cenário Locust por 30 s com 20 usuários. Observe RPS e p95 mudarem.
   Faça depois uma rodada exploratória de 100 usuários: procure p95, 5xx e estado
   do target, mas não corrija o SQLite neste desafio. Se não houver falha, registre
   que o comportamento não foi reproduzido em vez de inventar uma degradação.

## Critérios de aceite

- Prometheus faz scrape de `scalepass` com status `UP`;
- Grafana tem datasource e dashboard provisionados, sem configuração manual como
  única fonte de verdade;
- dashboard possui os cinco painéis e as consultas são semanticamente corretas;
- dados e senhas locais não entram no Git;
- `promtool check config`, `docker compose config` e os gates Python passam;
- evidência curta registra versões, target UP, consultas usadas e uma observação
  feita sob carga.

## Estudo direcionado

Leia primeiro:

- [Prometheus: getting started](https://prometheus.io/docs/prometheus/latest/getting_started/)
- [Prometheus: configuração de scrape](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
- [PromQL: `rate` e `histogram_quantile`](https://prometheus.io/docs/prometheus/latest/querying/functions/)
- [Grafana: provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Grafana: tutorial de dashboards e datasources como código](https://grafana.com/tutorials/provision-dashboards-and-data-sources/)

Vídeo recomendado: [Creating Grafana Dashboards for Prometheus — PromLabs](https://www.youtube.com/watch?v=EGgtJUjky8w).
Assista até a criação de Time Series, Gauge e Table; depois aplique as consultas
acima, em vez de copiar um dashboard genérico.

## Fora do escopo

Alertmanager, alertas, SLO formal, Loki, traces, Grafana Cloud, acesso externo,
HTTPS, autenticação de `/metrics`, correção de SQLite e deploy do stack no
notebook.

## Git

- Branch: `challenge/010-prometheus-grafana-dashboard`.
- Entrada: `challenge/010/start`.
- Conclusão: `challenge/010/solved`.
