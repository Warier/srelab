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
