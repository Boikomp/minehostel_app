from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField(
        'Электронная почта',
        validators=[DataRequired(message='Обязательное поле')]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Войти')
