from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти в профиль')


class RegistrationForm(FlaskForm):
    username = StringField('Логин*', validators=[DataRequired()])
    password = PasswordField('Пароль*', validators=[DataRequired(), ])  # добавить проверку длины пароля
    submit = SubmitField('Регистрация')


class CreateNewsForm(FlaskForm):
    title = StringField("Заголовок:", validators=[DataRequired()])
    content = StringField("Содержание новости:", validators=[DataRequired()])
    author = StringField("Автор:", validators=[DataRequired()])
    submit = SubmitField('Опубликовать')


class CreateProjectForm(FlaskForm):
    title = StringField("Название игры:", validators=[DataRequired()])
    content = StringField("Краткое описание (max: 200 символов):", validators=[DataRequired()])
    download_link = StringField("Ссылка на скачивание:", validators=[DataRequired()])
    submit = SubmitField('Опубликовать')


class ChangePasswordForm(FlaskForm):
    exist_password = PasswordField("Старый пароль:", validators=[DataRequired()])
    new_password = PasswordField("Новый пароль:", validators=[DataRequired()])
    repeat_password = PasswordField("Повтор пароля:", validators=[DataRequired()])
    submit = SubmitField('Изменить пароль')


class FindErrorForm(FlaskForm):
    title = StringField("Заголовок:", validators=[DataRequired()])
    content = StringField("Текст:", validators=[DataRequired()])
    submit = SubmitField('Отправить сообщение')
