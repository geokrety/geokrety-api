import factory

from app.models.user import db, User
import app.factories.common as common


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    name = 'someone'
    password = 'password'
    email = common.email_
    daily_mails = True
    ip = common.ip_
    language = 'fr'
    latitude = 48.8566
    longitude = 2.3522
    observation_radius = 5
    country = 'fr'
    hour = 17
    statpic_id = 1234
    last_mail_date_time = common.date_time_
    last_login_date_time = common.date_time_
    join_date_time = common.date_time_
    last_update_date_time = common.date_time_
    secid = '123456qwerty'
