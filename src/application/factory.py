"""Module."""

import asyncio
import os
from functools import partial
from typing import Callable, Coroutine, Iterable

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
    startup_tasks: Iterable[Callable[[], Coroutine]] | None = None,
    shutdown_tasks: Iterable[Callable[[], Coroutine]] | None = None,
    **kwargs,
) -> FastAPI:
    """The application factory using FastAPI framework.
    🎉 Only passing routes is mandatory to start.

    Args:
        startup_tasks (Iterable[Callable[[], Coroutine]] | None, optional): _description_. Defaults to None.
        shutdown_tasks (Iterable[Callable[[], Coroutine]] | None, optional): _description_. Defaults to None.
        **kwargs: Dynamic arguments.

    Returns:
        FastAPI: _description_
    """
    # Initialize the base FastAPI application
    app = FastAPI(**kwargs)

    register_static_file(app)
    register_middleware(app)
    register_router(app)
    register_page(app)

    register_exception(app)

    # Define startup tasks that are running asynchronous using FastAPI hook
    if startup_tasks:
        for task in startup_tasks:
            coro = partial(asyncio.create_task, task())
            app.on_event("startup")(coro)

    # Define shutdown tasks using FastAPI hook
    if shutdown_tasks:
        for task in shutdown_tasks:
            app.on_event("shutdown")(task)

    return app


def register_static_file(app: FastAPI):
    """Static file interactive development mode, production uses nginx static resource service.

    Args:
        app (FastAPI): _description_
    """
    if settings.STATIC_FILES:
        if not os.path.exists(STATIC_DIR):
            os.mkdir(STATIC_DIR)
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def register_middleware(app: FastAPI):
    """Middleware, execution order from bottom to top.

    Args:
        app (FastAPI): _description_
    """
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/")
                for origin in settings.BACKEND_CORS_ORIGINS
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
