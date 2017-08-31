from app.models import db


class News(db.Model):
    __tablename__ = 'gk-news'
    id = db.Column('news_id', db.Integer, primary_key=True, key='id')
    created_on_date_time = db.Column('date', db.DateTime, key='created_on_date_time')
    czas_postu = db.Column(db.DateTime, default="0000-00-00 00:00:00")
    title = db.Column('tytul', db.String, key='title')
    content = db.Column('tresc', db.String, key='content')
    username = db.Column('who', db.String, key='username')
    author_id = db.Column('userid', db.Integer, db.ForeignKey('gk-users.id'), key='author_id')
    comments_count = db.Column('komentarze', db.Integer, key='comments_count', default=0)
    last_comment = db.Column('ostatni_komentarz', db.DateTime, key='last_comment')

    author = db.relationship('User', backref=db.backref('news'))
