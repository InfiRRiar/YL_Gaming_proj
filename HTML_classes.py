from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти в профиль')


class RegistrationForm(FlaskForm):
    username = StringField('Логин*', validators=[DataRequired()])
    discord_tag = StringField('Discord tag')  # добавить проверку
    password = PasswordField('Пароль*', validators=[DataRequired()])  # добавить проверку длины пароля
    submit = SubmitField('Регистрация')
