import datetime
from typing import Annotated, Optional

from sqlalchemy import DateTime, Enum, Integer, String, ForeignKey, func, Boolean, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


class Base(DeclarativeBase):
    pass


class RoleEnum(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    phone_number: Mapped[str] = mapped_column(String(14), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    role: Mapped[RoleEnum]
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))
    created_at: Mapped[timestamp] = mapped_column(server_default=func.UTC_TIMESTAMP())
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    modified_at: Mapped[datetime.datetime]
    image_url: Mapped[str] = Mapped[Optional[str]]

    group = relationship("Group", back_populates="users")

    user_email_idx = Index("user_email_index", email, unique=True)
    user_username_idx = Index("user_username_index", username, unique=True)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime]

    users = relationship("User", back_populates="groups")

    group_name_idx = Index("group_name_idx", name)

