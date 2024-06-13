"""Module."""

from typing import Optional

from sqlalchemy.sql import Select

from src.common.exception import errors
from src.config import settings
from src.db.session import CurrentSession
from src.users.repository import UsersCRUD
from src.users.schemas import UserCreateOpen, UserOut


class UserService:
    """_summary_.

    Raises:
        errors.ForbiddenError: _description_
        errors.ForbiddenError: _description_
        errors.RequestError: _description_
        errors.ForbiddenError: _description_

    Returns:
        _type_: _description_
    """

    @staticmethod
    async def register(
        *, user_data: UserCreateOpen, db: CurrentSession
    ) -> UserOut:
        """_summary_.

        Args:
            user_data (UserCreateOpen): _description_
            db (CurrentSession): _description_

        Raises:
            errors.RequestError: _description_
            errors.ForbiddenError: _description_

        Returns:
            UserOut: _description_
        """
        if not settings.USERS_OPEN_REGISTRATION:
            raise errors.ForbiddenError(
                msg="Open user registration is forbidden on this server",
            )

        username = await UsersCRUD.get_by_username(db, user_data.username)
        if username:
            raise errors.RequestError(msg="This username is already registered")

        email = await UsersCRUD.get_user_by_email(db, email=user_data.email)

        if email:
            raise errors.RequestError(msg="The email has been registered")
        return await UsersCRUD.create(db, user_data)

    @staticmethod
    async def get_select(
        *,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[int] = None,
    ) -> Select:
        """Build Select query to be used while fetching records.

        Args:
            username (Optional[str], optional): User username. Defaults to None.
            phone (Optional[str], optional): User phone number. Defaults to None.
            status (Optional[int], optional): User status. Defaults to None.

        Returns:
            Select: SQLAlchemy Select class obj
        """
        return await UsersCRUD.get_list(
            username=username, phone=phone, status=status
        )


user_service = UserService()
