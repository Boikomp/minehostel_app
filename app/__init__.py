from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .reservations import reservations_bp
from .auth import auth_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(reservations_bp, url_prefix='/')
