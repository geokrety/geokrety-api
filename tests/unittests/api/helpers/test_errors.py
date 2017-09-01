from app import current_app as app

from tests.unittests.utils import GeokretyTestCase
from app.api.helpers.errors import ForbiddenError, NotFoundError, ServerError

class TestErrorsHelperValidation(GeokretyTestCase):

    def test_errors(self):
        with app.test_request_context():
            # Forbidden Error
            forbidden_error = ForbiddenError({'source': ''}, 'Super admin access is required')
            self.assertEqual(forbidden_error.status, 403)

            # Not Found Error
            not_found_error = NotFoundError({'source': ''}, 'Object not found.')
            self.assertEqual(not_found_error.status, 404)

            # Not Found Error
            internal_server_error = ServerError({'source': ''}, 'Internal Server Error.')
            self.assertEqual(internal_server_error.status, 500)
