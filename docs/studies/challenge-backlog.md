# Backlog direcionado de desafios

Este backlog define o foco esperado das próximas etapas. Somente o desafio ativo
possui enunciado completo; os demais ainda podem mudar conforme evidências do
projeto.

| Ordem | Estado | Resultado único | Ferramenta principal | Prova de conclusão |
|---|---|---|---|---|
| 001 | concluído | Testar a venda por HTTP sem tocar o banco local | Pytest + FastAPI TestClient | 3 cenários passam duas vezes; hash do banco não muda |
| 002 | concluído | Aplicar uma política automática de estilo | Ruff | `ruff check .` e `ruff format --check .` retornam zero |
| 003 | concluído | Tornar o código da aplicação verificável estaticamente | Mypy | `mypy app` retorna zero sem ignorar módulos inteiros |
| 004 | concluído | Medir quais regras de venda continuam sem teste | pytest-cov | relatório branch coverage e testes adicionados para lacunas acordadas |
| 005 | concluído | Executar testes em toda mudança proposta | GitHub Actions | PR propositalmente quebrado falha; correção fica verde |
| 006 | concluído | Gerar uma imagem executável e reproduzível | Docker | imagem sobe do zero, persiste dados e responde ao smoke test |
| 007 | concluído | Operar o processo no notebook com limite explícito | systemd + Docker | reinício automático, limites e acesso pela LAN comprovados |
| 008 | ativo | Medir o comportamento atual sob uma carga definida | Locust | cenário versionado produz RPS, erros e percentis por rota |
| 009 | planejado | Expor métricas HTTP essenciais | Prometheus client | erros, taxa e duração aparecem em `/metrics` e são consultáveis |
| 010 | planejado | Visualizar a saúde do serviço durante carga | Prometheus + Grafana | dashboard versionado explica uma degradação observada |
| 011 | planejado | Reproduzir venda incorreta sob concorrência | Pytest/Locust concorrente | teste falha demonstrando perda ou violação de estoque |
| 012 | planejado | Preservar a invariável de estoque no PostgreSQL | PostgreSQL | teste concorrente passa sem overselling |
| 013 | planejado | Corrigir uma consulta lenta de catálogo | `EXPLAIN ANALYZE` | plano e p95 melhoram sob dataset fixado |
| 014 | planejado | Evitar esgotamento de conexões ao escalar workers | PgBouncer | carga-alvo passa dentro do limite de conexões |
| 015 | planejado | Reduzir leituras repetidas sem servir estoque incorreto | Redis | hit rate medido e testes de invalidação passam |
| 016 | planejado | Retirar uma tarefa lenta da requisição | RabbitMQ + worker | latência HTTP cai e falhas vão para DLQ |
| 017 | planejado | Impedir duplicação causada por retry | chave de idempotência | mesma requisição repetida produz um único pedido |
| 018 | planejado | Subir duas instâncias sem depender de estado local | HAProxy/Nginx | carga alternada preserva login e resultados |
| 019 | planejado | Corrigir um risco de segurança reproduzido | ferramenta definida pelo incidente | exploit falha e teste de regressão passa |
| 020 | planejado | Conter falha em cascata de uma dependência lenta | Toxiproxy | timeout e recuperação atendem ao SLO definido |
| 021 | planejado | Reproduzir a dupla escrita não atômica no cadastro | PostgreSQL + Mailpit | matriz de falhas mostra conta sem e-mail e e-mail sem conta |
| 022 | planejado | Tornar a notificação de cadastro recuperável | outbox transacional + worker | usuário e outbox são atômicos; itens pendentes são entregues após matar o worker |

## Separação dos desafios iniciais

- 001 aprende isolamento e testes de integração;
- 002 aprende somente lint e formato com Ruff;
- 003 aprende somente análise de tipos com Mypy;
- 004 aprende cobertura como ferramenta de descoberta, não como nota;
- 005 compõe as verificações existentes em CI.

Isso evita instalar várias ferramentas sem compreender profundamente nenhuma.
