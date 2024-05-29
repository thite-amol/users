"""Module."""

from datetime import datetime

from pydantic import field_validator

from src.auth.security import get_password_hash, is_password_hashed
from src.common.schema import SchemaBase
from src.users.schemas import GetUserInfoNoRelationDetail, UserBase


class UserUpdatePassword(UserBase):
    """_summary_.

    Args:
        UserBase (_type_): _description_

    Returns:
        _type_: _description_
    """

    password: str

    @field_validator("password")
    def hash_password(cls, pw: str) -> str:
        """_summary_.

        Args:
            pw (str): _description_

        Returns:
            str: _description_
        """
        if is_password_hashed(pw):
            return pw
        return get_password_hash(pw)


class AuthSchemaBase(SchemaBase):
    """_summary_.

    Args:
        SchemaBase (_type_): _description_
    """

    username: str
    password: str | None


class AccessTokenBase(SchemaBase):
    """JWT token base class."""

    access_token: str
    token_type: str = "Bearer"
    access_token_expire_time: datetime


class GetLoginToken(AccessTokenBase):
    """Login JWT token class."""

    refresh_token: str
    refresh_token_type: str = "Bearer"
    refresh_token_expire_time: datetime
    user: GetUserInfoNoRelationDetail


class GetNewToken(AccessTokenBase):
    """New JWT token class."""

    refresh_token: str
    refresh_token_type: str = "Bearer"
    refresh_token_expire_time: datetime
