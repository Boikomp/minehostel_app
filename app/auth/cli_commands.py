from werkzeug.security import generate_password_hash

from .. import app, db
from .models import User


@app.cli.command("create_user")
def create_user():
    """Функция создания юзера"""
    email = input("Введите email пользователя: ")
    password = input("Введите пароль пользователя: ")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print("Пользователь с таким email уже существует")
        return

    new_user = User(email=email,
                    password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    print("Пользователь успешно создан")
