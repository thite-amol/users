"""Auth security operation module."""

from datetime import datetime, timedelta
from typing import Any, Optional, Union

import jwt
from passlib.context import CryptContext

from src.common.exception.errors import TokenError
from src.config import settings
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


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """_summary_.

    Args:
        plain_password (str): _description_
        hashed_password (str): _description_

    Returns:
        bool: _description_
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """_summary_.

    Args:
        password (str): _description_

    Returns:
        str: _description_
    """
    return pwd_context.hash(password)


def is_password_hashed(password: str) -> bool:
    """_summary_.

    Args:
        password (str): _description_

    Returns:
        bool: _description_
    """
    return bool(pwd_context.identify(password))
