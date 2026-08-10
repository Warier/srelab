# ScalePass

ScalePass é uma aplicação web para publicar eventos, disponibilizar ingressos e
acompanhar compras em um único lugar.

## Funcionalidades

- criação de conta e autenticação;
- publicação de eventos com data, local, preço e quantidade de ingressos;
- catálogo público de eventos;
- compra direta de até dez ingressos por pedido;
- histórico de ingressos comprados;
- consulta pública de eventos em JSON.

## Requisitos

- [`uv`](https://docs.astral.sh/uv/);
- Python 3.14, que pode ser instalado pelo próprio `uv`.

## Executando localmente

Na raiz do projeto, instale o Python e as dependências:

```bash
uv python install 3.14
uv sync
```

Inicie o servidor de desenvolvimento:

```bash
uv run uvicorn app.main:app --reload
```

Acesse [http://127.0.0.1:8000](http://127.0.0.1:8000). Na primeira execução, o
arquivo `scalepass.db` será criado automaticamente.

O fluxo mais curto para conhecer a aplicação é:

1. criar uma conta;
2. publicar um evento;
3. abrir o evento publicado;
4. comprar um ou mais ingressos;
5. consultar **Meus ingressos**.

## API

Os eventos publicados estão disponíveis em:

```text
GET /api/events
```

A documentação interativa gerada pelo FastAPI pode ser acessada em
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Configuração

A aplicação reconhece estas variáveis de ambiente:

| Variável | Valor padrão | Descrição |
|---|---|---|
| `SCALEPASS_DATABASE_URL` | `sqlite:///./scalepass.db` | URL de conexão do SQLAlchemy |
| `SCALEPASS_SECRET_KEY` | valor local embutido | Chave usada para assinar a sessão |

Exemplo:

```bash
export SCALEPASS_SECRET_KEY="uma-chave-local-diferente"
uv run uvicorn app.main:app --reload
```

Defina uma chave própria sempre que a aplicação for compartilhada em uma rede.

## Estrutura

```text
app/
├── auth.py          # autenticação e leitura da sessão
├── config.py        # configuração por ambiente
├── database.py      # engine e sessões do banco
├── main.py          # aplicação e rotas HTTP
├── models.py        # modelos relacionais
├── static/          # estilos da interface
└── templates/       # páginas Jinja2
docs/                # documentação técnica e funcional
```

## Desenvolvimento

Consulte [docs/development.md](docs/development.md) para detalhes do ambiente e
[docs/architecture.md](docs/architecture.md) para a arquitetura atual.
