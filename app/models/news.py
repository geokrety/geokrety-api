import datetime

from app.models import db


class News(db.Model):
    __tablename__ = 'gk-news'
    
    id = db.Column(
        'news_id',
        db.Integer,
        primary_key=True,
        key='id'
    )
    title = db.Column(
        'tytul',
        db.String(50),
        key='title',
        nullable=False
    )
    content = db.Column(
        'tresc',
        db.Text,
        key='content',
        nullable=False
    )
    username = db.Column(
        'who',
        db.String(20),
        key='username',
        nullable=True
    )
    author_id = db.Column(
        'userid',
        db.Integer,
        db.ForeignKey('gk-users.id'),
        key='author_id'
    )
    comments_count = db.Column(
        'komentarze',
        db.Integer,
        key='comments_count',
        default=0
    )
    last_comment_date_time = db.Column(
        'ostatni_komentarz',
        db.DateTime,
        key='last_comment_date_time',
        default="0000-00-00 00:00:00"
    )
    created_on_date_time = db.Column(
        'date',
        db.DateTime,
        key='created_on_date_time',
        default=datetime.datetime.utcnow
    )
    czas_postu = db.Column(
        db.DateTime,
        default="0000-00-00 00:00:00"
    )

    # author = db.relationship('User', backref=db.backref('news'))
    news_comments = db.relationship('NewsComment', backref="news", cascade="all,delete")
