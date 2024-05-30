"""Module to register users routes."""

from fastapi import APIRouter

from src.auth.schemas import AuthSchemaBase
from src.auth.service import login
from src.common.response.response_schema import ResponseModel, response_base
from src.db.session import CurrentSession

router = APIRouter()


@router.post(
    "/login",
    summary="User login",
    description="Generate reusable access token.",
)
async def user_login(
    obj: AuthSchemaBase, session: CurrentSession
) -> ResponseModel:
    """User authentication.

    Args:
        obj (AuthSchemaBase): User login data
        session (CurrentSession): database session

    Returns:
        ResponseModel: User token data if succeed
    """
    data = await login(db=session, obj=obj)
    return await response_base.success(data=data)


# @router.post('/token/new', summary='create new token', dependencies=[DependsJwtAuth])
# async def create_new_token(request: Request, refresh_token: Annotated[str, Query(...)]) -> ResponseModel:
#     data = await new_token(request=request, refresh_token=refresh_token)
#     return await response_base.success(data=data)
#
#
# @router.post('/logout', summary='User logout', dependencies=[DependsJwtAuth])
# async def user_logout(request: Request) -> ResponseModel:
#     await logout(request=request)
#     return await response_base.success()
