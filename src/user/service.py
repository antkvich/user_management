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


async def get_user(email, session: AsyncSession):
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
    user = await get_user(email, session)

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


async def update_user(user_update: UserPatch, session: AsyncSession, token: str = Depends(token_scheme)):

    user = await get_current_user(session, token)
    [setattr(user, k, v) for k, v in dict(user_update).items() if v]
    user.modified_at = datetime.now()

    return user
