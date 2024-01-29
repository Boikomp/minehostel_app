from datetime import datetime
from enum import Enum

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)


@app.route('/order-create')
def order_create():
    return render_template('order_create.html')


if __name__ == '__main__':
    app.run()
