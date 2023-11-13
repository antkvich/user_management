from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, asc, desc

from src.user.schemas import UserInput, UserPatch
from src.user.models import User, RoleEnum


async def get_user_by_email(email, session: AsyncSession):
    user_query = await session.execute(select(User).where(email == User.email))
    user = user_query.scalars().first()
    return user


async def delete_user(session: AsyncSession, user) -> bool:
    deleted = False
    await session.execute(delete(User).where(User.email == user.email))
    try:
        await session.commit()
        await session.flush()
    except IntegrityError as e:
        await session.rollback()
    deleted = True
    return deleted


async def update_user(
        user_update: UserPatch, session: AsyncSession, current_user: User, user_id_to_update: int = None
):
    if not user_id_to_update:
        user = current_user
    else:
        user = await get_user_by_id(int(user_id_to_update), session)
    [setattr(user, k, v) for k, v in dict(user_update).items() if v]
    user.modified_at = datetime.now()

    await session.commit()
    await session.flush()

    return user


async def get_user_by_id(user_id, session: AsyncSession):
    user = await session.execute(select(User).where(user_id == User.id))
    user = user.scalars().first()
    return user


async def get_users_query(
        session: AsyncSession,
        filter_by_name: str,
        sort_by_field: str,
        order_by: str,
        user_recipient: User
):
    if user_recipient.role == RoleEnum.ADMIN:
        if order_by == "desc":
            users = await session.execute(select(User).where(filter_by_name == User.name).order_by(desc(sort_by_field)))
        else:
            users = await session.execute(select(User).where(filter_by_name == User.name).order_by(asc(sort_by_field)))
    elif user_recipient.role == RoleEnum.MODERATOR:
        if order_by == "desc":
            users = await session.execute(select(User).where(filter_by_name == User.name).where(User.group_id == user_recipient.group_id).order_by(desc(sort_by_field)))
        else:
            users = await session.execute(select(User).where(filter_by_name == User.name).where(User.group_id == user_recipient.group_id).order_by(asc(sort_by_field)))
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    users = users.scalars().all()

    return users


async def access_to_get_user(user_recipient, user):
    if user_recipient.role == RoleEnum.ADMIN:
        return True
    elif user_recipient.role == RoleEnum.MODERATOR and user.group_id == user_recipient.group_id:
        return True
    else:
        return False
