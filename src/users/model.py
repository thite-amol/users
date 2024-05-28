"""Module."""

from datetime import datetime

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, id_key
from src.role.model import user_role
from src.utils.timezone import timezone


class User(Base):
    """_summary_.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "users"

    id: Mapped[id_key] = mapped_column(init=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    username: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        comment="Username if provided ow email is used",
    )
    password: Mapped[str | None] = mapped_column(
        String(255), comment="password"
    )
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)

    is_superuser: Mapped[bool] = mapped_column(
        default=False, comment="Super Privileges (0 No 1 Yes)"
    )
    avatar: Mapped[str | None] = mapped_column(String(255), default=None)

    phone: Mapped[str | None] = mapped_column(String(11), default=None)
    join_time: Mapped[datetime] = mapped_column(
        init=False, default_factory=timezone.now_utc
    )
    last_login_time: Mapped[datetime | None] = mapped_column(
        init=False, onupdate=timezone.now_utc
    )

    is_active = Column(Boolean(), default=True)

    roles: Mapped[list["Role"]] = relationship(  # noqa: F821
        init=False, secondary=user_role, back_populates="users"
    )
