"""Module to register users routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.api.deps import get_current_user
from src.common.pagination import DependsPagination, paging_data
from src.common.response.response_schema import ResponseModel, response_base
from src.db.session import CurrentSession
from src.users.schemas import GetUserInfoListDetails, UserCreateOpen
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


@router.get(
    "/users",
    summary="(Fuzzy condition) Get all users in paging",
    dependencies=[Depends(get_current_user), DependsPagination],
)
async def get_pagination_users(
    db: CurrentSession,
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    """Get all users.

    Args:
        db (CurrentSession): Current db session
        username (Annotated[str  |  None, Query, optional): Username if search by it. Defaults to None.
        phone (Annotated[str  |  None, Query, optional): phone if search by it. Defaults to None.
        status (Annotated[int  |  None, Query, optional): status if search by it. Defaults to None.

    Returns:
        ResponseModel: List of users
    """
    user_select = await user_service.get_select(
        username=username, phone=phone, status=status
    )
    page_data = await paging_data(db, user_select, GetUserInfoListDetails)
    return await response_base.success(data=page_data)
