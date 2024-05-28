"""User Schema."""

from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, field_validator

from src.auth.security import get_password_hash, is_password_hashed
from src.common.schema import SchemaBase
from src.role.schemas import GetRoleListDetails


# Shared properties
class UserBase(SchemaBase):
    """_summary_.

    Args:
        SchemaBase (_type_): _description_
    """

    id: Optional[int] = None
    email: Optional[EmailStr] = None
    username: str = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_superuser: bool = False
    avatar: Optional[str] = None
    phone: Optional[str] = None
    join_time: datetime = None
    last_login_time: datetime | None = None
    is_active: Optional[bool] = True
    roles: list[GetRoleListDetails]


# Properties to receive via API on creation
class UserCreate(SchemaBase):
    """_summary_.

    Args:
        SchemaBase (_type_): _description_

    Returns:
        _type_: _description_
    """

    email: EmailStr
    username: str = None
    password: str
    first_name: str = None
    last_name: str = None

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


class UserCreateOpen(UserCreate):
    """_summary_.

    Args:
        UserCreate (_type_): _description_
    """

    pass


class AuthSchemaBase(SchemaBase):
    """_summary_.

    Args:
        SchemaBase (_type_): _description_
    """

    username: str
    password: str | None


class AddUserParam(AuthSchemaBase):
    """_summary_.

    Args:
        AuthSchemaBase (_type_): _description_
    """

    roles: list[int]
    email: EmailStr = Field(..., example="user@example.com")


# Properties to receive via API on update
class UserUpdate(UserBase):
    """_summary_.

    Args:
        UserBase (_type_): _description_

    Returns:
        _type_: _description_
    """

    password: Optional[str] = None

    @field_validator("password")
    def hash_password(cls, pw: str) -> str:
        """_summary_.

        Args:
            pw (str): _description_

        Returns:
            str: _description_
        """
        if not pw:
            return pw

        if is_password_hashed(pw):
            return pw
        return get_password_hash(pw)


class UserOut(UserBase):
    """_summary_.

    Args:
        UserBase (_type_): _description_
    """

    id: int


class UserInDBBase(UserBase):
    """_summary_.

    Args:
        UserBase (_type_): _description_
    """

    id: Optional[int] = None


# Additional properties to return via API
class User(UserInDBBase):
    """_summary_.

    Args:
        UserInDBBase (_type_): _description_
    """

    pass


class UsersPublic(SchemaBase):
    """_summary_.

    Args:
        SchemaBase (_type_): _description_
    """

    data: list[UserOut]
    count: int
