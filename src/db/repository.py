"""Module."""

from typing import Any, AsyncGenerator, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Result, asc, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import Base

_Model = TypeVar("_Model")
_CreateSchema = TypeVar("_CreateSchema", bound=BaseModel)
_UpdateSchema = TypeVar("_UpdateSchema", bound=BaseModel)


class BaseRepository(Generic[_Model]):
    """This class implements the base interface for working with database and makes it easier to work with type annotations.

    Args:
        Generic (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """

    schema_class: Type[Base]

    def __init__(self, model: Type[_Model]) -> None:
        """_summary_.

        Args:
            model (Type[_Model]): _description_
        """
        self.schema_class = model

    async def _update(
        self,
        session: AsyncSession,
        key: str,
        value: Any,
        payload: dict[str, Any],
    ) -> Base:
        """Updates an existed instance of the model in the related table.
        If some data is not exist in the payload then the null value will
        be passed to the schema class.

        Args:
            session (AsyncSession): _description_
            key (str): _description_
            value (Any): _description_
            payload (dict[str, Any]): _description_

        Raises:
            Exception: _description_

        Returns:
            Base: _description_
        """
        query = (
            update(self.schema_class)
            .where(getattr(self.schema_class, key) == value)
            .values(payload)
            .returning(self.schema_class)
        )
        result: Result = await session.execute(query)
        await session.flush()
        await session.commit()
        await session.refresh(payload)

        if not (schema := result.scalar_one_or_none()):
            raise Exception

        return schema

    async def _get(
        self, session: AsyncSession, key: str, value: Any
    ) -> Base | None:
        """Return only one result by filters.

        Args:
            session (AsyncSession): _description_
            key (str): _description_
            value (Any): _description_

        Returns:
            Base | None: _description_
        """
        query = select(self.schema_class).where(
            getattr(self.schema_class, key) == value
        )

        result: Result = await session.execute(query)

        return result.scalars().one_or_none()

    async def count(self, session: AsyncSession) -> int:
        """_summary_.

        Args:
            session (AsyncSession): _description_

        Returns:
            int: _description_
        """
        result: Result = await session.execute(func.count(self.schema_class.id))
        value = result.scalar()

        return value

    async def _first(self, session: AsyncSession, by: str = "id") -> Base:
        """_summary_.

        Args:
            session (AsyncSession): _description_
            by (str, optional): _description_. Defaults to "id".

        Raises:
            Exception: _description_

        Returns:
            Base: _description_
        """
        result: Result = await session.execute(
            select(self.schema_class).order_by(asc(by)).limit(1)
        )

        if not (_result := result.scalar_one_or_none()):
            raise Exception

        return _result

    async def _last(self, session: AsyncSession, by: str = "id") -> Base:
        """_summary_.

        Args:
            session (AsyncSession): _description_
            by (str, optional): _description_. Defaults to "id".

        Raises:
            Exception: _description_

        Returns:
            Base: _description_
        """
        result: Result = await session.execute(
            select(self.schema_class).order_by(desc(by)).limit(1)
        )

        if not (_result := result.scalar_one_or_none()):
            raise Exception

        return _result

    async def _save(
        self, session: AsyncSession, payload: dict[str, Any]
    ) -> Base:
        """_summary_.

        Args:
            session (AsyncSession): _description_
            payload (dict[str, Any]): _description_

        Returns:
            Base: _description_
        """
        schema = self.schema_class(**payload)
        session.add(schema)
        return schema

    async def _all(self, session: AsyncSession) -> AsyncGenerator[Base, None]:
        """_summary_.

        Args:
            session (AsyncSession): _description_

        Returns:
            AsyncGenerator[Base, None]: _description_

        Yields:
            Iterator[AsyncGenerator[Base, None]]: _description_
        """
        result: Result = await session.execute(select(self.schema_class))
        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def delete(self, session: AsyncSession, id_: int) -> bool:
        """_summary_.

        Args:
            session (AsyncSession): _description_
            id_ (int): _description_

        Returns:
            bool: _description_
        """
        await session.execute(
            delete(self.schema_class).where(self.schema_class.id == id_)
        )
        await session.flush()
        await session.commit()

        return True
