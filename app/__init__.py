# -*- coding: utf-8 -*-

import pprint
import os
import logging
import sys

from envparse import env
from datetime import timedelta

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from flask_login import current_user
from flask_jwt import JWT

from app.views import BlueprintsManager
from app.api.helpers.auth import AuthManager
from app.api.helpers.jwt import jwt_authenticate, jwt_identity

from app.models import db
from app.views.sentry import sentry

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.dirname(os.path.dirname(__file__)) + "/static"
template_dir = os.path.dirname(__file__) + "/templates"
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

env.read_envfile()

def create_app():
    BlueprintsManager.register(app)

    app.config.from_object(env('APP_CONFIG', default='config.ProductionConfig'))
    db.init_app(app)

    # TODO take this from config
    app.secret_key = 'super secret key'

    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

    # set up jwt
    app.config['JWT_AUTH_USERNAME_KEY'] = 'username'
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=24 * 60 * 60)
    app.config['JWT_AUTH_URL_RULE'] = '/auth/session'
    _jwt = JWT(app, jwt_authenticate, jwt_identity)

    CORS(app, resources={r"/*": {"origins": "*"}})
    AuthManager.init_login(app)


    with app.app_context():
        from app.api.bootstrap import api_v1
        # from app.api.auth import auth_routes
        app.register_blueprint(api_v1)
        # app.register_blueprint(auth_routes)


    if app.config['SERVE_STATIC']:
        app.add_url_rule('/static/<path:filename>',
                         endpoint='static',
                         view_func=app.send_static_file)

    # sentry
    if 'SENTRY_DSN' in app.config:
        sentry.init_app(app, dsn=app.config['SENTRY_DSN'])

    return app, db, _jwt

current_app, database, jwt = create_app()

# @app.before_request
# def track_user():
#     if current_user.is_authenticated():
#         current_user.last_seen = datetime.utcnow()

@app.errorhandler(500)
def internal_server_error(error):
    if current_app.config['PROPOGATE_ERROR'] is True:
        exc = JsonApiException({'pointer': ''}, str(error))
    else:
        exc = JsonApiException({'pointer': ''}, 'Unknown error')
    return make_response(json.dumps(jsonapi_errors([exc.to_dict()])), exc.status,
        {'Content-Type': 'application/vnd.api+json'})


if __name__ == '__main__':
    # Start application
    current_app.run()
