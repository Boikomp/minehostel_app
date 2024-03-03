from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_paginate import get_page_parameter
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from .. import db, logger
from ..constants import ITEMS_PER_PAGE
from . import reservations_bp
from .forms import (OrderForm, OrderServiceForm, OrderUpdateForm,
                    SalaryDateForm, ServiceForm, ServiceUpdateForm)
from .models import Order, OrderService, Service, StatusEnum


@reservations_bp.route('/')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    orders = (Order.query
              .filter_by(status=StatusEnum.CREATED)
              .order_by(Order.checkin_date)
              .paginate(page, ITEMS_PER_PAGE, error_out=False))
    return render_template('reservations/index.html', orders=orders)


@reservations_bp.route('/orders-all')
@login_required
def orders_all():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    orders = (Order.query
              .order_by(desc(Order.checkout_date))
              .paginate(page, ITEMS_PER_PAGE, error_out=False))
    return render_template('reservations/orders_all.html', orders=orders)


@reservations_bp.route('/order/<int:id>', methods=['GET', 'POST'])
@login_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    form = OrderServiceForm()
    services = Service.query.filter_by(active=True).order_by('title').all()
    form.service.choices = [
        (str(service.id), f'{service.title} - {service.price} сом')
        for service in services
    ]

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                service_id = int(form.service.data)
                quantity = form.quantity.data

                order_service = OrderService.query.filter_by(
                    order_id=id,
                    service_id=service_id
                ).first()

                if order_service:
                    if quantity == 0:
                        db.session.delete(order_service)
                        logger.info(
                            f'Юзер {current_user.email} удалил из заказа '
                            f'{id=} услугу {service_id=}'
                        )
                        flash('Дополнительная услуга успешно удалена',
                              'order-success')
                    else:
                        order_service.quantity = quantity
                        logger.info(
                            f'Юзер {current_user.email} обновил в заказе '
                            f'{id=} количество услуги {service_id=} - '
                            f'{quantity} шт'
                        )
                        flash('Дополнительная услуга успешно обновлена',
                              'order-success')
                else:
                    order_service = OrderService(
                        order_id=id,
                        service_id=service_id,
                        quantity=quantity,
                    )
                    db.session.add(order_service)
                    logger.info(
                        f'Юзер {current_user.email} добавил к заказу {id=} '
                        f'услугу {service_id=} в количестве {quantity} шт'
                    )
                    flash('Дополнительная услуга успешно добавлена',
                          'order-success')

                db.session.commit()

                return redirect(url_for('reservations.order_detail', id=id))
            except Exception as e:
                db.session.rollback()
                logger.error(f'Ошибка при обновлении заказа {id=}:\n'
                             f'{str(e)}')
                flash('Ошибка при обновлении заказа', 'order-error')

    return render_template('reservations/order_detail.html',
                           order=order, form=form)


@reservations_bp.route('/order-create', methods=['GET', 'POST'])
@login_required
def order_create():
    form = OrderForm()

    if form.validate_on_submit():
        try:
            order = Order(
                name=form.name.data,
                guests_count=form.guests_count.data,
                guides_count=form.guides_count.data,
                checkin_date=form.checkin_date.data,
                checkout_date=form.checkout_date.data,
                price=form.price.data,
                comment=form.comment.data,
            )
            db.session.add(order)
            db.session.commit()
            logger.info(f'Юзер {current_user.email} создал заказ с данными:\n'
                        f'{form.data}')
            flash('Заказ успешно создан!', 'order-success')
            return redirect(url_for('reservations.order_detail', id=order.id))
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f'Ошибка IntegrityError при создании заказа:\n'
                         f'{str(e)}')
            flash('Заказ с таким именем и датами уже существует.',
                  'order-error')
        except Exception as e:
            db.session.rollback()
            logger.error(f'Ошибка при создании заказа:\n'
                         f'{str(e)}')
            flash('Ошибка при создании заказа', 'order-error')

    return render_template('reservations/order_create.html', form=form)


