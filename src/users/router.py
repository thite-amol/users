from typing import Any

from fastapi import APIRouter, HTTPException

from src.auth.dependencies import CurrentUser
from src.config import settings
from src.db.transaction import transaction
from src.users.repository import UsersRepository
from src.users.schemas import UserCreate, UserCreateOpen, UserOut


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/open", response_model=UserOut)
@transaction
async def create_user_open(user_in: UserCreateOpen) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    obj = UsersRepository()
    user = await obj.get_user_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = await obj.create(schema=user_create)
    return user


@user_router.get("/{user_id}", response_model=UserOut)
async def read_user_by_id(
        user_id: int, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    user = await UsersRepository().get(user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            # TODO: Review status code
            status_code=400,
            detail="The user doesn't have enough privileges",
        )
    return user

# @router.put(
#     "/{user_id}",
#     dependencies=[Depends(get_current_active_superuser)],
#     response_model=UserOut,
# )
# def update_user(
#     *,
#     session: SessionDep,
#     user_id: int,
#     user_in: UserUpdate,
# ) -> Any:
#     """
#     Update a user.
#     """
#
#     # TODO: Refactor when SQLModel has update
#     # user = session.get(User, user_id)
#     # if not user:
#     #     raise HTTPException(
#     #         status_code=404,
#     #         detail="The user with this username does not exist in the system",
#     #     )
#     # user = crud.user.update(session, db_obj=user, obj_in=user_in)
#     # return user
#
#
# @router.delete("/{user_id}")
# def delete_user(
#     session: SessionDep, current_user: CurrentUser, user_id: int
# ) -> Message:
#     """
#     Delete a user.
#     """
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if not current_user.is_superuser:
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     if user == current_user:
#         raise HTTPException(
#             status_code=400, detail="Users are not allowed to delete themselves"
#         )
#     session.delete(user)
#     session.commit()
#     return Message(message="User deleted successfully")
