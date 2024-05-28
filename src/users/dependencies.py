"""Module."""

from fastapi import Query


def get_pagination_params(
    limit: int = Query(20, ge=0), offset: int = Query(0, ge=0)
):
    """_summary_.

    Args:
        limit (int, optional): _description_. Defaults to Query(20, ge=0).
        offset (int, optional): _description_. Defaults to Query(0, ge=0).

    Returns:
        _type_: _description_
    """
    return {"limit": limit, "offset": offset}
