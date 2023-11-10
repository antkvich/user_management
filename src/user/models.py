import datetime
from enum import Enum
from typing import Annotated, Optional

from sqlalchemy import (Boolean, DateTime, ForeignKey, Index, Integer, String,
                        Text, func)
from sqlalchemy.orm import (DeclarativeBase, Mapped, Relationship,
                            mapped_column, relationship)

from src.database import Base

timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


class RoleEnum(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    surname: Mapped[str] = mapped_column(Text)
    username: Mapped[str] = mapped_column(Text, unique=True)
    phone_number: Mapped[str] = mapped_column(Text, unique=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.USER)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), nullable=True, default="1")
    created_at: Mapped[timestamp]
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    modified_at: Mapped[timestamp]
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hashed_password: Mapped[str] = mapped_column(Text)

    groups = relationship("Group", back_populates="users")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    created_at: Mapped[timestamp]

    users = relationship("User", back_populates="groups")
