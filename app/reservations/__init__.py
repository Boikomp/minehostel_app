from flask import Blueprint

reservations_bp = Blueprint('reservations', __name__)

from . import error_handlers, routes
