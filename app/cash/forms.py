from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, Optional

from .models import CashType, TransactionType

TYPE_CHOICES = [(type.name, type.value) for type in TransactionType]
CASH_CHOICES = [(type.name, type.value) for type in CashType]


class TransactionForm(FlaskForm):
    date = DateField(
        'Дата транзакции (ГГГГ-ММ-ДД)',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Обязательное поле')]
    )
    debit = IntegerField('Приход', validators=[Optional()])
    credit = IntegerField('Расход', validators=[Optional()])
    type = SelectField(
        'Тип транзакции', choices=TYPE_CHOICES,
        validators=[DataRequired(message='Обязательное поле')]
    )
    cash_type = SelectField(
        'Тип кассы', choices=CASH_CHOICES,
        validators=[DataRequired(message='Обязательное поле')]
    )
    comment = TextAreaField('Комментарий')
    submit = SubmitField('Сохранить')
