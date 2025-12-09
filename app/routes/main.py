from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from app.models import Article, News, Category
from app.forms import SearchForm, FeedbackForm
from sqlalchemy import or_


main_bp = Blueprint("main", __name__)


# ============================================================
#                       ГЛАВНАЯ СТРАНИЦА
# ============================================================
@main_bp.route("/")
def index():
    # последние статьи (3 шт.)
    latest_articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()

    # последние новости (3 шт.)
    latest_news = News.query.order_by(News.created_at.desc()).limit(3).all()

    # баннеры — просто изображения из папки
    banners = [
        "banner1.jpg",
        "banner2.jpg",
        "banner3.jpg"
    ]

    search_form = SearchForm()

    return render_template(
        "index.html",
        latest_articles=latest_articles,
        latest_news=latest_news,
        banners=banners,
        search_form=search_form
    )


# ============================================================
#                       ПОИСК ПО САЙТУ
# ============================================================
@main_bp.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        query = form.query.data.strip()

        # поиск в статьях + новостях
        articles = Article.query.filter(
            or_(
                Article.title.ilike(f"%{query}%"),
                Article.content.ilike(f"%{query}%")
            )
        ).all()

        news = News.query.filter(
            or_(
                News.title.ilike(f"%{query}%"),
                News.content.ilike(f"%{query}%")
            )
        ).all()

        return render_template(
            "search_results.html",
            query=query,
            articles=articles,
            news=news
        )

    return redirect(url_for("main.index"))


# ============================================================
#                    КАРТА САЙТА (sitemap)
# ============================================================
@main_bp.route("/sitemap")
def sitemap():
    categories = Category.query.all()
    return render_template("sitemap.html", categories=categories)


# ============================================================
#                       СТРАНИЦА КОНТАКТОВ
# ============================================================
@main_bp.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = FeedbackForm()

    if form.validate_on_submit():
        flash("Ваше сообщение отправлено. Спасибо!", "success")
        return redirect(url_for("main.contacts"))

    return render_template("contacts.html", form=form)


# ============================================================
#                  ПЕРЕКЛЮЧЕНИЕ ТЕМЫ ОФОРМЛЕНИЯ
# ============================================================
@main_bp.route("/style/<mode>")
def change_style(mode):
    """
    Переключение темы оформления:
    mode = normal | lowvision
    """
    if mode not in ("normal", "lowvision"):
        return redirect(url_for("main.index"))

    session["style_mode"] = mode
    return redirect(request.referrer or url_for("main.index"))
