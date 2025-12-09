from flask import (
    Blueprint, render_template, redirect,
    url_for, flash
)
from flask_login import current_user, login_required

from app.models import Message
from app.forms import FeedbackForm
from app.utils import role_required
from app import db


messages_bp = Blueprint("messages", __name__)


# ============================================================
#                   ОТПРАВКА СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЕМ
# ============================================================
@messages_bp.route("/send", methods=["GET", "POST"])
def send_message():
    form = FeedbackForm()

    if form.validate_on_submit():
        msg = Message(
            sender_name=form.sender_name.data,
            sender_email=form.sender_email.data,
            content=form.content.data,
            user_id=current_user.id if current_user.is_authenticated else None
        )

        db.session.add(msg)
        db.session.commit()

        flash("Ваше сообщение успешно отправлено!", "success")
        return redirect(url_for("main.index"))

    return render_template("messages/feedback.html", form=form)


# ============================================================
#            ПРОСМОТР СООБЩЕНИЙ ДЛЯ СОТРУДНИКОВ/АДМИНА
# ============================================================
@messages_bp.route("/inbox")
@login_required
@role_required("employee", "admin")
def inbox():
    messages = Message.query.order_by(Message.created_at.desc()).all()

    return render_template(
        "messages/inbox.html",
        messages=messages
    )


# ============================================================
#                   ПРОСМОТР ОТДЕЛЬНОГО СООБЩЕНИЯ
# ============================================================
@messages_bp.route("/view/<int:msg_id>")
@login_required
@role_required("employee", "admin")
def view_message(msg_id):
    msg = Message.query.get_or_404(msg_id)
    return render_template("messages/view_message.html", msg=msg)


# ============================================================
#                       УДАЛЕНИЕ СООБЩЕНИЯ
# ============================================================
@messages_bp.route("/delete/<int:msg_id>", methods=["POST"])
@login_required
@role_required("employee", "admin")
def delete_message(msg_id):
    msg = Message.query.get_or_404(msg_id)

    db.session.delete(msg)
    db.session.commit()

    flash("Сообщение удалено.", "info")
    return redirect(url_for("messages.inbox"))
