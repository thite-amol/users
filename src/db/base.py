"""Module."""

from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    declared_attr,
    mapped_column,
)

from src.utils.timezone import timezone

# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[  # pylint: disable=invalid-name
    int,
    mapped_column(
        primary_key=True, index=True, autoincrement=True, sort_order=-999
    ),
]


class MappedBase(DeclarativeBase):
    """`DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__.

    Args:
        DeclarativeBase (_type_): _description_

    Returns:
        _type_: _description_
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        """_summary_.

        Returns:
            str: _description_
        """
        return cls.__name__.lower()


class DateTimeMixin(MappedAsDataclass):
    """_summary_.

    Args:
        MappedAsDataclass (_type_): _description_
    """

    created_time: Mapped[datetime] = mapped_column(
        init=False, default_factory=timezone.now_utc, sort_order=999
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        init=False, onupdate=timezone.now_utc, sort_order=999
    )


class DataClassBase(MappedAsDataclass, MappedBase):
    """`MappedAsDataclass
    <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__.

    Args:
        MappedAsDataclass (_type_): _description_
        MappedBase (_type_): _description_
    """

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    """_summary_.

    Args:
        DataClassBase (_type_): _description_
        DateTimeMixin (_type_): _description_
    """

    __abstract__ = True
