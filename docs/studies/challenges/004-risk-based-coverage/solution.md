# Solução do desafio `testing-002`

## Estado

`documented`

## Solução

pytest-cov foi adicionado ao grupo `coverage`, com branch coverage, relatório de
linhas ausentes e limite mínimo de 90% configurados no `pyproject.toml`.

Foram adicionados testes HTTP para autenticação inválida, cadastro duplicado,
validação de evento, recurso inexistente e quantidades inválidas. As assertions
confirmam status e efeitos persistidos no banco temporário.

Durante a auditoria, uma cópia acidental dos três testes anteriores foi removida e
duas assertions foram fortalecidas: rejeição da segunda senha no cadastro duplicado
e ausência de pedido após quantidade inválida.

## Resultado

A cobertura subiu de 77% para 96,72%. Os 12 casos, Mypy e Ruff passaram sem
exclusões de cobertura. Consulte [evidence/README.md](evidence/README.md).
