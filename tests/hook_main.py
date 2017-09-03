import dredd_hooks as hooks

import sys
import os.path as path
import requests
from flask import Flask

# DO NOT REMOVE THIS. This adds the project root for successful imports. Imports from the project directory should be
# placed only below this
sys.path.insert(1, path.abspath(path.join(__file__, "../..")))

# from flask_migrate import Migrate, stamp
from app.models import db

from app.factories.user import UserFactory
from app.factories.news import NewsFactory
from app.factories.news_comment import NewsCommentFactory


stash = {}
api_username = "superadmin"
api_password = "password"
api_uri = "http://localhost:5000/auth/session"


def obtain_token():
    data = {
        "username": api_username,
        "password": api_password
    }
    url = api_uri
    response = requests.post(url, json=data)
    response.raise_for_status()
    parsed_body = response.json()
    token = parsed_body["access_token"]
    return token


def create_super_admin(name, password):
    user = UserFactory(name=name, password=password)
    db.session.add(user)
    db.session.commit()
    return user


@hooks.before_all
def before_all(transaction):
    app = Flask(__name__)
    app.config.from_object('config.TestingConfig')
    db.init_app(app)
    # Migrate(app, db)
    stash['app'] = app
    stash['db'] = db


@hooks.before_each
def before_each(transaction):
    with stash['app'].app_context():
        db.engine.execute("drop database geokrety_unittest")
        db.engine.execute("create database geokrety_unittest")
        db.engine.execute("use geokrety_unittest")
        db.create_all()
        # stamp()
        create_super_admin(api_username, api_password)
        # populate_without_print()

    if 'token' not in stash:
        stash['token'] = obtain_token()

    transaction['request']['headers']['Authorization'] = "JWT " + stash['token']


@hooks.after_each
def after_each(transaction):
    with stash['app'].app_context():
        db.session.remove()


# ------------------------- Authentication -------------------------
@hooks.before("Authentication > JWT Authentication > Authenticate and generate token")
def authentication_get_token(transaction):
    """
    POST /auth/session
    :param transaction:
    :return:
    """
    transaction['request']['headers']['Authorization'] = ""
    with stash['app'].app_context():
        user = UserFactory(name="your_username", password="your_password")
        db.session.add(user)
        db.session.commit()


# ------------------------- Users -------------------------
@hooks.before("Users > Users Collection > List All Users")
def user_get_list(transaction):
    """
    GET /v1/users
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory(name="your_username", password="your_password")
        db.session.add(user)
        db.session.commit()


@hooks.before("Users > News Author > Get News Author")
def user_get_news_author(transaction):
    """
    GET /v1/news/1/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("Users > NewsComment Author > Get NewsComment Author")
def user_get_newscomment_author(transaction):
    """
    GET /v1/news-comments/1/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        news = NewsFactory()
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()


# ------------------------- News -------------------------
@hooks.before("News > News Collection > List All News")
def news_get_list(transaction):
    """
    GET /v1/news
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("News > News Collection > Create News")
def news_post(transaction):
    """
    POST /v1/news
    :param transaction:
    :return:
    """
    pass


@hooks.before("News > News Details > News Details")
def news_get_details(transaction):
    """
    GET /v1/news/1
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("News > News Details > Update News")
def news_patch_details(transaction):
    """
    PATCH /v1/news/1
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("News > News Details > Delete News")
def news_delete_details(transaction):
    """
    DELETE /v1/news/1
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("News > Relationship Author > List News published by User")
def news_published_by_author_get_list(transaction):
    """
    GET /v1/users/1/news
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("News > Relationship Author > Get Relationship")
def news_author_get_list(transaction):
    """
    GET /v1/news/1/relationship/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("News > Relationship Author > Create Relationship")
def news_author_post_relationship(transaction):
    """
    POST /v1/news/1/relationship/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("News > Relationship Author > Update Relationship")
def news_author_patch_relationship(transaction):
    """
    PATCH /v1/news/1/relationship/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory(name="anotheruser")
        db.session.add(user)
        news = NewsFactory()
        db.session.add(news)
        db.session.commit()


@hooks.before("News > Relationship Author > Delete Relationship")
def news_author_delete_relationship(transaction):
    """
    DELETE /v1/news/1/relationship/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        news = NewsFactory()
        db.session.add(news)
        db.session.commit()


# ------------------------- News Comments -------------------------
@hooks.before("NewsComments > NewsComments Collection > List All NewsComments")
def newscomment_get_list(transaction):
    """
    GET /v1/news-comments
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()


@hooks.before("NewsComments > NewsComments Collection > Create NewsComments")
def newscomment_post(transaction):
    """
    POST /v1/news-comments
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        db.session.commit()


@hooks.before("NewsComments > NewsComments Details > NewsComments Details")
def newscomment_get_detail(transaction):
    """
    GET /v1/news-comments/1
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()


@hooks.before("NewsComments > NewsComments Details > Update NewsComments")
def newscomment_patch_detail(transaction):
    """
    PATCH /v1/news-comments/1
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()


@hooks.before("NewsComments > NewsComments Details > Delete NewsComments")
def newscomment_delete_detail(transaction):
    """
    DELETE /v1/news-comments/1
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()


@hooks.before("NewsComments > Relationship Author > Get Relationship")
def newscomment_author_get_relationship(transaction):
    """
    GET /v1/news-comments/1/relationship/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory()
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()


@hooks.before("NewsComments > Relationship Author > Create Relationship")
def newscomment_author_post_relationship(transaction):
    """
    POST /v1/news-comments/1/relationship/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory(name="anotheruser")
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()


@hooks.before("NewsComments > Relationship Author > Update Relationship")
def newscomment_author_patch_relationship(transaction):
    """
    PATCH /v1/news-comments/1/relationship/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory(name="anotheruser")
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()


@hooks.before("NewsComments > Relationship Author > Delete Relationship")
def newscomment_author_delete_relationship(transaction):
    """
    DELETE /v1/news-comments/1/relationship/author
    :param transaction:
    :return:
    """
    with stash['app'].app_context():
        user = UserFactory(name="anotheruser")
        db.session.add(user)
        news = NewsFactory(author=user)
        db.session.add(news)
        newscomment = NewsCommentFactory()
        db.session.add(newscomment)
        db.session.commit()
