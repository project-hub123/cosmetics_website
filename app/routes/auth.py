from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request
)
from flask_login import (
    login_user, logout_user, current_user, login_required
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from app.forms import RegisterForm, LoginForm
from app import db


auth_bp = Blueprint("auth", __name__)


# ============================================================
#                     РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# ============================================================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Если пользователь уже вошёл → не даём открыть регистрацию
    if current_user.is_authenticated:
        flash("Вы уже авторизованы.", "info")
        return redirect(url_for("main.index"))

    form = RegisterForm()

    if form.validate_on_submit():

        # Проверка уникальности логина
        if User.query.filter_by(username=form.username.data).first():
            flash("Пользователь с таким логином уже существует.", "danger")
            return redirect(url_for("auth.register"))

        # Проверка уникальности email
        if User.query.filter_by(email=form.email.data).first():
            flash("Этот email уже зарегистрирован.", "danger")
            return redirect(url_for("auth.register"))

        # Создание нового пользователя
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация успешна! Теперь войдите в систему.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


# ============================================================
#                          ВХОД
# ============================================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Вы уже вошли.", "info")
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():

        # Поиск пользователя в базе
        user = User.query.filter_by(username=form.username.data).first()

        # Проверка логина
        if not user:
            flash("Неверный логин или пароль.", "danger")
            return redirect(url_for("auth.login"))

        # Проверка хэша пароля
        if not check_password_hash(user.password, form.password.data):
            flash("Неверный логин или пароль.", "danger")
            return redirect(url_for("auth.login"))

        # Авторизация пользователя
        login_user(user)

        flash("Вы успешно вошли!", "success")

        next_page = request.args.get("next")
        
        # Проверка, что next действительно существует и безопасен
        if next_page and next_page.startswith("/"):
            return redirect(next_page)

        return redirect(url_for("main.index"))

    return render_template("auth/login.html", form=form)


# ============================================================
#                          ВЫХОД
# ============================================================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("main.index"))
