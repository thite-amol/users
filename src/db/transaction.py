from functools import wraps

from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import CTX_SESSION, get_session
from src.errors import DatabaseError


def transaction(coro):
    """This decorator should be used with all coroutines
    that want's access the database for saving a new data.
    """

    @wraps(coro)
    async def inner(*args, **kwargs):
        session: AsyncSession = get_session()
        CTX_SESSION.set(session)

        try:
            result = await coro(*args, **kwargs)
            await session.commit()
            return result
        except DatabaseError:
            # NOTE: If any sort of issues are occurred in the code
            #       they are handled on the BaseCRUD level and raised
            #       as a DatabseError.
            #       If the DatabseError is handled within domain/application
            #       levels it is possible that `await session.commit()`
            #       would raise an error.
            await session.rollback()
            raise DatabaseError
        except (IntegrityError, PendingRollbackError):
            # NOTE: Since there is a session commit on this level it should
            #       be handled because it can raise some errors also
            await session.rollback()
        finally:
            await session.close()

    return inner
