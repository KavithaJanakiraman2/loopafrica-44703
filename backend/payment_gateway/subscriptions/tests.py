from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from .views import SubscriptionViewSet
from unittest.mock import patch

class SubscriptionViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SubscriptionViewSet.as_view({'post': 'create'})

    def test_failed_transaction(self):
        # Create a POST request with required data
        request_data = {
            'reference': 'gp1au4l7j0',  # Use an invalid reference to simulate failed verification
            'customer': 'test_customer',
            'plan': 'test_plan',
            'authorization': 'test_authorization'
        }
        request = self.factory.post('/create-subscription/', data=request_data)

        # Set up a mock response for requests.get
        class MockResponse:
            def __init__(self, status_code, json_data):
                self.status_code = status_code
                self.json_data = json_data

            def json(self):
                return self.json_data

        # Mock the requests.get method for payment verification
        with patch('requests.get') as mock_get:
            # Mock response for payment verification failure
            mock_get.return_value = MockResponse(400, {'error': 'Payment verification failed'})

            # Make the request to the view
            response = self.view(request)

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Assert that the response contains the expected error message
        expected_error_message = {'error': 'Payment verification failed'}
        self.assertEqual(response.data, expected_error_message)
