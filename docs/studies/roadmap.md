# Roteiro de evolução técnica

Este roteiro não é um calendário imutável. Cada etapa é motivada por comportamento
observado e encerrada com evidência.

Cada etapa segue o [ciclo de vida](challenge-lifecycle.md), os checkpoints da
[estratégia de Git](git-workflow.md) e o escopo do
[backlog direcionado](challenge-backlog.md).

## 1. Fundação de engenharia

- testes HTTP isolados com Pytest e banco temporário;
- lint e formatação em desafio próprio com Ruff;
- tipos estáticos em desafio próprio com Mypy;
- cobertura orientada a risco com pytest-cov;
- execução das verificações aprendidas no GitHub Actions;
- checkpoints reproduzíveis com branches e tags.

## 2. Entrega em um host limitado

- imagem de container reproduzível;
- configuração por ambiente e secrets;
- deploy no notebook Arch Linux;
- limites de CPU e memória;
- reinício, health check e rollback.

## 3. Visibilidade e baseline de carga

- cenário Locust reproduzível;
- logs estruturados e correlação;
- métricas RED e USE;
- Prometheus e Grafana;
- SLI, percentis e capacidade inicial.

## 4. Concorrência e banco de dados

- reprodução de venda concorrente incorreta;
- PostgreSQL, transações e isolamento;
- locks otimistas e pessimistas;
- índices, planos de execução, paginação e N+1;
- pool, PgBouncer, backups e recuperação.

## 5. Desacoplamento operacional

- cache Redis e invalidação;
- cache stampede;
- jobs assíncronos e RabbitMQ;
- retries, DLQ e backpressure;
- idempotência e transactional outbox.

## 6. Escala horizontal e resiliência

- múltiplas instâncias e balanceamento;
- remoção de estado local inadequado;
- timeouts, circuit breaker e bulkheads;
- falhas com Toxiproxy;
- SLOs, error budgets e chaos testing.

## 7. Segurança

- threat modeling e OWASP ASVS;
- senha, autorização e sessão;
- rate limiting, CSRF e validação;
- SAST, DAST, SCA, imagens e secrets;
- auditoria e resposta a incidente.

## 8. Sistemas distribuídos e entrega avançada

- monólito modular e limites de domínio;
- eventos, CDC e Debezium;
- consistência eventual e sagas;
- extração seletiva de serviços;
- Ansible, Terraform e estratégias de deploy;
- recuperação de desastre.

Kubernetes, Kafka e microsserviços não são objetivos isolados. Entram somente se
resolverem um problema observado.
