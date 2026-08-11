# Solução do desafio `typing-001`

## Estado

`documented`

## Diagnóstico

Oito caminhos retornavam `RedirectResponse` em funções anotadas como
`HTMLResponse`. O comportamento funcionava, mas o contrato estático estava
incompleto.

## Contrato escolhido

As seis rotas com retornos mistos usam `Response`, classe-base comum de
`HTMLResponse` e `RedirectResponse`. É menos específico que uma união, mas é aceito
simultaneamente pelo Mypy e pela introspecção runtime do FastAPI.

A união `HTMLResponse | RedirectResponse` foi testada e rejeitada: Mypy passava,
porém o FastAPI tentava transformá-la em um response model Pydantic e falhava ao
importar a aplicação.

## Alterações

- Mypy 2.3.0 no dependency group `typing`;
- modo estrito configurado para os seis arquivos de `app/`;
- import de `Response` e correção das seis anotações em `app/main.py`;
- nenhuma mudança nas regras, redirects ou respostas HTTP.

## Prova final

Lockfile, Mypy, Ruff, formato e os três testes passaram. Consulte
[evidence/README.md](evidence/README.md).
