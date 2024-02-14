from datetime import datetime
from enum import StrEnum

from sqlalchemy.orm import validates

from .. import db


class StatusEnum(StrEnum):
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
    guides_count = db.Column(db.Integer)
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

    services = db.relationship('OrderService', back_populates='order',
                               cascade='all, delete-orphan')

    @property
    def days_count(self):
        return (self.checkout_date - self.checkin_date).days

    @property
    def total_price(self):
        accommodation_price = self.price * self.days_count * self.guests_count
        services_price = sum(
            order_service.service.price * order_service.quantity
            for order_service in self.services
        )
        total_price = accommodation_price + services_price
        return total_price

    @validates('price', 'guests_count', 'guides_count')
    def validate_non_negative(self, key, value):
        if value < 0:
            raise ValueError(f'{key} должно быть неотрицательным')
        return value

    @validates('checkout_date')
    def validate_checkout_date(self, key, value):
        if value < self.checkin_date:
            raise ValueError("Дата выезда не может быть раньше даты заезда")
        return value

    def __repr__(self):
        return (f'Бронирование {self.id}: {self.name}, '
                f'{self.checkin_date}, ночей - {self.days_count}, '
                f'статус - {self.status}')


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)

    orders = db.relationship('OrderService',
                             back_populates='service',
                             lazy='dynamic')

    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Стоимость должна быть неотрицательной")
        return price

    def __repr__(self):
        return (f'Услуга {self.title} - {self.price} сом')


class OrderService(db.Model):
    __tablename__ = 'order_services'
    __table_args__ = (
        db.UniqueConstraint('order_id', 'service_id',
                            name='unique_orderservice_constraint'),
    )

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
                         db.ForeignKey('orders.id'),
                         nullable=False)
    service_id = db.Column(db.Integer,
                           db.ForeignKey('services.id'),
                           nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='services',
                            single_parent=True)
    service = db.relationship('Service', back_populates='orders',
                              single_parent=True)

    def __repr__(self):
        return (f'Услуга {self.service_id} в заказе {self.order_id}, '
                f'количество - {self.quantity}')
