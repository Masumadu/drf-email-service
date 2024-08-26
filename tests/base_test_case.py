from rest_framework.test import APIRequestFactory, APITestCase

from .mock_response import MockSideEffects


class BaseTestCase(APITestCase, MockSideEffects):
    def setUp(self):
        self.setup_test_data()
        self.setup_patches()
        self.instantiate_classes()

    def setup_test_data(self):
        self.access_token = "lskjasljdlajdlfakjlakjlajf"
        self.refresh_token = self.access_token
        self.content_type = "application/json"
        self.data_format = "json"
        self.request_url = "http://localhost"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def instantiate_classes(self):
        """This is where all classes are instantiated for the test"""

    def setup_patches(self):
        """This is where all mocked object are setup for the test"""
        self.request_factory = APIRequestFactory()
