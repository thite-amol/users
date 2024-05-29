"""Module."""

from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Type


class _EnumBase:
    """_summary_.

    Returns:
        _type_: _description_
    """

    @classmethod
    def get_member_keys(cls: Type[Enum]) -> list[str]:
        """_summary_.

        Args:
            cls (Type[Enum]): _description_

        Returns:
            list[str]: _description_
        """
        return list(cls.__members__.keys())

    @classmethod
    def get_member_values(cls: Type[Enum]) -> list:
        """_summary_.

        Args:
            cls (Type[Enum]): _description_

        Returns:
            list: _description_
        """
        return [item.value for item in cls.__members__.values()]


class IntEnum(_EnumBase, SourceIntEnum):
    """integer enum."""

    pass


class RoleDataScopeType(IntEnum):
    """data range."""

    ALL = 1
    CUSTOM = 2


class StatusType(IntEnum):
    """status type."""

    DISABLE = 0
    ENABLE = 1
