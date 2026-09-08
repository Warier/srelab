# Desafio `observability-001`: métricas HTTP Prometheus

## Estado

`active`.

## Resultado esperado

Expor métricas HTTP úteis em `GET /metrics` no mesmo processo FastAPI e provar,
durante uma carga curta contra o notebook, que taxa, status e duração podem ser
consultados sem logs nem Grafana.

Este desafio introduz apenas a instrumentação e a exposição Prometheus. Ele não
instala servidor Prometheus, Grafana, logs estruturados ou tracing.

## Arquivos esperados

- `app/metrics.py`: definição das métricas e funções auxiliares;
- `app/main.py`: middleware HTTP e endpoint `/metrics`;
- testes de integração para a exposição e os rótulos;
- `pyproject.toml` e `uv.lock`: `prometheus-client` como dependência de runtime.

## Métricas obrigatórias

Use `Counter` e `Histogram` do `prometheus-client` com estes nomes expostos:

```text
scalepass_http_requests_total
scalepass_http_request_duration_seconds
```

As duas devem usar somente os rótulos `method`, `route` e `status_code`. `route`
precisa ser o template declarado pelo FastAPI, como `/events/{event_id}`, e nunca
o caminho concreto com IDs. Para uma rota não encontrada, use um valor fixo como
`unmatched`.

Isso é requisito de segurança operacional: usar `/events/1`, `/events/2` e assim
por diante cria uma série nova por ID e destrói a cardinalidade do Prometheus.

O contador permite calcular taxa por `rate(...)` futuramente. O histograma deve
usar segundos e seus buckets, `sum` e `count` permitirão p95/p99 em PromQL depois.
Não tente criar um campo `p95` na aplicação.

## Implementação guiada

1. Adicione a biblioteca ao runtime:

   ```bash
   uv add prometheus-client
   uv lock --check
   ```

2. Em `app/metrics.py`, defina o Counter e Histogram no registry padrão, com
   descrições úteis e os três rótulos exigidos. Use o nome-base
   `scalepass_http_requests`; o cliente expõe automaticamente o sufixo `_total`
   para counters.

3. Crie middleware HTTP em torno de `call_next`. Meça com `time.perf_counter()`;
   após a resposta, leia o template de rota do scope, obtenha status e incremente
   as duas métricas. Em exceção não tratada, registre status `500` e relance a
   exceção para não alterar o comportamento HTTP existente.

4. Exclua `/metrics` da própria instrumentação. Caso contrário, cada scrape
   adiciona tráfego artificial às séries que ele está lendo.

5. Implemente `GET /metrics` com `generate_latest()` e `CONTENT_TYPE_LATEST`.
   O endpoint é público nesta fase, porque ainda só existe na LAN de laboratório;
   restrição por rede/proxy será tratada quando houver deploy mais exposto.

## Testes exigidos

Após chamar `GET /api/events`, faça scrape de `/metrics` e prove que existem:

- uma série `scalepass_http_requests_total` para `GET`, rota `/api/events` e
  status `200`;
- o `scalepass_http_request_duration_seconds_count` com os mesmos rótulos;
- uma requisição inexistente que resulta em `404` usando o rótulo fixo
  `unmatched`, não o caminho concreto;
- `/metrics` responde 200, usa o content type de Prometheus e não gera série
  para a própria rota.

Use comparações `>=` em counters globais: os testes e as requisições anteriores
compartilham o registry do processo.

## Prova no notebook

Depois dos gates locais, atualize a imagem no notebook. Uma imagem nova não muda
um container existente: pare o serviço, recrie apenas o container usando as mesmas
opções do desafio 007 e o mesmo volume `scalepass-data`, então inicie o systemd.
Antes de removê-lo, confira a configuração existente com `docker inspect`.

No PC principal, gere carga curta e faça scrape da métrica:

```bash
uv run --env-file .env --group load locust -f load/locustfile.py \
  --headless --host http://<IP_LAN_DO_NOTEBOOK>:8000 \
  -u 20 -r 2 -t 30s

curl --fail -s http://<IP_LAN_DO_NOTEBOOK>:8000/metrics \
  | rg '^scalepass_http_(requests_total|request_duration_seconds_(bucket|sum|count))'
```

O serviço deve continuar disponível pela LAN. O scrape é evidência manual; o
servidor Prometheus que fará scrapes periódicos entra somente depois.

## Critérios de aceite

- contador e histograma obrigatórios são expostos em `/metrics`;
- rótulos são somente `method`, `route` e `status_code`, com rota normalizada;
- `/metrics` não conta a si próprio;
- testes cobrem 200, 404 normalizado e formato de exposição;
- carga curta no notebook aumenta séries de pelo menos catálogo, detalhe e compra;
- testes, cobertura, Ruff e Mypy permanecem verdes;
- evidência curta contém poucas linhas de `/metrics` e o resultado da carga.

## Estudo direcionado

- Counter, Histogram, labels e diferença entre medição no cliente e no servidor;
- séries temporais, cardinalidade e templates de rota;
- `rate`, `_count`, `_sum` e buckets cumulativos;
- middleware ASGI/FastAPI e tratamento de exceções;
- scrape pull-based e por que o endpoint não deve ser instrumentado.

Referências:

- [prometheus-client: Counter](https://prometheus.github.io/client_python/instrumenting/counter/)
- [prometheus-client: Histogram](https://prometheus.github.io/client_python/instrumenting/histogram/)
- [prometheus-client: exposição HTTP](https://prometheus.github.io/client_python/exporting/http/)

## Fora do escopo

Prometheus server, PromQL, Grafana, alertas, OpenTelemetry, logs estruturados,
traces, métricas de banco, autenticação de `/metrics` e correção do SQLite.

## Git

- Branch: `challenge/009-http-prometheus-metrics`.
- Entrada: `challenge/009/start`.
- Conclusão: `challenge/009/solved`.
