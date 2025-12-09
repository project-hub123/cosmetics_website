import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "secret-key-change-it"

    # Если Render задаёт DATABASE_URL — используем PostgreSQL.
    # Если нет — используем локальную SQLite.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'database.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.getenv("RENDER", None) is None  # Render отключает DEBUG

    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "img"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
