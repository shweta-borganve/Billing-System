from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_db_session():
    """Provide a mock database session for tests."""
    session = MagicMock()
    session.commit.return_value = None
    session.rollback.return_value = None
    session.close.return_value = None
    return session


@pytest.fixture
def mock_auth_user():
    """Provide a mock authenticated user for testing protected routes/functions."""
    return {"username": "test_user", "role": "admin", "authenticated": True}
