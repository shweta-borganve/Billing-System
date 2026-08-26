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
