"""Module."""

from typing import Optional

from pydantic import BaseModel, field_validator

from src.auth.security import get_password_hash, is_password_hashed
from src.users.schemas import UserBase


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


class NewPassword(BaseModel):
    """_summary_.

    Args:
        BaseModel (_type_): _description_
    """

    token: str
    new_password: str


class Token(BaseModel):
    """_summary_.

    Args:
        BaseModel (_type_): _description_
    """

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """_summary_.

    Args:
        BaseModel (_type_): _description_
    """

    sub: Optional[int] = None
