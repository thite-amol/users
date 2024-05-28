"""Module."""

from fastapi import APIRouter

from src.api.user.user import router as user_router
from src.config import settings

v1 = APIRouter(prefix=settings.API_V1_STR)

v1.include_router(user_router)
