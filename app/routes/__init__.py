# Файл нужен, чтобы папка routes была Python-пакетом
# Содержимого может не быть — проект будет работать

# Но можно добавить удобные импорты BP:
from .main import main_bp
from .auth import auth_bp
from .articles import articles_bp
from .news import news_bp
from .messages import messages_bp
from .admin import admin_bp

__all__ = [
    "main_bp",
    "auth_bp",
    "articles_bp",
    "news_bp",
    "messages_bp",
    "admin_bp"
]
