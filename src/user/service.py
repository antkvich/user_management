from datetime import datetime
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.config import settings
from src.user.schemas import UserInput, UserPatch
from src.user.models import User

token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_user_by_email(email, session: AsyncSession):
    user = await session.execute(select(User).where(email == User.email))
    user = user.scalars().first()
    return user

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(session: AsyncSession, token: str = Depends(token_scheme)):

    try:
        payload = jwt.decode(
            token, settings.jwt_access_token, algorithms=[settings.token_algorithm]
        )
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = await get_user_by_email(email, session)

    return user


async def delete_user(session: AsyncSession, token: str = Depends(token_scheme)):
    deleted = False
    try:
        payload = jwt.decode(
            token, settings.jwt_access_token, algorithms=[settings.token_algorithm]
        )
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    await session.execute(delete(User).where(User.email == email))
    deleted = True
    return deleted


async def update_user(
        user_update: UserPatch, session: AsyncSession, token: str = Depends(token_scheme), user_to_update: User = None
):
    if not user_to_update:
        user = await get_current_user(session, token)
    else:
        user = user_to_update
    [setattr(user, k, v) for k, v in dict(user_update).items() if v]
    user.modified_at = datetime.now()

    return user


async def get_user_by_id(user_id, session: AsyncSession, token: str = Depends(token_scheme)):
    user = await session.execute(select(User).where(user_id == User.id))
    user = user.scalars().first()
    return user


async def get_users_query(
        session: AsyncSession,
        limit: int,
        filter_by_name: str,
        sort_by_field: str,
        order_by: str,
        token: str = Depends(token_scheme)
):
    match sort_by_field:
        case "id":
            sort_by_field = User.id
        case "name":
            sort_by_field = User.name
        case "surname":
            sort_by_field = User.surname
        case "username":
            sort_by_field = User.username
        case "created_at":
            sort_by_field = User.created_at
        case "modified_at":
            sort_by_field = User.modified_at
        case "role":
            sort_by_field = User.role
        case "group_id":
            sort_by_field = User.group_id
        case "is_blocked":
            sort_by_field = User.is_blocked
        case _:
            sort_by_field = User.id

    if order_by == "desc":
        users = await session.execute(select(User).where(filter_by_name == User.name).order_by(sort_by_field.desc()).limit(limit))
    else:
        users = await session.execute(select(User).where(filter_by_name == User.name).order_by(sort_by_field.asc()).limit(limit))

    users = users.scalars().all()

    return users
