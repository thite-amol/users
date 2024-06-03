"""Auth security operation module."""

from datetime import datetime, timedelta
from typing import Any, Optional, Union

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from src.common.exception.errors import TokenError
from src.config import settings
from src.users.schemas import TokenPayload
from src.utils.timezone import timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> tuple[str, datetime]:
    """Generate encryption JWT token.

    Args:
        subject (Union[str, Any]): User identifier
        expires_delta (Optional[timedelta], optional): Time in token will expire. Defaults to None.

    Returns:
        tuple[str, datetime]: JWT token and expire delta
    """
    if expires_delta:
        expire = timezone.now_utc() + expires_delta
    else:
        expire = timezone.now_utc() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt, expire


def create_refresh_token(
    sub: str, expire_time: datetime | None = None, **kwargs
) -> tuple[str, datetime]:
    """Generate encryption refresh token, only used to create a new token.

    Args:
        sub (str): User identifier
        expire_time (datetime | None, optional): Time in token will expire. Defaults to None.
        kwargs: Dynamic params

    Raises:
        TokenError: If the refresh token is expired

    Returns:
        tuple[str, datetime]: JWT token and expire delta
    """
    if expire_time:
        expire = expire_time + timedelta(seconds=settings.TOKEN_EXPIRE_MINUTES)
        expire_datetime = timezone.f_datetime(expire_time)
        current_datetime = timezone.now_utc()
        if expire_datetime < current_datetime:
            raise TokenError(msg="Refresh token expired.")
    else:
        expire = timezone.now_utc() + timedelta(
            seconds=settings.TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": sub, **kwargs}
    refresh_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return refresh_token, expire


def decode_token(token: str) -> TokenPayload:
    """Decode JWT token.

    Args:
        token (str): JWT token

    Raises:
        TokenError: If token is not valid

    Returns:
        TokenPayload: Token data
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except jwt.DecodeError as e:
        raise TokenError(msg="Token decode error") from e
    except jwt.ExpiredSignatureError as e:
        raise TokenError(msg="Token Expired") from e
    except (InvalidTokenError, Exception) as e:
        raise TokenError(msg="Could not validate credentials") from e

    return token_data


async def update_refresh_token(
    sub: str,
    token: str,
    refresh_token: str,
    **kwargs,  # pylint: disable=unused-argument
) -> tuple[str, str, datetime, datetime]:
    """Update refresh and current token timedelta.

    Args:
        sub (str): User id / Token data
        token (str): Current token
        refresh_token (str): Refresh token
        **kwargs: Dynamic params

    Returns:
        tuple[str, str, datetime, datetime]: token data
    """
    new_access_token, new_access_token_expire_time = create_access_token(
        sub, **kwargs
    )
    new_refresh_token, new_refresh_token_expire_time = create_refresh_token(
        sub, **kwargs
    )
    return (
        new_access_token,
        new_refresh_token,
        new_access_token_expire_time,
        new_refresh_token_expire_time,
    )
