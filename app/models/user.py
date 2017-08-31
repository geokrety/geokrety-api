from app.models import db


class User(db.Model):
    __tablename__ = 'gk-users'

    id = db.Column('userid', db.Integer, primary_key=True, key='id')
    name = db.Column('user', db.String, key='name')
    password = db.Column('haslo2', db.String, key='password')
    email = db.Column(db.String)
    daily_mails = db.Column('wysylacmaile', db.Boolean, key='daily_news')
    ip = db.Column(db.String)
    language = db.Column('lang', db.String, key='language')
    latitude = db.Column('lat', db.Float, key='latitude')
    longitude = db.Column('lon', db.Float, key='longitude')
    observation_radius = db.Column('promien', db.Integer, key='observation_radius')
    country = db.Column(db.String)
    hour = db.Column('godzina', db.Integer, key='hour')
    statpic_id = db.Column('statpic', db.Integer, key='statpic_id')
    last_mail_date_time = db.Column('ostatni_mail', db.DateTime, nullable=False, key='last_mail_date_time')
    last_login_date_time = db.Column('ostatni_login', db.DateTime, key='last_login_date_time')
    join_date_time = db.Column('joined', db.DateTime, key='join_date_time')
    last_update_date_time = db.Column('timestamp', db.DateTime, key='last_update_date_time')
    secid = db.Column(db.String)


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
