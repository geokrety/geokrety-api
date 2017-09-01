import factory
import phpass

from app import current_app as app
from app.models.user import db, User
import app.factories.common as common


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    name = 'someone'
    password = '$2a$11$DCeuzrpFpIR3yGi33wQxXOu/SsTLYXm880l/lMT8S.unTzMl3I6OC' # == "password" with salt "unit_test"
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
    last_mail_date_time = common.date_
    last_login_date_time = common.date_
    join_date_time = common.date_
    last_update_date_time = common.date_
    secid = '123456qwerty'
