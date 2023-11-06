import datetime
from typing import Optional

from pydantic import BaseModel

from src.user.models import RoleEnum


class User(BaseModel):

    id: int
    name: str
    surname: str
    username: str
    phone_number: str
    email: str
    role: RoleEnum
    group_id: int
    created_at: datetime.datetime
    is_blocked: bool
    modified_at: datetime.datetime
    image_url: Optional[str]


class Group(BaseModel):

    id: int
    name: str
    created_at: datetime.datetime
