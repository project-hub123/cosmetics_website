import os
import uuid
from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user


# ============================================================
#                 ПРОВЕРКА РОЛИ ПОЛЬЗОВАТЕЛЯ
# ============================================================

def role_required(*roles):
    """
    Декоратор для защиты маршрутов.
    Использование:
        @role_required("admin")
        @role_required("employee", "admin")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # Проверка авторизации
            if not current_user.is_authenticated:
                flash("Необходимо войти в систему.", "warning")
                return redirect(url_for("auth.login"))

            # Проверка совпадения роли
            if current_user.role not in roles:
                abort(403)  # Нет доступа

            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
#                ПРОВЕРКА ФОРМАТА КАРТИНКИ
# ============================================================

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}


def allowed_image(filename: str) -> bool:
    """
    Проверяет, является ли файл картинкой допустимого формата.
    """
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS


# ============================================================
#        ГЕНЕРАЦИЯ УНИКАЛЬНОГО ИМЕНИ ДЛЯ ФАЙЛОВ
# ============================================================

def generate_filename(original_name: str) -> str:
    """
    Создаёт уникальный файл, сохраняя расширение.
    """
    ext = original_name.rsplit(".", 1)[1].lower()
    new_name = f"{uuid.uuid4().hex}.{ext}"
    return new_name


# ============================================================
#      СОХРАНЕНИЕ ФАЙЛА В НУЖНУЮ ПАПКУ (articles/news)
# ============================================================

def save_image(file, folder_path: str) -> str:
    """
    Сохраняет изображение в указанную папку.
    Возвращает имя файла или None.
    """
    if not file:
        return None

    filename = file.filename

    if not allowed_image(filename):
        return None

    unique_name = generate_filename(filename)
    full_path = os.path.join(folder_path, unique_name)

    file.save(full_path)

    return unique_name


# ============================================================
#           ПРОВЕРКА ДОСТУПА К СТРАНИЦАМ АДМИНА
# ============================================================

def is_admin() -> bool:
    return current_user.is_authenticated and current_user.role == "admin"


def is_employee() -> bool:
    return current_user.is_authenticated and current_user.role in ("employee", "admin")
