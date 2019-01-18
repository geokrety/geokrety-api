# -*- coding: utf-8 -*-
import os

from envparse import env

env.read_envfile()

basedir = os.path.abspath(os.path.dirname(__file__))

VERSION_NAME = '2.0.0-alpha.1'

LANGUAGES = {
    'en': 'English',
}


class Config(object):
    """
    The base configuration option. Contains the defaults.
    """

    DEBUG = False

    DEVELOPMENT = False
    STAGING = False
    PRODUCTION = False
    TESTING = False

    CACHING = False
    PROFILE = False
    SQLALCHEMY_RECORD_QUERIES = False

    FLASK_ADMIN_SWATCH = 'lumen'

    VERSION = VERSION_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ERROR_404_HELP = False
    CSRF_ENABLED = True
    SERVER_NAME = env('SERVER_NAME', default=None)
    CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_DATABASE_URI = env('DATABASE_URL', default=None)
    DATABASE_QUERY_TIMEOUT = 0.1

    SENTRY_DSN = env('SENTRY_DSN', default=None)
    REDIS_URL = env('REDIS_URL', default='redis://localhost:6379/0')
    RABBITMQ_URL = env('RABBITMQ_URL', default='amqp://guest:guest@localhost:5672/?'
                       'socket_timeout=10&'
                       'connection_attempts=2')

    MINIO_ENDPOINT = env('MINIO_ENDPOINT', default='play.minio.io:9000')
    MINIO_ACCESS_KEY = env('MINIO_ACCESS_KEY', default='Q3AM3UQ867SPQQA43P2F')
    MINIO_SECRET_KEY = env('MINIO_SECRET_KEY', default='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')
    MINIO_SECURE = env('MINIO_SECURE', default=False)
    MINIO_REGION = env('MINIO_REGION', default='eu-paris-1')

    PASSWORD_HASH_SALT = env('PASSWORD_HASH_SALT', default='')
    ALLOW_GEOKRET_OWNER_TO_MODERATE_MOVES = env('ALLOW_GEOKRET_OWNER_TO_MODERATE_MOVES', default=True)
    ALLOW_GEOKRET_OWNER_TO_MODERATE_MOVE_COMMENTS = env('ALLOW_GEOKRET_OWNER_TO_MODERATE_MOVE_COMMENTS', default=True)
    ALLOW_MOVE_AUTHOR_TO_MODERATE_MOVE_COMMENTS = env('ALLOW_MOVE_AUTHOR_TO_MODERATE_MOVE_COMMENTS', default=True)

    ASYNC_OBJECTS_ENHANCEMENT = env('ASYNC_OBJECTS_ENHANCEMENT', default=True)

    # API configs
    PAGE_SIZE = 20
    SOFT_DELETE = True
    DASHERIZE_API = True
    ETAG = True

    if not SQLALCHEMY_DATABASE_URI:  # pragma: no cover
        print('`DATABASE_URL` either not exported or empty')
        exit()

    BASE_DIR = basedir
    FORCE_SSL = os.getenv('FORCE_SSL', 'no') == 'yes'

    if FORCE_SSL:  # pragma: no cover
        PREFERRED_URL_SCHEME = 'https'


class ProductionConfig(Config):
    """
    The configuration for a production environment
    """

    MINIFY_PAGE = True
    PRODUCTION = True
    CACHING = True

    # if force on


class StagingConfig(ProductionConfig):
    """
    The configuration for a staging environment
    """

    PRODUCTION = False
    STAGING = True


class DevelopmentConfig(Config):
    """
    The configuration for a development environment
    """

    DEVELOPMENT = True
    DEBUG = True
    CACHING = True

    # Test database performance
    SQLALCHEMY_RECORD_QUERIES = True

    # Test features
    ALLOW_GEOKRET_OWNER_TO_MODERATE_MOVES = True
    ALLOW_GEOKRET_OWNER_TO_MODERATE_MOVE_COMMENTS = True
    ALLOW_MOVE_AUTHOR_TO_MODERATE_MOVE_COMMENTS = True


class TestingConfig(Config):
    """
    The configuration for a test suit
    """
    TESTING = True
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG_TB_ENABLED = False
    BROKER_BACKEND = 'memory'
    SQLALCHEMY_DATABASE_URI = env('TEST_DATABASE_URL', default=None)

    # Test features
    ALLOW_GEOKRET_OWNER_TO_MODERATE_MOVES = True
    ALLOW_GEOKRET_OWNER_TO_MODERATE_MOVE_COMMENTS = True
    ALLOW_MOVE_AUTHOR_TO_MODERATE_MOVE_COMMENTS = True

    ASYNC_OBJECTS_ENHANCEMENT = False
