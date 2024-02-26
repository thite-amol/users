from collections.abc import Mapping
from typing import Any, Generic

from pydantic import Field, conlist, BaseModel

from src.models.base import PublicModel, _PublicModel

__all__ = (
    "ResponseMulti",
    "Response",
    "_Response",
    "ErrorResponse",
    "ErrorResponseMulti",
)


class ResponseMulti(PublicModel, BaseModel, Generic[_PublicModel]):
    """Generic response model that consist multiple results."""

    result: list[_PublicModel]


class Response(PublicModel, BaseModel, Generic[_PublicModel]):
    """Generic response model that consist only one result."""

    result: _PublicModel


_Response = Mapping[int | str, dict[str, Any]]


class ErrorResponse(PublicModel):
    """Error response model."""

    message: str = Field(description="This field represent the message")
    path: list = Field(
        description="The path to the field that raised the error",
        default_factory=list,
    )


class ErrorResponseMulti(PublicModel):
    """The public error respnse model that includes multiple objects."""

    results: conlist(ErrorResponse, min_length=1)  # type: ignore
