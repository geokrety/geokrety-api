from sqlalchemy.exc import OperationalError

from tests.unittests.utils import GeokretyTestCase
from app.models.news_comment import NewsComment
from app.models import db
from app import current_app as app
from app.factories.news import NewsFactory
from app.factories.user import UserFactory
from app.factories.news_comment import NewsCommentFactory


def _create_news_comment():
    """
    Create a news comment with user and news relationship
    """

    with app.test_request_context():
        user = UserFactory()
        db.session.add(user)

        news = NewsFactory()
        db.session.add(news)

        newscomment = NewsCommentFactory(author=user, news=news)
        db.session.add(newscomment)
        db.session.commit()

    return newscomment, news, user

class TestNewsComment(GeokretyTestCase):

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

    def test_lookup(self):
        """
        Check create news_comment and read back
        """

        with app.test_request_context():
            newscomment, news, user = _create_news_comment()

            allnewscomment = NewsComment.query.all()
            self.assertTrue(newscomment in allnewscomment)
            self.assertEqual(len(allnewscomment), 1)

    def test_author_relationship(self):
        """
        Check author relationship
        """

        with app.test_request_context():
            newscomment, news, user = _create_news_comment()

            news_comment_1 = NewsComment.query.first()
            self.assertEqual(news_comment_1.author, user)

    def test_news_comment_relationship(self):
        """
        Check news relationship
        """

        with app.test_request_context():
            newscomment, news, user = _create_news_comment()

            news_comment_1 = NewsComment.query.first()
            self.assertEqual(news_comment_1.news, news)

    def test_news_comment_relationship_no_delete_news(self):
        """
        Check news_comment news relationship could not be deleted
        """

        self._send_delete('/v1/news-comments/1/relationship/news', code=405)

    def test_news_comment_relationship_no_delete_author(self):
        """
        Check news_comment author relationship could not be deleted
        """

        self._send_delete('/v1/news-comments/1/relationship/author', code=405)

    def test_news_comment_relationship_patch_news(self):
        """
        Check news_comment news relationship replace
        """

        with app.test_request_context():
            newscomment, news, user = _create_news_comment()

            payload = {
                "data": {
                    "type": "news",
                    "id": news.id
                }
            }
            # replace with the same value
            self._send_patch(
                '/v1/news-comments/1/relationship/news', payload=payload, code=204)

            news2 = NewsFactory()
            db.session.add(news2)
            db.session.commit()

            # replace with another value
            payload["data"]["id"] = news2.id
            self._send_patch(
                '/v1/news-comments/1/relationship/news', payload=payload, code=200)

            # replace with an unexistent value
            payload["data"]["id"] = 666
            self._send_patch(
                '/v1/news-comments/1/relationship/news', payload=payload, code=404)

    def test_news_comment_relationship_patch_author(self):
        """
        Check news_comment author relationship replace
        """

        with app.test_request_context():
            newscomment, news, user = _create_news_comment()

            payload = {
                "data": {
                    "type": "user",
                    "id": user.id
                }
            }
            # replace with the same value
            self._send_patch(
                '/v1/news-comments/1/relationship/author', payload=payload, code=204)

            user2 = UserFactory(name="kumy2")
            db.session.add(user2)
            db.session.commit()

            # replace with another value
            payload["data"]["id"] = user2.id
            self._send_patch(
                '/v1/news-comments/1/relationship/author', payload=payload, code=200)

            # replace with an unexistent value
            payload["data"]["id"] = 666
            self._send_patch(
                '/v1/news-comments/1/relationship/author', payload=payload, code=404)
