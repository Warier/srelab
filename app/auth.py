import hashlib

from fastapi import Request
from sqlalchemy.orm import Session

from app.models import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(database: Session, email: str, password: str) -> User | None:
    user = database.query(User).filter(User.email == email.lower().strip()).first()
    if user is None or user.password_hash != hash_password(password):
        return None
    return user


def current_user(request: Request, database: Session) -> User | None:
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return database.get(User, user_id)
