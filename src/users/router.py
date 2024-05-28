"""Module."""
# from typing import Any, Optional

# from fastapi import APIRouter, Depends, HTTPException

# from src.auth.dependencies import CurrentUser, get_current_active_superuser
# from src.config import settings
# from src.models.response import Message
# from src.users.dependencies import get_pagination_params
# from src.users.repository import UsersCRUD
# from src.users.schemas import (
#     UserCreate,
#     UserCreateOpen,
#     UserOut,
#     UsersPublic,
#     UserUpdate,
# )

# user_router = APIRouter(prefix="/user", tags=["user"])


# @user_router.post("/register", response_model=UserOut)
# @transaction
# async def open_user_registration(user_in: UserCreateOpen) -> Any:
#     """Create new user without the need to be logged in."""
#     if not settings.USERS_OPEN_REGISTRATION:
#         raise HTTPException(
#             status_code=403,
#             detail="Open user registration is forbidden on this server",
#         )
#     user = await UsersCRUD.get_user_by_email(email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system",
#         )
#     user_create = UserCreate.model_validate(user_in)
#     user = await UsersCRUD.create(schema=user_create)
#     return user


# @user_router.get("/users", response_model=UsersPublic)
# async def get_all_users(
#     pagination: dict = Depends(get_pagination_params),
# ) -> Any:
#     """Get a specific user by id."""
#     users, count = await UsersCRUD.paginate(**pagination)
#     converted = UsersPublic(data=users, count=count)

#     return converted


# @user_router.get("/", response_model=UserOut)
# @user_router.get("/{user_id}", response_model=UserOut)
# async def read_user_details(
#     current_user: CurrentUser, user_id: Optional[int] = None
# ) -> Any:
#     """Get a user details."""
#     if not user_id:
#         return current_user
#     user = await UsersCRUD.get(user_id)
#     if user == current_user:
#         return user

#     if not current_user.is_superuser:
#         raise HTTPException(
#             # TODO: Review status code
#             status_code=400,
#             detail="The user doesn't have enough privileges",
#         )
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="User details are missing.",
#         )

#     return user


# @user_router.put("/{user_id}", response_model=UserOut)
# async def update_user(
#     current_user: CurrentUser,
#     user_id: int,
#     user_in: UserUpdate,
# ) -> Any:
#     """Update a user."""
#     user = UsersCRUD.get(user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system",
#         )

#     if not current_user.is_superuser:
#         if user != current_user:
#             raise HTTPException(
#                 status_code=400, detail="Not enough permissions"
#             )

#     user_in = UserUpdate.model_validate(user_in)

#     user = UsersCRUD.update(obj_in=user_in)
#     return user


# @user_router.post(
#     "/",
#     response_model=UserOut,
#     dependencies=[Depends(get_current_active_superuser)],
# )
# async def create_user(
#     user_in: UserCreate,
# ) -> Any:
#     """Create a user."""
#     user = await UsersCRUD.get_user_by_email(email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system",
#         )
#     user_create = UserCreate.model_validate(user_in)
#     user = await UsersCRUD.create(schema=user_create)
#     return user


# @user_router.delete("/{user_id}")
# async def delete_user(current_user: CurrentUser, user_id: int) -> Message:
#     """Delete a user."""
#     user = await UsersCRUD.get(id_=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if not current_user.is_superuser:
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     if user == current_user:
#         raise HTTPException(
#             status_code=400, detail="Users are not allowed to delete themselves"
#         )

#     await UsersCRUD.delete(id_=user_id)
#     return Message(message="User deleted successfully")
