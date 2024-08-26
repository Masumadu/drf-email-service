import uuid

from django.test import tag
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request

from app.account.serializer import MailAccountSerializer
from core.exceptions import AppException

from .base_test_case import MailAccountTestCase


@tag("app.account.controller")
class TestMailAccountController(MailAccountTestCase):
    def test_view_all_accounts(self):
        request = Request(
            self.request_factory.get(self.request_url, data={"page": 1, "page_size": 1})
        )
        results = self.mail_account_controller.view_all_accounts(request)
        self.assertEqual(results.status_code, 200)
        self.assertIsInstance(results.data, dict)
        self.assertIsInstance(results.data.get("results"), list)
        self.assertEqual(
            len(results.data.get("results")), int(request.query_params.get("page_size"))
        )

    def test_get_account(self):
        results = self.mail_account_controller.get_account(self.mail_account_model.id)
        self.assertIsInstance(results, MailAccountSerializer)
        self.assertIsInstance(results.data, dict)

    def test_get_account_not_found_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            self.mail_account_controller.get_account(uuid.uuid4())
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_add_account(self):
        request = Request(
            self.request_factory.post(
                self.request_url,
                self.mail_account_test_data.add_account(),
                format=self.data_format,
            ),
            parsers=[JSONParser()],
        )
        request.user = self.mock_decode_token()
        result = self.mail_account_controller.add_account(request=request)
        self.assertIsInstance(result, MailAccountSerializer)
        self.assertIsInstance(result.data, dict)

    def test_add_account_invalid_data_exc(self):
        with self.assertRaises(AppException.ValidationException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.mail_account_test_data.add_account(mail="invalid"),
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.mail_account_controller.add_account(request)
        self.assertEqual(
            exception.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIsNotNone(exception.exception.error_message)

    def test_update_account(self):
        request = Request(
            self.request_factory.post(
                self.request_url,
                self.mail_account_test_data.update_account,
                format=self.data_format,
            ),
            parsers=[JSONParser()],
        )
        request.user = self.mock_decode_token()
        result = self.mail_account_controller.update_account(
            request=request, obj_id=self.mail_account_model.id
        )
        self.assertIsInstance(result, MailAccountSerializer)
        self.assertIsInstance(result.data, dict)

    def test_update_account_notfound_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.mail_account_test_data.update_account,
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.mail_account_controller.update_account(request, uuid.uuid4())
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_update_account_invalid_data_exc(self):
        with self.assertRaises(AppException.ValidationException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    {"sender_name": True},
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.mail_account_controller.update_account(request, uuid.uuid4())
        self.assertEqual(
            exception.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIsNotNone(exception.exception.error_message)

    def test_delete_account(self):
        request = Request(self.request_factory.delete(self.request_url))
        request.user = self.mock_decode_token()
        result = self.mail_account_controller.delete_account(
            request=request, obj_id=self.mail_account_model.id
        )
        self.assertIsNone(result)

    def test_delete_account_notfound_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            request = Request(self.request_factory.delete(self.request_url))
            request.user = self.mock_decode_token()
            self.mail_account_controller.delete_account(
                request=request, obj_id=uuid.uuid4()
            )
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)
