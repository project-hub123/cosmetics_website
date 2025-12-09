import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env (если есть)
load_dotenv()


class BaseConfig:
    """Базовая конфигурация для всего приложения."""

    # -----------------------------
    # Основные параметры приложения
    # -----------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "very-secret-key-change-me")
    DEBUG = False

    # -----------------------------
    # Настройки базы данных
    # -----------------------------
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "")
    DB_NAME = os.getenv("DB_NAME", "")

    # SQLite по умолчанию
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.abspath('database.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------------
    # Загрузка изображений
    # -----------------------------
    UPLOAD_FOLDER = "static/img"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # -----------------------------
    # Настройки сайта
    # -----------------------------
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # Время жизни сессии
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 дней


class DevelopmentConfig(BaseConfig):
    """Конфигурация для разработки."""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Конфигурация для продакшена."""

    DEBUG = False


# Выбор конфигурации из переменных окружения
def get_config():
    env = os.getenv("FLASK_ENV", "development").lower()

    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
