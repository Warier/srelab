# Desafio `quality-001`: lint e formato reproduzíveis com Ruff

## Estado

`solved`

## Resultado único esperado

Instalar e configurar o Ruff como a única ferramenta de estilo do projeto. Ao
final, o linter, a verificação de formato e os três testes existentes devem passar
com comandos reproduzíveis pelo `uv`.

Este desafio não inclui tipos, cobertura, hooks Git ou CI.

## Tempo e dificuldade estimados

- Tempo: 2 a 4 horas.
- Nível: júnior intermediário.
- Principal dificuldade: distinguir correção automática segura de uma mudança que
  exige julgamento e não esconder problemas com exceções amplas.

## Situação inicial

O projeto tem código legível e testes, mas nenhuma política executável de estilo.
Revisores precisam decidir manualmente sobre imports, código morto, sintaxe
obsoleta e formatação. Não existe um comando que produza a mesma resposta em toda
máquina.

## Ferramenta obrigatória

Use somente o **Ruff** para lint e formato. Adicione-o ao grupo separado `lint`:

```bash
uv add --group lint ruff
uv lock --check
```

O grupo separado explicita que Ruff é ferramenta de desenvolvimento e permite
executá-lo sem transformar dependência de qualidade em dependência de runtime.

Referência oficial:

- [uv: dependency groups](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-groups)
- [Ruff: instalação](https://docs.astral.sh/ruff/installation/)

## Configuração obrigatória

Centralize a configuração no `pyproject.toml`. Configure:

```toml
[tool.ruff]
target-version = "py314"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

Famílias escolhidas:

- `E`: erros de estilo do pycodestyle;
- `F`: erros do Pyflakes, como imports e nomes inválidos;
- `I`: ordenação de imports;
- `UP`: modernização compatível com a versão-alvo do Python;
- `B`: padrões propensos a bugs identificados pelo flake8-bugbear;
- `SIM`: simplificações que reduzem complexidade acidental.

Não selecione `ALL`: neste estágio, o exercício é entender uma política pequena e
explícita. O formatter não ordena imports, por isso `I` continua necessário.

Referências oficiais:

- [Ruff: configuração](https://docs.astral.sh/ruff/configuration/)
- [Ruff: linter e seleção de regras](https://docs.astral.sh/ruff/linter/)
- [Ruff: formatter](https://docs.astral.sh/ruff/formatter/)
- [Ruff: tutorial](https://docs.astral.sh/ruff/tutorial/)

## Trabalho a realizar

### 1. Capture o baseline antes de corrigir

Depois de adicionar a dependência e a configuração, execute:

```bash
uv run --group lint ruff check .
uv run --group lint ruff format --check .
```

Copie para `evidence/README.md` a quantidade total de ocorrências e os códigos de
regra encontrados. O primeiro comando pode falhar neste momento; isso é o baseline,
não o resultado final.

### 2. Classifique antes de automatizar

Para cada família encontrada, leia a explicação de pelo menos um código:

```bash
uv run --group lint ruff rule <CODIGO>
```

Separe no registro:

- mudanças mecânicas e seguras;
- mudanças que podem alterar comportamento;
- falsos positivos reais, se existirem.

### 3. Aplique correções seguras e revise o diff

Você pode usar:

```bash
uv run --group lint ruff check --fix .
uv run --group lint ruff format .
git diff
```

Não use `--unsafe-fixes`. Corrija manualmente o que permanecer e confirme que o
diff não mudou regras de negócio nem assertions dos testes.

### 4. Produza a prova final

```bash
uv lock --check
uv run --group lint ruff check .
uv run --group lint ruff format --check .
uv run pytest -q
```

## Critérios de aceite objetivos

Todos precisam ser verdadeiros:

1. Ruff está no dependency group `lint`, e não nas dependências de runtime.
2. `target-version`, `line-length` e `select` estão no `pyproject.toml` exatamente
   com os valores definidos neste enunciado.
3. `uv lock --check` encerra com código `0`.
4. `uv run --group lint ruff check .` encerra com código `0` e zero violações.
5. `uv run --group lint ruff format --check .` encerra com código `0` e informa
   que nenhum arquivo precisa ser reformatado.
6. `uv run pytest -q` continua mostrando os três testes passando.
7. Não há `# noqa`, `per-file-ignores`, `ignore` global ou exclusão nova usada
   apenas para esconder uma violação do baseline.
8. `evidence/README.md` contém o baseline, a classificação das mudanças e a saída
   final dos quatro comandos de prova.

Uma exceção só será aceita se trouxer código da regra, arquivo, linha, motivo
técnico e alternativa rejeitada. A preferência deste desafio é corrigir o código.

## O que estudar

Estude apenas:

- diferença entre linter e formatter;
- descoberta de configuração do Ruff no `pyproject.toml`;
- prefixos e códigos de regras;
- diferença entre `check`, `check --fix`, `format` e `format --check`;
- fixes seguros versus inseguros;
- por que revisar `git diff` após automação;
- dependency groups do `uv`.

Não é necessário estudar plugins Flake8 individualmente além das famílias
selecionadas nem montar uma política corporativa completa.

## Evidências a registrar

Em `evidence/README.md`, preencha:

- versões de Python, uv e Ruff;
- comando e saída resumida do baseline;
- códigos encontrados e o que significam neste projeto;
- correções feitas automaticamente e manualmente;
- qualquer exceção, com justificativa completa;
- saída resumida dos quatro comandos finais;
- confirmação de que os testes permaneceram com três cenários.

## Fora do escopo

- Mypy ou Pyright;
- pytest-cov ou meta de cobertura;
- pre-commit;
- GitHub Actions ou outra CI;
- Bandit, Semgrep ou regras específicas de segurança;
- refatoração de arquitetura;
- alteração de comportamento funcional;
- exigência de docstrings.

## Pistas progressivas

Leia somente se travar.

<details>
<summary>Pista 1 — imports continuam fora de ordem depois do formatter</summary>

O formatter não organiza imports. Confirme se a família `I` está selecionada e
execute o linter com fix seguro antes do formatter.
</details>

<details>
<summary>Pista 2 — não sei se o Ruff pode corrigir uma ocorrência</summary>

Execute `ruff rule <CODIGO>` e leia a seção sobre disponibilidade e segurança do
fix. Se houver dúvida sobre comportamento, corrija manualmente.
</details>

<details>
<summary>Pista 3 — quero adicionar um ignore para terminar</summary>

Primeiro explique por que o código não pode ser corrigido sem piorar clareza ou
comportamento. Se essa explicação não existir, o ignore apenas esconde a evidência.
</details>

## Checkpoint Git

- Tag inicial: `challenge/002/start`.
- Branch: `challenge/002-ruff-quality-gate`.
- Tag futura da solução: `challenge/002/solved`.
- Solução oficial: [solution.md](solution.md).
