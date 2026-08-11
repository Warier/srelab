import pytest
from fastapi.testclient import TestClient


def test_authenticated_user_can_buy_ticket(client: TestClient) -> None:
    # 1. Cadastrar usuario
    register_response = client.post(
        "/register",
        data={"email": "usuario@exemplo.com", "password": "password123"},
    )
    assert register_response.status_code == 303
    assert register_response.headers["location"] == "/"

    # 2. Criar um evento com estoque conhecido (10 ingressos)
    event_response = client.post(
        "/events",
        data={
            "title": "Festival de Musicas",
            "description": "Show incrivel",
            "venue": "Centro de Eventos",
            "event_date": "2026-12-31T20:00",
            "price": "50.00",
            "available_tickets": 10,
        },
    )
    assert event_response.status_code == 303
    assert event_response.headers["location"] == "/events/1"

    # 3. Comprar 2 ingressos
    buy_response = client.post(
        "/events/1/buy",
        data={"quantity": 2},
    )

    # 4. Confirmar redirecionamento de sucesso para /orders
    assert buy_response.status_code == 303
    assert buy_response.headers["location"] == "/orders"

    # 5. Confirmar que /orders exibe o pedido
    orders_response = client.get("/orders")
    assert orders_response.status_code == 200
    assert "Festival de Musicas" in orders_response.text
    assert "2 ingresso(s)" in orders_response.text

    # 6. Confirmar por GET /api/events que o estoque caiu exatamente em 2 (de 10 para 8)
    api_response = client.get("/api/events")
    assert api_response.status_code == 200
    events_data = api_response.json()
    assert len(events_data) == 1
    assert events_data[0]["id"] == 1
    assert events_data[0]["available_tickets"] == 8


def test_buying_more_tickets_than_available_is_rejected(client: TestClient) -> None:
    # Preparacao: autenticar para conseguir criar evento
    client.post(
        "/register",
        data={"email": "comprador@exemplo.com", "password": "password123"},
    )

    # 1. Criar um evento com estoque 2
    client.post(
        "/events",
        data={
            "title": "Workshop Intimo",
            "description": "Apenas 2 vagas",
            "venue": "Sala 101",
            "event_date": "2026-11-15T14:00",
            "price": "100.00",
            "available_tickets": 2,
        },
    )

    # 2. Tentar comprar 3 ingressos
    buy_response = client.post(
        "/events/1/buy",
        data={"quantity": 3},
    )

    # 3. Confirmar status 400 Bad Request e mensagem de erro
    assert buy_response.status_code == 400
    assert "ingressos suficientes para essa compra" in buy_response.text

    # 4. Confirmar que o estoque continua 2
    api_response = client.get("/api/events")
    assert api_response.status_code == 200
    events = api_response.json()
    assert events[0]["available_tickets"] == 2

    # 5. Confirmar que nenhum pedido foi criado
    orders_response = client.get("/orders")
    assert orders_response.status_code == 200
    assert "Workshop Intimo" not in orders_response.text


def test_visitor_cannot_buy_ticket(client: TestClient) -> None:
    # 1. Disponibilizar um evento
    client.post(
        "/register",
        data={"email": "organizador@exemplo.com", "password": "password123"},
    )
    client.post(
        "/events",
        data={
            "title": "Teatro na Praca",
            "description": "Aberto ao publico",
            "venue": "Praca Central",
            "event_date": "2026-10-10T18:00",
            "price": "10.00",
            "available_tickets": 5,
        },
    )

    # 2. Usar um cliente sem sessao autenticada
    client.cookies.clear()

    # 3. Tentar comprar um ingresso como visitante
    buy_response = client.post(
        "/events/1/buy",
        data={"quantity": 1},
    )

    # 4. Confirmar status 303 e destino /login
    assert buy_response.status_code == 303
    assert buy_response.headers["location"] == "/login"

    # 5. Confirmar que o estoque nao mudou (continua 5)
    api_response = client.get("/api/events")
    assert api_response.status_code == 200
    events = api_response.json()
    assert events[0]["available_tickets"] == 5


# --- CENÁRIOS DO DESAFIO 2 (COBERTURA DE RISCO) E EXPANSÃO ---


def test_login_with_invalid_credentials_fails(client: TestClient) -> None:
    client.post(
        "/register",
        data={"email": "valido@exemplo.com", "password": "senha_correta"},
    )
    client.cookies.clear()

    response = client.post(
        "/login",
        data={"email": "valido@exemplo.com", "password": "senha_errada"},
    )

    assert response.status_code == 400
    assert "E-mail ou senha incorretos." in response.text

    protected_response = client.get("/orders")
    assert protected_response.status_code == 303
    assert protected_response.headers["location"] == "/login"


