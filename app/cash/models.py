from enum import StrEnum

from sqlalchemy.orm import validates

from .. import db


class TransactionType(StrEnum):
    ACCOMMODATION = 'Проживание'
    EXTRA_SERVICES = 'Допуслуги'
    BAR_PAYMENT = 'Из бара'
    SALARY = 'Зарплата'
    OPERATING_COSTS = 'Операционные расходы'
    WITHDRAWAL = 'Изъятие средств'
    ELSE = 'Другое'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    debit = db.Column(db.Integer)
    credit = db.Column(db.Integer)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    comment = db.Column(db.Text)

    @classmethod
    def cash_balance(cls):
        transactions = cls.query.all()
        total_credit = sum(
            transaction.credit
            for transaction in transactions
            if transaction.credit is not None
        )
        total_debit = sum(
            transaction.debit
            for transaction in transactions
            if transaction.debit is not None
        )
        return total_debit - total_credit

    @validates('debit', 'credit')
    def validate_positive(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f'{key} должно быть положительным')
        return value

    def __repr__(self):
        amount = 'приход' if self.credit != 0 else 'расход'
        return (
            f'Транзакция {self.id} ({self.date}), '
            f'{amount}={self.debit or self.credit}, '
            f'тип - {self.type}'
        )
