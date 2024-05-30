"""Module."""

from datetime import datetime

from pydantic import ConfigDict, Field

from src.common.enums import RoleDataScopeType, StatusType
from src.common.schema import SchemaBase


class RoleSchemaBase(SchemaBase):
    """_summary_.

    Args:
        SchemaBase (_type_): _description_
    """

    name: str
    data_scope: RoleDataScopeType = Field(
        default=RoleDataScopeType.CUSTOM,
        description="Permission scope (1: All data permissions 2: Custom data permissions)",
    )
    status: StatusType = Field(default=StatusType.ENABLE)
    remark: str | None = None


class CreateRoleParam(RoleSchemaBase):
    """_summary_.

    Args:
        RoleSchemaBase (_type_): _description_
    """

    pass


class UpdateRoleParam(RoleSchemaBase):
    """_summary_.

    Args:
        RoleSchemaBase (_type_): _description_
    """

    pass


class GetRoleListDetails(SchemaBase):
    """_summary_.

    Args:
        SchemaBase (_type_): _description_
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
