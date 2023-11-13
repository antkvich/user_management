import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.user.models import RoleEnum, timestamp
from src.user.models import User


class UserInput(BaseModel):

    # id: int
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: RoleEnum
    group_id: int = 1
    created_at: timestamp
    is_blocked: bool = False
    modified_at: timestamp
    image_url: Optional[str] = None
    password: str


class UserPatch(BaseModel):

    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    image_url: Optional[str] = None


class UserOutput(BaseModel):

    id: int
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: RoleEnum
    group_id: int = 1
    created_at: timestamp
    is_blocked: bool = False
    modified_at: timestamp
    image_url: Optional[str] = None


class TokenInput(BaseModel):
    token: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Group(BaseModel):

    id: int
    name: str
    created_at: datetime.datetime
