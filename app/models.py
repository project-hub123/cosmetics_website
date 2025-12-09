from datetime import datetime
from flask_login import UserMixin
from app import db


# ============================================================
#                      РОЛИ ПОЛЬЗОВАТЕЛЕЙ
# ============================================================
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    # роли: "user", "employee", "admin"
    role = db.Column(db.String(50), nullable=False, default="user")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # отношения
    articles = db.relationship("Article", backref="author", lazy=True)
    news = db.relationship("News", backref="author", lazy=True)
    messages = db.relationship("Message", backref="sender", lazy=True)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# ============================================================
#                       КАТЕГОРИИ СТАТЕЙ
# ============================================================
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), unique=True, nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)

    articles = db.relationship("Article", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


# ============================================================
#                           СТАТЬИ
# ============================================================
class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)

    image = db.Column(db.String(250), nullable=True)  # путь к картинке
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # связи
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<Article {self.title}>"


# ============================================================
#                          НОВОСТИ
# ============================================================
class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(250), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<News {self.title}>"


# ============================================================
#                     СООБЩЕНИЯ / ОБРАТНАЯ СВЯЗЬ
# ============================================================
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    sender_name = db.Column(db.String(150), nullable=False)
    sender_email = db.Column(db.String(150), nullable=False)

    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # связь с пользователем (если он авторизован)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<Message от {self.sender_name}>"
