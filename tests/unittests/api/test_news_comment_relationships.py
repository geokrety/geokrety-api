from app import current_app as app
from app.models.news import News
from app.models.news_comment import NewsComment
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase


class TestNewsCommentRelationships(GeokretyTestCase):
    """Test User CRUD operations"""

    def _blend_users(self):
        """Create mocked User/News/NewsComments"""
        mixer.init_app(app)
        self.admin = mixer.blend(User)
        self.user1 = mixer.blend(User)
        self.user2 = mixer.blend(User)

    def _blend(self):
        """Create mocked User/News/NewsComments"""
        self.news1 = mixer.blend(News, author=self.user1)
        # self.news2 = mixer.blend(News)
        self.orphan_news = mixer.blend(News, author=None)
        self.newscomment1 = mixer.blend(NewsComment, author=self.user1, news=self.news1)
        # self.newscomment2 = mixer.blend(NewsComment, author=self.user2, news=self.news1)

    def test_get_news_author(self):
        """Check NewsCommentRelationships: GET relationship author"""
        with app.test_request_context():
            self._blend_users()
            self._blend()

            self._send_get('/v1/news-comments/1/relationship/news', code=200)
            self._send_get('/v1/news-comments/1/relationship/news', code=200, user=self.admin)
            self._send_get('/v1/news-comments/1/relationship/news', code=200, user=self.user1)
            self._send_get('/v1/news-comments/1/relationship/news', code=200, user=self.user2)

    def test_post_news_author(self):
        """Check NewsCommentRelationships: POST relationship author"""
        with app.test_request_context():
            self._blend_users()
            self._send_post('/v1/news-comments/1/relationship/news', code=405)
            self._send_post('/v1/news-comments/1/relationship/news', code=405, user=self.admin)
            self._send_post('/v1/news-comments/1/relationship/news', code=405, user=self.user1)
            self._send_post('/v1/news-comments/1/relationship/news', code=405, user=self.user2)

    def test_patch_news_author(self):
        """Check NewsCommentRelationships: PATCH relationship author"""
        with app.test_request_context():
            self._blend_users()
            self._send_patch('/v1/news-comments/1/relationship/news', code=405)
            self._send_patch('/v1/news-comments/1/relationship/news', code=405, user=self.admin)
            self._send_patch('/v1/news-comments/1/relationship/news', code=405, user=self.user1)
            self._send_patch('/v1/news-comments/1/relationship/news', code=405, user=self.user2)

    def test_delete_news_author(self):
        """Check NewsCommentRelationships: DELETE relationship author"""
        with app.test_request_context():
            self._blend_users()
            self._send_delete('/v1/news-comments/1/relationship/news', code=405)
            self._send_delete('/v1/news-comments/1/relationship/news', code=405, user=self.admin)
            self._send_delete('/v1/news-comments/1/relationship/news', code=405, user=self.user1)
            self._send_delete('/v1/news-comments/1/relationship/news', code=405, user=self.user2)

    def test_get_news(self):
        """Check NewsCommentRelationships: GET relationship news"""
        with app.test_request_context():
            self._blend_users()
            self._blend()
            self._send_get('/v1/news-comments/1/relationship/news', code=200)
            self._send_get('/v1/news-comments/1/relationship/news', code=200, user=self.admin)
            self._send_get('/v1/news-comments/1/relationship/news', code=200, user=self.user1)
            self._send_get('/v1/news-comments/1/relationship/news', code=200, user=self.user2)

    def test_post_news(self):
        """Check NewsCommentRelationships: POST relationship news"""
        with app.test_request_context():
            self._blend_users()
            self._send_post('/v1/news-comments/1/relationship/news', code=405)
            self._send_post('/v1/news-comments/1/relationship/news', code=405, user=self.admin)
            self._send_post('/v1/news-comments/1/relationship/news', code=405, user=self.user1)
            self._send_post('/v1/news-comments/1/relationship/news', code=405, user=self.user2)

    def test_patch_news(self):
        """Check NewsCommentRelationships: PATCH relationship news"""
        with app.test_request_context():
            self._blend_users()
            self._send_patch('/v1/news-comments/1/relationship/news', code=405)
            self._send_patch('/v1/news-comments/1/relationship/news', code=405, user=self.admin)
            self._send_patch('/v1/news-comments/1/relationship/news', code=405, user=self.user1)
            self._send_patch('/v1/news-comments/1/relationship/news', code=405, user=self.user2)

    def test_delete_news(self):
        """Check NewsCommentRelationships: DELETE relationship news"""
        with app.test_request_context():
            self._blend_users()
            self._send_delete('/v1/news-comments/1/relationship/news', code=405)
            self._send_delete('/v1/news-comments/1/relationship/news', code=405, user=self.admin)
            self._send_delete('/v1/news-comments/1/relationship/news', code=405, user=self.user1)
            self._send_delete('/v1/news-comments/1/relationship/news', code=405, user=self.user2)
