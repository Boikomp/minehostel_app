from datetime import datetime
from enum import Enum

from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import (DateField, IntegerField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sefj;4is4b4;j4;4h;oishtho4;otih4;thi'
db = SQLAlchemy(app)


class StatusEnum(Enum):
    CREATED = 'created'
    CANCELED = 'canceled'
    COMPLETED = 'completed'


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    guests_count = db.Column(db.Integer, nullable=False)
    checkin_date = db.Column(db.Date, index=True, nullable=False)
    checkout_date = db.Column(db.Date, index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    status = db.Column(db.Enum(StatusEnum),
                       default=StatusEnum.CREATED)
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    @property
    def days_count(self):
        return (self.checkout_date - self.checkin_date).days

    def __repr__(self):
        return (f'Бронирование {self.id}: {self.name}, '
                f'{self.checkin_date}, ночей - {self.days_count}, '
                f'статус - {self.status}')


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)


@app.route('/order-create', methods=['GET', 'POST'])
def order_create():
    form = OrderForm()
    name = form.name.data
    checkin_date = form.checkin_date.data
    checkout_date = form.checkout_date.data

    if Order.query.filter(and_(
        Order.name == name,
        Order.checkin_date == checkin_date,
        Order.checkout_date == checkout_date,
    )).first() is not None:
        flash('Заказ на эти даты для этого клиента уже существует.')
        return render_template('order_create.html', form=form)

    if form.validate_on_submit():
        order = Order(
            name=form.name.data,
            guests_count=form.guests_count.data,
            checkin_date=form.checkin_date.data,
            checkout_date=form.checkout_date.data,
            price=form.price.data,
            comment=form.comment.data,
        )

        db.session.add(order)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('order_create.html', form=form)


if __name__ == '__main__':
    app.run()
