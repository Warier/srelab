from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    events: Mapped[list[Event]] = relationship(back_populates="creator")
    orders: Mapped[list[Order]] = relationship(back_populates="buyer")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    venue: Mapped[str] = mapped_column(String(200))
    event_date: Mapped[datetime] = mapped_column(DateTime)
    price_cents: Mapped[int] = mapped_column(Integer)
    available_tickets: Mapped[int] = mapped_column(Integer)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    creator: Mapped[User] = relationship(back_populates="events")
    orders: Mapped[list[Order]] = relationship(back_populates="event")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)
    total_cents: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30), default="paid")
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    buyer: Mapped[User] = relationship(back_populates="orders")
    event: Mapped[Event] = relationship(back_populates="orders")
