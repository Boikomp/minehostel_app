from flask import flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError

from . import app, db
from .forms import OrderForm, OrderUpdateForm, ServiceForm, ServiceUpdateForm
from .models import Order, Service, StatusEnum


@app.route('/')
def index():
    orders = (Order.query
              .filter_by(status=StatusEnum.CREATED)
              .order_by(Order.checkin_date)
              .all())
    return render_template('index.html', orders=orders)


@app.route('/orders-all')
def orders_all():
    orders = Order.query.order_by(Order.checkin_date).all()
    return render_template('orders_all.html', orders=orders)


@app.route('/order/<int:id>')
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('order_detail.html', order=order)


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
            return redirect(url_for('order_detail', id=order.id))
        except IntegrityError:
            db.session.rollback()
            flash('Заказ с таким именем и датами уже существует.',
                  'order-error')

    return render_template('order_create.html', form=form)


@app.route('/order/<int:id>/update', methods=['GET', 'POST'])
def order_update(id):
    order = Order.query.get_or_404(id)
    form = OrderUpdateForm(obj=order)

    if form.validate_on_submit():
        try:
            form.populate_obj(order)
            db.session.commit()
            flash('Заказ успешно обновлен!', 'order-success')
            return redirect(url_for('order_detail', id=order.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка обновления: {str(e)}', 'order-error')

    return render_template('order_update.html', form=form, order_id=id)


@app.route('/service-create', methods=['GET', 'POST'])
def service_create():
    form = ServiceForm()

    if form.validate_on_submit():
        service = Service(
            title=form.title.data,
            price=form.price.data,
        )
        try:
            db.session.add(service)
            db.session.commit()
            flash('Услуга успешно создана!', 'service-success')
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash('Услуга с таким названием уже существует.',
                  'service-error')

    return render_template('service_create.html', form=form)


@app.route('/services-all')
def services_all():
    services = Service.query.all()
    return render_template('services_all.html', services=services)


@app.route('/service/<int:id>', methods=['GET', 'POST'])
def service_update(id):
    service = Service.query.get_or_404(id)
    form = ServiceUpdateForm(obj=service)

    if form.validate_on_submit():
        try:
            form.populate_obj(service)
            db.session.commit()
            flash('Услуга успешно обновлена!', 'service-success')
            return redirect(url_for('services_all'))
        except IntegrityError:
            db.session.rollback()
            flash('Услуга с таким названием уже существует.', 'service-error')

    return render_template('service_update.html', form=form, service_id=id)
