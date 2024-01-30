from flask import flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError

from . import app, db
from .forms import OrderForm
from .models import Order


@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)


@app.route('/order-create', methods=['GET', 'POST'])
def order_create():
    form = OrderForm()

    if form.validate_on_submit():
        order = Order(
            name=form.name.data,
            guests_count=form.guests_count.data,
            checkin_date=form.checkin_date.data,
            checkout_date=form.checkout_date.data,
            price=form.price.data,
            comment=form.comment.data,
        )
        try:
            db.session.add(order)
            db.session.commit()
            flash('Заказ успешно создан!', 'order-success')
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash('Заказ с таким именем и датами уже существует.',
                  'order-error')

    return render_template('order_create.html', form=form)
