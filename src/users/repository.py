from typing import AsyncGenerator

from pydantic import EmailStr

from src.db.repository import BaseRepository
from src.db.transaction import transaction
from src.users.model import User as UserTable
from src.users.schemas import UserBase, UserCreate

all = ("UsersRepository",)


class UsersRepository(BaseRepository[UserTable]):
    def __init__(self) -> None:
        super().__init__(UserTable)

    async def all(self) -> AsyncGenerator[UserBase, None]:
        async for instance in self._all():
            yield instance

    async def get(self, id_: int) -> UserBase:
        return await self._get(key="id", value=id_)

    async def create(self, schema: UserCreate) -> UserBase:
        return await self._save(schema.model_dump())

    @transaction
    async def update(self, schema: UserBase) -> UserBase:
        return await self._update(key="id", value=schema.id, payload=schema.model_dump(exclude_unset=True))

    async def get_user_by_email(self, email: EmailStr) -> UserBase | None:
        return await self._get(key="email", value=email)


UsersCRUD = UsersRepository()
