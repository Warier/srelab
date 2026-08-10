# Desenvolvimento local

## Preparação

Instale o interpretador definido em `.python-version` e sincronize as dependências:

```bash
uv python install
uv sync
```

O ambiente virtual é mantido pelo `uv` em `.venv`. Não é necessário ativá-lo para
usar comandos com `uv run`.

## Iniciando a aplicação

```bash
uv run uvicorn app.main:app --reload
```

Endereços úteis:

- aplicação: `http://127.0.0.1:8000`;
- OpenAPI: `http://127.0.0.1:8000/docs`;
- eventos em JSON: `http://127.0.0.1:8000/api/events`.

## Banco local

Por padrão, os dados ficam em `scalepass.db` na raiz. O arquivo é ignorado pelo
Git. Para usar outro caminho:

```bash
export SCALEPASS_DATABASE_URL="sqlite:////tmp/scalepass-local.db"
uv run uvicorn app.main:app --reload
```

Para reiniciar completamente os dados de desenvolvimento, pare a aplicação e
remova somente o arquivo SQLite que você configurou. Essa operação apaga todas as
contas, eventos e compras e não pode ser desfeita.

## Configuração

`app/config.py` lê as variáveis no momento em que o módulo é importado. Defina as
variáveis antes de iniciar o processo.

O arquivo `.env.example` documenta os nomes disponíveis, mas a aplicação não carrega
arquivos `.env` automaticamente.

## Diagnóstico básico

O baseline ainda não possui logging estruturado. Algumas operações imprimem uma
linha no terminal:

- início da aplicação;
- criação de usuário;
- publicação de evento;
- criação de pedido.

## Verificação manual

Até a criação da suíte automatizada, use este roteiro mínimo:

1. abrir `/` sem uma base existente;
2. criar uma conta;
3. publicar um evento com estoque 5;
4. comprar 2 ingressos;
5. confirmar o pedido em `/orders`;
6. confirmar que o evento exibe estoque 3;
7. abrir `/api/events` e conferir os dados do evento.
