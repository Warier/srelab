# Carga do ScalePass

Este diretório contém o cenário Locust usado para medir a navegação e a compra
de ingressos no ScalePass.

## Pré-requisitos

- `uv` instalado;
- dependências do projeto sincronizadas;
- ScalePass em execução no notebook;
- uma conta exclusiva para carga;
- um evento exclusivo para carga com pelo menos 10.000 ingressos.

Não use conta pessoal, senha real ou um evento usado normalmente.

## Configuração local

Crie um arquivo `.env` na raiz do projeto. Ele não deve ser versionado.

```dotenv
SCALEPASS_LOAD_EMAIL=load@example.test
SCALEPASS_LOAD_PASSWORD=senha-local-de-carga
SCALEPASS_LOAD_EVENT_ID=1
```

O arquivo `locustfile.py` falha explicitamente se alguma dessas variáveis não
estiver definida.

## Cenário

Cada usuário virtual faz login uma vez e executa estas ações:

| Peso | Rota | Resultado esperado |
|---:|---|---:|
| 6 | `GET /api/events` | 200 |
| 3 | `GET /events/{event_id}` | 200 |
| 1 | `POST /events/{event_id}/buy` com `quantity=1` | 303 |

Após cada tarefa, o usuário espera entre 0,5 e 1,5 segundos.

## Validação local

```bash
uv sync --locked
uv run --env-file .env --group load locust --version
uv run --env-file .env --group load locust -f load/locustfile.py --list
```

## Execução com interface

Substitua o endereço pelo IP LAN atual do notebook:

```bash
uv run --env-file .env --group load locust \
  -f load/locustfile.py \
  --host http://<IP_LAN_DO_NOTEBOOK>:8000
```

Abra `http://localhost:8089` no navegador do computador que executa o Locust.

## Execução headless do baseline

Execute no PC principal, com o ScalePass ativo no notebook:

```bash
mkdir -p artifacts/load

uv run --env-file .env --group load locust \
  -f load/locustfile.py \
  --headless \
  --host http://<IP_LAN_DO_NOTEBOOK>:8000 \
  -u 20 \
  -r 2 \
  -t 2m \
  --csv artifacts/load/notebook-run-1
```

Repita a mesma execução, alterando apenas o sufixo:

```bash
uv run --env-file .env --group load locust \
  -f load/locustfile.py \
  --headless \
  --host http://<IP_LAN_DO_NOTEBOOK>:8000 \
  -u 20 \
  -r 2 \
  -t 2m \
  --csv artifacts/load/notebook-run-2
```

Os CSVs, relatórios HTML e credenciais permanecem fora do Git.
