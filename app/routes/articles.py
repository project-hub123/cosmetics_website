import os
from flask import (
    Blueprint, render_template, redirect,
    url_for, request, flash, current_app
)
from flask_login import login_required, current_user

from app.models import Article, Category
from app.forms import ArticleForm
from app.utils import role_required, save_image

articles_bp = Blueprint("articles", __name__, url_prefix="/articles")


# ============================================================
#                    СПИСОК КАТЕГОРИЙ
# ============================================================
@articles_bp.route("/")
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template("articles/categories.html", categories=categories)


# ============================================================
#                   СПИСОК СТАТЕЙ В КАТЕГОРИИ
# ============================================================
@articles_bp.route("/category/<slug>")
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()

    articles = (
        Article.query.filter_by(category_id=category.id)
        .order_by(Article.created_at.desc())
        .all()
    )

    return render_template(
        "articles/category.html",
        category=category,
        articles=articles
    )


# ============================================================
#                     ПРОСМОТР СТАТЬИ
# ============================================================
@articles_bp.route("/view/<int:article_id>")
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("articles/article_detail.html", article=article)


# ============================================================
#                   ДОБАВЛЕНИЕ СТАТЬИ
# ============================================================
@articles_bp.route("/add", methods=["GET", "POST"])
@login_required
@role_required("employee", "admin")
def add_article():
    form = ArticleForm()
    form.set_categories()

    if form.validate_on_submit():

        # сохраняем изображение
        image_name = None
        if form.image.data:
            upload_folder = os.path.join(current_app.root_path, "static", "img", "articles")
            image_name = save_image(form.image.data, upload_folder)

        # создаём статью
        new_article = Article(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category.data,
            author_id=current_user.id,
            image=image_name
        )

        from app import db
        db.session.add(new_article)
        db.session.commit()

        flash("Статья успешно добавлена!", "success")
        return redirect(url_for("articles.article_detail", article_id=new_article.id))

    return render_template("articles/add_article.html", form=form)


# ============================================================
#                   РЕДАКТИРОВАНИЕ СТАТЬИ
# ============================================================
@articles_bp.route("/edit/<int:article_id>", methods=["GET", "POST"])
@login_required
@role_required("employee", "admin")
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)

    form = ArticleForm()
    form.set_categories()

    # предварительное заполнение
    if request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
        form.category.data = article.category_id

    if form.validate_on_submit():

        article.title = form.title.data
        article.content = form.content.data
        article.category_id = form.category.data

        # если загружено новое изображение
        if form.image.data:
            upload_folder = os.path.join(current_app.root_path, "static", "img", "articles")
            image_name = save_image(form.image.data, upload_folder)
            if image_name:
                article.image = image_name

        from app import db
        db.session.commit()

        flash("Изменения сохранены", "success")
        return redirect(url_for("articles.article_detail", article_id=article.id))

    return render_template("articles/edit_article.html", form=form, article=article)


# ============================================================
#                       УДАЛЕНИЕ СТАТЬИ
# ============================================================
@articles_bp.route("/delete/<int:article_id>", methods=["POST"])
@login_required
@role_required("employee", "admin")
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)

    from app import db
    db.session.delete(article)
    db.session.commit()

    flash("Статья удалена", "info")
    return redirect(url_for("articles.categories"))
