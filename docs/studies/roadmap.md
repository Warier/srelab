# Roteiro de evolução técnica

Este roteiro organiza possibilidades, não um calendário imutável. Cada etapa deve
ser motivada por um comportamento observado e encerrada com evidência antes/depois.

Cada etapa executada segue o processo de [ciclo de vida](challenge-lifecycle.md).
Seus estados reproduzíveis são preservados pelas tags descritas na
[estratégia de Git](git-workflow.md).

## 1. Fundação de engenharia

- ambiente e dependências reproduzíveis;
- testes unitários, integração e fluxo HTTP;
- lint, formatação, tipos e cobertura;
- primeira automação de CI;
- estratégia de branches e revisão.

## 2. Entrega em um host limitado

- empacotamento em container;
- configuração por ambiente e secrets;
- deploy no notebook Arch Linux;
- limites de CPU e memória;
- processo, reinício, health check e rollback.

## 3. Visibilidade e baseline de carga

- logs estruturados e correlação;
- métricas RED e USE;
- Prometheus e Grafana;
- cenários Locust reproduzíveis;
- SLI, latências percentis e capacidade inicial.

## 4. Concorrência e banco de dados

- venda concorrente e invariantes de estoque;
- PostgreSQL, transações e níveis de isolamento;
- locks otimistas e pessimistas;
- índices, planos de execução, paginação e N+1;
- pool de conexões e PgBouncer;
- backups e recuperação.

## 5. Desacoplamento operacional

- cache com Redis e invalidação;
- cache stampede e proteção contra avalanche;
- jobs assíncronos, RabbitMQ e workers;
- retries, dead-letter queues e backpressure;
- idempotência e transactional outbox.

## 6. Escala horizontal e resiliência

- múltiplas instâncias e balanceamento;
- remoção de estado local inadequado;
- timeouts, circuit breaker e bulkheads;
- testes de falha com Toxiproxy;
- SLOs, error budgets e chaos testing.

## 7. Segurança

- threat modeling e OWASP ASVS;
- armazenamento de senhas, autorização e sessão;
- rate limiting, CSRF e validação;
- SAST, DAST, SCA, scanning de imagens e secrets;
- trilha de auditoria e resposta a incidente.

## 8. Sistemas distribuídos e entrega avançada

- monólito modular e limites de domínio;
- eventos, CDC e Debezium;
- consistência eventual e sagas;
- extração seletiva de serviços;
- infraestrutura como código com Ansible/Terraform;
- deploy blue-green/canary e recuperação de desastre.

Kubernetes, Kafka e microsserviços não são objetivos isolados. Eles entram somente
se resolverem um problema que o estágio anterior tornou observável.
