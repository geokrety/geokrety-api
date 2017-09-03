from app import current_app as app
from app.api.helpers.exceptions import UnprocessableEntity
from tests.unittests.utils import GeokretyTestCase
from app.api.helpers.utilities import dasherize, require_relationship


class TestUtilitiesHelperValidation(GeokretyTestCase):

    def test_dasherize(self):
        with app.test_request_context():
            field = "starts_at"
            dasherized_field = "starts-at"
            result = dasherize(field)
            self.assertEqual(result, dasherized_field)

    def test_require_relationship(self):
        with self.assertRaises(UnprocessableEntity):
            data = ['event']
            require_relationship(['sponsor', 'event'], data)
