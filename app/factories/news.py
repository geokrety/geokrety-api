import factory

from app.models.news import db, News
import app.factories.common as common


class NewsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = News
        sqlalchemy_session = db.session

    title = 'News title'
    content = 'News content'
    username = 'news_author'
    author_id = None
    comments_count = 0
    last_comment_date_time = common.date_time_0_
    created_on_date_time = common.date_time_
    czas_postu = common.date_time_0_