def test_duplicate_registration_fails(client: TestClient) -> None:
    client.post(
        "/register",
        data={"email": "duplicado@exemplo.com", "password": "password123"},
    )

    dup_response = client.post(
        "/register",
        data={"email": "duplicado@exemplo.com", "password": "outrasenha123"},
    )

    assert dup_response.status_code == 400

    client.cookies.clear()
    rejected_login = client.post(
        "/login",
        data={"email": "duplicado.com", "password": "outrasenha123"},
    )
    assert rejected_login.status_code == 400

    login_response = client.post(
        "/login",
        data={"email": "duplicado@exemplo.com", "password": "password123"},
    )
    assert login_response.status_code == 303


@pytest.mark.parametrize(
    "invalid_data",
    [
        {
            "title": "   ",  # Titulo apenas com espacos
            "description": "Desc",
            "venue": "Local",
            "event_date": "2026-12-31T20:00",
            "price": "10.00",
            "available_tickets": 10,
        },
        {
            "title": "Evento",
            "description": "Desc",
            "venue": "Local",
            "event_date": "2026-12-31T20:00",
            "price": "-5.00",  # Preco negativo
            "available_tickets": 10,
        },
        {
            "title": "Evento",
            "description": "Desc",
            "venue": "Local",
            "event_date": "invalida",  # Data invalida no isoformat
            "price": "10.00",
            "available_tickets": 10,
        },
    ],
)
def test_create_event_with_invalid_data_fails(
    client: TestClient, invalid_data: dict[str, object]
) -> None:
    client.post(
        "/register",
        data={"email": "criador@exemplo.com", "password": "password123"},
    )

    response = client.post("/events", data=invalid_data)

    assert response.status_code == 400
    assert "Revise os dados do evento e tente novamente." in response.text

    api_response = client.get("/api/events")
    assert api_response.status_code == 200
    assert len(api_response.json()) == 0


def test_nonexistent_event_returns_404(client: TestClient) -> None:
    client.post(
        "/register",
        data={"email": "comprador404@exemplo.com", "password": "password123"},
    )

    detail_response = client.get("/events/999")
    assert detail_response.status_code == 404

    buy_response = client.post("/events/999/buy", data={"quantity": 1})
    assert buy_response.status_code == 404

    orders_response = client.get("/orders")
    assert orders_response.status_code == 200
    assert "ingresso(s)" not in orders_response.text


@pytest.mark.parametrize("invalid_quantity", [0, 11])
def test_buying_invalid_ticket_quantity_fails(
    client: TestClient, invalid_quantity: int
) -> None:
    client.post(
        "/register",
        data={"email": "vendedor@exemplo.com", "password": "password123"},
    )
    client.post(
        "/events",
        data={
            "title": "Show Restrito",
            "description": "Descricao",
            "venue": "Teatro",
            "event_date": "2026-12-31T20:00",
            "price": "20.00",
            "available_tickets": 5,
        },
    )

    buy_response = client.post("/events/1/buy", data={"quantity": invalid_quantity})

    assert buy_response.status_code == 400
    assert "Escolha entre 1 e 10 ingressos." in buy_response.text

    api_response = client.get("/api/events")
    assert api_response.status_code == 200
    events = api_response.json()
    assert events[0]["available_tickets"] == 5

    orders_response = client.get("/orders")
    assert orders_response.status_code == 200
    assert "Show Restrito" not in orders_response.text


# --- CENÁRIOS EXTRAS PARA COBERTURA 95%+ ---


def test_pages_render_and_auth_flows(client: TestClient) -> None:
    # Acessa paginas GET estaticas
    assert client.get("/register").status_code == 200
    assert client.get("/login").status_code == 200
    assert client.get("/events/new").status_code == 303  # Sem login redireciona

    # Tenta cadastro com email invalido
    res_email = client.post(
        "/register", data={"email": "email_invalido", "password": "1234"}
    )
    assert res_email.status_code == 400

    # Tenta cadastro com senha curta
    res_pass = client.post(
        "/register", data={"email": "ok@exemplo.com", "password": "123"}
    )
    assert res_pass.status_code == 400

    # Tenta criar evento sem estar logado
    res_event_unauth = client.post(
        "/events",
        data={
            "title": "Evento",
            "description": "D",
            "venue": "V",
            "event_date": "2026-12-31T20:00",
            "price": "10.00",
            "available_tickets": 5,
        },
    )
    assert res_event_unauth.status_code == 303

    # Loga, acessa formulario de evento e faz logout
    client.post(
        "/register", data={"email": "ok@exemplo.com", "password": "password123"}
    )
    assert client.get("/events/new").status_code == 200

    logout_res = client.post("/logout")
    assert logout_res.status_code == 303
