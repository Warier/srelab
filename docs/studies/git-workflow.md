# Estratégia de Git do ScalePass

## Decisão

Aplicação, documentação, scripts de carga, infraestrutura e futuros serviços ficam
em um único repositório.

O histórico deve permitir que outra pessoa recupere o sistema antes de cada
desafio, tente uma solução própria e depois compare seu resultado com a solução
oficial documentada.

## Por que um monorepo

- Código, configuração, documentação e evidências pequenas permanecem coerentes.
- Uma tag captura o estado completo de cada experimento.
- CI/CD evolui junto da aplicação.
- Uma pessoa não precisa coordenar versões de vários repositórios para refazer o
  estudo.

Quando surgirem microsserviços, eles começam em diretórios como
`services/payments/` ou `services/notifications/`. Separá-los em outros repositórios
só será considerado se houver uma necessidade demonstrada de permissões, ownership
ou ciclo de release independente. Essa separação seria um desafio e uma decisão
arquitetural, não uma organização feita antecipadamente.

## Branches

`main` contém o último estado oficial concluído e reproduzível. Aplicação e
documentação avançam juntas.

Cada desafio usa uma branch curta:

```text
codex/challenge/001-foundation-tests
codex/challenge/002-first-ci
codex/challenge/003-limited-host-deploy
```

Uma pessoa refazendo o laboratório pode usar seu próprio namespace:

```text
learn/alice/001-foundation-tests
```

Branches concluídas podem ser removidas. As tags são os checkpoints permanentes.

## Tags

Cada desafio possui duas tags anotadas:

```text
challenge/001/start
challenge/001/solved
```

- `start` contém a aplicação problemática, o enunciado e uma solução ainda
  marcada como `pending`.
- `solved` contém a solução, evidências, documentação atualizada e o código
  oficial corrigido.

Versões do produto usam tags SemVer independentes, como `v0.1.0`. Nunca mova uma
tag pedagógica já publicada.

## Commits

Não use obrigatoriamente um commit por lição. Uma lição pode conter refatoração,
testes, automação e documentação, e juntá-los em um commit tornaria a revisão pior.

Prefira commits pequenos, coerentes e executáveis:

```text
test: add isolated database fixture
refactor: make application dependencies configurable
ci: run quality checks on pull requests
docs: record challenge 001 solution and evidence
```

Regras práticas:

- cada commit deve ter uma intenção principal;
- não misture formatação mecânica e mudança de comportamento;
- não versione segredos, bancos locais, ambientes virtuais ou artefatos grandes;
- versione scripts e configurações usados para produzir evidências;
- resuma resultados em Markdown, JSON ou CSV pequeno;
- dashboards relevantes podem ser exportados como JSON;
- logs completos, dumps e relatórios HTML gerados ficam fora do Git.

## Fluxo de um desafio

### Preparar o checkpoint

O mantenedor registra o baseline, cria a tag de entrada e abre a branch:

```bash
git switch main
git tag -a challenge/001/start -m "Start challenge 001: foundation and tests"
git switch -c codex/challenge/001-foundation-tests
```

### Investigar e implementar

Faça commits lógicos. Registre hipóteses e resultados que influenciaram decisões;
não é necessário manter um diário de cada comando executado.

### Documentar a solução

Complete `solution.md` e as evidências pequenas do desafio. Atualize arquitetura,
currículo e `AGENTS.md` quando o estado do projeto mudar.

### Incorporar e marcar a conclusão

Depois da revisão:

```bash
git switch main
git merge --no-ff codex/challenge/001-foundation-tests
git tag -a challenge/001/solved -m "Solve challenge 001: foundation and tests"
```

O merge commit torna visível o limite pedagógico. Squash ou rebase podem ser úteis
em outros projetos; aqui, preservar a sequência da investigação tem valor.

## Como outra pessoa refaz o estudo

```bash
git clone <url-do-repositorio>
cd scalepass
git switch --detach challenge/001/start
git switch -c learn/seu-nome/001-foundation-tests
```

Depois de tentar, a solução oficial pode ser consultada sem alterar a branch:

```bash
git show challenge/001/solved:docs/studies/challenges/001-foundation-and-tests/solution.md
```

Para o desafio seguinte, use a respectiva tag `challenge/NNN/start`.
