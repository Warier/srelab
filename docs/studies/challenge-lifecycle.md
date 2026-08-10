# Ciclo de vida dos desafios

## Estrutura obrigatória

Cada desafio ocupa um diretório:

```text
docs/studies/challenges/NNN-slug/
├── README.md
├── solution.md
└── evidence/
    └── README.md
```

### Enunciado

`README.md` fica disponível na tag `challenge/NNN/start` e contém contexto,
sintomas, missão, restrições, áreas para estudo, critérios de aceite, evidências,
não objetivos e o checkpoint Git. Ele não entrega uma receita completa.

### Solução

`solution.md` existe desde o início com estado `pending`, mas sem spoilers. Depois
da conclusão, deve registrar:

- diagnóstico e causa raiz;
- hipóteses descartadas;
- solução implementada;
- alternativas e trade-offs;
- comandos de reprodução;
- resultados antes/depois;
- limitações restantes;
- arquivos e commits relevantes;
- lições e próximos problemas expostos.

Instalar uma ferramenta não é uma solução suficiente: o documento deve explicar
por que ela ajudou e quais custos introduziu.

### Evidências

`evidence/` contém somente artefatos pequenos e reproduzíveis, como resumos de
benchmarks, planos de execução, saídas curtas de testes, dashboards exportados e
instruções para regenerar dados.

Bancos, logs completos, datasets grandes, ambientes virtuais e relatórios HTML
gerados não entram no Git.

## Estados

```text
draft -> active -> investigating -> solved -> documented -> archived
```

- `draft`: desafio em preparação.
- `active`: enunciado e estado inicial disponíveis.
- `investigating`: trabalho iniciado em branch própria.
- `solved`: critérios técnicos atendidos.
- `documented`: solução e evidências reproduzíveis.
- `archived`: tag de conclusão criada e próximo desafio liberado.

`curriculum.json`, `AGENTS.md` e o diretório do desafio devem concordar sobre o
estado atual.

## Conclusão documental

Outra pessoa, em uma máquina limpa, deve conseguir identificar o checkpoint,
executar o experimento, aplicar a solução descrita e observar resultados
equivalentes dentro das limitações de hardware declaradas.
