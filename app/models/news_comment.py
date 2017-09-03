import datetime

from app.models import db


class NewsComment(db.Model):
    __tablename__ = 'gk-news-comments'
    id = db.Column('comment_id', db.Integer, primary_key=True, key='id')
    news_id = db.Column(db.Integer, db.ForeignKey('gk-news.id'), nullable=False)
    author_id = db.Column('user_id', db.Integer, db.ForeignKey('gk-users.id'), key='author_id', nullable=False)
    created_on_date = db.Column('date', db.Date, key='created_on_date', default=datetime.datetime.now().date())
    comment = db.Column(db.String(1000))
    icon = db.Column(db.Integer, default=0)

    # news = db.relationship('News', backref=db.backref('news_comments'))
    # author = db.relationship('User', backref=db.backref('news_comments'))
