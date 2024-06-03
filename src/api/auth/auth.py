"""Module to register users routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import HTTPBasicCredentials
from fastapi.security.utils import get_authorization_scheme_param

from src.api.deps import CurrentUser, get_current_user
from src.auth.service import login, new_token
from src.common.response.response_schema import ResponseModel, response_base
from src.db.session import CurrentSession

router = APIRouter()


@router.post(
    "/login",
    summary="User login",
    description="Generate reusable access token.",
)
async def user_login(
    form_data: Annotated[HTTPBasicCredentials, Depends()],
    session: CurrentSession,
) -> ResponseModel:
    """User authentication.

    Args:
        form_data (AuthSchemaBase): User login data
        session (CurrentSession): database session

    Returns:
        ResponseModel: User token data if succeed
    """
    data = await login(db=session, form_data=form_data)
    return await response_base.success(data=data)


@router.post("/login/test-token", response_model=ResponseModel)
async def test_token(current_user: CurrentUser) -> ResponseModel:
    """Test access token.

    Args:
        current_user (CurrentUser): Current logged in user

    Returns:
        ResponseModel: Current user data
    """
    return await response_base.success(data=current_user)


@router.post(
    "/token/new",
    summary="create new token",
    dependencies=[Depends(get_current_user)],
)
async def create_new_token(
    request: Request,
    session: CurrentSession,
    refresh_token: Annotated[str, Query(...)],
) -> ResponseModel:
    """_summary_.

    Args:
        request (Request): Current app request
        session (CurrentSession): db session
        refresh_token (Annotated[str, Query): refresh token

    Returns:
        ResponseModel: Token data
    """
    authorization = request.headers.get("Authorization")
    _, token = get_authorization_scheme_param(authorization)
    data = await new_token(
        request=request,
        db=session,
        refresh_token=refresh_token,
        current_token=token,
    )
    return await response_base.success(data=data)
