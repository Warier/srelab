# Desafio `typing-001`: contratos de retorno verificados com Mypy

## Estado

`solved`

## Resultado único esperado

Configurar Mypy em modo estrito para `app/` e corrigir os contratos de retorno das
rotas até a análise terminar sem erros, sem esconder diagnósticos.

## Baseline conhecido

Uma execução temporária de Mypy 2.3.0 encontrou:

```text
8 erros return-value em app/main.py
6 arquivos verificados
```

As funções afetadas estão anotadas como se sempre retornassem `HTMLResponse`, mas
alguns caminhos retornam `RedirectResponse`. O comportamento HTTP funciona; o
contrato estático é que não descreve todos os caminhos possíveis.

## Preparação

Adicione Mypy somente ao grupo `typing`:

```bash
uv add --group typing mypy
```

No `pyproject.toml`, configure:

```toml
[tool.mypy]
python_version = "3.14"
strict = true
files = ["app"]
show_error_codes = true
```

Depois capture seu próprio baseline:

```bash
uv run --group typing mypy app
```

## Trabalho a realizar

1. Leia as oito funções indicadas pelo Mypy e identifique todos os tipos realmente
   retornados por cada caminho.
2. Escolha contratos honestos: uma união explícita ou uma classe-base adequada são
   possibilidades. Compare clareza, precisão e facilidade de evolução.
3. Altere somente anotações e imports necessários. Não mude redirects, templates,
   status HTTP ou regras de negócio para satisfazer o checker.
4. Execute a prova final e registre apenas o resumo em `evidence/README.md`.

## Regras

- Não use `# type: ignore`, `Any`, `cast()` ou assertions artificiais apenas para
  silenciar os oito erros.
- Não desative `strict`, `return-value` ou arquivos específicos.
- Não use `ignore_missing_imports` nem `follow_imports = "skip"`.
- Não instale `sqlalchemy-stubs`, `sqlalchemy2-stubs` ou o plugin Mypy do
  SQLAlchemy. Os modelos já usam `Mapped` e `mapped_column` do SQLAlchemy 2.
- Não altere testes para acomodar uma mudança funcional.

## Prova final

```bash
uv lock --check
uv run --group typing mypy app
uv run --group lint ruff check .
uv run --group lint ruff format --check .
uv run pytest -q
```

## Critérios de aceite

1. Mypy está no dependency group `typing`, não nas dependências de runtime.
2. A configuração possui exatamente a versão-alvo, modo estrito, arquivos e error
   codes definidos acima.
3. `mypy app` termina com código `0` e informa seis arquivos sem erros.
4. Nenhum mecanismo proibido foi usado para ocultar os diagnósticos.
5. Ruff e os três testes continuam passando.
6. O diff não altera comportamento HTTP.
7. A evidência curta contém baseline, decisão de modelagem e prova final.

## Estudo direcionado

Estude:

- checagem estática versus validação em runtime;
- o que `strict` ativa e por que funções anotadas são checadas integralmente;
- compatibilidade de tipos de retorno e princípio de substituição;
- união de tipos versus classe-base comum;
- inferência e narrowing;
- diferença entre corrigir um contrato e silenciar um checker.

Referências oficiais:

- [Mypy: primeiros passos e modo estrito](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [Mypy: anotações de tipos](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [Mypy: configuração](https://mypy.readthedocs.io/en/stable/config_file.html)
- [SQLAlchemy 2: tipagem nativa e situação do plugin Mypy](https://docs.sqlalchemy.org/en/20/orm/extensions/mypy.html)

## Fora do escopo

- tipar `tests/`;
- criar schemas Pydantic;
- cobertura, CI ou pre-commit;
- refatorar rotas em serviços;
- corrigir o warning do TestClient;
- aumentar ou reduzir o conjunto de regras do Ruff.

## Checkpoint Git

- Tag inicial: `challenge/003/start`.
- Branch: `challenge/003-static-typing`.
- Tag futura: `challenge/003/solved`.
- Solução: [solution.md](solution.md).
