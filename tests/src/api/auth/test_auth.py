"""Module to test auth API."""

from unittest.mock import AsyncMock

from src.config import settings

PYTEST_USERNAME = "admin"
PYTEST_PASSWORD = "string"


def test_login(mocker, client, admin_user) -> None:
    """Test normal user login."""
    data = {
        "username": PYTEST_USERNAME,
        "password": PYTEST_PASSWORD,
    }

    headers = {}

    async_mock = AsyncMock(return_value=admin_user)
    mocker.patch(
        "src.auth.service.UsersCRUD.get_by_username", side_effect=async_mock
    )
    mocker.patch(
        "src.auth.service.UsersCRUD.update_login_time", return_value=True
    )
    response = client.post(
        f"{settings.base.API_V1_STR}/login", data=data, headers=headers
    )

    data = response.json()
    assert data["code"] == 200
    assert "access_token" in data["data"]
    assert "token_type" in data["data"]


def test_login_user_not_exist(mocker, client, admin_user):
    """Test login if user not exist."""
    data = {
        "username": PYTEST_USERNAME,
        "password": PYTEST_PASSWORD,
    }

    headers = {}

    async_mock = AsyncMock(return_value=False)
    mocker.patch(
        "src.auth.service.UsersCRUD.get_by_username", side_effect=async_mock
    )

    response = client.post(
        f"{settings.base.API_V1_STR}/login", data=data, headers=headers
    )

    data = response.json()
    assert data["code"] == 404
    assert data["msg"] == "User does not exist"


def test_token_invalid(mocker, client, admin_user):
    """Test if token is valid or not."""
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NDZjMDU2Zi1iNTdiLTRmMTgtYjFjYS04ODcxNWYzNDUzODciLCJhdWQiOlsiZmFzdGFwaS11c2VyczphdXRoIl0sImV4cCI6MTcwODA4MTk3MH0.4p6LMuEZe-ZWXx-FDwbCBLaaG_Cj185dJxwGDDfuMuM"
    }
    response = client.post(
        f"{settings.base.API_V1_STR}/login/test-token", data={}, headers=headers
    )

    data = response.json()
    assert data["code"] == 401
