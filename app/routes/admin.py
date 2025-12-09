from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request
)
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app.models import User
from app.forms import AdminCreateUserForm
from app.utils import role_required
from app import db


admin_bp = Blueprint("admin", __name__)


# ============================================================
#                СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
# ============================================================
@admin_bp.route("/users")
@login_required
@role_required("employee", "admin")
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users_list.html", users=users)


# ============================================================
#              СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ (СОТРУДНИКОМ)
# ============================================================
@admin_bp.route("/create_user", methods=["GET", "POST"])
@login_required
@role_required("employee", "admin")
def create_user():
    form = AdminCreateUserForm()

    # если роль employee → нельзя создавать админов
    if current_user.role == "employee":
        # убираем возможность выбрать admin
        form.role.choices = [
            ("user", "Пользователь"),
            ("employee", "Сотрудник")
        ]

    if form.validate_on_submit():

        # Проверка логина
        if User.query.filter_by(username=form.username.data).first():
            flash("Логин уже существует.", "danger")
            return redirect(url_for("admin.create_user"))

        # Проверка email
        if User.query.filter_by(email=form.email.data).first():
            flash("Email уже зарегистрирован.", "danger")
            return redirect(url_for("admin.create_user"))

        # Создание пользователя
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Пользователь успешно создан!", "success")
        return redirect(url_for("admin.users_list"))

    return render_template("admin/create_user.html", form=form)


# ============================================================
#                     ИЗМЕНЕНИЕ РОЛИ ПОЛЬЗОВАТЕЛЯ
# ============================================================
@admin_bp.route("/change_role/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def change_role(user_id):
    user = User.query.get_or_404(user_id)

    new_role = request.form.get("role")

    if new_role not in ("user", "employee", "admin"):
        flash("Некорректная роль.", "danger")
        return redirect(url_for("admin.users_list"))

    # защита: нельзя менять роль у самого себя
    if user.id == current_user.id:
        flash("Нельзя изменить собственную роль.", "warning")
        return redirect(url_for("admin.users_list"))

    user.role = new_role
    db.session.commit()

    flash("Роль пользователя изменена!", "success")
    return redirect(url_for("admin.users_list"))


# ============================================================
#                    УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
# ============================================================
@admin_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # защита: админ не может удалить сам себя
    if user.id == current_user.id:
        flash("Нельзя удалить собственную учетную запись.", "warning")
        return redirect(url_for("admin.users_list"))

    db.session.delete(user)
    db.session.commit()

    flash("Пользователь удалён.", "info")
    return redirect(url_for("admin.users_list"))
