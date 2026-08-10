# AGENTS.md — ScalePass

## Propósito deste repositório

ScalePass é uma aplicação web de criação de eventos e venda de ingressos. O produto
começa como um monólito pequeno e funcional e será evoluído em etapas conforme
necessidades concretas de qualidade, operação, segurança e escala aparecerem.

Este arquivo orienta agentes que trabalham no repositório. O `README.md` é voltado
exclusivamente a usuários e desenvolvedores do produto e não deve mencionar o
programa de estudos. Material pedagógico pertence a `docs/studies/`.

## Estado atual

- Estágio: `baseline-v0`.
- Desafio ativo: `foundation-001`, descrito em
  `docs/studies/challenges/001-foundation-and-tests/README.md`.
- Runtime: CPython 3.14, gerenciado por `uv`.
- Aplicação: monólito FastAPI com páginas Jinja2.
- Persistência: SQLite local por meio do SQLAlchemy.
- Autenticação: sessão por cookie e hash de senha propositalmente simples.
- Operação: processo único, sem containers, CI, métricas, traces ou logs
  estruturados.
- Testes automatizados: ainda não existem; criá-los é parte do primeiro desafio.

Antes de modificar código, leia, nesta ordem:

1. `README.md`;
2. `docs/architecture.md`;
3. `docs/domain.md`;
4. o desafio ativo em `docs/studies/challenges/`;
5. `docs/studies/curriculum.json`.

## Princípios de evolução

1. Não antecipe soluções de etapas futuras. Redis, PostgreSQL, filas,
   observabilidade, containers e microsserviços só devem entrar quando o desafio
   atual justificar sua presença.
2. Preserve uma aplicação executável ao final de cada mudança.
3. Prefira problemas plausíveis de produção a falhas artificiais ou código
   deliberadamente ilegível.
4. Não faça refatorações amplas sem uma hipótese, uma necessidade do produto ou
   um critério mensurável.
5. Registre mudanças arquiteturais relevantes em `docs/architecture.md` e, quando
   houver uma escolha entre alternativas significativas, em um ADR dentro de
   `docs/decisions/`.
6. Atualize `docs/studies/curriculum.json` apenas com evidência. Usar uma
   ferramenta uma vez significa `introduced`, não `well_covered`.
7. Um tema só vai para `well_covered` quando já tiver sido aplicado, medido,
   operado e discutido com trade-offs em mais de um cenário relevante.

## Protocolo dos desafios

Cada desafio deve conter sintoma, contexto, restrições, sugestões de estudo e
critérios de aceite. A causa exata e uma receita completa de solução não devem
ser entregues antes da investigação do aluno.

Ao ajudar durante um desafio, ofereça pistas progressivas:

1. área conceitual a investigar;
2. evidências ou medições que podem confirmar hipóteses;
3. componentes ou arquivos possivelmente envolvidos;
4. alternativas de solução e trade-offs;
5. implementação direta somente quando solicitada.

Depois da solução, registre resultados antes/depois e um post-mortem curto. Não
trate a simples instalação de uma ferramenta como conclusão do aprendizado.

## Rotas prováveis a partir do estado atual

A ordem pode mudar conforme as evidências, mas a progressão esperada é:

1. ambiente reproduzível, testes e primeira automação de qualidade;
2. empacotamento e deploy no notebook Arch Linux;
3. observabilidade mínima e testes de carga;
4. concorrência na venda e migração para PostgreSQL;
5. índices, consultas e pool de conexões;
6. cache e invalidação;
7. filas, retries, idempotência e outbox;
8. múltiplas instâncias e balanceamento;
9. segurança ofensiva e defensiva;
10. resiliência, SLOs e chaos testing;
11. CDC, eventos e possível extração seletiva de serviços;
12. infraestrutura como código, CI/CD avançado e recuperação de desastre.

Não presuma que a etapa final precisa ser uma arquitetura de microsserviços. Um
monólito modular pode continuar sendo a solução correta.

## Convenções do código

- Código, nomes de módulos e identificadores em inglês.
- Documentação e mensagens de interface podem ser em português.
- Valores monetários são armazenados em centavos inteiros.
- Rotas devem permanecer pequenas; regras que crescerem devem migrar para uma
  camada de serviço quando houver necessidade concreta.
- A sessão do SQLAlchemy é criada por requisição em `app/database.py`.
- Alterações de esquema futuras devem usar migrações; o baseline ainda usa
  `Base.metadata.create_all()` por simplicidade.
- Nunca registre senha, cookie de sessão ou segredo.

## Verificações do estágio atual

Enquanto o desafio `foundation-001` não estiver concluído, a verificação mínima é:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Depois do desafio, este bloco deverá incluir lint, análise de tipos e testes.

## Política de documentação

- `README.md`: apresentação real do produto, instalação e uso.
- `docs/architecture.md`: arquitetura que existe hoje, não a arquitetura desejada.
- `docs/domain.md`: regras e fluxos funcionais.
- `docs/development.md`: instruções detalhadas para desenvolvimento local.
- `docs/studies/roadmap.md`: direção pedagógica de longo prazo.
- `docs/studies/curriculum.json`: inventário enxuto do que falta, foi introduzido
  ou já foi bem coberto.
- `docs/studies/git-workflow.md`: estratégia de branches, commits e checkpoints.
- `docs/studies/challenge-lifecycle.md`: formato obrigatório de um desafio.
- `docs/studies/challenges/`: enunciado, solução e evidências de cada desafio.
- `docs/decisions/`: ADRs de decisões importantes.

## Git e checkpoints pedagógicos

O projeto usa um único repositório. Aplicação, documentação, infraestrutura e
futuros serviços permanecem juntos para preservar a evolução completa.

- `main` representa o último estado oficial concluído.
- Cada desafio usa uma branch curta `codex/challenge/NNN-slug`.
- A entrada recebe uma tag anotada `challenge/NNN/start`.
- A conclusão documentada recebe `challenge/NNN/solved`.
- Versões do produto usam tags SemVer separadas, como `v0.1.0`.
- Commits devem ser pequenos e coerentes; não existe a obrigação de um único
  commit por lição.
- Evidências grandes não entram no Git. Scripts, configurações e resumos pequenos
  são versionados.

Consulte `docs/studies/git-workflow.md` antes de iniciar ou concluir um desafio.

Sempre mantenha o estado declarado aqui sincronizado com o projeto real.
