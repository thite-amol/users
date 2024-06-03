"""Dependencies for API."""
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.security import decode_token
from src.common.exception.errors import HTTPError
from src.db.session import CurrentSession
from src.users.model import User

security = HTTPBearer()


async def get_current_user(
    session: CurrentSession,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> User:
    """Check current user credentials.

    Args:
        session (CurrentSession): Current db session
        credentials (Annotated[HTTPAuthorizationCredentials, Depends): Get the Bearer token

    Raises:
        HTTPException: _description_

    Returns:
        User: Current user details
    """
    token_data = decode_token(credentials.credentials)
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPError(code=404, msg="User not found")
    if not user.is_active:
        raise HTTPError(code=400, msg="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
