# Evidências do desafio `ci-001`

## Estado

`verified`

## Workflow

- Arquivo: `.github/workflows/quality.yml`.
- PR: [#1](https://github.com/Warier/srelab/pull/1).
- Eventos: pull request e push na `main`.
- Gates: pytest-cov, Mypy, Ruff lint e Ruff format.

## Prova vermelha/verde

- [Execução vermelha](https://github.com/Warier/srelab/actions/runs/31470504561):
  `Run Ruff Lint` falhou com `I001` e `F401` pelo import não usado de `os`.
- [Execução verde](https://github.com/Warier/srelab/actions/runs/31470916691): todos os
  gates passaram após remover o import de prova.

## Auditoria local

- 12 testes passaram; cobertura 96,72%.
- Mypy sem erros em 6 arquivos.
- Ruff sem violações; 37 arquivos formatados.
