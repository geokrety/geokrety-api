from app.models import db
from sqlalchemy.ext.hybrid import hybrid_property
import phpass
from flask import current_app as app


class User(db.Model):
    __tablename__ = 'gk-users'

    id = db.Column('userid', db.Integer, primary_key=True, key='id')
    name = db.Column('user', db.String(80), key='name')
    _password = db.Column('haslo2', db.String(120), key='password')
    email = db.Column(db.String(150))
    daily_mails = db.Column('wysylacmaile', db.Boolean, key='daily_news')
    ip = db.Column(db.String(39))
    language = db.Column('lang', db.String(2), key='language')
    latitude = db.Column('lat', db.Float, key='latitude')
    longitude = db.Column('lon', db.Float, key='longitude')
    observation_radius = db.Column(
        'promien', db.Integer, key='observation_radius')
    country = db.Column(db.String(3))
    hour = db.Column('godzina', db.Integer, key='hour')
    statpic_id = db.Column('statpic', db.Integer, key='statpic_id')
    last_mail_date_time = db.Column('ostatni_mail',
                                    db.DateTime,
                                    nullable=False,
                                    key='last_mail_date_time',
                                    default="0000-00-00 00:00:00")
    last_login_date_time = db.Column(
        'ostatni_login', db.DateTime, key='last_login_date_time')
    join_date_time = db.Column('joined', db.DateTime, key='join_date_time')
    last_update_date_time = db.Column(
        'timestamp', db.DateTime, key='last_update_date_time')
    secid = db.Column(db.String(128))

    news = db.relationship('News', backref="author")
    news_comments = db.relationship('NewsComment', backref="author")

    @hybrid_property
    def password(self):
        """
        Hybrid property for password
        :return:
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Setter for _password, saves hashed password, salt and reset_password string
        :param password:
        :return:
        """
        t_hasher = phpass.PasswordHash(11, False)
        self._password = t_hasher.hash_password(
            password.encode('utf-8') + app.config['PASSWORD_HASH_SALT']
        )

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    @property
    def is_super_admin(self):
        return self.id in [1, 26422]

    @property
    def is_admin(self):
        return self.id in [1, 26422]
