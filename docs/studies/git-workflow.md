# Estratégia de Git do ScalePass

## Decisão

Aplicação, documentação, scripts de carga, infraestrutura e futuros serviços ficam
em um único repositório. Uma tag captura o estado completo de cada experimento e
permite que outra pessoa refaça o estudo do zero.

Futuros microsserviços começam em diretórios como `services/payments/`. Um serviço
só muda de repositório se um desafio demonstrar necessidade real de permissões,
ownership ou release independente.

## Branches e tags

- `main`: último estado oficial, concluído e reproduzível.
- `challenge/NNN-slug`: trabalho do desafio ativo.
- `challenge/NNN/start`: enunciado publicado, antes da solução.
- `challenge/NNN/solved`: solução, evidências e documentação incorporadas à `main`.
- `vX.Y.Z`: versão do produto, independente dos checkpoints pedagógicos.

Exemplos:

```text
challenge/001-isolated-http-tests
challenge/002-ruff-quality-gate
challenge/003-static-typing
```

Branches concluídas podem ser mantidas para navegação ou removidas depois do
merge. As tags são os checkpoints permanentes e nunca devem ser movidas depois de
publicadas.

## 1. Trabalhar no desafio ativo

Antes do primeiro commit:

```bash
git status
git diff
```

Faça commits pequenos e coerentes. Por exemplo:

```bash
git add pyproject.toml uv.lock tests/
git diff --cached --check
git diff --cached
git commit -m "test: add isolated ticket purchase tests"
```

Não existe a regra de um único commit por desafio. Código, correções mecânicas e
documentação podem formar commits diferentes quando têm intenções diferentes.

## 2. Concluir e documentar um desafio

Na própria branch, preencha `solution.md` e `evidence/README.md`, atualize o estado
do currículo e registre as limitações conhecidas:

```bash
git add AGENTS.md docs/
git diff --cached --check
git diff --cached
git commit -m "docs: document challenge 001 solution"
```

Só considere o desafio solucionado depois de executar novamente suas provas.

## 3. Incorporar a solução na `main`

Exemplo para o desafio 001:

```bash
git switch main
git merge --no-ff challenge/001-isolated-http-tests
git tag -a challenge/001/solved -m "Solve challenge 001: isolated HTTP tests"
```

O merge `--no-ff` preserva no grafo a fronteira pedagógica do desafio. A tag
`solved` aponta para o estado oficial na `main`, não para um commit intermediário.

## 4. Publicar o enunciado do desafio seguinte

Ainda na `main`, crie apenas enunciado, arquivos de evidência vazios e atualizações
de estado. Não implemente a solução:

```bash
git add AGENTS.md docs/
git diff --cached --check
git commit -m "docs: add Ruff quality challenge 002"
git tag -a challenge/002/start -m "Start challenge 002: Ruff quality gate"
git switch -c challenge/002-ruff-quality-gate
```

A ordem importa: a tag `start` deve incluir o enunciado, mas não a resposta do
aluno. A nova branch começa exatamente nessa tag.

## 5. Enviar para um remoto, quando existir

Confira primeiro se há um remoto configurado:

```bash
git remote -v
```

Se `origin` existir:

```bash
git push origin main
git push origin challenge/001/solved challenge/002/start
git push -u origin challenge/002-ruff-quality-gate
```

Não é necessário ter GitHub ou outro remoto para fazer o laboratório localmente.

## Como outra pessoa refaz um desafio

```bash
git clone <url-do-repositorio>
cd scalepass
git switch --detach challenge/002/start
git switch -c learn/seu-nome/002-ruff-quality-gate
```

Depois da tentativa, a solução oficial pode ser lida sem mudar de branch:

```bash
git show challenge/002/solved:docs/studies/challenges/002-ruff-quality-gate/solution.md
```

Para voltar ao estado oficial mais recente:

```bash
git switch main
```

## Resumo do ciclo

```text
main + tag start -> branch challenge -> commits -> documentação
-> merge --no-ff em main -> tag solved -> novo enunciado
-> nova tag start -> nova branch challenge
```

Segredos, bancos, `.venv` e artefatos grandes não são versionados. Scripts,
configurações e resumos pequenos que permitem reproduzir evidências são
versionados.
