from app import current_app as app
from tests.unittests.utils.base_test_case import BaseTestCase
from app.api.helpers.errors import ErrorResponse, ForbiddenError, NotFoundError, ServerError

class TestErrorsHelperValidation(BaseTestCase):

    def test_errors(self):
        """Check ErrorsHelper: errors codes"""
        with app.test_request_context():
            # Base error
            base_error = ErrorResponse({'source': ''}, 'Internal Server Error.', title='Internal Server Error.', status=500)
            self.assertEqual(base_error.status, 500)

            # Forbidden Error
            forbidden_error = ForbiddenError({'source': ''}, 'Super admin access is required')
            self.assertEqual(forbidden_error.status, 403)

            # Not Found Error
            not_found_error = NotFoundError({'source': ''}, 'Object not found.')
            self.assertEqual(not_found_error.status, 404)

            # Not Found Error
            internal_server_error = ServerError({'source': ''}, 'Internal Server Error.')
            self.assertEqual(internal_server_error.status, 500)

    def test_errors_response(self):
        """Check ErrorsHelper: errors response headers"""
        with app.test_request_context():
            not_found_error = NotFoundError({'source': ''}, 'Object not found.')
            response = not_found_error.respond()

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.status, "404 NOT FOUND")
            self.assertTrue('Content-Type' in response.headers)
            self.assertTrue('application/vnd.api+json' in response.headers['Content-Type'])
