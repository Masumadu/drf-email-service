import tempfile
import uuid

from django.test import tag
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.request import Request

from app.template.serializer import MailTemplateSerializer
from core.exceptions import AppException

from .base_test_case import MailTemplateTestCase


@tag("app.template.controller")
class TestMailTemplateController(MailTemplateTestCase):
    def test_view_all_templates(self):
        request = Request(
            self.request_factory.get(self.request_url, data={"page": 1, "page_size": 1})
        )
        results = self.mail_template_controller.view_all_templates(request)
        self.assertEqual(results.status_code, 200)
        self.assertIsInstance(results.data, dict)
        self.assertIsInstance(results.data.get("results"), list)
        self.assertEqual(
            len(results.data.get("results")), int(request.query_params.get("page_size"))
        )

    def test_get_template(self):
        results = self.mail_template_controller.get_template(
            self.mail_template_model.id
        )
        self.assertIsInstance(results, MailTemplateSerializer)
        self.assertIsInstance(results.data, dict)

    def test_get_template_not_found_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            self.mail_template_controller.get_template(uuid.uuid4())
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_add_template(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write("<html><body><h1>test</h1></body></html>".encode("utf-8"))
            temp_file.seek(0)
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.mail_template_test_data.add_template(
                        file=self.mail_template_test_data.template_file(
                            temp_file.read()
                        )
                    ),
                    format="multipart",
                ),
                parsers=[MultiPartParser()],
            )
            request.user = self.mock_decode_token()
            result = self.mail_template_controller.add_template(request=request)
            self.assertIsInstance(result, MailTemplateSerializer)
            self.assertIsInstance(result.data, dict)

    def test_add_template_name_exist_exc(self):
        with self.assertRaises(AppException.ResourceExistException) as exception:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(
                    "<html><body><h1>test</h1></body></html>".encode("utf-8")
                )
                temp_file.seek(0)
                request = Request(
                    self.request_factory.post(
                        self.request_url,
                        self.mail_template_test_data.add_template(
                            name=self.mail_template_model.name,
                            file=self.mail_template_test_data.template_file(
                                temp_file.read()
                            ),
                        ),
                        format="multipart",
                    ),
                    parsers=[MultiPartParser()],
                )
                request.user = self.mock_decode_token()
                self.mail_template_controller.add_template(request=request)
        self.assertEqual(exception.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertIsNotNone(exception.exception.error_message)

    def test_add_template_invalid_data_exc(self):
        with self.assertRaises(AppException.ValidationException) as exception:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(
                    "<html><body><h1>test</h1></body></html>".encode("utf-8")
                )
                temp_file.seek(0)
                request = Request(
                    self.request_factory.post(
                        self.request_url,
                        self.mail_template_test_data.add_template(
                            file=self.mail_template_test_data.template_file(
                                temp_file.read()
                            )
                        ),
                        format=self.data_format,
                    ),
                    parsers=[JSONParser()],
                )
                request.user = self.mock_decode_token()
                self.mail_template_controller.add_template(request=request)
        self.assertEqual(
            exception.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIsNotNone(exception.exception.error_message)

    def test_add_placeholder(self):
        request = Request(
            self.request_factory.post(
                self.request_url,
                self.mail_template_test_data.add_placeholders,
                format=self.data_format,
            ),
            parsers=[JSONParser()],
        )
        request.user = self.mock_decode_token()
        result = self.mail_template_controller.add_template_placeholder(
            request, self.mail_template_model.id
        )
        self.assertIsInstance(result, MailTemplateSerializer)
        self.assertIsInstance(result.data, dict)

    def test_add_placeholder_invalid_data_exc(self):
        with self.assertRaises(AppException.ValidationException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.mail_template_test_data.add_placeholders[0],
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.mail_template_controller.add_template_placeholder(
                request, self.mail_template_model.id
            )
        self.assertEqual(
            exception.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIsNotNone(exception.exception.error_message)

    def test_add_placeholder_notfound_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.mail_template_test_data.add_placeholders,
                    format=self.data_format,
                ),
                parsers=[JSONParser()],
            )
            request.user = self.mock_decode_token()
            self.mail_template_controller.add_template_placeholder(
                request, uuid.uuid4()
            )
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_update_template(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write("<html><body><h1>test</h1></body></html>".encode("utf-8"))
            temp_file.seek(0)
            request = Request(
                self.request_factory.patch(
                    self.request_url,
                    self.mail_template_test_data.update_template(
                        file=self.mail_template_test_data.template_file(
                            temp_file.read()
                        )
                    ),
                    format="multipart",
                ),
                parsers=[MultiPartParser()],
            )
            request.user = self.mock_decode_token()
            result = self.mail_template_controller.update_template(
                request=request, obj_id=self.mail_template_model.id
            )
            self.assertIsInstance(result, MailTemplateSerializer)
            self.assertIsInstance(result.data, dict)

    def test_update_template_notfound_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(
                    "<html><body><h1>test</h1></body></html>".encode("utf-8")
                )
                temp_file.seek(0)
                request = Request(
                    self.request_factory.patch(
                        self.request_url,
                        self.mail_template_test_data.update_template(
                            file=self.mail_template_test_data.template_file(
                                temp_file.read()
                            )
                        ),
                        format="multipart",
                    ),
                    parsers=[MultiPartParser()],
                )
                request.user = self.mock_decode_token()
                self.mail_template_controller.update_template(
                    request=request, obj_id=uuid.uuid4()
                )
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_update_template_invalid_data_exc(self):
        with self.assertRaises(AppException.ValidationException) as exception:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(
                    "<html><body><h1>test</h1></body></html>".encode("utf-8")
                )
                temp_file.seek(0)
                request = Request(
                    self.request_factory.post(
                        self.request_url,
                        self.mail_template_test_data.update_template(
                            file=self.mail_template_test_data.template_file(
                                temp_file.read()
                            )
                        ),
                        format=self.data_format,
                    ),
                    parsers=[JSONParser()],
                )
                request.user = self.mock_decode_token()
                self.mail_template_controller.update_template(
                    request=request, obj_id=self.mail_template_model.id
                )
        self.assertEqual(
            exception.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIsNotNone(exception.exception.error_message)

    def test_delete_template(self):
        result = self.mail_template_controller.delete_template(
            obj_id=self.mail_template_model.id
        )
        self.assertIsNone(result)

    def test_delete_template_notfound_exc(self):
        with self.assertRaises(AppException.NotFoundException) as exception:
            self.mail_template_controller.delete_template(obj_id=uuid.uuid4())
        self.assertEqual(exception.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(exception.exception.error_message)

    def test_generate_message(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write("<html><body><h1>test</h1></body></html>".encode("utf-8"))
            temp_file.seek(0)
            request = Request(
                self.request_factory.post(
                    self.request_url,
                    self.mail_template_test_data.add_template(
                        file=self.mail_template_test_data.template_file(
                            temp_file.read()
                        )
                    ),
                    format="multipart",
                ),
                parsers=[MultiPartParser()],
            )
            request.user = self.mock_decode_token()
            template = self.mail_template_controller.add_template(request=request)
            result = self.mail_template_controller.generate_message(
                query_template={"id": template.data.get("id")}, keywords={}
            )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
