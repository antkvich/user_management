from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import add_user, create_access_token, create_refresh_token, verify_password
from src.user.models import User
from src.user.schemas import UserInput, UserLogin
from src.database import get_session

from sqlalchemy import select

router = APIRouter()


@router.post("/signup")
async def signup(data: UserInput, session: AsyncSession = Depends(get_session)):
    mail_user = await session.execute(select(User).where(data.email == User.email))
    if mail_user.scalars().all():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    user = add_user(session, data)
    try:
        await session.commit()
        return user
    except IntegrityError as e:
        await session.rollback()


@router.post("/login")
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    mail_user = await session.execute(select(User).where(data.email == User.email))
    mail_user = mail_user.scalar()
    if mail_user is None:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = mail_user.hashed_password
    if not verify_password(data.password, hashed_pass):
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(mail_user.email),
        "refresh_token": create_refresh_token(mail_user.email),
    }


@router.post("/refresh_token")
async def refresh_token():
    pass


@router.post("/reset_password")
async def reset_password():
    pass
