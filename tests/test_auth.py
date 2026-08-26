feature/auth-and-roles
from unittest.mock import patch

from src.auth.auth import login, require_role


def test_login_success_admin():
    # Simulate user inputs for username and password
    with patch("builtins.input", side_effect=["admin", "1234"]):
        user = login()
        assert user is not None
        assert user["username"] == "admin"
        assert user["role"] == "admin"


def test_login_success_staff():
    with patch("builtins.input", side_effect=["staff", "abcd"]):
        user = login()
        assert user is not None
        assert user["username"] == "staff"
        assert user["role"] == "staff"


def test_login_failure():
    with patch("builtins.input", side_effect=["admin", "wrongpassword"]):
        user = login()
        assert user is None


def test_require_role_allowed():
    @require_role("admin")
    def dummy_admin_action():
        return "Success"

    admin_user = {"username": "admin", "role": "admin"}
    result = dummy_admin_action(admin_user)
    assert result == "Success"


def test_require_role_denied():
    @require_role("admin")
    def dummy_admin_action():
        return "Success"

    staff_user = {"username": "staff", "role": "staff"}
    result = dummy_admin_action(staff_user)
    assert result is None

from src.auth.auth import login


def test_login_success(monkeypatch):
    """Test successful login with correct username and password."""
    inputs = iter(["admin", "1234"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = login()
    assert result is True


def test_login_failure(monkeypatch):
    """Test failed login with incorrect credentials."""
    inputs = iter(["wrong_user", "wrong_pass"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = login()
    assert result is False
main
