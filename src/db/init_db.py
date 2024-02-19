from src.auth.schemas import UserCreate
from src.auth.service import create_user, get_user_by_email
from src.config import settings
from src.db.engine import SessionLocal


def init_db(session: SessionLocal) -> None:
    # Tables should be created with Alembic migrations
    user = get_user_by_email(session=session, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            first_name="Admin",
            last_name="User"
        )

        create_user(session=session, user_create=user_in)
