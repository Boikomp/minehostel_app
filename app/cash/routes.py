from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_paginate import get_page_parameter
from sqlalchemy import desc

from .. import db, logger
from ..constants import ITEMS_PER_PAGE
from . import cash_bp
from .forms import TransactionForm
from .models import CashType, Transaction


@login_required
@cash_bp.route('/transactions-list')
def transactions_list():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    transactions = (Transaction.query
                    .order_by(desc(Transaction.date))
                    .paginate(page, ITEMS_PER_PAGE, error_out=False))
    cash_balance = Transaction.cash_balance(CashType.MAIN_CASH)
    return render_template('cash/transactions_list.html',
                           transactions=transactions,
                           cash_balance=cash_balance)


@login_required
@cash_bp.route('/transaction-create', methods=['GET', 'POST'])
def transaction_create():
    form = TransactionForm()

    if form.validate_on_submit():
        try:
            transaction = Transaction(
                date=form.date.data,
                debit=form.debit.data,
                credit=form.credit.data,
                type=form.type.data,
                cash_type=form.cash_type.data,
                comment=form.comment.data,
            )
            db.session.add(transaction)
            db.session.commit()
            logger.info(f'Юзер {current_user.email} создал транзакцию '
                        f'с данными:\n{form.data}')
            flash('Транзакция успешно создана!', 'cash-success')
            return redirect(url_for('cash.transactions_list'))
        except ValueError as e:
            db.session.rollback()
            logger.error(f'Ошибка при создании транзакции:\n'
                         f'{str(e)}')
            flash('Ошибка при создании транзакции', 'cash-error')

    return render_template('cash/transaction_create.html', form=form)


@login_required
@cash_bp.route('/transaction-update/<int:id>', methods=['GET', 'POST'])
def transaction_update(id):
    transaction = Transaction.query.get_or_404(id)
    form = TransactionForm(obj=transaction)

    if form.validate_on_submit():
        try:
            form.populate_obj(transaction)
            db.session.commit()
            logger.info(f'Юзер {current_user.email} обновил транзакцию {id=} '
                        f'данными:\n{form.data}')
            flash('Транзакция успешно обновлена!', 'cash-success')
            return redirect(url_for('cash.transactions_list', id=id))
        except ValueError as e:
            db.session.rollback()
            logger.error(f'Ошибка при обновлении транзакции {id=}:\n'
                         f'{str(e)}')
            flash(f'Ошибка при обновлении транзакции: {str(e)}', 'cash-error')

    return render_template('cash/transaction_update.html',
                           form=form, transaction_id=id)


@login_required
@cash_bp.route('/transaction-delete/<int:id>')
def transaction_delete(id):
    transaction = Transaction.query.get_or_404(id)

    try:
        db.session.delete(transaction)
        db.session.commit()
        logger.info(f'Юзер {current_user.email} удалил транзакцию {id=}')
        flash('Транзакция успешно удалена!', 'cash-success')
    except Exception as e:
        db.session.rollback()
        logger.error(f'Ошибка при удалении транзакции {id=}: {str(e)}')
        flash('Ошибка при удалении транзакции', 'cash-error')

    return redirect(url_for('cash.transactions_list'))
