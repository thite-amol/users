"""Router module."""

from fastapi import APIRouter

from src.api.auth.auth import router as auth_router
from src.api.user.user import router as user_router
from src.config import settings

v1 = APIRouter(prefix=settings.base.API_V1_STR)

v1.include_router(user_router)
v1.include_router(auth_router)
