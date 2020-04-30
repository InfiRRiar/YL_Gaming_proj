from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти в профиль')


class RegistrationForm(FlaskForm):
    username = StringField('Логин*', validators=[DataRequired()])
    vk_id = StringField('VK id')  # добавить проверку
    password = PasswordField('Пароль*', validators=[DataRequired()])  # добавить проверку длины пароля
    submit = SubmitField('Регистрация')


class CreateNews(FlaskForm):
    title = StringField("Заголовок:", validators=[DataRequired()])
    content = StringField("Содержание новости:", validators=[DataRequired()])
    author = StringField("Автор:", validators=[DataRequired()])
    submit = SubmitField('Опубликовать')


class CreateProject(FlaskForm):
    title = StringField("Название игры:", validators=[DataRequired()])
    content = StringField("Краткое описание (max: 200 символов):", validators=[DataRequired()])
    download_link = StringField("Ссылка на скачивание:", validators=[DataRequired()])
    submit = SubmitField('Опубликовать')
