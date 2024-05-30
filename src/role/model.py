"""Module."""

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, id_key

# Database model, database table inferred from class name
user_role = Table(
    "user_role",
    Base.metadata,
    # Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Role(Base):
    """_summary_.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "roles"

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    data_scope: Mapped[int | None] = mapped_column(
        default=2,
        comment="Permission Scope (1: All Data Permissions 2: Custom Data Permissions)",
    )
    status: Mapped[int] = mapped_column(default=1)
    remark: Mapped[str | None] = mapped_column(Text, default=None)
    #  Role users are many-to-many
    users: Mapped[list["User"]] = relationship(  # noqa: F821
        init=False, secondary=user_role, back_populates="roles"
    )
