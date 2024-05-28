"""Module."""

from datetime import datetime, timedelta
from typing import Any, Optional, Union

import jwt
from passlib.context import CryptContext

from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """_summary_.

    Args:
        subject (Union[str, Any]): _description_
        expires_delta (Optional[timedelta], optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


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
