# Ciclo de vida dos desafios

## Regra principal de escopo

Cada desafio deve possuir um único resultado técnico principal, descrito de forma
falseável. Se a conclusão puder ser resumida apenas como “melhorar qualidade”,
“configurar ambiente” ou “adicionar observabilidade”, o escopo ainda está amplo.

Exemplo inadequado:

> Adicionar testes, lint, tipos, cobertura e CI.

Exemplo adequado:

> Criar três testes HTTP do fluxo de compra que usam SQLite temporário e provar que
> `scalepass.db` não mudou.

Desafios grandes são permitidos quando representam um único incidente ou capacidade
indivisível, mas devem continuar tendo uma prova final concreta.

## Estrutura obrigatória

```text
docs/studies/challenges/NNN-slug/
├── README.md
├── solution.md
└── evidence/
    └── README.md
```

## Requisitos do enunciado

O `README.md` fica disponível em `challenge/NNN/start` e deve conter:

- um resultado principal;
- sintoma ou estado inicial observável;
- ferramenta definida, salvo quando comparar ferramentas for o próprio objetivo;
- comandos relevantes;
- lista limitada dos conceitos exatos a estudar;
- links diretos para documentação primária e tutoriais pertinentes;
- entregáveis nomeados;
- critérios de aceite numerados e mensuráveis;
- evidências que precisam ser registradas;
- itens explicitamente fora do escopo;
- pistas progressivas que não entreguem o código final;
- checkpoint Git.

Não junte lint, testes, tipos, cobertura e CI no mesmo desafio. Cada capacidade deve
ser aprendida e comprovada separadamente antes de compor um quality gate completo.

## Seleção de recursos de estudo

Priorize nesta ordem:

1. documentação oficial da ferramenta;
2. tutorial oficial mantido pelo projeto;
3. especificação ou padrão relevante;
4. palestra de mantenedor ou conferência reconhecida;
5. tutorial externo atual, identificado como material complementar.

Não entregue apenas a página inicial de uma ferramenta. Indique a seção a estudar
e por que ela é necessária para o desafio.

## Solução

`solution.md` existe desde o início com estado `pending`, sem spoilers. Depois da
conclusão, registra:

- diagnóstico e causa raiz;
- hipóteses descartadas;
- solução implementada;
- alternativas e trade-offs;
- comandos de reprodução;
- resultados antes/depois;
- limitações restantes;
- arquivos e commits relevantes;
- próximos problemas expostos.

Instalar uma ferramenta não é uma solução: é necessário provar o comportamento que
ela passou a garantir.

## Evidências

`evidence/` guarda artefatos pequenos e reproduzíveis: resumo de testes, benchmark
em JSON/CSV, plano de execução, dashboard exportado e instruções de reprodução.

Bancos, logs completos, datasets grandes, ambientes virtuais e relatórios gerados
não entram no Git.

## Estados

```text
draft -> active -> investigating -> solved -> documented -> archived
```

- `draft`: desafio em preparação.
- `active`: enunciado e estado inicial disponíveis.
- `investigating`: trabalho iniciado.
- `solved`: critérios técnicos atendidos.
- `documented`: solução e evidências reproduzíveis.
- `archived`: tag de conclusão criada e próximo desafio liberado.

`curriculum.json`, `AGENTS.md` e o diretório do desafio devem concordar sobre o
estado atual.

## Conclusão documental

Outra pessoa, em uma máquina limpa, deve conseguir recuperar o checkpoint, executar
o experimento, aplicar a solução e observar resultados equivalentes dentro das
limitações de hardware declaradas.
