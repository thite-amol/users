"""Dependencies for API."""
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.auth.security import decode_token
from src.common.exception.errors import HTTPError
from src.config.base import settings
from src.db.session import CurrentSession
from src.users.model import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(
    session: CurrentSession,
    token: TokenDep,
) -> User:
    """Check current user credentials.

    Args:
        session (CurrentSession): Current db session
        token (str): Get the Bearer token

    Raises:
        HTTPException: _description_

    Returns:
        User: Current user details
    """
    token_data = decode_token(token)
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPError(code=404, msg="User not found")
    if not user.is_active:
        raise HTTPError(code=400, msg="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
