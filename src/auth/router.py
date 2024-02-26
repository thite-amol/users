from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import CurrentUser
from src.auth.schemas import UserInDBBase, Message, NewPassword, Token, UserUpdatePassword
from src.auth.security import create_access_token
from src.auth.service import authenticate
from src.auth.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from src.config import settings
from src.users.repository import UsersCRUD

login_router = APIRouter()


@login_router.post("/login/access-token")
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@login_router.post("/login/test-token", response_model=UserInDBBase)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@login_router.post("/password-recovery/{email}")
async def recover_password(email: str) -> Message:
    """
    Password Recovery
    """
    user = await UsersCRUD.get_user_by_email(email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return Message(message="Password recovery email sent")


@login_router.post("/reset-password/")
async def reset_password(body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    print(email)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await UsersCRUD.get_user_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    user.password = body.new_password
    user_update = UserUpdatePassword.model_validate(user)
    await UsersCRUD.update(user_update)
    return Message(message="Password updated successfully")
