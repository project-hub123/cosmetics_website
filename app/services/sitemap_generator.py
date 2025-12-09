from flask import url_for
from datetime import datetime
from app.models import Article, News, Category


def generate_sitemap():
    """
    Генератор XML-карты сайта.
    Создаёт список URL и возвращает готовый XML-текст.
    """

    # Список URL
    urls = []

    # =======================
    # Основные статические страницы
    # =======================
    static_pages = [
        ("main.index", {}),
        ("main.contacts", {}),
        ("main.sitemap", {}),
        ("auth.login", {}),
        ("auth.register", {}),
    ]

    for endpoint, params in static_pages:
        try:
            urls.append({
                "loc": url_for(endpoint, **params, _external=True),
                "lastmod": datetime.utcnow().date().isoformat()
            })
        except:
            pass

    # =======================
    # Категории статей
    # =======================
    for cat in Category.query.all():
        try:
            urls.append({
                "loc": url_for("articles.category", slug=cat.slug, _external=True),
                "lastmod": datetime.utcnow().date().isoformat()
            })
        except:
            pass

    # =======================
    # Статьи
    # =======================
    for a in Article.query.all():
        urls.append({
            "loc": url_for("articles.article_detail", article_id=a.id, _external=True),
            "lastmod": a.created_at.date().isoformat() if a.created_at else datetime.utcnow().date().isoformat()
        })

    # =======================
    # Новости
    # =======================
    for n in News.query.all():
        urls.append({
            "loc": url_for("news.news_detail", news_id=n.id, _external=True),
            "lastmod": n.created_at.date().isoformat() if n.created_at else datetime.utcnow().date().isoformat()
        })

    # =======================
    # Генерация XML
    # =======================
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for item in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{item['loc']}</loc>")
        xml.append(f"    <lastmod>{item['lastmod']}</lastmod>")
        xml.append("    <changefreq>weekly</changefreq>")
        xml.append("    <priority>0.8</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")

    return "\n".join(xml)
