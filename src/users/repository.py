"""Module."""

from typing import AsyncGenerator

from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repository import BaseRepository
from src.role.model import Role
from src.users.model import User as UserTable
from src.users.schemas import AddUserParam, UserBase, UserCreate

all = ("UsersRepository",)


class UsersRepository(BaseRepository[UserTable]):
    """_summary_.

    Args:
        BaseRepository (_type_): _description_
    """

    def __init__(self) -> None:
        """_summary_."""
        super().__init__(UserTable)

    async def all(self) -> AsyncGenerator[UserBase, None]:
        """_summary_.

        Returns:
            AsyncGenerator[UserBase, None]: _description_

        Yields:
            Iterator[AsyncGenerator[UserBase, None]]: _description_
        """
        async for instance in self._all():
            yield instance

    async def get(self, id_: int) -> UserBase:
        """_summary_.

        Args:
            id_ (int): _description_

        Returns:
            UserBase: _description_
        """
        return await self._get(key="id", value=id_)

    async def create(self, db: AsyncSession, user_data: UserCreate) -> UserBase:
        """_summary_.

        Args:
            db (AsyncSession): _description_
            user_data (UserCreate): _description_

        Returns:
            UserBase: _description_
        """
        dict_user = user_data.model_dump()
        return await self._save(session=db, payload=dict_user)

    async def add(self, db: AsyncSession, obj: AddUserParam) -> None:
        """_summary_.

        Args:
            db (AsyncSession): _description_
            obj (AddUserParam): _description_
        """
        dict_obj = obj.model_dump(exclude={"roles"})
        new_user = self.schema_class(**dict_obj)

        role_list = []
        for role_id in obj.roles:
            role_list.append(await db.get(Role, role_id))
        new_user.roles.extend(role_list)
        db.add(new_user)

    async def update(self, schema: UserBase) -> UserBase:
        """_summary_.

        Args:
            schema (UserBase): _description_

        Returns:
            UserBase: _description_
        """
        return await self._update(
            key="id",
            value=schema.id,
            payload=schema.model_dump(exclude_unset=True),
        )

    async def get_user_by_email(
        self, db: AsyncSession, email: EmailStr
    ) -> UserBase | None:
        """_summary_.

        Args:
            db (AsyncSession): _description_
            email (EmailStr): _description_

        Returns:
            UserBase | None: _description_
        """
        return await self._get(session=db, key="email", value=email)

    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> UserBase | None:
        """_summary_.

        Args:
            db (AsyncSession): _description_
            username (str): _description_

        Returns:
            UserBase | None: _description_
        """
        return await self._get(session=db, key="username", value=username)

    async def paginate(self, limit: int, offset: int):
        """_summary_.

        Args:
            limit (int): _description_
            offset (int): _description_

        Returns:
            _type_: _description_
        """
        query = select(func.count()).select_from(self.schema_class)
        result = await self.execute(query)
        count = result.scalar()
        query = (
            select(self.schema_class).limit(limit).offset(offset).order_by("id")
        )
        data = await self.execute(query)
        return data.scalars().all(), count


UsersCRUD = UsersRepository()
