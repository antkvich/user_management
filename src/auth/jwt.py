from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import settings
from src.database import get_session
from src.user.service import get_user_by_email
from fastapi import status


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: Annotated[str, Depends(token_scheme)], session: AsyncSession = Depends(get_session)):

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
