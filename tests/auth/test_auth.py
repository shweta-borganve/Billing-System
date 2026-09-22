from unittest.mock import patch

from src.auth.auth import login, require_role


def test_login_success_admin():
    """Test successful login for admin user."""
    with patch("builtins.input", side_effect=["admin", "1234"]):
        user = login()
        assert user is not None
        assert user["username"] == "admin"
        assert user["role"] == "admin"


def test_login_success_staff():
    """Test successful login for staff user."""
    with patch("builtins.input", side_effect=["staff", "abcd"]):
        user = login()
        assert user is not None
        assert user["username"] == "staff"
        assert user["role"] == "staff"


def test_login_failure():
    """Test failed login with incorrect credentials."""
    with patch("builtins.input", side_effect=["admin", "wrongpassword"]):
        user = login()
        assert user is None


def test_require_role_allowed():
    """Test that an allowed role can execute a protected function."""

    @require_role("admin")
    def dummy_admin_action(user=None):
        return "Success"

    admin_user = {"username": "admin", "role": "admin"}
    result = dummy_admin_action(admin_user)
    assert result == "Success"


def test_require_role_denied():
    """Test that a restricted role is denied access."""

    @require_role("admin")
    def dummy_admin_action(user=None):
        return "Success"

    staff_user = {"username": "staff", "role": "staff"}
    result = dummy_admin_action(staff_user)
    assert result is None
