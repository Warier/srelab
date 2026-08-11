# Solução do desafio `ci-001`

## Estado

`documented`

## Workflow e decisões

O workflow usa um job efêmero em `ubuntu-latest`, permissões somente de leitura,
timeout de 10 minutos, uv 0.9.30 com cache e Python 3.14. As dependências são
sincronizadas com `uv sync --locked --all-groups`.

Os mesmos gates locais executam com `uv run --frozen`: cobertura/testes, Mypy,
Ruff lint e verificação de formato. Nenhuma etapa usa `continue-on-error`.

## Prova vermelha/verde

Um import deliberadamente não usado produziu `I001/F401` e fez o job falhar na
etapa Ruff. Um segundo commit removeu a violação e deixou o mesmo PR verde,
demonstrando que o workflow bloqueia e libera alterações conforme os gates.

Links estão em [evidence/README.md](evidence/README.md).
