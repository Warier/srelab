# AGENTS.md — ScalePass

## Propósito deste repositório

ScalePass é uma aplicação web de criação de eventos e venda de ingressos. O produto
começa como um monólito pequeno e funcional e será evoluído conforme necessidades
concretas de qualidade, operação, segurança e escala aparecerem.

Este arquivo orienta agentes que trabalham no repositório. O `README.md` é voltado
exclusivamente a usuários e desenvolvedores do produto e não deve mencionar o
programa de estudos. Material pedagógico pertence a `docs/studies/`.

## Estado atual

- Estágio: `baseline-v0`.
- Desafio ativo: `operation-001`, descrito em
  `docs/studies/challenges/007-notebook-service-operation/README.md`.
- Runtime: CPython 3.14, gerenciado por `uv`.
- Aplicação: monólito FastAPI com páginas Jinja2.
- Persistência: SQLite local por meio do SQLAlchemy.
- Autenticação: sessão por cookie e hash de senha propositalmente simples.
- Operação: processo único, sem containers, CI, métricas, traces ou logs
  estruturados.
- Testes automatizados: três testes de integração HTTP isolados com Pytest.

Antes de modificar código, leia, nesta ordem:

1. `README.md`;
2. `docs/architecture.md`;
3. `docs/domain.md`;
4. o desafio ativo em `docs/studies/challenges/`;
5. `docs/studies/curriculum.json`.

## Princípios de evolução

1. Não antecipe soluções futuras. Redis, PostgreSQL, filas, observabilidade,
   containers e microsserviços só entram quando o desafio justificar.
2. Preserve uma aplicação executável ao final de cada mudança.
3. Prefira problemas plausíveis a falhas artificiais ou código ilegível.
4. Não faça refatorações amplas sem hipótese, necessidade ou critério mensurável.
5. Registre mudanças arquiteturais em `docs/architecture.md` e decisões relevantes
   em um ADR dentro de `docs/decisions/`.
6. Atualize `curriculum.json` apenas com evidência. Usar uma ferramenta uma vez
   significa `introduced`, não `well_covered`.
7. Um tema só vai para `well_covered` depois de aplicado, medido, operado e
   discutido com trade-offs em mais de um cenário.

## Protocolo dos desafios

Cada desafio deve possuir um resultado técnico principal, ferramentas definidas,
estudo direcionado, critérios falseáveis e evidências reproduzíveis. Não agrupe
testes, lint, tipos, cobertura e CI em um único exercício.

Ao ajudar durante um desafio, ofereça pistas progressivas:

1. conceito ou seção de documentação a estudar;
2. evidência que pode confirmar a hipótese;
3. componente possivelmente envolvido;
4. alternativas e trade-offs;
5. implementação direta somente quando solicitada.

Depois da solução, registre resultados antes/depois e um post-mortem curto. A
simples instalação de uma ferramenta não conclui um aprendizado.

## Rotas prováveis

1. testes HTTP isolados com Pytest;
2. lint e formato com Ruff;
3. tipos estáticos com Mypy;
4. cobertura orientada a risco com pytest-cov;
5. integração contínua com GitHub Actions;
6. empacotamento e deploy no notebook Arch Linux;
7. observabilidade mínima e testes de carga;
8. concorrência na venda e migração para PostgreSQL;
9. índices, consultas e pool de conexões;
10. cache e invalidação;
11. filas, retries, idempotência e outbox;
12. múltiplas instâncias e balanceamento;
13. segurança ofensiva e defensiva;
14. resiliência, SLOs e chaos testing;
15. CDC, eventos e possível extração seletiva de serviços;
16. infraestrutura como código e recuperação de desastre.

Não presuma que o final precisa ser microsserviços. Um monólito modular pode
continuar sendo a solução correta.

## Convenções do código

- Código, módulos e identificadores em inglês.
- Documentação e interface podem ser em português.
- Valores monetários são armazenados em centavos inteiros.
- Rotas permanecem pequenas; regras migram para serviço quando houver necessidade.
- A sessão SQLAlchemy é criada por requisição em `app/database.py`.
- Alterações de esquema futuras usam migrações; o baseline ainda usa
  `Base.metadata.create_all()`.
- Nunca registre senha, cookie de sessão ou segredo.

## Verificações do estágio atual

Verificações atualmente incorporadas ao projeto:

```bash
uv sync --locked
uv run pytest -q
uv run --group coverage pytest --cov=app --cov-report=term-missing
uv run --group lint ruff check .
uv run --group lint ruff format --check .
uv run --group typing mypy app
uv run uvicorn app.main:app --reload
```

Ruff, Mypy, cobertura, CI e Docker foram incorporados. A operação no notebook
está no desafio ativo.

## Política de documentação

- `README.md`: produto, instalação e uso.
- `docs/architecture.md`: arquitetura que existe hoje.
- `docs/domain.md`: regras e fluxos funcionais.
- `docs/development.md`: desenvolvimento local.
- `docs/studies/roadmap.md`: direção pedagógica de longo prazo.
- `docs/studies/challenge-backlog.md`: próximos resultados e provas concretas.
- `docs/studies/curriculum.json`: temas pendentes, introduzidos e bem cobertos.
- `docs/studies/git-workflow.md`: branches, commits e checkpoints.
- `docs/studies/challenge-lifecycle.md`: formato obrigatório de um desafio.
- `docs/studies/challenges/`: enunciado, solução e evidências.
- `docs/decisions/`: ADRs.

## Git e checkpoints pedagógicos

O projeto usa um único repositório. Aplicação, documentação, infraestrutura e
futuros serviços permanecem juntos.

- `main` representa o último estado oficial concluído.
- Cada desafio usa uma branch `challenge/NNN-slug`.
- A entrada recebe `challenge/NNN/start`.
- A conclusão documentada recebe `challenge/NNN/solved`.
- Versões do produto usam SemVer, como `v0.1.0`.
- Commits são pequenos e coerentes; não existe um único commit obrigatório por
  lição.
- Evidências grandes não entram no Git; scripts, configurações e resumos entram.

Consulte `docs/studies/git-workflow.md` antes de iniciar ou concluir um desafio e
mantenha o estado declarado aqui sincronizado com o projeto real.
