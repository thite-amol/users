import os
import secrets
from typing import Any, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class AppSettings(BaseSettings):
    class Config:
        env_file = DOTENV
        env_file_encoding = "utf-8"
        env_prefix = ""
        case_sensitive = True

    IS_GOOD_ENV: bool = True
    # ALLOWED_CORS_ORIGINS: set[AnyUrl]

    PROJECT_NAME: str = "Amol's Experiment"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SQL_DB: str = os.getenv("SQL_DB")
    DATABASE_CONNECTION_URL: str = ''

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    JWT_ALGORITHM: str = "HS256"
    ROOT_DIR: str = os.path.dirname(__file__)

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str]
    SMTP_USER: Optional[str]
    SMTP_PASSWORD: Optional[str]
    EMAILS_FROM_EMAIL: Optional[EmailStr]
    EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str, info: FieldValidationInfo) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @field_validator("DATABASE_CONNECTION_URL", mode='before')
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        return f"sqlite:///./{os.path.join(os.path.dirname(__file__), info.data.get('SQL_DB', ''))}.db"

    @field_validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], info: FieldValidationInfo) -> str:
        if not v:
            return info.data.get("PROJECT_NAME")
        return v

    SERVER_HOST: str = "localhost"
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = os.path.join(ROOT_DIR, "email-templates", "build")
    EMAILS_ENABLED: bool = True

    @field_validator("EMAILS_ENABLED")
    def get_emails_enabled(cls, v: bool, info: FieldValidationInfo) -> bool:

        return bool(
            info.data.get("SMTP_HOST")
            and info.data.get("SMTP_PORT")
            and info.data.get("EMAILS_FROM_EMAIL")
        )


settings = AppSettings()
