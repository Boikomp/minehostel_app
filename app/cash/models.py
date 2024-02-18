from enum import StrEnum

from .. import db


class TransactionType(StrEnum):
    ACCOMMODATION = 'Проживание'
    EXTRA_SERVICES = 'Допуслуги'
    BAR_PAYMENT = 'Из бара'
    SALARY = 'Зарплата'
    OPERATING_COSTS = 'Операционные расходы'
    WITHDRAWAL = 'Изъятие средств'
    ELSE = 'Другое'


class CashType(StrEnum):
    MAIN_CASH = 'Основная касса'
    BAR_CASH = 'Барная касса'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    debit = db.Column(db.Integer, default=0)
    credit = db.Column(db.Integer, default=0)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    cash_type = db.Column(db.Enum(CashType), nullable=False)
    comment = db.Column(db.Text)

    @classmethod
    def cash_balance(cls, cash_type):
        transactions = cls.query.filter_by(cash_type=cash_type).all()
        total_credit = sum(transaction.credit for transaction in transactions)
        total_debit = sum(transaction.debit for transaction in transactions)
        return total_debit - total_credit

    def __repr__(self):
        amount = 'дебит' if self.credit != 0 else 'кредит'
        return (
            f'Транзакция {self.id} ({self.date}), '
            f'{amount}={self.debit or self.credit}, '
            f'тип - {self.type}, тип кассы - {self.cash_type}'
        )
