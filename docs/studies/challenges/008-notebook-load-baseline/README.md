# Desafio `load-001`: baseline de carga no notebook

## Estado

`active`.

## Resultado esperado

Versionar um cenário Locust pequeno, executá-lo a partir do PC principal contra o
ScalePass no notebook e registrar o comportamento atual da navegação e compra
sob os limites já definidos: 384 MiB e 0,5 CPU.

O resultado é um baseline, não uma meta de desempenho. Se houver lentidão ou
erros, registre-os; não corrija arquitetura, SQLite ou concorrência neste
desafio. A medição vem antes da intervenção.

```text
PC principal: Locust headless ── LAN ──> notebook: systemd -> Docker -> ScalePass
```

## Arquivos a criar ou alterar

- `load/locustfile.py`: cenário versionado;
- `load/README.md`: dados necessários e comando reprodutível;
- `pyproject.toml` e `uv.lock`: grupo `load` com Locust;
- `.gitignore`: artefatos gerados em `artifacts/load/`.

Não versione CSV, HTML, credenciais, IP do notebook nem resultados completos. O
resumo final cabe em `evidence/README.md`.

## Cenário fixo

Crie antes, manualmente no notebook, uma conta de carga e um evento de carga com
pelo menos 10.000 ingressos. Anote somente o ID do evento e forneça os valores
ao Locust por variáveis locais:

```bash
export SCALEPASS_LOAD_EMAIL='load@example.test'
export SCALEPASS_LOAD_PASSWORD='senha-local-de-carga'
export SCALEPASS_LOAD_EVENT_ID='1'
```

Não use a conta pessoal nem senha real. Vários usuários virtuais podem autenticar
com essa mesma conta: cada `HttpUser` possui o próprio cookie de sessão, mas todos
testam o mesmo fluxo funcional.

O `locustfile.py` deve falhar de modo explícito se qualquer variável obrigatória
estiver ausente. Depois do login, implemente estas tarefas com nomes estáveis no
relatório:

| Peso | Requisição | Resultado esperado |
|---:|---|---|
| 6 | `GET /api/events` | 200 |
| 3 | `GET /events/{event_id}` | 200 |
| 1 | `POST /events/{event_id}/buy` com `quantity=1` | 303 |

Faça login em `on_start` por `POST /login` com formulário `email` e `password`.
Valide os status com `catch_response=True`; redirecionamentos não devem ser
seguidos nas requisições POST, pois o cenário mede a rota que tomou a decisão.
Use espera entre 0,5 e 1,5 segundos para evitar um loop artificial sem pausa.

## Instalação e validação local

Adicione Locust somente ao grupo de desenvolvimento de carga:

```bash
uv add --group load locust
uv lock --check
uv run --group load locust --version
uv run --group load locust -f load/locustfile.py --list
```

Também mantenha os gates existentes verdes. O cenário deve passar no Ruff; Mypy
continua restrito a `app`, por decisão já registrada no projeto.

## Execução no PC principal

Com o serviço do notebook ativo e as três variáveis configuradas, execute duas
vezes o mesmo perfil, separadamente, a partir do PC principal. Substitua o alvo
pelo IP LAN atual do notebook:

```bash
mkdir -p artifacts/load
uv run --group load locust -f load/locustfile.py \
  --headless --host http://<IP_LAN_DO_NOTEBOOK>:8000 \
  -u 20 -r 2 -t 2m \
  --csv artifacts/load/notebook-run-1
```

Repita apenas trocando o sufixo para `notebook-run-2`. Os parâmetros significam:

- `-u 20`: máximo de vinte usuários virtuais simultâneos;
- `-r 2`: criação de dois usuários por segundo;
- `-t 2m`: duração total de dois minutos;
- `--headless`: execução reprodutível sem depender da interface web.

Antes de cada rodada, confirme que o serviço continua ativo. Durante a execução,
não altere limites, versão da imagem, rede ou dados de carga.

## Evidência exigida

Registre apenas uma tabela com as duas rodadas. Para cada rota nomeada, inclua
quantidade de requisições, falhas, RPS, mediana, p95 e p99. Inclua também versão
do Locust, perfil usado e limites do container. Não fixe uma meta de p95 ainda.

Se uma rota falhar, classifique a resposta observada (por exemplo, 400, 500 ou
timeout) e preserve os CSVs localmente para investigação; a correção pertence a
um desafio posterior. Compare as duas rodadas apenas como indicação de
variabilidade, não como benchmark científico.

## Critérios de aceite

- `locustfile.py` é configurável por ambiente e não possui segredo ou IP fixo;
- o cenário efetua login e as três rotas definidas, com nomes estáveis;
- duas rodadas headless usam exatamente `20` usuários, spawn `2/s` e `2m`;
- resultados por rota registram RPS, falhas, p95 e p99;
- Locust, testes, cobertura, Ruff e Mypy passam no PC principal;
- CSVs e credenciais não entram no Git.

## Estudo direcionado

- diferença entre usuário virtual, taxa de spawn, RPS, tempo de resposta e
  throughput;
- percentis (p50, p95 e p99) e por que média não descreve caudas;
- `HttpUser`, `on_start`, tasks ponderadas, `wait_time` e `catch_response`;
- efeitos de gerar carga de uma máquina separada do servidor;
- aquecimento, variabilidade e limites de um baseline sem observabilidade.

Referências:

- [Locust: escrever um locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html)
- [Locust: execução sem interface](https://docs.locust.io/en/stable/running-without-web-ui.html)
- [Locust: métricas e estatísticas](https://docs.locust.io/en/stable/retrieving-stats.html)

## Fora do escopo

Prometheus, Grafana, ajuste de performance, múltiplas instâncias, banco remoto,
testes de pico, caos e qualquer alteração corretiva na aplicação.

## Git

- Branch: `challenge/008-notebook-load-baseline`.
- Entrada: `challenge/008/start`.
- Conclusão: `challenge/008/solved`.
