from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, SelectField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, NumberRange, Optional

from .models import CashType, TransactionType

TYPE_CHOICES = [(type.name, type.value) for type in TransactionType]
CASH_CHOICES = [(type.name, type.value) for type in CashType]


class TransactionForm(FlaskForm):
    date = DateField(
        'Дата транзакции (ГГГГ-ММ-ДД)',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Обязательное поле')]
    )
    debit = IntegerField(
        'Приход',
        validators=[
            Optional(),
            NumberRange(
                min=1,
                message='Введите положительное число'
            )
        ]
    )
    credit = IntegerField(
        'Расход',
        validators=[
            Optional(),
            NumberRange(
                min=1,
                message='Введите положительное число'
            )
        ]
    )
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

    def validate(self):
        if not super().validate():
            return False

        if self.debit.data is None and self.credit.data is None:
            self.debit.errors.append(
                'Поле "Приход" или "Расход" должно быть заполнено'
            )
            self.credit.errors.append(
                'Поле "Приход" или "Расход" должно быть заполнено'
            )
            return False
        elif self.debit.data is not None and self.credit.data is not None:
            self.debit.errors.append(
                'Заполните только одно из полей "Приход" или "Расход"'
            )
            self.credit.errors.append(
                'Заполните только одно из полей "Приход" или "Расход"'
            )
            return False

        return True
