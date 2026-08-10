# Evidências do desafio `testing-001`

## Estado

`pending`

## Ambiente

- Python: 3.14
- uv uv 0.9.30:.
- Sistema operacional: ubuntu 24.04.

## Execuções

### Primeira execução

 uv run pytest -q
...                                                                                                                                                                                                                         [100%]
======================================================================================================== warnings summary =========================================================================================================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  /home/wary/jetbrains/srelab/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
3 passed, 1 warning in 0.28s


### Segunda execução

 uv run pytest -q
...                                                                                                                                                                                                                         [100%]
======================================================================================================== warnings summary =========================================================================================================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  /home/wary/jetbrains/srelab/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
3 passed, 1 warning in 0.28s


## Integridade de `scalepass.db`

- Estado ou hash antes: 215e1ebf74c9910f757c55396ce911cba6292872f0aa1dc8d18d9ff27a6020c9.
- Estado ou hash depois: 215e1ebf74c9910f757c55396ce911cba6292872f0aa1dc8d18d9ff27a6020c9.

## Isolamento implementado

Para garantir que a aplicação rode de forma isolada sem tocar no banco de desenvolvimento (`scalepass.db`), a seguinte estratégia de infraestrutura de testes foi configurada na fixture `client` (`tests/conftest.py`):

- **Arquivo SQLite Temporário:** A fixture consome a fixture nativa `tmp_path` do pytest, criando um banco SQLite exclusivo em um diretório temporário isolado por função de teste (ex: `tmp_path / "test_scalepass.db"`).
- **Substituição do Engine no Startup:** A variável global `app.database.engine` é reatribuída dinamicamente com o novo engine temporário antes da inicialização do aplicativo. Com isso, quando o gerenciador de contexto `TestClient(app)` executa o evento `lifespan` do FastAPI, a função `create_tables()` direciona a criação do DDL/schema para o SQLite temporário em vez do arquivo local.
- **Sessões e Dependências HTTP (`get_db`):** Um `sessionmaker` local (`TestingSessionLocal`) é associado ao engine temporário. A função `get_db` da aplicação é sobrescrita através de `app.dependency_overrides[get_db]`, garantindo que todas as requisições disparadas pelo cliente HTTP abram sessões conectadas unicamente ao banco do teste.
- **Gerenciamento de Estado do Cliente:** Os testes utilizam uma mesma instância de `TestClient` para preservar cookies de sessão Starlette entre chamadas (`/register`, `/login`, `/events`, `/orders`). No cenário de teste para visitantes, os cookies são zerados via `client.cookies.clear()`.
- **Teardown Rígido:** Ao final da execução de cada teste (mesmo em caso de falhas ou exceções), o bloco `finally`/pós-`yield` da fixture restaura o `app.database.engine` original e limpa os overrides com `app.dependency_overrides.clear()`.
## Limitações conhecidas

- **Concorrência e Modificação de Módulo Global:** A substituição em tempo de execução do atributo `app.database.engine` altera uma referência global em memória durante o teste. Embora funcione perfeitamente para execuções sequenciais (comportamento padrão do `pytest`), isso exigiria adaptações adicionais (como injeção de dependência no próprio objeto `FastAPI` ou `app.state`) caso os testes passem a rodar de forma paralela através do `pytest-xdist` no mesmo processo Python.
- **Sensibilidade a Warnings do `httpx`:** Em ambientes com Python 3.14+ e versões mais recentes do FastAPI/Starlette, o `TestClient` pode emitir avisos de depreciação (*deprecation warnings*) relacionados ao suporte interno do `httpx` (não afetando a execução ou o resultado dos testes).
- **Sem Persistência de Dados de Diagnóstico:** Como o arquivo `.db` é gerado dentro de `tmp_path`, os bancos criados são descartados automaticamente pelo sistema operacional/pytest após a execução. Caso seja necessário inspecionar o arquivo SQLite de um teste que falhou, deve-se usar a flag `--basetemp` na chamada do Pytest.