"""Module."""

import starlette.status as http_status
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pydantic.errors import PydanticUserError
from starlette.exceptions import HTTPException
from uvicorn.protocols.http.h11_impl import STATUS_PHRASES

from src.common.exception.errors import BaseExceptionMixin
from src.common.response.response_code import CustomResponseCode
from src.common.response.response_schema import response_base
from src.config import settings
from src.utils.serializers import MsgSpecJSONResponse


async def _get_exception_code(status_code: int):
    """_summary_.

    Args:
        status_code (int): _description_

    Returns:
        _type_: _description_
    """
    try:
        STATUS_PHRASES[status_code]
    except Exception:  # pylint: disable=broad-exception-caught
        code = http_status.HTTP_400_BAD_REQUEST
    else:
        code = status_code
    return code


async def _validation_exception_handler(
    request: Request, e: RequestValidationError | ValidationError
):
    """_summary_.

    Args:
        request (Request): _description_
        e (RequestValidationError | ValidationError): _description_

    Returns:
        _type_: _description_
    """
    msg = "Invalid request data. Please provide correct inputs."
    data = {"errors": e.errors()}
    content = {
        "code": http_status.HTTP_422_UNPROCESSABLE_ENTITY,
        "msg": msg,
        "data": data,
    }
    request.state.__request_validation_exception__ = (
        content  # used To Obtain Exception Information In Middleware
    )
    return MsgSpecJSONResponse(
        status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY, content=content
    )


def register_exception(app: FastAPI):
    """_summary_.

    Args:
        app (FastAPI): _description_

    Returns:
        _type_: _description_
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """_summary_.

        Args:
            request (Request): _description_
            exc (HTTPException): _description_

        Returns:
            _type_: _description_
        """
        if settings.base.ENVIRONMENT == "dev":
            content = {
                "code": exc.status_code,
                "msg": exc.detail,
                "data": None,
            }
        else:
            res = await response_base.fail(res=CustomResponseCode.HTTP_400)
            content = res.model_dump()
        request.state.__request_http_exception__ = (
            content  # Used to obtain exception information in middleware
        )
        return MsgSpecJSONResponse(
            status_code=await _get_exception_code(exc.status_code),
            content=content,
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def fastapi_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """_summary_.

        Args:
            request (Request): _description_
            exc (RequestValidationError): _description_

        Returns:
            _type_: _description_
        """
        return await _validation_exception_handler(request, exc)

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(
        request: Request, exc: ValidationError
    ):
        """_summary_.

        Args:
            request (Request): _description_
            exc (ValidationError): _description_

        Returns:
            _type_: _description_
        """
        return await _validation_exception_handler(request, exc)

    @app.exception_handler(PydanticUserError)
    async def pydantic_user_error_handler(
        request: Request,  # pylint: disable=unused-argument
        exc: PydanticUserError,
    ):
        """_summary_.

        Args:
            request (Request): _description_
            exc (PydanticUserError): _description_

        Returns:
            _type_: _description_
        """
        return MsgSpecJSONResponse(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                "msg": exc.message,
                "data": None,
            },
        )

    @app.exception_handler(AssertionError)
    async def assertion_error_handler(request: Request, exc: AssertionError):  # pylint: disable=unused-argument
        """_summary_.

        Args:
            request (Request): _description_
            exc (AssertionError): _description_

        Returns:
            _type_: _description_
        """
        if settings.base.ENVIRONMENT == "dev":
            content = {
                "code": http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                "msg": str("".join(exc.args) if exc.args else exc.__doc__),
                "data": None,
            }
        else:
            res = await response_base.fail(res=CustomResponseCode.HTTP_500)
            content = res.model_dump()
        return MsgSpecJSONResponse(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=content,
        )

    @app.exception_handler(BaseExceptionMixin)
    async def base_exception_error_handler(
        request: Request, exc: BaseExceptionMixin
    ):  # pylint: disable=unused-argument
        """Handles Exception raised by base exception.

        Args:
            request (Request): Current connection properties
            exc (BaseExceptionMixin): Current Exception

        Returns:
            MsgSpecJSONResponse: JSON Response
        """
        content = {
            "code": exc.code,
            "msg": exc.msg,
            "data": exc.data,
        }

        return MsgSpecJSONResponse(
            status_code=exc.code,
            content=content,
        )

    # @app.exception_handler(Exception)
    # async def all_exception_handler(request: Request, exc: Exception):  # pylint: disable=unused-argument
    #     """_summary_.
    #
    #     Args:
    #         request (Request): _description_
    #         exc (Exception): _description_
    #
    #     Returns:
    #         _type_: _description_
    #     """
    #     if isinstance(exc, BaseExceptionMixin):
    #         return MsgSpecJSONResponse(
    #             status_code=await _get_exception_code(exc.code),
    #             content={
    #                 "code": exc.code,
    #                 "msg": str(exc.msg),
    #                 "data": exc.data if exc.data else None,
    #             },
    #             background=exc.background,
    #         )
    #     else:
    #         log.error(f"Unknown exception: {exc}")
    #         log.error(traceback.format_exc())
    #         if settings.base.ENVIRONMENT == "dev":
    #             content = {
    #                 "code": http_status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                 "msg": str(exc),
    #                 "data": None,
    #             }
    #         else:
    #             res = await response_base.fail(res=CustomResponseCode.HTTP_500)
    #             content = res.model_dump()
    #         return MsgSpecJSONResponse(
    #             status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             content=content,
    #         )
    #
    # if settings.base.BACKEND_CORS_ORIGINS:
    #
    #     @app.exception_handler(http_status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     async def cors_status_code_500_exception_handler(request, exc):
    #         """_summary_.
    #
    #         Args:
    #             request (_type_): _description_
    #             exc (_type_): _description_
    #
    #         Returns:
    #             _type_: _description_
    #         """
    #         if isinstance(exc, BaseExceptionMixin):
    #             content = {
    #                 "code": exc.code,
    #                 "msg": exc.msg,
    #                 "data": exc.data,
    #             }
    #         else:
    #             if settings.base.ENVIRONMENT == "dev":
    #                 content = {
    #                     "code": http_status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                     "msg": str(exc),
    #                     "data": None,
    #                 }
    #             else:
    #                 res = await response_base.fail(
    #                     res=CustomResponseCode.HTTP_500
    #                 )
    #                 content = res.model_dump()
    #         response = MsgSpecJSONResponse(
    #             status_code=exc.code
    #             if isinstance(exc, BaseExceptionMixin)
    #             else http_status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             content=content,
    #             background=exc.background
    #             if isinstance(exc, BaseExceptionMixin)
    #             else None,
    #         )
    #         origin = request.headers.get("origin")
    #         if origin:
    #             cors = CORSMiddleware(
    #                 app=app,
    #                 allow_origins=["*"],
    #                 allow_credentials=True,
    #                 allow_methods=["*"],
    #                 allow_headers=["*"],
    #             )
    #             response.headers.update(cors.simple_headers)
    #             has_cookie = "cookie" in request.headers
    #             if cors.allow_all_origins and has_cookie:
    #                 response.headers["Access-Control-Allow-Origin"] = origin
    #             elif not cors.allow_all_origins and cors.is_allowed_origin(
    #                     origin=origin
    #             ):
    #                 response.headers["Access-Control-Allow-Origin"] = origin
    #                 response.headers.add_vary_header("Origin")
    #         return response
