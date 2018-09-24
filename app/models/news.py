import datetime

from app.models import db
from sqlalchemy.ext.hybrid import hybrid_property
import bleach
import htmlentities


class News(db.Model):
    __tablename__ = 'gk-news'

    id = db.Column(
        'news_id',
        db.Integer,
        primary_key=True,
        key='id'
    )
    _title = db.Column(
        'tytul',
        db.String(50),
        key='title',
        nullable=False
    )
    _content = db.Column(
        'tresc',
        db.Text,
        key='content',
        nullable=False
    )
    _username = db.Column(
        'who',
        db.String(80),
        key='username',
        nullable=True
    )
    author_id = db.Column(
        'userid',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='author_id',
        nullable=False,
    )
    comments_count = db.Column(
        'komentarze',
        db.Integer,
        key='comments_count',
        default=0
    )
    last_comment_datetime = db.Column(
        'ostatni_komentarz',
        db.DateTime,
        key='last_comment_datetime',
        nullable=False,
        default="0000-00-00T00:00:00"
    )
    created_on_datetime = db.Column(
        'date',
        db.DateTime,
        key='created_on_datetime',
        default=datetime.datetime.utcnow
    )
    czas_postu = db.Column(
        db.DateTime,
        default="0000-00-00T00:00:00"
    )

    # author = db.relationship('User', backref=db.backref('news'))
    news_comments = db.relationship('NewsComment', backref="news", cascade="all,delete")
    news_subscriptions = db.relationship('NewsSubscription', backref="news", cascade="all,delete")

    @hybrid_property
    def title(self):
        return htmlentities.decode(self._title)

    @title.setter
    def title(self, title):
        title_clean = bleach.clean(title, tags=[], strip=True)
        title_clean = htmlentities.decode(title_clean).strip()
        self._title = htmlentities.encode(title_clean)

    @title.expression
    def title(cls):
        return cls._title

    @hybrid_property
    def content(self):
        return htmlentities.decode(self._content)

    @content.setter
    def content(self, content):
        # Drop all unallowed html tags
        content_clean = bleach.clean(content, strip=True)
        # Strip spaces
        content_clean = htmlentities.decode(content_clean).strip()
        self._content = htmlentities.encode(content_clean)

    @content.expression
    def content(cls):
        return cls._content

    @hybrid_property
    def username(self):
        if self._username:
            return htmlentities.decode(self._username)

    @username.setter
    def username(self, username):
        username_clean = bleach.clean(username, tags=[], strip=True)
        username_clean = htmlentities.decode(username_clean).strip()
        self._username = htmlentities.encode(username_clean)

    @username.expression
    def username(cls):
        return cls._username
