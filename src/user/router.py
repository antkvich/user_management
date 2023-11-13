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
from src.user.models import RoleEnum
from src.user.schemas import UserInput, UserOutput, UserPatch
from src.user.service import delete_user, update_user, get_user_by_id, get_users_query

router = APIRouter()

token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/me", response_model=UserOutput)
async def get_me(token: Annotated[str, Depends(token_scheme)], session: AsyncSession = Depends(get_session)):
    user = await service.get_current_user(session, token)
    return user


@router.get("/{user_id}")
async def get_user(user_id, token: Annotated[str, Depends(token_scheme)], session: AsyncSession = Depends(get_session)):
    try:
        user = await get_user_by_id(int(user_id), session)
    except ValueError:
        raise HTTPException(status_code=404)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_recipient = await service.get_current_user(session, token)
    if user_recipient.role == RoleEnum.ADMIN:
        return user
    elif user_recipient.role == RoleEnum.MODERATOR and user.group_id == user_recipient.group_id:
        return user
    else:
        raise HTTPException(status_code=403, detail="Access denied")


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


@router.patch("/{user_id}")
async def patch_user(user_id, update_data: UserPatch, token: Annotated[str, Depends(token_scheme)], session: AsyncSession = Depends(get_session)):
    try:
        user = await get_user_by_id(int(user_id), session)
    except ValueError:
        raise HTTPException(status_code=404)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_recipient = await service.get_current_user(session, token)
    if user_recipient.role == RoleEnum.ADMIN:
        user = await update_user(update_data, session, token, user)

        await session.commit()
        await session.flush()

    else:
        raise HTTPException(status_code=403, detail="Access denied")

    return user


@router.get("/all")
async def get_users(token: Annotated[str, Depends(token_scheme)],
                    page: int = 1,
                    limit: int = 30,
                    filter_by_name: str = "",
                    sort_by: str = "id",
                    order_by: str = "asc",
                    session: AsyncSession = Depends(get_session)):
    users = get_users_query(session, limit, filter_by_name, sort_by, order_by, token)
    return users
