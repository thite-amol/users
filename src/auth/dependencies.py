"""Module."""

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import TokenPayload
from src.config import settings
from src.db.session import CTX_SESSION
from src.users.model import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_session():
    """_summary_.

    Returns:
        _type_: _description_
    """
    return CTX_SESSION.get()


SessionDep = Annotated[AsyncSession, Depends(get_current_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """_summary_.

    Args:
        session (SessionDep): _description_
        token (TokenDep): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        User: _description_
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    """_summary_.

    Args:
        current_user (CurrentUser): _description_

    Raises:
        HTTPException: _description_

    Returns:
        User: _description_
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


SuperUser = Annotated[User, Depends(get_current_active_superuser)]
