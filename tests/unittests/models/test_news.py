from sqlalchemy.exc import OperationalError

from tests.unittests.utils import GeokretyTestCase
from app.models.news import News
from app.models import db
from app import current_app as app
from app.factories.news import NewsFactory
from app.factories.user import UserFactory
from app.factories.news_comment import NewsCommentFactory


class TestNews(GeokretyTestCase):

    def test_lookup(self):
        """
        Check create news and read back
        """

        with app.test_request_context():
            news = NewsFactory()
            db.session.add(news)
            db.session.commit()

            allnews = News.query.all()
            self.assertTrue(news in allnews)
            self.assertEqual(len(allnews), 1)

    def test_mandatory_fields(self):
        """
        Check News mandatory fields
        """

        with app.test_request_context():
            news = News()
            self._check_commit_and_raise(news, OperationalError)
            news.title = "News title"
            self._check_commit_and_raise(news, OperationalError)
            news.content = "News content"
            self._check_commit_and_not_raise(news)

    def test_author_relationship(self):
        """
        Check author relationship
        """

        with app.test_request_context():
            news = NewsFactory()
            db.session.add(news)
            db.session.commit()

            news_1 = News.query.first()
            self.assertEqual(news_1.author, None)

            user = UserFactory()
            db.session.add(user)
            news.author = user
            db.session.commit()

            news_2 = News.query.first()
            self.assertEqual(news_2.author, user)

    def test_news_comment_relationship(self):
        """
        Check news_comment relationship
        """

        with app.test_request_context():
            news = NewsFactory()
            db.session.add(news)
            db.session.commit()

            news_1 = News.query.first()
            self.assertEqual(len(news_1.news_comments), 0)

            newscomment = NewsCommentFactory()
            news.news_comments.append(newscomment)
            user = UserFactory()
            db.session.add(user)
            db.session.commit()

            news_2 = News.query.first()
            self.assertEqual(len(news_2.news_comments), 1)
            self.assertEqual(news_2.news_comments[0], newscomment)
