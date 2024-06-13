"""User repository to perform database operations."""

from typing import AsyncGenerator, Callable, Optional

from pydantic import EmailStr
from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from src.db.repository import BaseRepository
from src.users.model import User as UserTable
from src.users.schemas import UserBase, UserCreate
from src.utils.timezone import timezone

func: Callable


class UsersRepository(BaseRepository[UserTable]):
    """Repository class to perform database operations."""

    def __init__(self) -> None:
        """Initializer."""
        super().__init__(UserTable)

    async def all(self, db: AsyncSession) -> AsyncGenerator[UserBase, None]:
        """Return all records.

        Returns:
            AsyncGenerator[UserBase, None]: _description_

        Yields:
            Iterator[AsyncGenerator[UserBase, None]]: _description_
        """
        async for instance in self._all(session=db):
            yield instance

    async def get(self, db: AsyncSession, id_: int) -> UserBase:
        """_summary_.

        Args:
            db (AsyncSession): _description_
            id_ (int): _description_

        Returns:
            UserBase: _description_
        """
        return await self._get(session=db, key="id", value=id_)

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

    # async def add(self, db: AsyncSession, obj: AddUserParam) -> None:
    #     """_summary_.

    #     Args:
    #         db (AsyncSession): _description_
    #         obj (AddUserParam): _description_
    #     """
    #     dict_obj = obj.model_dump(exclude={"roles"})
    #     new_user = self.schema_class(**dict_obj)

    #     role_list = []
    #     for role_id in obj.roles:
    #         role_list.append(await db.get(Role, role_id))
    #     new_user.roles.extend(role_list)
    #     db.add(new_user)

    async def update(self, db: AsyncSession, schema: UserBase) -> UserBase:
        """_summary_.

        Args:
            db (AsyncSession): _description_
            schema (UserBase): _description_

        Returns:
            UserBase: _description_
        """
        return await self._update(
            session=db,
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

    async def update_login_time(
        self, db: AsyncSession, user_data: UserBase
    ) -> UserBase:
        """Update user login time.


        Args:
            db (AsyncSession): database session
            user_data (str): Current user data

        Returns:
            UserBase: User detail
        """
        user_data.last_login_time = timezone.now_utc()
        await db.commit()
        await db.refresh(user_data)
        return user_data

    async def get_list(
        self,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[int] = None,
    ) -> Select:
        """_summary_.

        Args:
            username (str, optional): _description_. Defaults to None.
            phone (str, optional): _description_. Defaults to None.
            status (int, optional): _description_. Defaults to None.

        Returns:
            Select: _description_
        """
        se = (
            select(self.schema_class)
            .options(selectinload(self.schema_class.roles))
            .order_by(desc(self.schema_class.join_time))
        )
        where_list = []
        if username:
            where_list.append(self.schema_class.username.like(f"%{username}%"))
        if phone:
            where_list.append(self.schema_class.phone.like(f"%{phone}%"))
        if status is not None:
            where_list.append(self.schema_class.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        return se


UsersCRUD = UsersRepository()
