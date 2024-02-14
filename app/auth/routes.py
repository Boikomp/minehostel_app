from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from . import auth_bp
from .forms import LoginForm
from .models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('reservations.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not check_password_hash(user.password_hash,
                                                   form.password.data):
            flash('Неверная почта или пароль', 'auth-error')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('reservations.index'))

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('reservations.index'))
