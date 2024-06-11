"""Base app config module."""

import os
import secrets
from typing import List, Literal, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

from src.config.path_conf import DOTENV, SRC_PATH


class BaseConfig(BaseSettings):
    """Base class with config."""

    class Config:
        """Pydantic config option class."""

        env_file = DOTENV
        env_file_encoding = "utf-8"
        env_prefix = ""
        case_sensitive = True
        extra = "allow"


class CoreSettings(BaseConfig):
    """Core app settings."""

    IS_GOOD_ENV: bool = True
    DEBUG: bool = False
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    PROJECT_NAME: str = "Users management"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    DOCS_URL: str | None = f"{API_V1_STR}/docs"
    REDOCS_URL: str | None = f"{API_V1_STR}/redocs"
    OPENAPI_URL: str | None = f"{API_V1_STR}/openapi"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    TOKEN_EXPIRE_MINUTES: int = 15
    JWT_ALGORITHM: str = "HS256"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:4200",
        "http://localhost:3000",
    ]

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(
        cls,
        v: str,
        info: ValidationInfo,  # pylint: disable=unused-argument
    ) -> Union[List[str], str]:
        """Build cors url's list.

        Args:
            v (str): Variable value
            info (ValidationInfo): validation info

        Raises:
            ValueError: If value is invalid.

        Returns:
            Union[List[str], str]: List of allowed domains
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # DateTime
    DATETIME_TIMEZONE: str = "Asia/Kolkata"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # Log config
    LOG_STDOUT_FILENAME: str = "users_access.log"
    LOG_STDERR_FILENAME: str = "users_error.log"

    STATIC_FILES: bool = False


class DatabaseSettings(BaseConfig):
    """Database config."""

    SQL_DB: str = os.getenv("SQL_DB")
    DATABASE_CONNECTION_URL: str = ""
    QUERY_ECHO: bool = True

    @field_validator("DATABASE_CONNECTION_URL", mode="before")
    def assemble_db_connection(
        cls,
        v: Optional[str],  # pylint: disable=unused-argument
        info: ValidationInfo,
    ) -> str:
        """Build database connection url.

        Args:
            v (Optional[str]): variable value
            info (ValidationInfo): validation info

        Returns:
            str: database connection url
        """
        file_path = os.path.join(SRC_PATH, info.data.get("SQL_DB", ""))
        return f"sqlite+aiosqlite:///{file_path}.db"  # pylint: disable=inconsistent-quotes


class EmailSettings(BaseConfig):
    """Email config."""

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str]
    SMTP_USER: Optional[str]
    SMTP_PASSWORD: Optional[str]
    EMAILS_FROM_EMAIL: Optional[EmailStr]
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

    @field_validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], info: ValidationInfo) -> str:
        """Build project name.

        Args:
            v (Optional[str]): variable value
            info (ValidationInfo): validation info

        Returns:
            str: project name
        """
        if not v:
            return info.data.get("PROJECT_NAME")
        return v

    SERVER_HOST: str = "localhost"
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = os.path.join(
        SRC_PATH, "email-templates", "build"
    )
    EMAILS_ENABLED: bool = True

    @field_validator("EMAILS_ENABLED")
    def get_emails_enabled(cls, v: bool, info: ValidationInfo) -> bool:  # pylint: disable=unused-argument
        """Check if email is enabled.

        Args:
            v (bool): variable value
            info (ValidationInfo): validation info

        Returns:
            bool: _description_
        """
        return bool(
            info.data.get("SMTP_HOST")
            and info.data.get("SMTP_PORT")
            and info.data.get("EMAILS_FROM_EMAIL")
        )


class AppSettings(BaseConfig):
    """_summary_.

    Args:
        BaseSettings (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    database: DatabaseSettings = DatabaseSettings()
    email: EmailSettings = EmailSettings()
    base: CoreSettings = CoreSettings()


settings = AppSettings()
