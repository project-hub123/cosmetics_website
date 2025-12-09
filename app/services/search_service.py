from app.models import Article, News
from sqlalchemy import or_


def search_content(query: str):
    """
    Поиск по статьям и новостям.
    Возвращает объединённый список результатов.
    """

    if not query or not query.strip():
        return []

    q = f"%{query.strip()}%"

    # Поиск по статьям
    articles = Article.query.filter(
        or_(
            Article.title.ilike(q),
            Article.content.ilike(q)
        )
    ).order_by(Article.created_at.desc()).all()

    # Поиск по новостям
    news_items = News.query.filter(
        or_(
            News.title.ilike(q),
            News.content.ilike(q)
        )
    ).order_by(News.created_at.desc()).all()

    # Объединяем результаты в единый формат
    results = []

    for a in articles:
        results.append({
            "type": "article",
            "id": a.id,
            "title": a.title,
            "content": a.content[:200] + "...",
            "created_at": a.created_at,
        })

    for n in news_items:
        results.append({
            "type": "news",
            "id": n.id,
            "title": n.title,
            "content": n.content[:200] + "...",
            "created_at": n.created_at,
        })

    # Сортировка по дате — от новых к старым
    results.sort(key=lambda x: x["created_at"], reverse=True)

    return results
