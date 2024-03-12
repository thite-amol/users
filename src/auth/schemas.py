from typing import Optional

from pydantic import BaseModel, field_validator

from src.auth.security import get_password_hash, is_password_hashed
from src.users.schemas import UserBase


class UserUpdatePassword(UserBase):
    password: str

    @field_validator("password")
    def hash_password(cls, pw: str) -> str:
        if is_password_hashed(pw):
            return pw
        return get_password_hash(pw)


class NewPassword(BaseModel):
    token: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
