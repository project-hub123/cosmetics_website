from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
    FileField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models import Category


# ============================================================
#                     ФОРМА РЕГИСТРАЦИИ
# ============================================================
class RegisterForm(FlaskForm):
    username = StringField(
        "Логин",
        validators=[DataRequired(), Length(min=3, max=50)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm = PasswordField(
        "Подтвердите пароль",
        validators=[DataRequired(), EqualTo("password", message="Пароли должны совпадать")]
    )

    submit = SubmitField("Зарегистрироваться")


# ============================================================
#                     ФОРМА ВХОДА
# ============================================================
class LoginForm(FlaskForm):
    username = StringField(
        "Логин",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired()]
    )
    submit = SubmitField("Войти")


# ============================================================
#         ФОРМА СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ (АДМИН/СОТРУДНИК)
# ============================================================
class AdminCreateUserForm(FlaskForm):
    username = StringField(
        "Логин",
        validators=[DataRequired(), Length(min=3, max=50)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(),
            EqualTo("password", message="Пароли должны совпадать")
        ]
    )

    role = SelectField(
        "Роль",
        choices=[
            ("user", "Пользователь"),
            ("employee", "Сотрудник"),
            ("admin", "Администратор")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Создать пользователя")


# ============================================================
#                     ФОРМА СТАТЬИ
# ============================================================
class ArticleForm(FlaskForm):
    title = StringField(
        "Название статьи",
        validators=[DataRequired(), Length(min=3, max=250)]
    )

    content = TextAreaField(
        "Текст статьи",
        validators=[DataRequired(), Length(min=20)]
    )

    category = SelectField(
        "Категория",
        coerce=int,
        validators=[DataRequired()]
    )

    image = FileField("Изображение (необязательно)")

    submit = SubmitField("Сохранить")

    def set_categories(self):
        self.category.choices = [
            (c.id, c.name) for c in Category.query.order_by(Category.name).all()
        ]


# ============================================================
#                     ФОРМА НОВОСТЕЙ
# ============================================================
class NewsForm(FlaskForm):
    title = StringField(
        "Заголовок новости",
        validators=[DataRequired(), Length(min=3, max=250)]
    )

    content = TextAreaField(
        "Текст новости",
        validators=[DataRequired(), Length(min=20)]
    )

    image = FileField("Изображение (необязательно)")

    submit = SubmitField("Опубликовать")


# ============================================================
#                 ФОРМА ОБРАТНОЙ СВЯЗИ
# ============================================================
class FeedbackForm(FlaskForm):
    sender_name = StringField(
        "Ваше имя",
        validators=[DataRequired(), Length(min=2, max=150)]
    )

    sender_email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    content = TextAreaField(
        "Сообщение",
        validators=[DataRequired(), Length(min=10)]
    )

    submit = SubmitField("Отправить")


# ============================================================
#                       ФОРМА ПОИСКА
# ============================================================
class SearchForm(FlaskForm):
    query = StringField(
        "Поиск",
        validators=[DataRequired(), Length(min=2)]
    )

    submit = SubmitField("Найти")
