from app import current_app as app
from app.models.news import News
from app.models.news_comment import NewsComment
from app.models.user import User
from mixer.backend.flask import mixer
from tests.unittests.utils import GeokretyTestCase
from app.api.helpers.db import safe_query
from app.models import db


# TODO
# It is possible to access news-comment list by author
#  /v1/user/1/news-comments


def _relationship_builder(relation_type, relation_id):
    return {
        "data": {
            "type": relation_type,
            "id": relation_id
        }
    }

def _payload(comment="My news comment", news_id=1, author_id=1):
    """Build a base payload"""
    attributes = {}
    if comment is not None:
        attributes["comment"] = comment
    if news_id is not None:
        attributes["news_id"] = news_id
    if author_id is not None:
        attributes["author_id"] = author_id

    result = {
        "data": {
            "type": "news-comment",
            "attributes": {},
            "relationships": {}
        }
    }

    if comment is not None:
        result["data"]["attributes"]["comment"] = comment
    if news_id is not None:
        result["data"]["relationships"]["news"] = _relationship_builder("news", news_id)
    if author_id is not None:
        result["data"]["relationships"]["author"] = _relationship_builder("user", author_id)

    return result



class TestNewsComment(GeokretyTestCase):
    """Test News Comment CRUD operations"""

    def _blend(self):
        """
        Create mocked User/News/NewsComments
        """
        mixer.init_app(app)
        self.admin = mixer.blend(User)
        self.user1 = mixer.blend(User)
        self.user2 = mixer.blend(User)
        self.news1 = mixer.blend(News)
        self.news2 = mixer.blend(News)
        self.newscomment1 = mixer.blend(NewsComment, author=self.user1, news=self.news1)
        self.newscomment2 = mixer.blend(NewsComment, author=self.user2, news=self.news1)

    def test_post_content_types(self):
        """Check accepted content types"""
        with app.test_request_context():
            self._blend()
            # Bad content_type
            self._send_post("/v1/news-comments", payload="not a json", code=415,
                            content_type='application/json',
                            user=self.user1)

            # Bad body
            # self._send_post("/v1/users", "not a json", 400)

            # Bad body
            self._send_post("/v1/news-comments", payload={}, code=422,
                            user=self.user1)

            # Bad body
            self._send_post("/v1/news-comments", payload={"user": "kumy"}, code=422,
                            user=self.user1)

    def test_create_incomplete(self):
        """Check incomplete create request"""
        with app.test_request_context():
            self._blend()
            payload = _payload(author_id=None, news_id=None)
            self._send_post("/v1/news-comments", payload=payload, code=401)
            self._send_post("/v1/news-comments", payload=payload, code=422, user=self.admin)
            self._send_post("/v1/news-comments", payload=payload, code=422, user=self.user1)
            self._send_post("/v1/news-comments", payload=payload, code=422, user=self.user2)

    def test_create_news_comment(self):
        """Check create news_comment"""
        with app.test_request_context():
            self._blend()
            payload = _payload()
            self._send_post("/v1/news-comments", payload=payload, code=401)

            payload = _payload(author_id=self.admin.id)
            self._send_post("/v1/news-comments", payload=payload, code=201, user=self.admin)
            self._send_post("/v1/news-comments", payload=payload, code=403, user=self.user1)
            self._send_post("/v1/news-comments", payload=payload, code=403, user=self.user2)

            payload = _payload(author_id=self.user1.id)
            self._send_post("/v1/news-comments", payload=payload, code=201, user=self.admin)
            self._send_post("/v1/news-comments", payload=payload, code=201, user=self.user1)
            self._send_post("/v1/news-comments", payload=payload, code=403, user=self.user2)

            payload = _payload(author_id=self.user2.id)
            self._send_post("/v1/news-comments", payload=payload, code=201, user=self.admin)
            self._send_post("/v1/news-comments", payload=payload, code=403, user=self.user1)
            self._send_post("/v1/news-comments", payload=payload, code=201, user=self.user2)

    def test_create_news_comment_increment_news(self):
        """Check create news_comment increment count on news"""
        with app.test_request_context():
            self._blend()
            payload = _payload(news_id=2, author_id=self.admin.id)

            obj = safe_query(db, News, 'id', '2', 'news_id')
            self.assertEqual(obj.comments_count, 0)

            self._send_post("/v1/news-comments", payload=payload, code=201, user=self.admin)

            obj = safe_query(db, News, 'id', '2', 'news_id')
            self.assertEqual(obj.comments_count, 1)

    def test_public_access_list(self):
        """Check GET news-comments listing is public"""
        with app.test_request_context():
            self._blend()

            self._send_get('/v1/news-comments', code=200)
            self._send_get('/v1/news-comments', code=200, user=self.admin)
            self._send_get('/v1/news-comments', code=200, user=self.user1)
            self._send_get('/v1/news-comments', code=200, user=self.user2)

            self._send_get('/v1/news/1/news-comments', code=200)
            self._send_get('/v1/news/1/news-comments', code=200, user=self.admin)
            self._send_get('/v1/news/1/news-comments', code=200, user=self.user1)
            self._send_get('/v1/news/1/news-comments', code=200, user=self.user2)

            self._send_get('/v1/news/2/news-comments', code=200)
            self._send_get('/v1/news/2/news-comments', code=200, user=self.admin)
            self._send_get('/v1/news/2/news-comments', code=200, user=self.user1)
            self._send_get('/v1/news/2/news-comments', code=200, user=self.user2)

            self._send_get('/v1/news/3/news-comments', code=404)
            self._send_get('/v1/news/3/news-comments', code=404, user=self.admin)
            self._send_get('/v1/news/3/news-comments', code=404, user=self.user1)
            self._send_get('/v1/news/3/news-comments', code=404, user=self.user2)

    def test_public_access_details(self):
        """Check GET news-comments details is public"""
        with app.test_request_context():
            self._blend()
            self._send_get('/v1/news-comments/1', code=200)
            self._send_get('/v1/news-comments/2', code=200)
            self._send_get('/v1/news-comments/3', code=404)

            self._send_get('/v1/news-comments/1', code=200, user=self.admin)
            self._send_get('/v1/news-comments/2', code=200, user=self.admin)
            self._send_get('/v1/news-comments/3', code=404, user=self.admin)

            self._send_get('/v1/news-comments/1', code=200, user=self.user1)
            self._send_get('/v1/news-comments/2', code=200, user=self.user1)
            self._send_get('/v1/news-comments/3', code=404, user=self.user1)

            self._send_get('/v1/news-comments/1', code=200, user=self.user2)
            self._send_get('/v1/news-comments/2', code=200, user=self.user2)
            self._send_get('/v1/news-comments/3', code=404, user=self.user2)

    def test_get_list_from_user(self):
        """Check GET news-comments listing from user"""
        with app.test_request_context():
            self._blend()

            self._send_get('/v1/users/%s/news-comments' % self.user1.id, code=200)
            self._send_get('/v1/users/%s/news-comments' % self.user1.id, code=200, user=self.admin)
            self._send_get('/v1/users/%s/news-comments' % self.user1.id, code=200, user=self.user1)
            self._send_get('/v1/users/%s/news-comments' % self.user1.id, code=200, user=self.user2)

            self._send_get('/v1/users/666/news-comments', code=404)
            self._send_get('/v1/users/666/news-comments', code=404, user=self.admin)
            self._send_get('/v1/users/666/news-comments', code=404, user=self.user1)
            self._send_get('/v1/users/666/news-comments', code=404, user=self.user2)

    def test_get_list_from_news(self):
        """Check GET news-comments listing from news"""
        with app.test_request_context():
            self._blend()

            self._send_get('/v1/news/%s/news-comments' % self.news1.id, code=200)
            self._send_get('/v1/news/%s/news-comments' % self.news1.id, code=200, user=self.admin)
            self._send_get('/v1/news/%s/news-comments' % self.news1.id, code=200, user=self.user1)
            self._send_get('/v1/news/%s/news-comments' % self.news1.id, code=200, user=self.user2)

            self._send_get('/v1/news/666/news-comments', code=404)
            self._send_get('/v1/news/666/news-comments', code=404, user=self.admin)
            self._send_get('/v1/news/666/news-comments', code=404, user=self.user1)
            self._send_get('/v1/news/666/news-comments', code=404, user=self.user2)

    def test_patch_list(self):
        """
        Check patch list cannot be patched
        """
        with app.test_request_context():
            self._blend()
            self._send_patch("/v1/news-comments", code=405)
            self._send_patch("/v1/news-comments", code=405, user=self.admin)
            self._send_patch("/v1/news-comments", code=405, user=self.user1)
            self._send_patch("/v1/news-comments", code=405, user=self.user2)

    def test_patch_title(self):
        """
        Check patch title
        """
        with app.test_request_context():
            self._blend()
            payload = {
                "data": {
                    "type": "news-comment",
                    "attributes": {
                        "comment": "Fresh News comment"
                    }
                }
            }

            payload["data"]["id"] = "1"
            self._send_patch("/v1/news-comments/1", payload=payload, code=401)
            self._send_patch("/v1/news-comments/1", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/news-comments/1", payload=payload, code=200, user=self.user1)
            self._send_patch("/v1/news-comments/1", payload=payload, code=403, user=self.user2)

            payload["data"]["id"] = "2"
            self._send_patch("/v1/news-comments/2", payload=payload, code=401)
            self._send_patch("/v1/news-comments/2", payload=payload, code=200, user=self.admin)
            self._send_patch("/v1/news-comments/2", payload=payload, code=403, user=self.user1)
            self._send_patch("/v1/news-comments/2", payload=payload, code=200, user=self.user2)

            payload["data"]["id"] = "3"
            self._send_patch("/v1/news-comments/3", payload=payload, code=404)
            self._send_patch("/v1/news-comments/3", payload=payload, code=404, user=self.admin)
            self._send_patch("/v1/news-comments/3", payload=payload, code=404, user=self.user1)
            self._send_patch("/v1/news-comments/3", payload=payload, code=404, user=self.user2)

    def test_delete_anonymous(self):
        """Check delete Anonymous"""
        with app.test_request_context():
            self._blend()
            payload = _payload()
            self._send_delete("/v1/news-comments", payload=payload, code=405)
            self._send_delete("/v1/news-comments/1", payload=payload, code=401)
            self._send_delete("/v1/news-comments/2", payload=payload, code=401)
            self._send_delete("/v1/news-comments/3", payload=payload, code=404)

    def test_delete_admin(self):
        """Check delete Admin"""
        with app.test_request_context():
            self._blend()
            payload = _payload()
            self._send_delete("/v1/news-comments", payload=payload, code=405, user=self.admin)
            self._send_delete("/v1/news-comments/1", payload=payload, code=200, user=self.admin)
            self._send_delete("/v1/news-comments/2", payload=payload, code=200, user=self.admin)
            self._send_delete("/v1/news-comments/3", payload=payload, code=404, user=self.admin)

    def test_delete_user1(self):
        """Check delete User1"""
        with app.test_request_context():
            self._blend()
            payload = _payload()
            self._send_delete("/v1/news-comments", payload=payload, code=405, user=self.user1)
            self._send_delete("/v1/news-comments/1", payload=payload, code=200, user=self.user1)
            self._send_delete("/v1/news-comments/2", payload=payload, code=403, user=self.user1)
            self._send_delete("/v1/news-comments/3", payload=payload, code=404, user=self.user1)

    def test_delete_user2(self):
        """Check delete User2"""
        with app.test_request_context():
            self._blend()
            payload = _payload()
            self._send_delete("/v1/news-comments", payload=payload, code=405, user=self.user2)
            self._send_delete("/v1/news-comments/1", payload=payload, code=403, user=self.user2)
            self._send_delete("/v1/news-comments/2", payload=payload, code=200, user=self.user2)
            self._send_delete("/v1/news-comments/3", payload=payload, code=404, user=self.user2)

    def test_delete_news_comment_decrement_news(self):
        """Check delete news_comment decrement count on news"""
        with app.test_request_context():
            self._blend()
            news_id = 2
            payload = _payload(news_id=news_id)

            obj = safe_query(db, News, 'id', news_id, 'news_id')
            self.assertEqual(obj.comments_count, 0)

            news_comment = self._send_post("/v1/news-comments", payload=payload, code=201, user=self.admin)

            obj = safe_query(db, News, 'id', news_id, 'news_id')
            self.assertEqual(obj.comments_count, 1)

            self._send_delete("/v1/news-comments/%s" % news_comment['data']['id'], code=200, user=self.admin)

            obj = safe_query(db, News, 'id', news_id, 'news_id')
            self.assertEqual(obj.comments_count, 0)
