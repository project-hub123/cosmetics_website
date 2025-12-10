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
from sqlalchemy import or_

main_bp = Blueprint("main", __name__)


# ============================================================
#                       ГЛАВНАЯ СТРАНИЦА
# ============================================================
@main_bp.route("/")
def index():
    latest_articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()
    latest_news = News.query.order_by(News.created_at.desc()).limit(3).all()

    banners = ["banner1.jpg", "banner2.jpg", "banner3.jpg"]

    return render_template(
        "index.html",
        latest_articles=latest_articles,
        latest_news=latest_news,
        banners=banners
    )


# ============================================================
#                       ПОИСК (GET)
# ============================================================
@main_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()

    if not query:
        flash("Введите текст для поиска.", "warning")
        return redirect(url_for("main.index"))

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

# ============================================================
#                       КАРТА САЙТА
# ============================================================
@main_bp.route("/sitemap")
def sitemap():
    categories = Category.query.all()
    return render_template("sitemap.html", categories=categories)


# ============================================================
#                       КОНТАКТЫ
# ============================================================
@main_bp.route("/contacts", methods=["GET", "POST"])
def contacts():
    from app.forms import FeedbackForm
    form = FeedbackForm()

    if form.validate_on_submit():
        flash("Ваше сообщение отправлено!", "success")
        return redirect(url_for("main.contacts"))

    return render_template("contacts.html", form=form)


# ============================================================
#                       ПЕРЕКЛЮЧЕНИЕ СТИЛЯ
# ============================================================
@main_bp.route("/style/<mode>")
def change_style(mode):
    if mode not in ("normal", "lowvision"):
        return redirect(url_for("main.index"))

    session["style_mode"] = mode
    return redirect(request.referrer or url_for("main.index"))
