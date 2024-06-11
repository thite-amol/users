"""Module."""

import sys
from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.common.log import log
from src.config import settings


def create_engine_and_session(url: str | URL):
    """_summary_.

    Args:
        url (str | URL): _description_

    Returns:
        _type_: _description_
    """
    try:
        engine = create_async_engine(
            url,
            echo=settings.database.QUERY_ECHO,
            future=True,
            pool_pre_ping=True,
        )
    except Exception as e:  # pylint: disable=broad-except
        log.error(f"❌ database link failed {e}")
        sys.exit()
    else:
        db_session = async_sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False
        )
        return engine, db_session


# SQLALCHEMY_DATABASE_URL = (
#     f'mysql+asyncmy://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:'
#     f'{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset={settings.MYSQL_CHARSET}'
# )

async_engine, async_db_session = create_engine_and_session(
    settings.database.DATABASE_CONNECTION_URL
)


async def get_db() -> AsyncSession:
    """Session builder.

    Raises:
        se: _description_

    Returns:
        AsyncSession: _description_

    Yields:
        Iterator[AsyncSession]: _description_
    """
    session = async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()


CurrentSession = Annotated[AsyncSession, Depends(get_db)]
