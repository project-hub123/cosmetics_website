from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ---------------------------------------------------------
    # 🔧 БАЗОВАЯ КОНФИГУРАЦИЯ
    # ---------------------------------------------------------
    app.config['SECRET_KEY'] = "super_secret_key_change_in_production"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cosmetics.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.permanent_session_lifetime = timedelta(days=7)

    # ---------------------------------------------------------
    # 🔧 ИНИЦИАЛИЗАЦИЯ РАСШИРЕНИЙ
    # ---------------------------------------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # ---------------------------------------------------------
    # 🔧 ЗАГРУЗКА ПОЛЬЗОВАТЕЛЯ
    # ---------------------------------------------------------
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ---------------------------------------------------------
    # 🔧 ПЕРЕДАЧА СТИЛЯ ВО ВСЕ ШАБЛОНЫ
    # ---------------------------------------------------------
    @app.context_processor
    def inject_style_mode():
        """Передаёт в шаблоны текущий выбранный стиль"""
        mode = session.get("style_mode", "normal")
        return {"style_mode": mode}

    # ---------------------------------------------------------
    # 🔧 ПЕРЕКЛЮЧЕНИЕ СТИЛЯ (ОБЫЧНЫЙ ↔ СЛАБОВИДЯЩИЕ)
    # ---------------------------------------------------------
    @app.route("/toggle-style")
    def toggle_style():
        """Переключение темы сайта"""
        current = session.get("style_mode", "normal")
        session["style_mode"] = "lowvision" if current == "normal" else "normal"

        # Важно: ДОЛЖЕН БЫТЬ redirect!
        return redirect(request.referrer or url_for("main.index"))

    # ---------------------------------------------------------
    # 🔧 РЕГИСТРАЦИЯ BLUEPRINTS
    # ---------------------------------------------------------
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.articles import articles_bp
    from app.routes.news import news_bp
    from app.routes.messages import messages_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(articles_bp, url_prefix="/articles")
    app.register_blueprint(news_bp, url_prefix="/news")
    app.register_blueprint(messages_bp, url_prefix="/messages")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ---------------------------------------------------------
    # 🔧 ГЛОБАЛЬНАЯ СТРАНИЦА 404
    # ---------------------------------------------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # ---------------------------------------------------------
    # 🔧 АВТОМАТИЧЕСКОЕ СОЗДАНИЕ ПАПОК КОНТЕНТА
    # ---------------------------------------------------------
    content_dirs = [
        "static/img/banners",
        "static/img/articles",
        "static/img/news"
    ]
    for d in content_dirs:
        full = os.path.join(app.root_path, d)
        os.makedirs(full, exist_ok=True)

    return app
