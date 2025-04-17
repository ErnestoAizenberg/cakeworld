# forms.py
from flask_wtf import FlaskForm
from wtforms import (BooleanField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Length, Regexp


class CategoryForm(FlaskForm):
    name = StringField(
        "Название категории", validators=[DataRequired(), Length(max=100)]
    )
    description = TextAreaField("Описание категории", validators=[Length(max=500)])
    color = SelectField(
        "Цвет оформления",
        choices=[
            ("#FFFFFF", "Белый"),
            ("#000000", "Черный"),
            ("#FF0000", "Красный"),
            ("#00FF00", "Зеленый"),
            ("#0000FF", "Синий"),
        ],
    )


class ServerForm(FlaskForm):
    server_name = StringField(
        "Имя Сервера", validators=[DataRequired(), Length(max=10)]
    )
    server_description = TextAreaField("Описание Сервера", validators=[DataRequired()])
    server_background = StringField(
        "Фоновое изображение (URL)", validators=[DataRequired()]
    )
    color_scheme = StringField(
        "Цвет Оформления (HEX)",
        validators=[DataRequired()],
        render_kw={"type": "color"},
    )
    content_html = TextAreaField(
        "HTML Контент", validators=[DataRequired()], render_kw={"id": "inputField"}
    )
    submit = SubmitField("Создать Сервис")


class ChatForm(FlaskForm):
    title = StringField("Название Чата", validators=[DataRequired()])
    url_name = StringField("URL Чата", validators=[DataRequired()])
    is_private = BooleanField("Приватный Чат")
    description = TextAreaField("Описание")
    avatar_path = StringField("URL для аватара (опционально)")
    submit = SubmitField("Создать Чат")


class TopicForm(FlaskForm):
    title = StringField("Название темы", validators=[DataRequired()])
    url_name = StringField(
        "URL-имя",
        validators=[
            DataRequired(),
            Regexp(r"^[a-z0-9-]+$", message="Только латинские буквы, цифры и дефисы"),
        ],
    )
    category = SelectField("Категория", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Создать")

    def __init__(self, categories_choices=None, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        if categories_choices:
            self.category.choices = categories_choices
        else:
            self.category.choices = []


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(min=5)])
    content = TextAreaField(
        "Содержание",
        validators=[DataRequired(), Length(min=90)],
        render_kw={"id": "inputField"},
    )
    submit = SubmitField("Опубликовать")


class ReplyForm(FlaskForm):
    content = TextAreaField("Содержание", validators=[DataRequired()])
    submit = SubmitField("Добавить")


# Контейнер для форм
forms = {
    "CategoryForm": CategoryForm,
    "ServerForm": ServerForm,
    "ChatForm": ChatForm,
    "TopicForm": TopicForm,
    "PostForm": PostForm,
    "ReplyForm": ReplyForm,
}
