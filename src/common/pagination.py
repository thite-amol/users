"""Pagination base module."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Dict, Generic, Sequence, TypeVar

from fastapi import Depends, Query
from fastapi_pagination import pagination_ctx
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links.bases import create_links
from pydantic import BaseModel

if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
DataT = TypeVar("DataT")
SchemaT = TypeVar("SchemaT")


class _Params(BaseModel, AbstractParams):
    """Params class."""

    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(20, gt=0, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class _Page(AbstractPage[T], Generic[T]):
    """Page class."""

    items: Sequence[T]
    total: int
    page: int
    size: int
    total_pages: int
    links: Dict[str, str | None]

    __params_type__ = _Params  # Use custom Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: _Params,
    ) -> _Page[T]:
        """Creates Page class objects with config.

        Args:
            items (Sequence[T]): List of items
            total (int): Total numbers of items
            params (_Params): Current value of params

        Returns:
            _Page[T]: Page class object with config
        """
        page = params.page
        size = params.size
        total_pages = math.ceil(total / params.size)
        links = create_links(
            **{
                "first": {"page": 1, "size": f"{size}"},
                "last": {
                    "page": f"{math.ceil(total / params.size)}",
                    "size": f"{size}",
                }
                if total > 0
                else None,
                "next": {"page": f"{page + 1}", "size": f"{size}"}
                if (page + 1) <= total_pages
                else None,
                "prev": {"page": f"{page - 1}", "size": f"{size}"}
                if (page - 1) >= 1
                else None,
            }
        ).model_dump()

        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            total_pages=total_pages,
            links=links,
        )


class _PageData(BaseModel, Generic[DataT]):
    page_data: DataT | None = None


async def paging_data(
    db: AsyncSession, select: Select, page_data_schema: SchemaT
) -> dict:
    """Create paginated data based on SQLAlchemy.

    Args:
        db (AsyncSession): Current session
        select (Select): SQLAlchemy Select class object
        page_data_schema (SchemaT): Page config

    Returns:
        dict: Pagination on given items
    """
    paginate_obj = await paginate(db, select)
    page_data = _PageData[_Page[page_data_schema]](
        page_data=paginate_obj
    ).model_dump()["page_data"]
    return page_data


DependsPagination = Depends(pagination_ctx(_Page))
