from urllib.parse import urlencode

from django.test import tag
from django.urls import reverse
from rest_framework import status

from .base_test_case import SingleMailTestCase


@tag("app.single.view")
class TestSingleMailView(SingleMailTestCase):
    def test_view_all_mails(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        query_params = {"page": 1, "page_size": 1}
        response = self.client.get(
            f"{reverse('view_all_mails')}?{urlencode(query_params)}",
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

    def test_get_all_mails_unauthorized_exc(self):
        response = self.client.get(
            f"{reverse('view_all_mails')}?{urlencode({'page': 1, 'page_size': 1})}"
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_get_mail(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.get(
            reverse(
                "get_mail",
                kwargs={"mail_id": self.single_mail_model.id},
            ),
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)

    def test_get_mail_unauthorized_exc(self):
        response = self.client.get(
            reverse(
                "get_mail",
                kwargs={"mail_id": self.single_mail_model.id},
            )
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_send_mail(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.post(
            reverse("send_mail"),
            data=self.single_mail_test_data.send_mail(
                sender=self.mail_account_model.mail_address
            ),
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response_data, dict)

    def test_send_mail_invalid_data_exc(self):
        response = self.client.post(
            reverse("send_mail"),
            data=self.single_mail_test_data.send_mail(sender="invalid"),
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIsInstance(response_data, dict)

    def test_send_mail_with_template(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.post(
            reverse("send_template_mail"),
            data=self.single_mail_test_data.send_email_with_template(
                sender=self.mail_account_model.mail_address,
                template_id=self.mail_template_model.id,
            ),
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response_data, dict)

    def test_send_mail_with_template_invalid_data_exc(self):
        response = self.client.post(
            reverse("send_template_mail"),
            data=self.single_mail_test_data.send_email_with_template(
                sender="invalid", template_id=self.mail_template_model.id
            ),
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIsInstance(response_data, dict)

    def test_delete_mail(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.delete(
            reverse("delete_mail", kwargs={"mail_id": self.single_mail_model.id}),
            format=self.data_format,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_mail_unauthorize_exc(self):
        response = self.client.delete(
            reverse("delete_mail", kwargs={"mail_id": self.single_mail_model.id}),
            format=self.data_format,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)
