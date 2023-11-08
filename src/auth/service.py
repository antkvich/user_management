from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from typing import Any, Union

from src.user.schemas import UserInput
from src.user.models import User

from uuid import uuid4

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_access_token, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_refresh_token, ALGORITHM)
    return encoded_jwt


def add_user(session: AsyncSession, data: UserInput):
    hashed_password = get_hashed_password(data.password)
    new_user = User(
        name=data.name,
        surname=data.surname,
        group_id=data.group_id,
        username=data.username,
        phone_number=data.phone_number,
        email=data.email,
        role=data.role,
        created_at=data.created_at.replace(tzinfo=None),
        modified_at=data.modified_at.replace(tzinfo=None),
        image_url=data.image_url,
        hashed_password=hashed_password,
        is_blocked=data.is_blocked,
    )
    session.add(new_user)
    return new_user
