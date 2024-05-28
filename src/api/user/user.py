"""Module."""

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
    """_summary_.

    Args:
        obj (UserCreateOpen): _description_
        session (CurrentSession): _description_

    Returns:
        ResponseModel: _description_
    """
    user_data = await user_service.register(user_data=obj, db=session)
    return await response_base.success(data=user_data)
