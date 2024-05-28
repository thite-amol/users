"""Module."""

from src.config import settings
from src.users.repository import UsersCRUD
from src.users.schemas import UserCreate


async def init_db() -> None:
    """Tables should be created with Alembic migrations."""
    user = await UsersCRUD.get_user_by_email(email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            first_name="Admin",
            last_name="User",
        )

        await UsersCRUD.create(schema=user_in)
    else:
        pass
