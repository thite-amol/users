"""Module to register users routes."""

from fastapi import APIRouter

from src.common.response.response_schema import ResponseModel, response_base
from src.db.session import CurrentSession
from src.users.schemas import UserCreateOpen
from src.users.service import user_service

router = APIRouter()


@router.post("/register", summary="Register user")
async def register_user(
    obj: UserCreateOpen, session: CurrentSession
) -> ResponseModel:
    """Register users without superuser.

    Args:
        obj (UserCreateOpen): User fields
        session (CurrentSession): db session

    Returns:
        ResponseModel: User details if succeed
    """
    user_data = await user_service.register(user_data=obj, db=session)
    return await response_base.success(data=user_data)
