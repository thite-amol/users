"""Module."""

import dataclasses
from enum import Enum


class CustomCodeBase(Enum):
    """Custom code class."""

    @property
    def code(self):
        """Get status code."""
        return self.value[0]

    @property
    def msg(self):
        """Response message."""
        return self.value[1]


class CustomResponseCode(CustomCodeBase):
    """Custom Response Status Code."""

    HTTP_200 = (200, "request success")
    HTTP_201 = (201, "new request successful ")
    HTTP_202 = (
        202,
        "The request has been accepted, but the processing has not been completed",
    )
    HTTP_204 = (
        204,
        "The request was successful, but the content was not returned",
    )
    HTTP_400 = (400, "request error")
    HTTP_401 = (401, "Unauthorized")
    HTTP_403 = (403, "Forbidden access")
    HTTP_404 = (404, "The resource of request does not exist")
    HTTP_410 = (410, "The request resources have been permanently deleted")
    HTTP_422 = (422, "request parameters illegal")
    HTTP_425 = (
        425,
        "cannot execute the request, because the server cannot meet the requirements",
    )
    HTTP_429 = (429, "Excessive requests, server limit")
    HTTP_500 = (500, "Internal error of the server")
    HTTP_502 = (502, "gateway error")
    HTTP_503 = (503, "The server cannot handle the request for the time being")
    HTTP_504 = (504, "gateway timeout")


@dataclasses.dataclass
class CustomResponse:
    """Custom response class."""

    code: int
    msg: str
