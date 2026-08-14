import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "billing.db")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
SECRET_KEY = os.getenv("APP_SECRET_KEY", "default-secret-key")
