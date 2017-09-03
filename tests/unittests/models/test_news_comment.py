from sqlalchemy.exc import IntegrityError, OperationalError

from tests.unittests.utils import GeokretyTestCase
from app.models.news_comment import NewsComment
from app.models import db
from app import current_app as app
from app.factories.news import NewsFactory
from app.factories.user import UserFactory
from app.factories.news_comment import NewsCommentFactory


class TestNewsComment(GeokretyTestCase):

    def test_lookup(self):
        """
        Check create news_comment and read back
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)

            news = NewsFactory()
            db.session.add(news)

            newscomment = NewsCommentFactory(author=user, news=news)
            db.session.add(newscomment)
            db.session.commit()

            allnewscomment = NewsComment.query.all()
            self.assertTrue(newscomment in allnewscomment)
            self.assertEqual(len(allnewscomment), 1)

    def test_mandatory_fields(self):
        """
        Check news_comment mandatory fields
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)

            news = NewsFactory()
            db.session.add(news)

            newscomment = NewsComment()
            self._check_commit_and_raise(newscomment, OperationalError)
            newscomment.author = user
            self._check_commit_and_raise(newscomment, OperationalError)
            newscomment.news = news
            self._check_commit_and_not_raise(newscomment)

    def test_author_relationship(self):
        """
        Check author relationship
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)

            news = NewsFactory()
            db.session.add(news)

            newscomment = NewsCommentFactory(author=user, news=news)
            db.session.add(newscomment)
            db.session.commit()

            news_comment_1 = NewsComment.query.first()
            self.assertEqual(news_comment_1.author, user)

    def test_news_comment_relationship(self):
        """
        Check news relationship
        """

        with app.test_request_context():
            user = UserFactory()
            db.session.add(user)

            news = NewsFactory()
            db.session.add(news)

            newscomment = NewsCommentFactory(author=user, news=news)
            db.session.add(newscomment)
            db.session.commit()

            news_comment_1 = NewsComment.query.first()
            self.assertEqual(news_comment_1.news, news)
