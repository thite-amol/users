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

from src.auth.schemas import AuthSchemaBase, GetLoginToken
from src.auth.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from src.common.exception import errors
from src.config import settings
from src.db.session import CurrentSession
from src.users.repository import UsersCRUD


async def login(*, db: CurrentSession, obj: AuthSchemaBase) -> GetLoginToken:
    """_summary_.

    Args:
        db (CurrentSession): _description_
        obj (AuthSchemaBase): _description_

    Raises:
        errors.NotFoundError: _description_
        errors.AuthorizationError: _description_
        errors.AuthorizationError: _description_
        errors.NotFoundError: _description_
        errors.AuthorizationError: _description_
        e: _description_

    Returns:
        GetLoginToken: _description_
    """
    try:
        current_user = await UsersCRUD.get_by_username(db, obj.username)
        if not current_user:
            raise errors.NotFoundError(msg="User does not exist")
        elif not verify_password(obj.password, current_user.password):
            raise errors.AuthorizationError(msg="Invalid Username or Password")
        elif not current_user.is_active:
            raise errors.AuthorizationError(msg="User is locked, login failed")
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
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


# async def new_token(*,db:CurrentSession, refresh_token: str) -> GetNewToken:
#     user_id = await jwt_decode(refresh_token)
#     if request.user.id != user_id:
#         raise errors.TokenError(msg='Refresh token is invalid')
#
#     current_user = await UsersCRUD.get(db, user_id)
#     if not current_user:
#         raise errors.NotFoundError(msg='User does not exist')
#     elif not current_user.status:
#         raise errors.AuthorizationError(msg='User is locked, operation failed')
#     current_token = await get_token(request)
#     (
#         new_access_token,
#         new_refresh_token,
#         new_access_token_expire_time,
#         new_refresh_token_expire_time,
#     ) = await create_new_token(
#         str(current_user.id), current_token, refresh_token, multi_login=current_user.is_multi_login
#     )
#     data = GetNewToken(
#         access_token=new_access_token,
#         access_token_expire_time=new_access_token_expire_time,
#         refresh_token=new_refresh_token,
#         refresh_token_expire_time=new_refresh_token_expire_time,
#     )
#     return data


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
#     key = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:{token}'
#     await redis_client.delete(key)
# else:
#     prefix = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:'
#     await redis_client.delete_prefix(prefix)
