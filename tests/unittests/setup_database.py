import os
import sys

from flask import logging

from app import current_app as app
from app.models import db

_basedir = os.path.abspath(os.path.dirname(__file__))


class Setup(object):
    @staticmethod
    def create_app():
        app.config.from_object('config.TestingConfig')
        app.secret_key = 'super secret key'
        app.logger.addHandler(logging.StreamHandler(sys.stdout))
        app.logger.setLevel(logging.ERROR)
        with app.test_request_context():
            db.create_all()

        return app.test_client()

    @staticmethod
    def drop_db():
        with app.test_request_context():
            db.session.remove()
            db.drop_all()
