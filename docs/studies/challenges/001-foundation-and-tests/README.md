# Desafio `foundation-001`: fundação e testes confiáveis

## Estado

`active`

## Situação

ScalePass está funcional e foi validado manualmente. Entretanto, uma alteração em
cadastro, publicação ou compra pode quebrar outro fluxo sem ser percebida. Engine,
sessões e criação de tabelas também estão ligadas diretamente ao processo normal,
o que pode dificultar verificações automatizadas isoladas.

Antes de provocar problemas de concorrência, carga e infraestrutura, precisamos
ser capazes de distinguir uma falha nova de uma regressão funcional comum.

## Sintomas observáveis

- Não existe comando automatizado que confirme o fluxo principal.
- O lockfile existe, mas ainda não há um quality gate que exija sua consistência.
- Não há dependências ou configuração próprias para desenvolvimento e testes.
- Cada mudança exige repetir manualmente cadastro, evento e compra.
- Não há garantia de que um teste futuro deixará `scalepass.db` intacto.
- Estilo, tipos e cobertura não possuem uma política executável.

## Missão

Crie uma fundação de qualidade que permita modificar o ScalePass com confiança e
executar as mesmas verificações localmente e em automações futuras.

Você pode alterar a organização interna quando isso for necessário para tornar
dependências substituíveis, mas não deve mudar os fluxos funcionais nem corrigir
antecipadamente limitações de outras etapas.

## O que estudar

- pirâmide de testes e diferença entre unidade, integração e end-to-end;
- fixtures, isolamento e determinismo;
- injeção e sobrescrita de dependências no FastAPI;
- ciclo de vida de engine e sessão do SQLAlchemy;
- bancos temporários e particularidades do SQLite em memória;
- `TestClient`/HTTPX e cookies de sessão;
- dependency groups e lockfile do `uv`;
- lint, formatação, análise estática de tipos e cobertura;
- critérios de qualidade úteis versus métricas de vaidade.

Ferramentas candidatas: Pytest, pytest-cov, Ruff e Mypy ou Pyright. A escolha e a
configuração fazem parte do desafio.

## Requisitos

1. Demonstrar uma instalação limpa com `uv sync --locked` e manter o lock coerente.
2. Separar dependências de desenvolvimento das dependências de runtime.
3. Disponibilizar comandos claros para lint, formato, tipos e testes.
4. Testar ao menos estes comportamentos pela interface HTTP:
   - cadastro e login;
   - rejeição de cadastro duplicado;
   - publicação autenticada de evento;
   - bloqueio da publicação para visitante;
   - compra válida e redução do estoque;
   - rejeição de compra acima do estoque;
   - isolamento do histórico por usuário;
   - resposta de `GET /api/events`.
5. Testes não podem criar, remover ou alterar `scalepass.db`.
6. Cada teste deve executar sozinho e em ordem aleatória.
7. Uma falha em qualquer verificação deve retornar código diferente de zero.
8. Documentar os comandos em `README.md`, `docs/development.md` e `AGENTS.md`
   sem duplicar explicações extensas.

## Evidências esperadas

- instalação limpa e sincronizada usando o lockfile;
- resumo dos testes passando;
- cobertura inicial observada, sem meta percentual arbitrária;
- demonstração de que `scalepass.db` não foi alterado;
- classificação dos testes como unidade ou integração, com justificativa;
- limitações que a suíte ainda não cobre.

## Restrições

- não adicionar PostgreSQL, Redis, containers ou filas;
- não implementar monitoramento ou logging estruturado;
- não corrigir ainda a venda concorrente;
- não substituir o mecanismo de senha nem redesenhar autorização;
- evitar mocks do SQLAlchemy nos testes de fluxo HTTP;
- não testar detalhes internos quando o comportamento público for suficiente.

## Critério de conclusão

Outro desenvolvedor deve conseguir clonar o repositório, sincronizar o ambiente
travado e executar uma sequência curta que confirme estilo, tipos e comportamento
funcional sem tocar em dados locais.

Ao concluir, mova no `curriculum.json` as ferramentas utilizadas de `to_cover`
para `introduced`. Nenhuma vai diretamente para `well_covered`.

## Não objetivos

- configurar deploy;
- resolver problemas de escala;
- elevar a autenticação a um padrão de produção;
- escolher a arquitetura futura;
- perseguir 100% de cobertura;
- implementar CI/CD completo.

## Checkpoint Git

- Tag de entrada: `challenge/001/start`.
- Branch ativa: `codex/challenge/001-foundation-tests`.
- Tag de saída futura: `challenge/001/solved`.
- Solução: [solution.md](solution.md), mantida como `pending` até a conclusão.

## Extensão opcional

Depois que as verificações locais estiverem estáveis, execute-as em uma integração
contínua simples. Não inclua deploy.