@reservations_bp.route('/order-update/<int:id>', methods=['GET', 'POST'])
@login_required
def order_update(id):
    order = Order.query.get_or_404(id)
    form = OrderUpdateForm(obj=order)

    if form.validate_on_submit():
        try:
            form.populate_obj(order)
            db.session.commit()
            logger.info(f'Юзер {current_user.email} обновил заказ {id=} '
                        f'данными:\n{form.data}')
            flash('Заказ успешно обновлен!', 'order-success')
            return redirect(url_for('reservations.order_detail', id=order.id))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Ошибка при обновлении заказа {id=}:\n'
                         f'{str(e)}')
            flash('Ошибка при обновлении заказа', 'order-error')

    return render_template('reservations/order_update.html',
                           form=form, order_id=id)


@reservations_bp.route('/service-create', methods=['GET', 'POST'])
@login_required
def service_create():
    form = ServiceForm()

    if form.validate_on_submit():
        try:
            service = Service(
                title=form.title.data,
                price=form.price.data,
            )
            db.session.add(service)
            db.session.commit()
            logger.info(f'Юзер {current_user.email} создал услугу с данными:\n'
                        f'{form.data}')
            flash('Услуга успешно создана!', 'service-success')
            return redirect(url_for('reservations.services_list'))
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f'Ошибка при создании услуги:\n'
                         f'{str(e)}')
            flash('Услуга с таким названием уже существует',
                  'service-error')

    return render_template('reservations/service_create.html', form=form)


@reservations_bp.route('/services-list')
@login_required
def services_list():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    services = (Service.query
                .filter_by(active=True)
                .order_by('title')
                .paginate(page, ITEMS_PER_PAGE, error_out=False))
    return render_template('reservations/services_list.html',
                           services=services)


@reservations_bp.route('/services-archive')
@login_required
def services_archive():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    services = (Service.query
                .filter_by(active=False)
                .paginate(page, ITEMS_PER_PAGE, error_out=False))
    return render_template('reservations/services_archive.html',
                           services=services)


@reservations_bp.route('/service-update/<int:id>', methods=['GET', 'POST'])
@login_required
def service_update(id):
    service = Service.query.get_or_404(id)
    form = ServiceUpdateForm(obj=service)

    if form.validate_on_submit():
        try:
            form.populate_obj(service)
            db.session.commit()
            logger.info(f'Юзер {current_user.email} обновил услугу {id=} '
                        f'данными:\n{form.data}')
            flash('Услуга успешно обновлена!', 'service-success')
            return redirect(url_for('reservations.services_list'))
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f'Ошибка при обновлении услуги {id=}:\n'
                         f'{str(e)}')
            flash('Услуга с таким названием уже существует',
                  'service-error')

    return render_template('reservations/service_update.html',
                           form=form, service_id=id)


@reservations_bp.route('/service-delete/<int:id>')
@login_required
def service_delete(id):
    service = Service.query.get_or_404(id)

    try:
        service.active = False
        db.session.commit()
        logger.info(f'Юзер {current_user.email} удалил услугу {id=}')
        flash('Услуга успешно удалена!', 'service-success')
        return redirect(url_for('reservations.services_archive'))
    except Exception as e:
        db.session.rollback()
        logger.error(f'Ошибка при удалении услуги {id=}:\n'
                     f'{str(e)}')
        flash('Ошибка при удалении услуги', 'service-error')
        return redirect(url_for('reservations.services_list'))


@reservations_bp.route('/service-restore/<int:id>')
@login_required
def service_restore(id):
    service = Service.query.get_or_404(id)

    try:
        service.active = True
        db.session.commit()
        logger.info(f'Юзер {current_user.email} восстановил услугу {id=}')
        flash('Услуга успешно восстановлена!', 'service-success')
        return redirect(url_for('reservations.services_list'))
    except Exception as e:
        db.session.rollback()
        logger.error(f'Ошибка при восстановлении услуги {id=}:\n'
                     f'{str(e)}')
        flash('Ошибка восстановления', 'service-error')
        return redirect(url_for('reservations.services_archive'))


@reservations_bp.route('/admin-salary', methods=['GET', 'POST'])
@login_required
def admin_salary():
    form = SalaryDateForm()

    if form.validate_on_submit():
        from_date = form.start_date.data
        to_date = form.finish_date.data
        orders = Order.query.filter(
            Order.status != StatusEnum.CANCELED,
            Order.checkin_date >= from_date,
            Order.checkout_date <= to_date
        ).all()
        total_salary = sum(order.admin_procent for order in orders)
        return render_template('reservations/salary.html', form=form,
                               orders=orders, total_salary=total_salary,
                               from_date=from_date, to_date=to_date)

    return render_template('reservations/salary.html', form=form)
