# MineHostel_app

Проект учета бронирований и кассы хостела.

## Описание

Приложение для учета бронирований, допуслуг, остатка в кассе хостела MineHostel Jyrgalan, вычисление премиальной части зарплаты администратора хостела. Неавторизованному пользователю доступна только "главная страница" проекта. Регистрация пользователей не доступна. Только создание пользователя через пользовательскую команду.

#### Бронирования

На "главной странице" выводятся только предстоящие бронирования. На странице "все бронирования" выводятся все бронирования. На странице деталей конкретного бронирования можно посмотреть подробную информацию о бронировании, о всех допуслугах включенных в бронирование, конечную стоимость бронирования.

Ключевые возможности:
- добавление нового бронирования
- редактирование бронирования, в том числе редактирование статуса бронирования (создан, отменен, завершен)
- добавление к бронированию допуслуг, количество допуслуг в бронировании можно редактировать (при установке количества "0" - допуслуга в бронировании удаляется)

#### Услуги

На странице "услуги" выводятся все активные допуслуги. Неактивные можно посмотреть в "архиве услуг".

Ключевые возможности:
- добавление новой допуслуги
- редактирование допуслуги
- удаление допуслуги (при нажатии "удалить" допуслуга перемещается в архив, ее можно восстановить нажав "восстановить" в "архиве услуг")

#### Касса

На странице "касса" отображаются все транзакции и остаток в кассе на текущий момент.

Ключевые возможности:
- добавление новой транзакции
- редактирование транзакции
- удаление транзакции

#### ЗП

На странице "зп" можно рассчитать премиальную часть зарплаты администратора в зависимости от отработанных дат. При рассчете выводится список бронирований за эти даты и премиальная часть от каждого бронирования.

Премия вычисляется следующим образом:
- за каждую занятую койку (и клиентом и гидом) в бронировании за каждую ночь выплачивается 200 денег
- в случае если в бронирование вкючена баня, также выплачивается 200 денег за каждый час

## Технологии и библиотеки

- Python3.11
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Paginate
- Flask-WTF

## Пример заполнения конфигурационного .env файла

```
FLASK_APP=app
FLASK_ENV=<development/production>
DATABASE_URI=<sqlite:///db.sqlite3>
SECRET_KEY=<your_secret_key>
```

## Запуск проекта

Клонировать репозиторий:
```bash
git clone git@github.com:Boikomp/minehostel_app.git
```

Cоздать и активировать виртуальное окружение:
```bash
-для Windows
python -m venv venv
-для Linux, MacOs:
python3 -m venv venv
```
```bash
-для Windows
venv\Scripts\activate.bat
-для Linux, MacOs:
source venv/bin/activate
```

Обновить pip:
```bash
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```

Создать и заполнить файл **.env**:
```bash
touch .env
```

Команда создания пользователя:
```bash
flask create_user
```

Запустить проект:
```bash
flask run
```

Локальный сайт доступен по ссылке http://127.0.0.1:5000/

## Автор
[Бойко Максим](https://github.com/Boikomp)
tg @BoikoMP