"""Module."""

from pydantic import BaseModel, ConfigDict, EmailStr, validate_email
from pydantic_extra_types.phone_numbers import PhoneNumber


class CustomPhoneNumber(PhoneNumber):
    """_summary_.

    Args:
        PhoneNumber (_type_): _description_
    """

    default_region_code = "IN"


class CustomEmailStr(EmailStr):
    """_summary_.

    Args:
        EmailStr (_type_): _description_

    Returns:
        _type_: _description_
    """

    @classmethod
    def _validate(cls, __input_value: str) -> str:
        return None if __input_value == "" else validate_email(__input_value)[1]


class SchemaBase(BaseModel):
    """_summary_.

    Args:
        BaseModel (_type_): _description_
    """

    model_config = ConfigDict(use_enum_values=True)
