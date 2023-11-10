from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_session
from src.user import service
from src.user.schemas import UserInput, UserOutput, UserPatch
from src.user.service import delete_user, update_user

router = APIRouter()

token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/me", response_model=UserOutput)
async def get_me(token: Annotated[str, Depends(token_scheme)], session: AsyncSession = Depends(get_session)):
    user = await service.get_current_user(session, token)
    # user = service.serialise_user_out(user)
    return user


@router.get("/user_id", response_model=UserOutput)
async def get_user(user_id):
    pass


@router.delete("/me")
async def delete_me(token: Annotated[str, Depends(token_scheme)], session: AsyncSession = Depends(get_session)):
    deleted = await delete_user(session, token)

    try:
        await session.commit()
        await session.flush()
    except IntegrityError as e:
        await session.rollback()

    return {"deleted": deleted}


@router.patch("/me", response_model=UserOutput)
async def patch_me(
        user: UserPatch, token: Annotated[str, Depends(token_scheme)], session: AsyncSession = Depends(get_session)
) -> UserOutput:

    user = await update_user(user, session, token)

    await session.commit()
    await session.flush()

    return user


@router.patch("/user_id")
async def patch_user(user: UserInput):
    return user


@router.get("/all")
async def get_uses():
    pass
