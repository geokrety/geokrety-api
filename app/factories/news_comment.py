import factory

from app.models.news_comment import db, NewsComment
import app.factories.common as common


class NewsCommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = NewsComment
        sqlalchemy_session = db.session

    comment = 'News comment text'
    news_id = 1
    author_id = 1
    icon = 0
    created_on_date = common.date_
