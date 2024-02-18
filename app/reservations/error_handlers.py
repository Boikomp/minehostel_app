from http import HTTPStatus

from flask import render_template

from .. import app, db


@app.errorhandler(404)
def page_not_found(error):
    return (render_template('errors/404.html'),
            HTTPStatus.NOT_FOUND)


@app.errorhandler(405)
def method_not_allowed(error):
    return (render_template('errors/405.html'),
            HTTPStatus.NOT_FOUND)


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return (render_template('errors/500.html'),
            HTTPStatus.INTERNAL_SERVER_ERROR)
