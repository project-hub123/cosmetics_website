from app import create_app, db
from app.models import User, Category
from werkzeug.security import generate_password_hash

"""
init_db.py — инициализация базы данных.

Запуск:
    python init_db.py
"""

app = create_app()

with app.app_context():
    print("Создаю таблицы...")
    db.create_all()

    # -------------------------------
    # 1. Создание стандартных категорий
    # -------------------------------
    default_categories = [
        ("skin", "Уход за кожей"),
        ("hair", "Уход за волосами"),
        ("makeup", "Макияж"),
        ("perfume", "Парфюмерия"),
        ("body", "Уход за телом"),
    ]

    for slug, name in default_categories:
        if not Category.query.filter_by(slug=slug).first():
            db.session.add(Category(slug=slug, name=name))
            print(f"Добавлена категория: {name}")

    # -------------------------------
    # 2. Создание администратора
    # -------------------------------
    admin_username = "admin"
    admin_password = "admin123"
    admin_email = "admin@example.com"

    if not User.query.filter_by(username=admin_username).first():
        admin = User(
            username=admin_username,
            email=admin_email,
            role="admin",
            password=generate_password_hash(admin_password)
        )
        db.session.add(admin)
        print("Создан администратор:")
        print(f"  Логин: {admin_username}")
        print(f"  Пароль: {admin_password}")

    # -------------------------------
    # Завершение транзакции
    # -------------------------------
    db.session.commit()
    print("\nГотово! База данных инициализирована успешно.")
