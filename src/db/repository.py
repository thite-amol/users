from typing import Any, AsyncGenerator, Generic, Type, TypeVar

from sqlalchemy import Result, asc, delete, desc, func, select, update

from src.db.base import Base
from src.db.session import Session
from src.errors import (
    DatabaseError,
    NotFoundError,
    UnprocessableError,
)

__all__ = ("BaseRepository",)
ModelType = TypeVar("ModelType", bound=Any)


# Mypy error: https://github.com/python/mypy/issues/13755
class BaseRepository(Session, Generic[Base]):  # type: ignore
    """This class implements the base interface for working with database
    # and makes it easier to work with type annotations.
    """

    schema_class: Type[Base]

    def __init__(self, model: type[ModelType]) -> None:
        super().__init__()
        self.schema_class = model

        if not self.schema_class:
            raise UnprocessableError(
                message=(
                    "Can not initiate the class without schema_class attribute"
                )
            )

    async def _update(
            self, key: str, value: Any, payload: dict[str, Any]
    ) -> Base:
        """Updates an existed instance of the model in the related table.
        If some data is not exist in the payload then the null value will
        be passed to the schema class."""

        query = (
            update(self.schema_class)
            .where(getattr(self.schema_class, key) == value)
            .values(payload)
            .returning(self.schema_class)
        )
        result: Result = await self.execute(query)
        await self._session.flush()
        await self._session.commit()
        await self._session.refresh(payload)

        if not (schema := result.scalar_one_or_none()):
            raise DatabaseError

        return schema

    async def _get(self, key: str, value: Any) -> Base:
        """Return only one result by filters"""

        query = select(self.schema_class).where(
            getattr(self.schema_class, key) == value
        )
        result: Result = await self.execute(query)

        return result.scalars().one_or_none()

    async def count(self) -> int:
        result: Result = await self.execute(func.count(self.schema_class.id))
        value = result.scalar()

        if not isinstance(value, int):
            raise UnprocessableError(
                message=(
                    "For some reason count function returned not an integer."
                    f"Value: {value}"
                ),
            )

        return value

    async def _first(self, by: str = "id") -> Base:
        result: Result = await self.execute(
            select(self.schema_class).order_by(asc(by)).limit(1)
        )

        if not (_result := result.scalar_one_or_none()):
            raise NotFoundError

        return _result

    async def _last(self, by: str = "id") -> Base:
        result: Result = await self.execute(
            select(self.schema_class).order_by(desc(by)).limit(1)
        )

        if not (_result := result.scalar_one_or_none()):
            raise NotFoundError

        return _result

    async def _save(self, payload: dict[str, Any]) -> Base:
        try:
            schema = self.schema_class(**payload)
            self._session.add(schema)
            await self._session.flush()
            await self._session.commit()
            await self._session.refresh(schema)
            return schema
        except self._ERRORS:
            raise DatabaseError

    async def _all(self) -> AsyncGenerator[Base, None]:
        result: Result = await self.execute(select(self.schema_class))
        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def delete(self, id_: int) -> None:
        await self.execute(
            delete(self.schema_class).where(self.schema_class.id == id_)
        )
        await self._session.flush()
