from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class TopicForm(FlaskForm):
    title = StringField('Название темы', validators=[DataRequired()])
    submit = SubmitField('Создать')

class PostForm(FlaskForm):
    content = TextAreaField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')