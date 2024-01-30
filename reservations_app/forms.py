from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Length


class OrderForm(FlaskForm):
    name = StringField(
        'Имя гостя',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 100)]
    )
    guests_count = IntegerField(
        'Количество гостей',
        validators=[DataRequired(message='Обязательное поле')]
    )
    checkin_date = DateField(
        'Дата заезда (ГГГГ-ММ-ДД)',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Обязательное поле')]
    )
    checkout_date = DateField(
        'Дата выезда (ГГГГ-ММ-ДД)',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Обязательное поле')]
    )
    price = IntegerField(
        'Стоимость одной ночи',
        validators=[DataRequired(message='Обязательное поле')]
    )
    comment = TextAreaField('Комментарий')
    submit = SubmitField('Создать')
