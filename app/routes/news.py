import os
from flask import (
    Blueprint, render_template, redirect,
    url_for, request, flash, current_app
)
from flask_login import login_required, current_user

from app.models import News
from app.forms import NewsForm
from app.utils import role_required, save_image
from app import db


news_bp = Blueprint("news", __name__)


# ============================================================
#                       ЛЕНТА НОВОСТЕЙ
# ============================================================
@news_bp.route("/")
def news_list():
    news = News.query.order_by(News.created_at.desc()).all()
    return render_template("news/news_list.html", news=news)


# ============================================================
#                   ПРОСМОТР ОТДЕЛЬНОЙ НОВОСТИ
# ============================================================
@news_bp.route("/<int:news_id>")
def news_detail(news_id):
    news_item = News.query.get_or_404(news_id)
    return render_template("news/news_detail.html", news_item=news_item)


# ============================================================
#                      ДОБАВЛЕНИЕ НОВОСТИ
# ============================================================
@news_bp.route("/add", methods=["GET", "POST"])
@login_required
@role_required("employee", "admin")
def add_news():
    form = NewsForm()

    if form.validate_on_submit():
        image_name = None

        if form.image.data:
            upload_folder = os.path.join(current_app.root_path, "static", "img", "news")
            image_name = save_image(form.image.data, upload_folder)

        news_item = News(
            title=form.title.data,
            content=form.content.data,
            image=image_name,
            author_id=current_user.id
        )

        db.session.add(news_item)
        db.session.commit()

        flash("Новость успешно опубликована!", "success")
        return redirect(url_for("news.news_detail", news_id=news_item.id))

    return render_template("news/add_news.html", form=form)


# ============================================================
#                      РЕДАКТИРОВАНИЕ НОВОСТИ
# ============================================================
@news_bp.route("/edit/<int:news_id>", methods=["GET", "POST"])
@login_required
@role_required("employee", "admin")
def edit_news(news_id):
    news_item = News.query.get_or_404(news_id)
    form = NewsForm()

    if request.method == "GET":
        form.title.data = news_item.title
        form.content.data = news_item.content

    if form.validate_on_submit():

        news_item.title = form.title.data
        news_item.content = form.content.data

        if form.image.data:
            upload_folder = os.path.join(current_app.root_path, "static", "img", "news")
            image_name = save_image(form.image.data, upload_folder)
            if image_name:
                news_item.image = image_name

        db.session.commit()

        flash("Новость обновлена.", "success")
        return redirect(url_for("news.news_detail", news_id=news_item.id))

    return render_template("news/edit_news.html", form=form, news_item=news_item)


# ============================================================
#                        УДАЛЕНИЕ НОВОСТИ
# ============================================================
@news_bp.route("/delete/<int:news_id>", methods=["POST"])
@login_required
@role_required("employee", "admin")
def delete_news(news_id):
    news_item = News.query.get_or_404(news_id)

    db.session.delete(news_item)
    db.session.commit()

    flash("Новость удалена.", "info")
    return redirect(url_for("news.news_list"))
