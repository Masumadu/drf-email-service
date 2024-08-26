import tempfile
from urllib.parse import urlencode

from django.test import tag
from django.urls import reverse
from rest_framework import status

from .base_test_case import MailTemplateTestCase


@tag("app.template.view")
class TestTemplateView(MailTemplateTestCase):
    def test_view_all_templates(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        query_params = {"page": 1, "page_size": 1}
        response = self.client.get(
            f"{reverse('view_all_templates')}?{urlencode(query_params)}",
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)
        self.assertIn("count", response_data)
        self.assertIn("next", response_data)
        self.assertIn("previous", response_data)
        self.assertIsInstance(response_data.get("results"), list)
        self.assertEqual(
            len(response_data.get("results")), query_params.get("page_size")
        )

    def test_get_all_templates_unauthorized_exc(self):
        response = self.client.get(
            f"{reverse('view_all_templates')}?{urlencode({'page': 1, 'page_size': 1})}"
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_get_template(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.get(
            reverse(
                "get_template",
                kwargs={"template_id": self.mail_template_model.id},
            ),
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)

    def test_get_account_unauthorized_exc(self):
        response = self.client.get(
            reverse(
                "get_template",
                kwargs={"template_id": self.mail_template_model.id},
            )
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_add_template(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write("<html><body><h1>test</h1></body></html>".encode("utf-8"))
            temp_file.seek(0)
            self.jwt_decode.return_value = self.mock_decode_token()
            response = self.client.post(
                reverse("add_template"),
                data=self.mail_template_test_data.add_template(
                    file=self.mail_template_test_data.template_file(temp_file.read())
                ),
                format="multipart",
                headers=self.headers,
            )
            response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response_data, dict)

    def test_add_template_invalid_data_exc(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write("<html><body><h1>test</h1></body></html>".encode("utf-8"))
            temp_file.seek(0)
            self.jwt_decode.return_value = self.mock_decode_token()
            response = self.client.post(
                reverse("add_template"),
                data=self.mail_template_test_data.add_template(file="invalid"),
                format="multipart",
                headers=self.headers,
            )
            response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIsInstance(response_data, dict)

    def test_add_template_unauthorize_exc(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write("<html><body><h1>test</h1></body></html>".encode("utf-8"))
            temp_file.seek(0)
            self.jwt_decode.return_value = self.mock_decode_token()
            response = self.client.post(
                reverse("add_template"),
                data=self.mail_template_test_data.add_template(file="invalid"),
                format="multipart",
            )
            response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_add_template_placeholder(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.patch(
            reverse(
                "add_placeholders", kwargs={"template_id": self.mail_template_model.id}
            ),
            data=self.mail_template_test_data.add_placeholders,
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)

    def test_add_template_placeholder_invalid_data_exc(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.patch(
            reverse(
                "add_placeholders", kwargs={"template_id": self.mail_template_model.id}
            ),
            data=self.mail_template_test_data.add_placeholders[0],
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIsInstance(response_data, dict)

    def test_add_template_placeholder_unauthorize_exc(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.patch(
            reverse(
                "add_placeholders", kwargs={"template_id": self.mail_template_model.id}
            ),
            data=self.mail_template_test_data.add_placeholders,
            format=self.data_format,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_update_template(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.patch(
            reverse(
                "update_template", kwargs={"template_id": self.mail_template_model.id}
            ),
            data={"name": "update_name"},
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)

    def test_update_template_unauthorized_exc(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.patch(
            reverse(
                "update_template", kwargs={"template_id": self.mail_template_model.id}
            ),
            data={"name": "update_name"},
            format=self.data_format,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_delete_template(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.delete(
            reverse(
                "delete_template", kwargs={"template_id": self.mail_template_model.id}
            ),
            format=self.data_format,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_template_unauthorize_exc(self):
        response = self.client.delete(
            reverse(
                "delete_template", kwargs={"template_id": self.mail_template_model.id}
            ),
            format=self.data_format,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)
