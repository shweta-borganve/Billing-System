from logger_config import logger

USERNAME = "admin"
PASSWORD = "1234"  # nosec


def login():
    print("\n===== Admin Login =====")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == USERNAME and password == PASSWORD:
        print("Login successful!")
        logger.info("Admin logged in successfully.")
        return True

    print("Invalid username or password.")
    logger.warning(f"Failed login attempt for username: {username}")
    return False
