"""Mimic session variables."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import create_engine_and_session

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///"

engine, test_async_db_session = create_engine_and_session(
    SQLALCHEMY_DATABASE_URL
)


async def override_get_db() -> AsyncSession:
    """Session builder."""
    session = test_async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()
