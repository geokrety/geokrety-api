from app import current_app as app
from tests.unittests.utils import GeokretyTestCase
from app.views import LoginForm

class TestDBHelperValidation(GeokretyTestCase):

    def test_validate_login(self):

        with app.test_request_context():
            form = LoginForm()

            # TODO...
            # with self.assertRaises(Exception):
            #     try:
            #         form = LoginForm()
            #         form.validate_login('')
            #     except:
            #         pass
            #     else:
            #         raise Exception
