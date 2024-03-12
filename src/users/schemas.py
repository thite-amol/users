from typing import Optional

from pydantic import EmailStr, field_validator

from src.auth.security import get_password_hash, is_password_hashed
from src.models import InternalModel


# Shared properties
class UserBase(InternalModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

    @field_validator("password")
    def hash_password(cls, pw: str) -> str:
        if is_password_hashed(pw):
            return pw
        return get_password_hash(pw)


class UserCreateOpen(UserCreate):
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

    @field_validator("password")
    def hash_password(cls, pw: str) -> str:
        if not pw:
            return pw

        if is_password_hashed(pw):
            return pw
        return get_password_hash(pw)


class UserOut(UserBase):
    id: int


class UserInDBBase(UserBase):
    id: Optional[int] = None


# Additional properties to return via API
class User(UserInDBBase):
    pass
