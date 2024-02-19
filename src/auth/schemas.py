from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from src.auth.security import is_password_hashed, get_password_hash


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

    # first_name: str
    # last_name: str
    @field_validator('password')
    def hash_password(cls, pw: str) -> str:
        if is_password_hashed(pw):
            return pw
        return get_password_hash(pw)


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class NewPassword(BaseModel):
    token: str
    new_password: str


class UserOut(UserBase):
    id: int


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class Msg(BaseModel):
    msg: str


class Message(BaseModel):
    message: str
