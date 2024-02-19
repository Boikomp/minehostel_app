from flask import Blueprint

cash_bp = Blueprint('cash', __name__)

from . import models, routes
