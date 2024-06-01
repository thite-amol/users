"""Fixture for test cases."""

import pytest
from starlette.testclient import TestClient

from src.db.session import get_db
from src.main import app
from src.users.model import User

from tests.src.utils.db_mysql import override_get_db

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Create main app object.

    Returns:
        TestClient: A callable test client object

    Yields:
        Iterator[TestClient]: A callable test client object
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_user() -> User:
    """Create user data fixture.

    Returns:
        User: User data for test case operation
    """
    admin_user = User(
        email="admin@example.com",
        username="admin",
        password="$2b$12$8KzDpWiJbRhgWRUHzNi6bOhKojiEQuQrvdFxL39/8AJiSOt5dg.H6",
        first_name="Admin",
        last_name="User",
        is_superuser=True,
        avatar=None,
        phone=None,
        is_active=True,
    )
    admin_user.id = 3
    return admin_user
