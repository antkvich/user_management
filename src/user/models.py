import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Integer, String, ForeignKey, func, Boolean, Index, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from src.database import Base


class RoleEnum(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text(30))
    surname: Mapped[str] = mapped_column(Text(30))
    username: Mapped[str] = mapped_column(Text(30), unique=True)
    phone_number: Mapped[str] = mapped_column(Text(14), unique=True)
    email: Mapped[str] = mapped_column(Text(30), unique=True)
    role: Mapped[RoleEnum]
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))
    created_at: Mapped[datetime]
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    modified_at: Mapped[datetime.datetime]
    image_url: Mapped[Optional[str]] = mapped_column(Text)

    group = relationship("Group", back_populates="users")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text(30))
    created_at: Mapped[datetime.datetime]

    users = relationship("User", back_populates="groups")
