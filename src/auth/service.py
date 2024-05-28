"""Module."""

from src.auth.security import verify_password
from src.users.model import User
from src.users.repository import UsersCRUD


async def authenticate(*, email: str, password: str) -> User | None:
    """_summary_.

    Args:
        email (str): _description_
        password (str): _description_

    Returns:
        User | None: _description_
    """
    user_data = await UsersCRUD.get_user_by_email(email=email)
    if not user_data:
        return None
    if not verify_password(password, user_data.password):
        return None
    return user_data
