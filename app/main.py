from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Annotated

from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.auth import authenticate, current_user, hash_password
from app.config import settings
from app.database import create_tables, get_db
from app.models import Event, Order, User


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    create_tables()
    print("ScalePass started")
    yield


app = FastAPI(title="ScalePass", version="0.1.0", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


def format_money(value: int) -> str:
    return f"R$ {value / 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


templates.env.filters["money"] = format_money


def page_context(request: Request, database: Session, **extra: object) -> dict[str, object]:
    return {
        "request": request,
        "current_user": current_user(request, database),
        **extra,
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request, database: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    events = database.scalars(select(Event).order_by(Event.event_date)).all()
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=page_context(request, database, events=events),
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(
    request: Request,
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context=page_context(request, database),
    )


@app.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    normalized_email = email.lower().strip()
    error = None

    if "@" not in normalized_email or "." not in normalized_email:
        error = "Informe um e-mail válido."
    elif len(password) < 4:
        error = "A senha precisa ter ao menos 4 caracteres."
    elif database.scalar(select(User).where(User.email == normalized_email)):
        error = "Já existe uma conta com esse e-mail."

    if error:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context=page_context(request, database, error=error, email=normalized_email),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = User(email=normalized_email, password_hash=hash_password(password))
    database.add(user)
    database.commit()
    database.refresh(user)
    request.session["user_id"] = user.id
    print(f"New user registered: {user.id}")
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request,
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=page_context(request, database),
    )


@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    user = authenticate(database, email, password)
    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context=page_context(
                request,
                database,
                error="E-mail ou senha incorretos.",
                email=email,
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/logout")
def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/events/new", response_class=HTMLResponse)
def new_event_page(
    request: Request,
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    if current_user(request, database) is None:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request=request,
        name="new_event.html",
        context=page_context(request, database),
    )


@app.post("/events", response_class=HTMLResponse)
def create_event(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    venue: Annotated[str, Form()],
    event_date: Annotated[str, Form()],
    price: Annotated[str, Form()],
    available_tickets: Annotated[int, Form()],
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    user = current_user(request, database)
    if user is None:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    try:
        parsed_date = datetime.fromisoformat(event_date)
        price_cents = int(
            (Decimal(price.replace(",", ".")) * 100).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
        )
        if not title.strip() or not venue.strip():
            raise ValueError
        if price_cents < 0 or available_tickets < 1:
            raise ValueError
    except (InvalidOperation, ValueError):
        return templates.TemplateResponse(
            request=request,
            name="new_event.html",
            context=page_context(
                request,
                database,
                error="Revise os dados do evento e tente novamente.",
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    event = Event(
        title=title.strip(),
        description=description.strip(),
        venue=venue.strip(),
        event_date=parsed_date,
        price_cents=price_cents,
        available_tickets=available_tickets,
        creator_id=user.id,
    )
    database.add(event)
    database.commit()
    database.refresh(event)
    print(f"New event created: {event.id}")
    return RedirectResponse(
        f"/events/{event.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.get("/events/{event_id}", response_class=HTMLResponse)
def event_detail(
    event_id: int,
    request: Request,
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    event = database.get(Event, event_id)
    if event is None:
        return templates.TemplateResponse(
            request=request,
            name="not_found.html",
            context=page_context(request, database),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return templates.TemplateResponse(
        request=request,
        name="event_detail.html",
        context=page_context(request, database, event=event),
    )


@app.post("/events/{event_id}/buy", response_class=HTMLResponse)
def buy_tickets(
    event_id: int,
    request: Request,
    quantity: Annotated[int, Form()],
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    user = current_user(request, database)
    if user is None:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    event = database.get(Event, event_id)
    if event is None:
        return templates.TemplateResponse(
            request=request,
            name="not_found.html",
            context=page_context(request, database),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if quantity < 1 or quantity > 10:
        error = "Escolha entre 1 e 10 ingressos."
    elif event.available_tickets < quantity:
        error = "Não existem ingressos suficientes para essa compra."
    else:
        error = None

    if error:
        return templates.TemplateResponse(
            request=request,
            name="event_detail.html",
            context=page_context(request, database, event=event, error=error),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    event.available_tickets -= quantity
    order = Order(
        quantity=quantity,
        total_cents=event.price_cents * quantity,
        buyer_id=user.id,
        event_id=event.id,
        status="paid",
    )
    database.add(order)
    database.commit()
    print(f"Order paid: {order.id}")
    return RedirectResponse("/orders", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/orders", response_class=HTMLResponse)
def orders(
    request: Request,
    database: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    user = current_user(request, database)
    if user is None:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    user_orders = database.scalars(
        select(Order).where(Order.buyer_id == user.id).order_by(Order.created_at.desc())
    ).all()
    return templates.TemplateResponse(
        request=request,
        name="orders.html",
        context=page_context(request, database, orders=user_orders),
    )


@app.get("/api/events")
def list_events(database: Annotated[Session, Depends(get_db)]) -> list[dict[str, object]]:
    events = database.scalars(select(Event).order_by(Event.event_date)).all()
    return [
        {
            "id": event.id,
            "title": event.title,
            "venue": event.venue,
            "event_date": event.event_date,
            "price_cents": event.price_cents,
            "available_tickets": event.available_tickets,
        }
        for event in events
    ]
