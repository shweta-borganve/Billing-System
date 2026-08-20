from src.services.logger_config import logger

# Define users with roles
USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "staff": {"password": "abcd", "role": "staff"},
}


def login():
    print("\n===== System Login =====")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in USERS and USERS[username]["password"] == password:
        role = USERS[username]["role"]
        print(f"Login successful! Welcome, {username} ({role}).")
        logger.info(f"User '{username}' logged in successfully with role '{role}'.")
        return {"username": username, "role": role}

    print("Invalid username or password.")
    logger.warning(f"Failed login attempt for username: {username}")
    return None


def require_role(required_role):
    """Decorator or helper to check if a user role has permission."""

    def decorator(func):
        def wrapper(current_user, *args, **kwargs):
            if not current_user or current_user.get("role") != required_role:
                print(
                    "Access Denied: You do not have permission to perform this action."
                )
                logger.warning(f"Unauthorized access attempt by user: {current_user}")
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator
