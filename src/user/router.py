from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.config import settings
from src.database import get_session
from src.user import service
from src.user.models import RoleEnum, User
from src.user.schemas import UserInput, UserOutput, UserPatch
from src.user.service import delete_user, update_user, get_user_by_id, get_users_query, access_to_get_user

router = APIRouter()

token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/me", response_model=UserOutput)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/{user_id}")
async def get_user(user_id, user_recipient: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_session)):
    try:
        user = await get_user_by_id(int(user_id), session)
    except ValueError:
        raise HTTPException(status_code=404)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if await access_to_get_user(user_recipient, user):
        return user


@router.delete("/me")
async def delete_me(current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_session)):
    deleted = await delete_user(session, current_user)
    return {"deleted": deleted}


@router.patch("/me", response_model=UserOutput)
async def patch_me(
        user: UserPatch, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_session)
):

    user = await update_user(user, session, current_user)

    return user


@router.patch("/{user_id}")
async def patch_user(user_id, update_data: UserPatch, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_session)):

    if current_user.role == RoleEnum.ADMIN:
        user = await update_user(update_data, session, current_user, user_id)

    else:
        raise HTTPException(status_code=403, detail="Access denied")

    return user


@router.get("/all/")
async def get_users(current_user: Annotated[User, Depends(get_current_user)],
                    page: int = 1,
                    limit: int = 30,
                    filter_by_name: str = "",
                    sort_by: str = "id",
                    order_by: str = "asc",
                    session: AsyncSession = Depends(get_session)):

    users = await get_users_query(session, filter_by_name, sort_by, order_by, current_user)

    return users[(page - 1) * limit: page * limit]
