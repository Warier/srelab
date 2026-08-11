# Desafio `ci-001`: quality gate no GitHub Actions

## Estado

`solved`.

## Resultado esperado

Executar automaticamente cobertura/testes, Mypy e Ruff em todo pull request e em
push para `main`, provando uma execução vermelha e outra verde.

## Pré-requisito

O repositório ainda não possui remoto. Crie um repositório no GitHub, configure
`origin` e envie `main` e a branch do desafio quando ele for ativado.

## Arquivo único

Crie `.github/workflows/quality.yml` com:

- eventos `pull_request` e `push` somente para `main`;
- `permissions: contents: read`;
- runner `ubuntu-latest` e `timeout-minutes: 10`;
- `actions/checkout@v5`;
- `astral-sh/setup-uv` fixado no SHA da versão `v9.0.0`;
- uv `0.9.30`, cache habilitado e Python `3.14`;
- `uv sync --locked --all-groups`;
- os gates abaixo sem `continue-on-error` ou `|| true`.

Use o action imutável:

```yaml
uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
```

## Gates obrigatórios

```bash
uv run --frozen pytest --cov=app --cov-report=term-missing
uv run --frozen mypy app
uv run --frozen ruff check .
uv run --frozen ruff format --check .
```

## Prova de funcionamento

1. Abra um PR com uma violação Ruff deliberada e confirme o job vermelho.
2. Em outro commit do mesmo PR, remova a violação e confirme o job verde.
3. Registre na evidência os links das duas execuções e qual etapa falhou.

Não faça merge do estado quebrado. A falha deliberada deve existir apenas no
histórico da branch de prova.

## Critérios de aceite

- workflow válido nos dois eventos;
- instalação totalmente baseada no lockfile;
- todos os gates locais aparecem no job;
- permissões mínimas e actions versionadas;
- execução quebrada realmente falha e correção realmente passa;
- nenhum segredo é necessário.

## Estudo direcionado

- workflow, event, job, step e runner;
- ambientes efêmeros e lockfile;
- permissões do `GITHUB_TOKEN`;
- cache versus artefato;
- branch protection e required status checks.

Referências:

- [GitHub: testar Python](https://docs.github.com/actions/automating-builds-and-tests/building-and-testing-python)
- [GitHub: sintaxe de workflows](https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax)
- [uv no GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/)

## Fora do escopo

Deploy, matrix de sistemas, publicação de imagem, secrets e runner self-hosted.

## Git

- Branch futura: `challenge/005-github-actions-quality-gate`.
- Tags futuras: `challenge/005/start` e `challenge/005/solved`.
