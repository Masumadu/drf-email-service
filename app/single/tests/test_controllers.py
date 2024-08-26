import uuid

from django.test import tag
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request

from app.single.serializer import (
    SingleMailResponseSerializer,
    SingleMailSerializer,
)
from core.exceptions import AppException

from .base_test_case import SingleMailTestCase


@tag("app.single.controller")
class TestSingleMailController(SingleMailTestCase):
    def test_view_all_mails(self):
        request = Request(
            self.request_factory.get(self.request_url, data={"page": 1, "page_size": 1})
        )
        results = self.single_mail_controller.view_all_mails(request)
        self.assertEqual(results.status_code, 200)
        self.assertIsInstance(results.data, dict)
        self.assertIsInstance(results.data.get("results"), list)
        self.assertEqual(
            len(results.data.get("results")), int(request.query_params.get("page_size"))
        )

    def test_get_mail(self):
        results = self.single_mail_controller.get_mail(self.single_mail_model.id)
        self.assertIsInstance(results, SingleMailSerializer)
        self.assertIsInstance(results.data, dict)

    def test_get_mail_not_found_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            self.single_mail_controller.get_mail(uuid.uuid4())
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_send_mail(self):
        request = Request(
            self.request_factory.post(
                self.request_url,
                self.single_mail_test_data.send_mail(
                    self.mail_account_model.mail_address
                ),
                format=self.data_format,
            ),
            parsers=[JSONParser()],
        )
        request.user = self.mock_decode_token()
        result = self.single_mail_controller.send_mail(request=request)
        self.assertIsInstance(result, SingleMailResponseSerializer)
        self.assertIsInstance(result.data, dict)

    def test_send_mail_invalid_data_exc(self):
        with self.assertRaises(AppException.ValidationException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.single_mail_test_data.send_mail(sender="invalid"),
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.single_mail_controller.send_mail(request)
        self.assertEqual(
            exception.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIsNotNone(exception.exception.error_message)

    def test_send_mail_sender_notfound_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.single_mail_test_data.send_mail(sender="notfound@example.com"),
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.single_mail_controller.send_mail(request)
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_send_mail_with_template(self):
        request = Request(
            self.request_factory.post(
                self.request_url,
                self.single_mail_test_data.send_email_with_template(
                    self.mail_account_model.mail_address, self.mail_template_model.id
                ),
                format=self.data_format,
            ),
            parsers=[JSONParser()],
        )
        request.user = self.mock_decode_token()
        result = self.single_mail_controller.send_mail_with_template(request=request)
        self.assertIsInstance(result, SingleMailResponseSerializer)
        self.assertIsInstance(result.data, dict)

    def test_send_mail_with_template_invalid_data_exc(self):
        with self.assertRaises(AppException.ValidationException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.single_mail_test_data.send_email_with_template(
                        sender="invalid", template_id=self.mail_template_model.id
                    ),
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.single_mail_controller.send_mail_with_template(request)
        self.assertEqual(
            exception.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIsNotNone(exception.exception.error_message)

    def test_send_mail_with_template_sender_notfound_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.single_mail_test_data.send_email_with_template(
                        sender="notfound@example.com",
                        template_id=self.mail_template_model.id,
                    ),
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.single_mail_controller.send_mail_with_template(request)
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_delete_mail(self):
        result = self.single_mail_controller.delete_mail(
            obj_id=self.single_mail_model.id
        )
        self.assertIsNone(result)

    def test_delete_mail_notfound_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            self.single_mail_controller.delete_mail(obj_id=uuid.uuid4())
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_create_task(self):
        result = self.single_mail_controller.create_task(
            obj_data=self.single_mail_test_data.mail_task
        )
        self.assertIsNone(result)

    def test_create_task_celery_exc(self):
        with self.assertRaises(AppException.InternalServerException) as exception:
            self.celery_task.side_effect = self.celery_exc
            self.single_mail_controller.create_task(
                obj_data=self.single_mail_test_data.mail_task
            )
        self.assertEqual(
            exception.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertIsNotNone(exception.exception.error_message)
