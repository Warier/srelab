# Estratégia de Git do ScalePass

## Decisão

Aplicação, documentação, scripts de carga, infraestrutura e futuros serviços ficam
em um único repositório.

O histórico deve permitir que outra pessoa recupere o sistema antes de cada
desafio, tente uma solução própria e depois compare com a solução oficial.

## Por que um monorepo

- Código, configuração, documentação e evidências permanecem coerentes.
- Uma tag captura o estado completo de cada experimento.
- CI/CD evolui junto da aplicação.
- Não é necessário coordenar versões de vários repositórios para refazer o estudo.

Futuros microsserviços começam em diretórios como `services/payments/` ou
`services/notifications/`. Um serviço só muda de repositório se um desafio
demonstrar necessidade de permissões, ownership ou release independente.

## Branches

`main` contém o último estado oficial concluído e reproduzível. Aplicação e
documentação avançam juntas.

Cada desafio usa uma branch curta sem prefixo de ferramenta:

```text
challenge/001-isolated-http-tests
challenge/002-ruff-quality-gate
challenge/003-static-typing
```

Uma pessoa refazendo o laboratório pode usar seu próprio namespace:

```text
learn/alice/001-isolated-http-tests
```

Branches concluídas podem ser removidas. Tags são os checkpoints permanentes.

## Tags

Cada desafio possui duas tags anotadas:

```text
challenge/001/start
challenge/001/solved
```

- `start` contém a aplicação problemática, o enunciado e `solution.md` pendente.
- `solved` contém código, solução, evidências e documentação atualizados.

Versões do produto usam tags SemVer independentes, como `v0.1.0`. Nunca mova uma
tag pedagógica publicada.

## Commits

Não use obrigatoriamente um commit por lição. Prefira commits pequenos, coerentes e
executáveis:

```text
test: add temporary database fixture
test: cover successful ticket purchase
test: cover rejected ticket purchases
docs: record challenge 001 solution and evidence
```

Regras práticas:

- cada commit tem uma intenção principal;
- formatação mecânica e comportamento não são misturados;
- segredos, bancos, ambientes virtuais e artefatos grandes não são versionados;
- scripts e configurações usados para produzir evidências são versionados;
- resultados são resumidos em Markdown, JSON ou CSV pequeno.

## Fluxo do desafio 001

### Preparar o checkpoint

```bash
git switch main
git tag -a challenge/001/start -m "Start challenge 001: isolated HTTP tests"
git switch -c challenge/001-isolated-http-tests
```

### Investigar e implementar

Faça commits lógicos e registre hipóteses que influenciaram a solução. Não é
necessário manter um diário de cada comando.

### Documentar

Complete `solution.md` e `evidence/README.md`. Atualize arquitetura, currículo e
`AGENTS.md` quando o estado do projeto mudar.

### Incorporar e marcar

```bash
git switch main
git merge --no-ff challenge/001-isolated-http-tests
git tag -a challenge/001/solved -m "Solve challenge 001: isolated HTTP tests"
```

O merge commit preserva a fronteira pedagógica da etapa.

## Como outra pessoa refaz o estudo

```bash
git clone <url-do-repositorio>
cd scalepass
git switch --detach challenge/001/start
git switch -c learn/seu-nome/001-isolated-http-tests
```

Depois de tentar, a solução oficial pode ser consultada sem alterar a branch:

```bash
git show challenge/001/solved:docs/studies/challenges/001-isolated-http-tests/solution.md
```

Para o desafio seguinte, use a respectiva tag `challenge/NNN/start`.
