"""Authentication service module."""

# from src.common.security.jwt import (
#     create_access_token,
#     create_new_token,
#     create_refresh_token,
#     get_token,
#     jwt_decode,
#     password_verify,
# )
from datetime import timedelta

from fastapi.security import HTTPBasicCredentials

from src.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    update_refresh_token,
)
from src.auth.utils import verify_password
from src.common.exception import errors
from src.config import settings
from src.db.session import CurrentSession
from src.users.repository import UsersCRUD
from src.users.schemas import GetLoginToken, GetNewToken


async def login(
    *, db: CurrentSession, form_data: HTTPBasicCredentials
) -> GetLoginToken:
    """Generate login token by validating credentials.

    Args:
        db (CurrentSession): Current database session
        form_data (HTTPBasicCredentials): User form details

    Raises:
        errors.NotFoundError: If user id not present in database
        errors.AuthorizationError: If credentials are invalid

    Returns:
        GetLoginToken: JWT token
    """
    try:
        current_user = await UsersCRUD.get_by_username(db, form_data.username)
        if not current_user:
            raise errors.NotFoundError(msg="User does not exist")
        elif not verify_password(form_data.password, current_user.password):
            raise errors.AuthorizationError(msg="Invalid Username or Password")
        elif not current_user.is_active:
            raise errors.AuthorizationError(msg="User is locked, login failed")
        access_token_expires = timedelta(
            minutes=settings.base.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token, access_token_expire_time = create_access_token(
            str(current_user.id), expires_delta=access_token_expires
        )
        refresh_token, refresh_token_expire_time = create_refresh_token(
            str(current_user.id), access_token_expire_time
        )
        await UsersCRUD.update_login_time(db, current_user)
    except errors.NotFoundError as e:
        raise errors.NotFoundError(msg=e.msg)
    except (errors.AuthorizationError, errors.CustomError) as e:
        raise errors.AuthorizationError(msg=e.msg)
    except Exception as e:
        raise e
    else:
        data = GetLoginToken(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expire_time=access_token_expire_time,
            refresh_token_expire_time=refresh_token_expire_time,
            user=current_user,
        )
        return data


async def new_token(
    *, request, db: CurrentSession, refresh_token: str, current_token: str
) -> GetNewToken:
    """Create a new token.

    Args:
        request (_type_): Current app request
        db (CurrentSession): Current app db session
        refresh_token (str): refresh token
        current_token (str): Current user token

    Raises:
        errors.TokenError: If token is invalid
        errors.NotFoundError: If user is not available
        errors.AuthorizationError: If token data mismatched

    Returns:
        GetNewToken: Token data
    """
    user_id = await decode_token(refresh_token)
    if request.user.id != user_id:
        raise errors.TokenError(msg="Refresh token is invalid")

    current_user = await UsersCRUD.get(db, user_id)
    if not current_user:
        raise errors.NotFoundError(msg="User does not exist")
    elif not current_user.status:
        raise errors.AuthorizationError(msg="User is locked, operation failed")
    (
        new_access_token,
        new_refresh_token,
        new_access_token_expire_time,
        new_refresh_token_expire_time,
    ) = await update_refresh_token(
        str(current_user.id),
        current_token,
        refresh_token,
        multi_login=current_user.is_multi_login,
    )

    data = GetNewToken(
        access_token=new_access_token,
        access_token_expire_time=new_access_token_expire_time,
        refresh_token=new_refresh_token,
        refresh_token_expire_time=new_refresh_token_expire_time,
    )
    return data


# async def logout(*, request: Request) -> None:
#     """_summary_.
#
#     Args:
#         request (Request): _description_
#     """
#     # TODO implement logout
#     pass
# token = await get_token(request)
# if request.user.is_multi_login:
#     key = f'{settings.base.TOKEN_REDIS_PREFIX}:{request.user.id}:{token}'
#     await redis_client.delete(key)
# else:
#     prefix = f'{settings.base.TOKEN_REDIS_PREFIX}:{request.user.id}:'
#     await redis_client.delete_prefix(prefix)
