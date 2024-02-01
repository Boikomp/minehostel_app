from datetime import datetime
from enum import Enum

from . import db


class StatusEnum(Enum):
    CREATED = 'Создан'
    CANCELED = 'Отменен'
    COMPLETED = 'Завершен'


class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = (
        db.UniqueConstraint('name', 'checkin_date', 'checkout_date',
                            name='unique_order_constraint'),
    )

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

    services = db.relationship('OrderService', backref='order',
                               cascade='all, delete-orphan')

    @property
    def days_count(self):
        return (self.checkout_date - self.checkin_date).days

    def __repr__(self):
        return (f'Бронирование {self.id}: {self.name}, '
                f'{self.checkin_date}, ночей - {self.days_count}, '
                f'статус - {self.status}')


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    orders = db.relationship('OrderService', backref='service',
                             cascade='all, delete-orphan')

    def __repr__(self):
        return (f'Услуга {self.title} - {self.price} сом')


class OrderService(db.Model):
    __tablename__ = 'order_services'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
                         db.ForeignKey('orders.id'),
                         nullable=False)
    service_id = db.Column(db.Integer,
                           db.ForeignKey('services.id'),
                           nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship('Order', backref='order_services',
                            cascade='all, delete-orphan')

    order = db.relationship('Order', backref='order_services',
                            cascade='all, delete-orphan')
    service = db.relationship('Service', backref='order_services',
                              cascade='all, delete-orphan')

    def __repr__(self):
        return (f'Услуга {self.service_id} в заказе {self.order_id}, '
                f'количество - {self.quantity}')
