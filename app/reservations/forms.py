from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

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
        validators=[
            InputRequired('Обязательное поле'),
            NumberRange(
                min=0,
                message='Введите неотрицательное число'
            )]
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
        validators=[
            InputRequired(message='Обязательное поле'),
            NumberRange(
                min=0,
                message='Введите неотрицательное число'
            )]
    )
    guides_count = IntegerField(
        'Количество гидов',
        validators=[
            InputRequired(message='Обязательное поле'),
            NumberRange(
                min=0,
                message='Введите неотрицательное число'
            )
            ]
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
        validators=[
            InputRequired('Обязательное поле'),
            NumberRange(
                min=0,
                message='Введите неотрицательное число'
            )
        ]
    )
    comment = TextAreaField('Комментарий')
    submit = SubmitField('Создать')


class OrderUpdateForm(OrderForm):
    status = SelectField(
        'Статус', choices=STATUS_CHOICES,
        validators=[DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Сохранить изменения')


class OrderServiceForm(FlaskForm):
    service = SelectField('Дополнительная услуга', validators=[DataRequired()])
    quantity = IntegerField(
        'Количество',
        validators=[
            InputRequired('Обязательное поле'),
            NumberRange(
                min=0,
                message='Введите неотрицательное число'
            )
        ]
    )
    submit = SubmitField('Сохранить')


class SalaryDateForm(FlaskForm):
    start_date = DateField(
        'Начальная дата (ГГГГ-ММ-ДД)',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Обязательное поле')]
    )
    finish_date = DateField(
        'Конечная дата (ГГГГ-ММ-ДД)',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Рассчитать')

    def validate(self):
        if not super().validate():
            return False
        if self.start_date.data >= self.finish_date.data:
            self.start_date.errors.append(
                'Начальная дата должна быть раньше конечной даты'
            )
            return False
        return True
