from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length, NumberRange

from .models import StatusEnum

STATUS_CHOICES = [(status.name, status.value) for status in StatusEnum]


class ServiceForm(FlaskForm):
    title = StringField(
        'Название услуги',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 100)]
    )
    price = IntegerField(
        'Стоимость одной услуги',
        validators=[DataRequired(message='Обязательное поле'),
                    NumberRange(min=0)]
    )
    submit = SubmitField('Добавить')


class ServiceUpdateForm(ServiceForm):
    submit = SubmitField('Сохранить изменения')


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


class OrderUpdateForm(OrderForm):
    status = SelectField(
        'Статус', choices=STATUS_CHOICES,
        validators=[DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Сохранить изменения')
