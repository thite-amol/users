"""Global business exception class."""

from typing import Any, Optional

import starlette.status as http_status
from fastapi import HTTPException
from starlette.background import BackgroundTask

from src.common.response.response_code import CustomCodeBase


class BaseExceptionMixin(Exception):
    """_summary_.

    Args:
        Exception (_type_): _description_
    """

    code: int

    def __init__(
        self,
        *,
        msg: Optional[str] = None,
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        """_summary_.

        Args:
            msg (Optional[str], optional): _description_. Defaults to None.
            data (Any, optional): _description_. Defaults to None.
            background (BackgroundTask | None, optional): _description_. Defaults to None.
        """
        self.msg = msg
        self.data = data
        # The original background task: https://www.starlette.io/background/
        self.background = background


class HTTPError(HTTPException):
    """_summary_.

    Args:
        HTTPException (_type_): _description_
    """

    def __init__(
        self,
        *,
        code: int,
        msg: Any = None,
        headers: dict[str, Any] | None = None,
    ):
        """_summary_.

        Args:
            code (int): _description_
            msg (Any, optional): _description_. Defaults to None.
            headers (dict[str, Any] | None, optional): _description_. Defaults to None.
        """
        super().__init__(status_code=code, detail=msg, headers=headers)


class CustomError(BaseExceptionMixin):
    """_summary_.

    Args:
        BaseExceptionMixin (_type_): _description_
    """

    def __init__(
        self,
        *,
        error: CustomCodeBase,
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        """_summary_.

        Args:
            error (CustomCodeBase): _description_
            data (Any, optional): _description_. Defaults to None.
            background (BackgroundTask | None, optional): _description_. Defaults to None.
        """
        self.code = error.code
        super().__init__(msg=error.msg, data=data, background=background)


class RequestError(BaseExceptionMixin):
    """_summary_.

    Args:
        BaseExceptionMixin (_type_): _description_
    """

    code = http_status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        *,
        msg: str = "Bad Request",
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        """_summary_.

        Args:
            msg (str, optional): _description_. Defaults to "Bad Request".
            data (Any, optional): _description_. Defaults to None.
            background (BackgroundTask | None, optional): _description_. Defaults to None.
        """
        super().__init__(msg=msg, data=data, background=background)


class ForbiddenError(BaseExceptionMixin):
    """_summary_.

    Args:
        BaseExceptionMixin (_type_): _description_
    """

    code = http_status.HTTP_403_FORBIDDEN

    def __init__(
        self,
        *,
        msg: str = "Forbidden",
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        """_summary_.

        Args:
            msg (str, optional): _description_. Defaults to "Forbidden".
            data (Any, optional): _description_. Defaults to None.
            background (BackgroundTask | None, optional): _description_. Defaults to None.
        """
        super().__init__(msg=msg, data=data, background=background)


class NotFoundError(BaseExceptionMixin):
    """_summary_.

    Args:
        BaseExceptionMixin (_type_): _description_
    """

    code = http_status.HTTP_404_NOT_FOUND

    def __init__(
        self,
        *,
        msg: str = "Not Found",
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        """_summary_.

        Args:
            msg (str, optional): _description_. Defaults to "Not Found".
            data (Any, optional): _description_. Defaults to None.
            background (BackgroundTask | None, optional): _description_. Defaults to None.
        """
        super().__init__(msg=msg, data=data, background=background)


class ServerError(BaseExceptionMixin):
    """_summary_.

    Args:
        BaseExceptionMixin (_type_): _description_
    """

    code = http_status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        *,
        msg: str = "Internal Server Error",
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        """_summary_.

        Args:
            msg (str, optional): _description_. Defaults to "Internal Server Error".
            data (Any, optional): _description_. Defaults to None.
            background (BackgroundTask | None, optional): _description_. Defaults to None.
        """
        super().__init__(msg=msg, data=data, background=background)


class GatewayError(BaseExceptionMixin):
    """_summary_.

    Args:
        BaseExceptionMixin (_type_): _description_
    """

    code = http_status.HTTP_502_BAD_GATEWAY

    def __init__(
        self,
        *,
        msg: str = "Bad Gateway",
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        """_summary_.

        Args:
            msg (str, optional): _description_. Defaults to "Bad Gateway".
            data (Any, optional): _description_. Defaults to None.
            background (BackgroundTask | None, optional): _description_. Defaults to None.
        """
        super().__init__(msg=msg, data=data, background=background)


class AuthorizationError(BaseExceptionMixin):
    """_summary_.

    Args:
        BaseExceptionMixin (_type_): _description_
    """

    code = http_status.HTTP_401_UNAUTHORIZED

    def __init__(
        self,
        *,
        msg: str = "Permission Denied",
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        """_summary_.

        Args:
            msg (str, optional): _description_. Defaults to "Permission Denied".
            data (Any, optional): _description_. Defaults to None.
            background (BackgroundTask | None, optional): _description_. Defaults to None.
        """
        super().__init__(msg=msg, data=data, background=background)


class TokenError(HTTPError):
    """_summary_.

    Args:
        HTTPError (_type_): _description_
    """

    code = http_status.HTTP_401_UNAUTHORIZED

    def __init__(
        self,
        *,
        msg: str = "Not Authenticated",
        headers: dict[str, Any] | None = None,
    ):
        """_summary_.

        Args:
            msg (str, optional): _description_. Defaults to "Not Authenticated".
            headers (dict[str, Any] | None, optional): _description_. Defaults to None.
        """
        super().__init__(
            code=self.code,
            msg=msg,
            headers=headers or {"WWW-Authenticate": "Bearer"},
        )
