# Backlog direcionado de desafios

Este backlog define o foco esperado das próximas etapas. Somente o desafio ativo
possui enunciado completo; os demais ainda podem mudar conforme evidências do
projeto.

| Ordem | Resultado único | Ferramenta principal | Prova de conclusão |
|---|---|---|---|
| 001 | Testar a venda por HTTP sem tocar o banco local | Pytest + FastAPI TestClient | 3 cenários passam duas vezes; hash do banco não muda |
| 002 | Aplicar uma política automática de estilo | Ruff | `ruff check .` e `ruff format --check .` retornam zero |
| 003 | Tornar o código da aplicação verificável estaticamente | Mypy | `mypy app` retorna zero sem ignorar módulos inteiros |
| 004 | Medir quais regras de venda continuam sem teste | pytest-cov | relatório branch coverage e testes adicionados para lacunas acordadas |
| 005 | Executar testes em toda mudança proposta | GitHub Actions | PR propositalmente quebrado falha; correção fica verde |
| 006 | Gerar uma imagem executável e reproduzível | Docker | imagem sobe do zero, persiste dados e responde ao smoke test |
| 007 | Operar o processo no notebook com limite explícito | systemd + Docker/Podman | reinício automático e limite de memória comprovados |
| 008 | Medir o comportamento atual sob uma carga definida | Locust | cenário versionado produz RPS e p95 repetíveis |
| 009 | Expor métricas HTTP essenciais | Prometheus client | erros, taxa e duração aparecem em `/metrics` e são consultáveis |
| 010 | Visualizar a saúde do serviço durante carga | Prometheus + Grafana | dashboard versionado explica uma degradação observada |
| 011 | Reproduzir venda incorreta sob concorrência | Pytest/Locust concorrente | teste falha demonstrando perda ou violação de estoque |
| 012 | Preservar a invariável de estoque no PostgreSQL | PostgreSQL | teste concorrente passa sem overselling |
| 013 | Corrigir uma consulta lenta de catálogo | `EXPLAIN ANALYZE` | plano e p95 melhoram sob dataset fixado |
| 014 | Evitar esgotamento de conexões ao escalar workers | PgBouncer | carga-alvo passa dentro do limite de conexões |
| 015 | Reduzir leituras repetidas sem servir estoque incorreto | Redis | hit rate medido e testes de invalidação passam |
| 016 | Retirar uma tarefa lenta da requisição | RabbitMQ + worker | latência HTTP cai e falhas vão para DLQ |
| 017 | Impedir duplicação causada por retry | chave de idempotência | mesma requisição repetida produz um único pedido |
| 018 | Subir duas instâncias sem depender de estado local | HAProxy/Nginx | carga alternada preserva login e resultados |
| 019 | Corrigir um risco de segurança reproduzido | ferramenta definida pelo incidente | exploit falha e teste de regressão passa |
| 020 | Conter falha em cascata de uma dependência lenta | Toxiproxy | timeout e recuperação atendem ao SLO definido |

## Separação dos desafios iniciais

Os antigos temas de “qualidade básica” foram deliberadamente separados:

- 001 aprende isolamento e testes de integração;
- 002 aprende apenas lint e formato com Ruff;
- 003 aprende apenas análise de tipos com Mypy;
- 004 aprende cobertura como ferramenta de descoberta, não como nota;
- 005 compõe as verificações existentes em CI.

Isso evita instalar cinco ferramentas sem compreender profundamente nenhuma delas.
