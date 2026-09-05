# Evidências do desafio `operation-001`

## Estado

`verified`.

- Unidade: `scalepass.service` habilitada e ativa no notebook.
- Container: `Memory=402653184` (384 MiB), `NanoCpus=500000000` (0,5 CPU) e
  `RestartPolicy=no`.
- Rede: o PC principal obteve HTTP 200 em `GET /api/events` pela LAN.
- Recuperação: após `sudo docker kill scalepass`, systemd restaurou o serviço;
  `NRestarts=1` e a aplicação voltou a responder HTTP 200.
- Journal: registrou `Started ScalePass container` e a inicialização completa do
  Uvicorn após a falha.

## Gates do repositório

- `systemd-analyze verify deploy/systemd/scalepass.service` passou.
- 12 testes passaram; cobertura total de 96,72%.
- Mypy sem erros; Ruff sem violações; 40 arquivos formatados.
