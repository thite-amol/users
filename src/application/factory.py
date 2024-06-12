"""Module."""

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from src.api.router import v1 as route
from src.common.exception.exception_handler import register_exception
from src.config import settings
from src.config.path_conf import STATIC_DIR

# from src.utils.openapi import simplify_operation_ids

__all__ = ("create",)


def create(
    *_,
    **kwargs,
) -> FastAPI:
    """The application factory using FastAPI framework.
    🎉 Only passing routes is mandatory to start.

    Args:
        **kwargs: Dynamic arguments.

    Returns:
        FastAPI: FastAPI application.
    """
    # Initialize the base FastAPI application
    app = FastAPI(**kwargs)

    register_static_file(app)
    register_middleware(app)
    register_router(app)
    register_page(app)

    register_exception(app)

    return app


def register_static_file(app: FastAPI):
    """Static file interactive development mode, production uses nginx static resource service.

    Args:
        app (FastAPI): _description_
    """
    if settings.base.STATIC_FILES:
        if not os.path.exists(STATIC_DIR):
            os.mkdir(STATIC_DIR)
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def register_middleware(app: FastAPI):
    """Middleware, execution order from bottom to top.

    Args:
        app (FastAPI): _description_
    """
    if settings.base.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/")
                for origin in settings.base.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def register_router(app: FastAPI):
    """Routing.

    Args:
        app (FastAPI): _description_
    """
    # API
    app.include_router(route)

    # Extra
    # simplify_operation_ids(app)


def register_page(app: FastAPI):
    """Paging query.

    Args:
        app (FastAPI): _description_
    """
    add_pagination(app)
